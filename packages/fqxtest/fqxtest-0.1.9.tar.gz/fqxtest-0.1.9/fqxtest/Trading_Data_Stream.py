import time
import threading
import pandas as pd
from signalrcore.hub_connection_builder import HubConnectionBuilder
from .RealTimeData import RealTimeData
import logging
import queue
from datetime import datetime
from typing import Union
import numpy as np

REALTIME_API = "https://fiinquant-realtime.fiintrade.vn/RealtimeHub"


class CustomHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_messages = []

    def emit(self, record):
        log_entry = self.format(record)
        self.log_messages.append(log_entry)

    def get_logs(self):
        logs = self.log_messages[:]
        self.log_messages.clear()
        return logs


class Trading_Data_Stream:
    def __init__(self, access_token: callable, tickers: Union[list[str], str], callback: callable):
        self.url = REALTIME_API
        self.connected = False
        self.callback = callback
        self.access_token = access_token
        self.hub_connection = None
        self.df = {
            'Index': pd.DataFrame(columns=['TotalMatchVolume', 'MarketStatus', 'TradingDate', 'ComGroupCode', 'ReferenceIndex',
                                           'OpenIndex', 'CloseIndex', 'HighestIndex', 'LowestIndex', 'IndexValue', 'IndexChange',
                                           'PercentIndexChange', 'MatchVolume', 'MatchValue', 'TotalMatchValue', 'TotalDealVolume',
                                           'TotalDealValue', 'TotalStockUpPrice', 'TotalStockDownPrice', 'TotalStockNoChangePrice',
                                           'TotalStockOverCeiling', 'TotalStockUnderFloor', 'ForeignBuyVolumeTotal',
                                           'ForeignBuyValueTotal', 'ForeignSellVolumeTotal', 'ForeignSellValueTotal', 'VolumeBu',
                                           'VolumeSd']),

            'Ticker': pd.DataFrame(columns=['TotalMatchVolume', 'MarketStatus', 'TradingDate', 'MatchType', 'ComGroupCode',
                                            'OrganCode', 'Ticker', 'ReferencePrice', 'OpenPrice', 'ClosePrice', 'CeilingPrice',
                                            'FloorPrice', 'HighestPrice', 'LowestPrice', 'MatchPrice', 'PriceChange',
                                            'PercentPriceChange', 'MatchVolume', 'MatchValue', 'TotalMatchValue',
                                            'TotalBuyTradeVolume', 'TotalSellTradeVolume', 'DealPrice', 'TotalDealVolume',
                                            'TotalDealValue', 'ForeignBuyVolumeTotal', 'ForeignBuyValueTotal',
                                            'ForeignSellVolumeTotal', 'ForeignSellValueTotal', 'ForeignTotalRoom',
                                            'ForeignCurrentRoom']),

            'CoveredWarrant': pd.DataFrame(columns=['TotalMatchVolume', 'MarketStatus', 'TradingDate', 'MatchType', 'ComGroupCode',
                                                    'OrganCode', 'Ticker', 'ReferencePrice', 'OpenPrice', 'ClosePrice', 'CeilingPrice',
                                                    'FloorPrice', 'HighestPrice', 'LowestPrice', 'MatchPrice', 'PriceChange',
                                                    'PercentPriceChange', 'MatchVolume', 'MatchValue', 'TotalMatchValue',
                                                    'TotalBuyTradeVolume', 'TotalSellTradeVolume', 'DealPrice', 'TotalDealVolume',
                                                    'TotalDealValue', 'ForeignBuyVolumeTotal', 'ForeignBuyValueTotal',
                                                    'ForeignSellVolumeTotal', 'ForeignSellValueTotal', 'ForeignTotalRoom',
                                                    'ForeignCurrentRoom']),

            'Derivative': pd.DataFrame(columns=['TotalMatchVolume', 'MarketStatus', 'TradingDate', 'MatchType', 'ComGroupCode',
                                                'DerivativeCode', 'ReferencePrice', 'OpenPrice', 'ClosePrice', 'CeilingPrice',
                                                'FloorPrice', 'HighestPrice', 'LowestPrice', 'MatchPrice', 'PriceChange',
                                                'PercentPriceChange', 'MatchVolume', 'MatchValue', 'TotalMatchValue',
                                                'TotalBuyTradeVolume', 'TotalSellTradeVolume', 'DealPrice', 'TotalDealVolume',
                                                'TotalDealValue', 'ForeignBuyVolumeTotal', 'ForeignBuyValueTotal',
                                                'ForeignSellVolumeTotal', 'ForeignSellValueTotal', 'ForeignTotalRoom',
                                                'ForeignCurrentRoom', 'OpenInterest'])
        }
        self.tickers = [tickers] if isinstance(tickers, str) else tickers
        self._stop = False
        self._stop_event = threading.Event()
        self.message_queues = {ticker: queue.Queue() for ticker in self.tickers}
        self.worker_threads = {}
        # Add a lock for thread safety during connection management
        self.connection_lock = threading.Lock()

        for ticker in self.tickers:
            t = threading.Thread(target=self._message_worker, args=(ticker,), daemon=True)
            self.worker_threads[ticker] = t
            t.start()

        # Create and configure custom handler
        self.custom_handler = CustomHandler()
        self.custom_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.custom_handler.setFormatter(formatter)

        # Add custom handler to logger
        logger = logging.getLogger()
        logger.addHandler(self.custom_handler)
        logger.setLevel(logging.DEBUG)

    def _detect_code(self, code):
        if len(code) == 3:
            return 'Ticker'
        elif code in ['VNMID', 'VNHEAL', 'HNXINDEX', 'VNDIAMOND', 'VNREAL', 'VNMAT', 'VNX50',
                      'VNIT', 'VNSI', 'VNIND', 'VNENE', 'VNCOND', 'VNXALL', 'VN30', 'VNALL',
                      'VNUTI', 'VNFIN', 'VNSML', 'HNX30', 'VN100', 'VNCONS', 'UPCOMINDEX',
                      'VNFINLEAD', 'VNFINSELECT', 'VNINDEX']:
            return 'Index'
        elif len(code) == 8:
            if code[0] == 'C':
                return 'CoveredWarrant'
            else:
                return 'Ticker'
        elif len(code) == 7 or len(code) == 9:
            return 'Derivative'

    def _process_data(self, ticker_type, data):
        df = self.df.get(ticker_type)
        if df is None:
            print(f"Unknown ticker type: {ticker_type}")
            return None
        data_dict = dict(zip(df.columns, data))
        df.loc[0] = data_dict
        df = df.iloc[-1:].reset_index(drop=True)
        self.df[ticker_type] = df
        return df

    def _data_handler(self, message):
        messages = message if isinstance(message, list) else [message]
        for msg in messages:
            try:
                ticker_data = msg['data'][0].split('|')
                ticker = msg['chanel'].split('.')[-1]
                ticker_type = self._detect_code(ticker)
                if ticker_type:
                    df = self._process_data(ticker_type, ticker_data)
                    df_copy = df[-1:].copy()
                    df_copy['Ticker'] = ticker

                    if ticker_type in {'Ticker', 'CoveredWarrant'}:
                        close_price = float(ticker_data[9]) if float(ticker_data[9]) != 0 else float(ticker_data[14])
                        match_type = ticker_data[3]
                        volume = ticker_data[17]
                        df_copy['ClosePrice'] = close_price
                    elif ticker_type == 'Index':
                        match_type = 3
                    else:
                        match_type = ticker_data[3]
                        volume = ticker_data[16]
                        close = float(ticker_data[8]) if float(ticker_data[8]) != 0 else float(ticker_data[13])
                        df_copy['ClosePrice'] = close
                    df_copy['Bu'] = volume if match_type == '1' else (0 if match_type == '2' else np.nan)
                    df_copy['Sd'] = volume if match_type == '2' else (0 if match_type == '1' else np.nan)
                    if self.callback:
                        self.callback(RealTimeData(df_copy))
                else:
                    print(f"Unable to detect ticker type for {ticker}.")
            except Exception as e:
                print(f"Error in data_handler: {e}")

    def _get_log_messages(self):
        return self.custom_handler.get_logs()

    def _build_connection(self):
        return HubConnectionBuilder()\
            .with_url(self.url, options={
                "access_token_factory": lambda: self.access_token()
            })\
            .with_automatic_reconnect({
                "type": "raw",
                "keep_alive_interval": 10,
                "reconnect_interval": [1, 3, 5, 7, 11]
            }).build()

    def _receive_message(self, message):
        try:
            ticker = message[0]['chanel'].split('.')[-1]
            if ticker:
                if ticker in self.message_queues:
                    self.message_queues[ticker].put(message)
                else:
                    print(f"Ticker {ticker} not in queue.")
            else:
                print("No ticker name found in message.")
        except Exception as e:
            print(f"Error in _receive_message: {e}")

    def _message_worker(self, ticker):
        while not self._stop_event.is_set():
            try:
                msg = self.message_queues[ticker].get(timeout=0.01)
            except queue.Empty:
                continue
            try:
                self._data_handler(msg)
            except Exception as e:
                print(f"Error processing message for {ticker}: {e}")
            finally:
                self.message_queues[ticker].task_done()

    def _on_connect(self):
        print("Connection established. Waiting for server processing...")
        time.sleep(5)
        self.connected = True
        self._join_groups()

    def _on_disconnect(self):
        self.connected = False
        if self.hub_connection is not None:
            try:
                self.hub_connection.stop()
                time.sleep(1)  # Ensure the WebSocket is fully closed
            except Exception as e:
                print(f"Error stopping hub connection in _on_disconnect: {e}")
            finally:
                self.hub_connection = None
        print("Disconnected from the hub")

    def _join_groups(self):
        if self.connected and self.hub_connection is not None:
            for ticker in self.tickers:
                self.hub_connection.send("JoinGroup", [f"Realtime.{self._detect_code(ticker)}.{ticker}"])
                time_established_connection = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{time_established_connection} Joined group: Realtime.{self._detect_code(ticker)}.{ticker}")
        else:
            raise ValueError("Cannot join groups, not connected or hub_connection is None")

    def _run(self):
        # Ensure any existing connection is properly stopped
        if self.hub_connection is not None:
            try:
                self.hub_connection.stop()
                time.sleep(1)  # Ensure the WebSocket is fully closed
            except Exception as e:
                print(f"Error stopping hub connection in _run: {e}")
            finally:
                self.hub_connection = None

        # Build and start the connection
        with self.connection_lock:  # Ensure thread safety
            self.hub_connection = self._build_connection()
            if self.hub_connection is None:
                raise ValueError("Failed to build hub connection")

            self.hub_connection.on("ReceiveMessage", self._receive_message)
            self.hub_connection.on_open(self._on_connect)
            self.hub_connection.on_close(self._on_disconnect)
            self.hub_connection.on_close(self._handle_disconnect)
            self.hub_connection.start()

        logging.basicConfig(level=logging.DEBUG)

        while not self._stop_event.is_set():
            time.sleep(0.1)
            mess_error = self._get_log_messages()
            for message in mess_error:
                if "An unexpected error occurred invoking 'JoinGroup' on the server." in message:
                    print(message)
                if "Connection closed with an error" in message:
                    print(message)

    def start(self):
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self._stop_event.set()
        if self.connected and self.hub_connection is not None:
            print("Disconnecting...")
            try:
                self.hub_connection.stop()
                time.sleep(1)  # Ensure the WebSocket is fully closed
            except Exception as e:
                print(f"Error stopping hub connection in stop: {e}")
            finally:
                self.hub_connection = None
        self._stop = True
        self.thread.join()

    def _handle_disconnect(self):
        with self.connection_lock:  # Ensure thread safety during reconnection
            self.connected = False
            while not self.connected and not self._stop_event.is_set():
                try:
                    # Ensure any existing connection is properly stopped
                    if self.hub_connection is not None:
                        try:
                            self.hub_connection.stop()
                            time.sleep(1)  # Add a small delay to ensure the WebSocket is fully closed
                        except Exception as e:
                            print(f"Error stopping hub connection in _handle_disconnect: {e}")
                        finally:
                            self.hub_connection = None

                    # Rebuild the connection
                    print("Attempting to reconnect...")
                    self.hub_connection = self._build_connection()
                    if self.hub_connection is None:
                        raise ValueError("Failed to build hub connection")

                    # Set up handlers
                    self.hub_connection.on("ReceiveMessage", self._receive_message)
                    self.hub_connection.on_open(self._on_connect)
                    self.hub_connection.on_close(self._on_disconnect)
                    self.hub_connection.on_close(self._handle_disconnect)

                    # Start the connection
                    self.hub_connection.start()
                    time.sleep(5)  # Give it some time to establish the connection

                    # Check if the connection is actually established
                    if self.hub_connection.transport is not None:
                        self.connected = True
                        print("Reconnected successfully")
                    else:
                        raise ConnectionError("Failed to establish connection after starting")

                except Exception as e:
                    print(f"Error in reconnection: {e}")
                    self.hub_connection = None  # Ensure it's reset on failure
                    time.sleep(5)  # Wait before retrying