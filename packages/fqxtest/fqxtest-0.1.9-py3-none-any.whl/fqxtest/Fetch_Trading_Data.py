# This code is encrypted and does not contain viruses or Trojans.
import time
import queue
import logging
import warnings
import threading
import numpy as np
import pandas as pd
from typing import Union
from datetime import datetime
from datetime import time as dt_time
from concurrent.futures import ThreadPoolExecutor
from .Aggregates import BarDataUpdate, GetBarData
from signalrcore.hub_connection_builder import HubConnectionBuilder

warnings.filterwarnings("ignore")

### Product API
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

class Fetch_Trading_Data:
    def __init__(self, access_token: callable, 
                 realtime: bool,
                 tickers: Union[list[str], str], 
                 fields: list,
                 adjusted: bool,
                 period: Union[int,None],
                 by: str, 
                 from_date: Union[str, datetime, None],
                 to_date: Union[str, datetime, None],
                 callback: callable,  
                 wait_for_full_timeFrame: bool,
                 lasted: Union[bool,None]):
        
        ### Params

        self.access_token = access_token
        self.realtime = realtime
        self.tickers = [tickers] if isinstance(tickers, str) else tickers
        if isinstance(fields, str):
            fields = [fields]
        if fields == ['full']:
            self.fields = ['open', 'high', 'low', 'close', 'volume', 'bu', 'sd', 'fb', 'fs', 'fn']
        else:
            self.fields = fields 
        self.adjusted = adjusted
        self.period = period
        self.by = by
        self.from_date = from_date
        self.to_date = to_date
        self.callback = callback
        self.wait_for_full_timeFrame = wait_for_full_timeFrame

        if self.realtime and self.callback is None:
            raise ValueError("Callback function is required when realtime = True.")
        
        
        ### Initation
        if self.realtime:
            
            self.connection_log = []
            self.url = REALTIME_API
            self.connected = False 
            self._stop = False
            self.__flag = {ticker: 0 for ticker in self.tickers}
            self.__check = {ticker: 0 for ticker in self.tickers}
            self.message_queue = {ticker: queue.Queue() for ticker in self.tickers}  
            self.temp_data = {ticker: pd.DataFrame() for ticker in self.tickers}
            self.df = {ticker: pd.DataFrame() for ticker in self.tickers}
            self.call_back_data = {ticker: pd.DataFrame() for ticker in self.tickers}
            self.data_rt_final = {ticker: pd.DataFrame() for ticker in self.tickers}
            self.next_time_1M = {ticker: None for ticker in self.tickers}
            self.next_time_1 = {ticker: None for ticker in self.tickers}
            self.next_time_temp_1 = {ticker: None for ticker in self.tickers}
            self.FB_temp = {ticker: 0 for ticker in self.tickers}
            self.FS_temp = {ticker: 0 for ticker in self.tickers}
            self.queue_callback = {ticker: queue.Queue() for ticker in self.tickers}
            self.agg_funcs = {
            'ticker': 'first',
            'open': 'first',
            'low': 'min',
            'high': 'max',
            'close': 'last',
            'volume': 'sum',
            'bu': lambda x: x.sum() if not x.isna().all() else float('nan'),
            'sd': lambda x: x.sum() if not x.isna().all() else float('nan'),
            'fb': 'sum',
            'fs': 'sum',
            'tfb': 'last',
            'tfs': 'last'
            }
        
            self._stop_event = threading.Event()
            self.first_check = {ticker: 0 for ticker in self.tickers}
            self._last_reset_date = None
            self.last_received_time = {ticker: None for ticker in self.tickers}  ##
            self.data_rt_temp = {ticker: pd.DataFrame() for ticker in self.tickers}
            self.hub_connection = None
            self.worker_threads = {}
            self.bardata = {ticker: BarDataUpdate(self.fields) for ticker in self.tickers}
            self.lasted_time_callback = {ticker: 0 for ticker in self.tickers} ##
            self.connection_lock = threading.Lock()
            if self.wait_for_full_timeFrame:
                for ticker in self.tickers:
                    thread = threading.Thread(target=self._message_worker_1, args=(ticker,), daemon=True)
                    self.worker_threads[ticker] = thread
                    thread.start()
            elif self.wait_for_full_timeFrame == False:
                if self.by == '1m':
                    for ticker in self.tickers:
                        thread = threading.Thread(target=self._message_worker_2, args=(ticker,), daemon=True)
                        self.worker_threads[ticker] = thread
                        thread.start()
                else:
                    for ticker in self.tickers:
                        thread = threading.Thread(target=self._message_worker_3, args=(ticker,), daemon=True)
                        self.worker_threads[ticker] = thread
                        thread.start()     
            
            self.callback_thread = {}
            for ticker in self.tickers:
                self.callback_thread[ticker] = threading.Thread(target=self._callback_worker, args=(ticker,), daemon=True)
                self.callback_thread[ticker].start()
            self._validate_realtime()
        else:
            self.lasted = lasted
            self._validate_historical()
        ### Dict
        self.VALID_BY = {
            '1m': 'EachMinute', 
            '5m': 'EachFiveMinutes', 
            '15m': 'EachFifteenMinutes', 
            '30m': 'EachThirtyMinutes',
            '1h': 'EachOneHour', 
            '2h': 'EachTwoHours',
            '4h': 'EachFourHours',
            '1d': 'Daily'
        }

        self.FREQ_MUL = {
            'EachMinute': 1, 
            'EachFiveMinutes': 5, 
            'EachFifteenMinutes': 15, 
            'EachThirtyMinutes': 30,
            'EachOneHour': 60, 
            'EachTwoHours': 120,
            'EachFourHours': 240,
            'Daily': 1440
        }
        
 
        try:
            self.freq = self.VALID_BY[self.by]
        except:
            raise ValueError('Invalid value for "by". Must be one of: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d')
        self.multiplier = self.FREQ_MUL[self.freq]
        
        # self._stop_event = threading.Event()
        self.custom_handler = CustomHandler()
        self.custom_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.custom_handler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(self.custom_handler)
        logger.setLevel(logging.DEBUG)
        
       
       
    def _validate_historical(self):
        if not self.from_date and not self.to_date and self.period is None: 
            raise ValueError("From_date, To_date cannot be left blank")
        
        if not self.from_date and self.to_date and self.period is None:
            raise ValueError("From_date cannot be left blank")
        if (self.from_date or self.to_date) and self.period is not None:
            raise ValueError("From_date, To_date and Period cannot coexist")
        
        if self.from_date and self.period is not None:
            raise ValueError("From_date, To_date and Period cannot coexist")
        
        if self.lasted is None:
            self.lasted = False

        if self.from_date and not self.to_date and self.period is None:
            self.to_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        if not self.from_date and not self.to_date and self.period is not None:
            self.to_date = datetime.now().strftime('%Y-%m-%d %H:%M')


    def _validate_realtime(self):
        if self.to_date:
            raise ValueError("To_date is not required for realtime data")
        
        if self.from_date and self.period is not None:
            raise ValueError("From_date and Period cannot coexist")
        
        if not self.from_date and self.period is None:
            raise ValueError("From_date or Period is required for realtime data")
        
    def _calculate_next_time_one_min(self, trading_date_local):
        trading_date_pd = pd.Timestamp(trading_date_local)
        trading_date_pd_plus_1min = (trading_date_pd + pd.Timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M')
        return trading_date_pd_plus_1min

    def _calculate_next_time(self, trading_date_local, multiplier, freq):
        trading_date_pd = pd.Timestamp(trading_date_local)

        if freq in ['EachMinute', 'EachFiveMinutes', 'EachFifteenMinutes', 'EachThirtyMinutes']:
            freq_multiplier = {'EachMinute': 1, 'EachFiveMinutes': 5, 'EachFifteenMinutes': 15, 'EachThirtyMinutes': 30}           
            num_of_minutes = trading_date_pd.hour * 60 + trading_date_pd.minute - 540  ### 09:00    
            group = num_of_minutes // (multiplier * freq_multiplier[freq])
            time_standard = (group + 1) * (multiplier * freq_multiplier[freq]) + 540   ### 09:00
            hour_standard, minute_standard = divmod(time_standard, 60)
            next_time = f"{trading_date_pd.date()} {hour_standard:02}:{minute_standard:02}"
            
        elif freq in ['EachOneHour', 'EachTwoHours', 'EachFourHours']:
            freq_multiplier = {'EachOneHour': 1, 'EachTwoHours': 2, 'EachFourHours': 4}
            group = (trading_date_pd.hour - 9) // (multiplier * freq_multiplier[freq])
            hour_standard = (group + 1) * (multiplier * freq_multiplier[freq]) + 9
            if hour_standard > 14:
                hour_standard = 9
                if trading_date_pd.weekday() == 4:
                    trading_date_pd += pd.Timedelta(days=3)   
                elif trading_date_pd.weekday() == 5:
                    trading_date_pd += pd.Timedelta(days=2)        
                else:
                    trading_date_pd += pd.Timedelta(days=1)      
            next_time = f"{trading_date_pd.date()} {hour_standard:02}:00"

        else:
            if trading_date_pd.weekday() == 4:
                trading_date_pd += pd.Timedelta(days=3)        
            elif trading_date_pd.weekday() == 5:
                trading_date_pd += pd.Timedelta(days=2)      
            else:
                trading_date_pd += pd.Timedelta(days=1)   
            next_time = trading_date_pd

        return next_time
    
    def _detect_code(self, code):
        if len(code) == 3:
            return 'Ticker'
        
        elif code in ['VNMID', 'VNHEAL', 'HNXIndex', 'VNDIAMOND', 'VNREAL', 'VNMAT', 
                    'VNX50', 'VNIT', 'VNSI', 'VNIND', 'VNENE', 'VNCOND', 'VNXALL', 
                    'VN30', 'VNALL', 'VNUTI', 'VNFIN', 'VNSML', 'HNX30', 'VN100', 
                    'VNCONS', 'UPCOMINDEX', 'VNFINLEAD', 'VNFINSELECT', 'VNINDEX']:
            return 'Index'
        
        elif len(code) == 8:           
            if code[0] == 'C':
                return 'CoveredWarrant'
            else:
                return 'Ticker'
        
        elif (len(code) == 7 or len(code) == 9) and code[4] == 'F':
            return 'Derivative'
     
    def _data_handler_1(self, message):            
            try:           
                ticker_data = message[0]['data'][0].split('|')
                ticker = message[0]['chanel'].split('.')[-1]
                if ticker in self.tickers:
                    try:
                        code_type = self._detect_code(ticker)
                        trading_date_str = ticker_data[2]
                        if code_type in {'Ticker', 'CoveredWarrant'}:  
                            close_price = float(ticker_data[9]) if float(ticker_data[9]) != 0 else float(ticker_data[14])
                            volume = float(ticker_data[17])
                            match_type = ticker_data[3]
                            FBuy = int(ticker_data[26])
                            FSell = int(ticker_data[28])
                            FNet = FBuy - FSell        

                        elif code_type == 'Index':
                            close_price = float(ticker_data[6])
                            volume = float(ticker_data[12])
                            match_type = 3                    
                            FBuy = int(ticker_data[23])
                            FSell = int(ticker_data[25])
                            FNet = FBuy - FSell
                            
                        else:
                            close_price = float(ticker_data[8]) if float(ticker_data[8]) != 0 else float(ticker_data[13])
                            volume = float(ticker_data[16])
                            match_type = ticker_data[3]   
                            FBuy = int(ticker_data[25])
                            FSell = int(ticker_data[27])
                            FNet = FBuy - FSell  

                        self.next_time_temp_1[ticker] = self._calculate_next_time(pd.to_datetime(trading_date_str).strftime('%Y-%m-%d %H:%M'), 1, self.freq)
                        
                        if self.__check[ticker] == 0: 
                            self.next_time_1M[ticker] = self._calculate_next_time_one_min(trading_date_str)
                            self.__check[ticker] = 1
                            
                    except Exception as e:
                        # print(f"Error processing message: {e}")
                        return
                    
                    self.last_received_time[ticker] = trading_date_str
                    trading_date_local = pd.to_datetime(trading_date_str).strftime('%Y-%m-%d %H:%M')
                    
                    if trading_date_local < self.next_time_1M[ticker]:
                        return                           
                    
                    else:
                        
                        minutes_data = {
                            'ticker': ticker,
                            'timestamp': trading_date_local,
                            'open': close_price,
                            'low': close_price,
                            'high': close_price,
                            'close': close_price,
                            'volume': volume,
                            'bu': volume if match_type == '1' else (0 if match_type == '2' else np.nan),
                            'sd': volume if match_type == '2' else (0 if match_type == '1' else np.nan),
                            'fb': FBuy,
                            'fs': FSell,
                            'fn': FNet,
                            'tfb': FBuy,
                            'tfs': FSell
                        }
            
                        if self.__flag[ticker] == 0:
                            if any(field in self.fields for field in ['fn', 'fb', 'fs']):
                                lst_fields = list(set(self.fields + ['fn', 'fb', 'fs']))
                            else:
                                lst_fields = self.fields
                            params = {
                                "access_token": self.access_token(),
                                "tickers": [ticker],  
                                "by": self.by,
                                "fields": lst_fields,
                                "adjusted": self.adjusted
                            }

                            if self.period is not None:
                                params["period"] = self.period + 2
                                params["from_date"] = None
                                params["to_date"] = None
                            else:
                                params["from_date"] = self.from_date
                                params["to_date"] = self.next_time_1M

                            temp_data = GetBarData(**params).get(get_total_F=True).to_dataFrame()
                            if not temp_data.empty:
                                ticker_data = temp_data[temp_data['ticker'] == ticker]
                                if not ticker_data.empty:
                                    ticker_data['ticker'] = ticker 

                                    self.df[ticker] = pd.concat([self.df[ticker], ticker_data], ignore_index=True)
                                    self.FB_temp[ticker] = self.df[ticker]['tfb'].iloc[-1]
                                    self.FS_temp[ticker] = self.df[ticker]['tfs'].iloc[-1]
                                    
                                    # if self.by == '1m':
                                    #     if self.df[ticker]['timestamp'].iloc[-1] == datetime.now().strftime('%Y-%m-%d %H:%M'):
                                    #         self.df[ticker] = self.df[ticker][:-1]
                                    #     else:
                                    #         self.df[ticker] = self.df[ticker][1:]
                                    # else:
                                    #     if self.df[ticker]['timestamp'].iloc[-1] == datetime.now().strftime('%Y-%m-%d %H:%M'):
                                    #         self.df[ticker] = self.df[ticker][:-1]
                                
                                self.__flag[ticker] = 1
                        
                        self.data_rt_temp[ticker] = pd.concat([self.data_rt_temp[ticker], pd.DataFrame([minutes_data])], ignore_index=True)
                        self.data_rt_temp[ticker]['timestamp'] = pd.to_datetime(self.data_rt_temp[ticker]['timestamp'], errors='coerce')
                
                        if self.freq != "Daily":  
                            minuteOrder = self.data_rt_temp[ticker]['timestamp'].dt.hour * 60 + self.data_rt_temp[ticker]['timestamp'].dt.minute - 540
                            group = minuteOrder // self.multiplier
                            timeStandard = group * self.multiplier + 540
                            hoursStandard = (timeStandard // 60).astype(int).astype(str).str.zfill(2)
                            minutesStandard = (timeStandard % 60).astype(int).astype(str).str.zfill(2)
                            date = self.data_rt_temp[ticker]['timestamp'].dt.date.astype(str)
                            self.data_rt_temp[ticker]['timestamp'] = date + ' ' + hoursStandard + ':' + minutesStandard 
                        else:
                            date = self.data_rt_temp[ticker]['timestamp'].dt.date.astype(str)
                            self.data_rt_temp[ticker]['timestamp'] = date + ' 00:00'

                        try:
                            if self.data_rt_temp[ticker]['timestamp'].iloc[-1][0:10] == self.data_rt_temp[ticker]['timestamp'].iloc[-2][0:10]:
                                self.data_rt_temp[ticker]['fb'].iloc[-1] = self.data_rt_temp[ticker]['tfb'].iloc[-1] - self.data_rt_temp[ticker]['tfb'].iloc[-2]
                                self.data_rt_temp[ticker]['fs'].iloc[-1] = self.data_rt_temp[ticker]['tfs'].iloc[-1] - self.data_rt_temp[ticker]['tfs'].iloc[-2]
                            else:
                                self.data_rt_temp[ticker]['fb'].iloc[-1] = self.data_rt_temp[ticker]['tfb'].iloc[-1] 
                                self.data_rt_temp[ticker]['fs'].iloc[-1] = self.data_rt_temp[ticker]['tfs'].iloc[-1]
                        except:
                            if self.data_rt_temp[ticker]['timestamp'].iloc[-1][0:10] == self.df[ticker]['timestamp'].iloc[-1][0:10]:
                                self.data_rt_temp[ticker]['fb'].iloc[-1] = self.data_rt_temp[ticker]['tfb'].iloc[-1] - self.FB_temp[ticker]
                                self.data_rt_temp[ticker]['fs'].iloc[-1] = self.data_rt_temp[ticker]['tfs'].iloc[-1] - self.FS_temp[ticker]
                            else:
                                self.data_rt_temp[ticker]['fb'].iloc[-1] = self.data_rt_temp[ticker]['tfb'].iloc[-1]
                                self.data_rt_temp[ticker]['fs'].iloc[-1] = self.data_rt_temp[ticker]['tfs'].iloc[-1]

                        self.data_rt_temp[ticker] = self.data_rt_temp[ticker].groupby('timestamp').agg(self.agg_funcs).reset_index()
                        self.temp_data[ticker] = pd.concat([self.df[ticker], self.data_rt_temp[ticker]], ignore_index=True)
                        self.data_rt_final[ticker] = self.temp_data[ticker]
                    
                if self.next_time_1[ticker] != self.next_time_temp_1[ticker] and self.next_time_temp_1[ticker] is not None:

                    self.next_time_1[ticker] = self.next_time_temp_1[ticker]
                    # temp = self.data_rt_final[ticker]
                    # selected_columns = ['ticker', 'timestamp'] + [self.FIELD_FORMATS[field] for field in self.fields if field in self.FIELD_FORMATS]
                    try:
                        filtered_data = self.data_rt_final[ticker]                
                        try:
                            filtered_data = filtered_data.drop(columns=['fn'])
                        except:
                            pass
                        valid_columns = [col for col in self.agg_funcs.keys() if col in filtered_data.columns]
                
                        valid_aggregation_rules = {col: self.agg_funcs[col] for col in valid_columns}
                        
                        self.call_back_data[ticker] = (filtered_data.groupby('timestamp').agg(valid_aggregation_rules).reset_index())

                        if self.call_back_data[ticker]['timestamp'].iloc[-1] == datetime.now().strftime('%Y-%m-%d %H:%M'):
                            self.call_back_data[ticker] = self.call_back_data[ticker][:-1]
                        
                        if self.period is not None and len(self.call_back_data[ticker]) > self.period:
                            self.call_back_data[ticker].drop(index=self.call_back_data[ticker].index[:-self.period], inplace=True)
                        
                        self.call_back_data[ticker]['fn'] = self.call_back_data[ticker]['fb'] - self.call_back_data[ticker]['fs']
                        self.queue_callback[ticker].put(self.call_back_data[ticker])     
                    except:
                        pass     
            except Exception as e:
                print(f"Unexpected error: {e}")
                return
    
    def _data_handler_2(self, message):   
            try:    
                ticker_data = message[0]['data'][0].split('|')
                ticker = message[0]['chanel'].split('.')[-1]
                if ticker in self.tickers:
                    try:                
                        code_type = self._detect_code(ticker)
                        trading_date_str = ticker_data[2]
                        if code_type in {'Ticker', 'CoveredWarrant'}:     
                            close_price = float(ticker_data[9]) if float(ticker_data[9]) != 0 else float(ticker_data[14])
                            volume = float(ticker_data[17])
                            match_type = ticker_data[3]
                            FBuy = int(ticker_data[26])
                            FSell = int(ticker_data[28])
                            FNet = FBuy - FSell
                        
                        elif code_type == 'Index':
                            close_price = float(ticker_data[6])
                            volume = float(ticker_data[12])
                            match_type = 3                   
                            FBuy = int(ticker_data[23])
                            FSell = int(ticker_data[25])
                            FNet = FBuy - FSell
                            
                        else:
                            close_price = float(ticker_data[8]) if float(ticker_data[8]) != 0 else float(ticker_data[13])
                            volume = float(ticker_data[16])
                            match_type = ticker_data[3]   
                            FBuy = int(ticker_data[25])
                            FSell = int(ticker_data[27])
                            FNet = FBuy - FSell  
                            
                        if self.__check[ticker] == 0:       
                            self.next_time_1M[ticker] = self._calculate_next_time_one_min(trading_date_str)                         
                            self.__check[ticker] = 1

                    except Exception as e:
                        # print(f"Error processing message: {e}")
                        return
                    self.last_received_time[ticker] = trading_date_str
                    trading_date_local = pd.to_datetime(trading_date_str).strftime('%Y-%m-%d %H:%M')
                   
                    if trading_date_local < self.next_time_1M[ticker]:
                        return                           
                    else:
                        minutes_data = {
                            'ticker': ticker,
                            'timestamp': trading_date_local,
                            'open': close_price,
                            'low': close_price,
                            'high': close_price,
                            'close': close_price,
                            'volume': volume,
                            'bu': volume if match_type == '1' else (0 if match_type == '2' else np.nan),
                            'sd': volume if match_type == '2' else (0 if match_type == '1' else np.nan),   
                            'fb': FBuy,
                            'fs': FSell,
                            'fn': FNet, 
                            'tfb': FBuy,
                            'tfs': FSell       
                        }       
                                        
                        if self.__flag[ticker] == 0:
                            if any(field in self.fields for field in ['fn', 'fb', 'fs']):
                                lst_fields = list(set(self.fields + ['fn', 'fb', 'fs']))
                            else:
                                lst_fields = self.fields
                                
                            params = {
                                "access_token": self.access_token(),
                                "tickers": [ticker],
                                "by": self.by,
                                "fields": lst_fields,
                                "adjusted": self.adjusted
                            }
                            
                            if self.period is not None:
                                params["period"] = self.period 
                                params["from_date"] = None
                                params["to_date"] = None
                            else:
                                params["from_date"] = self.from_date
                                params["to_date"] = self.next_time_1M[ticker]

                            historical_data = GetBarData(**params).get(get_total_F=True).to_dataFrame()
                            
                            if not historical_data.empty:
        
                                ticker_data = historical_data[historical_data['ticker'] == ticker]
                                if not ticker_data.empty:
                                    ticker_data['ticker'] = ticker 

                                    self.df[ticker] = pd.concat([self.df[ticker], ticker_data], ignore_index=True)
                                    self.FB_temp[ticker] = self.df[ticker]['tfb'].iloc[-1]
                                    self.FS_temp[ticker] = self.df[ticker]['tfs'].iloc[-1]
                                    # if self.df[ticker]['timestamp'].iloc[-1] == datetime.now().strftime('%Y-%m-%d %H:%M'):
                                    if self.df[ticker]['timestamp'].iloc[-1] == trading_date_local:
                                        self.df[ticker] = self.df[ticker][:-1]
                                    else:
                                        self.df[ticker] = self.df[ticker][1:]

                                # del ticker_data
                                # del historical_data
                                
                                self.__flag[ticker] = 1 

                        self.data_rt_temp[ticker] = pd.concat([self.data_rt_temp[ticker], pd.DataFrame([minutes_data])], ignore_index=True)
                        
                        self.data_rt_temp[ticker]['timestamp'] = pd.to_datetime(self.data_rt_temp[ticker]['timestamp'], errors='coerce')         
                        minuteOrder = self.data_rt_temp[ticker]['timestamp'].dt.hour * 60 + self.data_rt_temp[ticker]['timestamp'].dt.minute - 540
                        group = minuteOrder // self.multiplier
                        timeStandard = group * self.multiplier + 540
                        hoursStandard = (timeStandard // 60).astype(int).astype(str).str.zfill(2)
                        minutesStandard = (timeStandard % 60).astype(int).astype(str).str.zfill(2)
                        date = self.data_rt_temp[ticker]['timestamp'].dt.date.astype(str)
                        self.data_rt_temp[ticker]['timestamp'] = date + ' ' + hoursStandard + ':' + minutesStandard 

                        try:
                            if self.data_rt_temp[ticker]['timestamp'].iloc[-1][0:10] == self.data_rt_temp[ticker]['timestamp'].iloc[-2][0:10]:
                                self.data_rt_temp[ticker]['fb'].iloc[-1] = self.data_rt_temp[ticker]['tfb'].iloc[-1] - self.data_rt_temp[ticker]['tfb'].iloc[-2]
                                self.data_rt_temp[ticker]['fs'].iloc[-1] = self.data_rt_temp[ticker]['tfs'].iloc[-1] - self.data_rt_temp[ticker]['tfs'].iloc[-2]
                            else:
                                self.data_rt_temp[ticker]['fb'].iloc[-1] = self.data_rt_temp[ticker]['tfb'].iloc[-1] 
                                self.data_rt_temp[ticker]['fs'].iloc[-1] = self.data_rt_temp[ticker]['tfs'].iloc[-1]
                        except:
                            if self.data_rt_temp[ticker]['timestamp'].iloc[-1][0:10] == self.df[ticker]['timestamp'].iloc[-1][0:10]:
                                self.data_rt_temp[ticker]['fb'].iloc[-1] = self.data_rt_temp[ticker]['tfb'].iloc[-1] - self.FB_temp[ticker]
                                self.data_rt_temp[ticker]['fs'].iloc[-1] = self.data_rt_temp[ticker]['tfs'].iloc[-1] - self.FS_temp[ticker]
                            else:
                                self.data_rt_temp[ticker]['fb'].iloc[-1] = self.data_rt_temp[ticker]['tfb'].iloc[-1]
                                self.data_rt_temp[ticker]['fs'].iloc[-1] = self.data_rt_temp[ticker]['tfs'].iloc[-1]
                        
                        self.data_rt_temp[ticker] = self.data_rt_temp[ticker].groupby('timestamp').agg(self.agg_funcs).reset_index()
                                        
                        self.call_back_data[ticker] = pd.concat([self.df[ticker], self.data_rt_temp[ticker]], ignore_index=True)
                       
                        if self.period is not None and len(self.call_back_data[ticker]) > self.period:
                            self.call_back_data[ticker].drop(index=self.call_back_data[ticker].index[:-self.period], inplace=True)
                    
                        if 'fn' in self.fields:
                            self.call_back_data[ticker]['fn'] = self.call_back_data[ticker]['fb'] - self.call_back_data[ticker]['fs']
          
                        self.queue_callback[ticker].put(self.call_back_data[ticker])
            except Exception as e:
                print(f"Unexpected error: {e}")
                return    
            
    def _data_handler_3(self, message):
            try:
                ticker_data = message[0]['data'][0].split('|')
                ticker = message[0]['chanel'].split('.')[-1]
                if ticker in self.tickers:
                    try:                
                        code_type = self._detect_code(ticker)
                        trading_date_str = ticker_data[2]
                        if code_type in {'Ticker', 'CoveredWarrant'}:     
                            close_price = float(ticker_data[9]) if float(ticker_data[9]) != 0 else float(ticker_data[14])
                            volume = float(ticker_data[17])
                            match_type = ticker_data[3]
                            FBuy = int(ticker_data[26])
                            FSell = int(ticker_data[28])
                            FNet = FBuy - FSell
                        
                        elif code_type == 'Index':
                            close_price = float(ticker_data[6])
                            volume = float(ticker_data[12])
                            match_type = 3                   
                            FBuy = int(ticker_data[23])
                            FSell = int(ticker_data[25])
                            FNet = FBuy - FSell
                            
                        else:
                            close_price = float(ticker_data[8]) if float(ticker_data[8]) != 0 else float(ticker_data[13])
                            volume = float(ticker_data[16])
                            match_type = ticker_data[3]   
                            FBuy = int(ticker_data[25])
                            FSell = int(ticker_data[27])
                            FNet = FBuy - FSell  
                        
                        if self.__check[ticker] == 0:       
                            self.next_time_1M[ticker] = self._calculate_next_time_one_min(trading_date_str)                         
                            self.__check[ticker] = 1

                    except Exception as e:
                        # print(f"Error processing message: {e}")
                        return
                    self.last_received_time[ticker] = trading_date_str
                    trading_date_local = pd.to_datetime(trading_date_str).strftime('%Y-%m-%d %H:%M')
                    
                    if trading_date_local < self.next_time_1M[ticker]:
                        return                           
                    else:
                        minutes_data = {
                            'ticker': ticker,
                            'timestamp': trading_date_local,
                            'open': close_price,
                            'low': close_price,
                            'high': close_price,
                            'close': close_price,
                            'volume': volume,
                            'bu': volume if match_type == '1' else (0 if match_type == '2' else np.nan),
                            'sd': volume if match_type == '2' else (0 if match_type == '1' else np.nan),   
                            'fb': FBuy,
                            'fs': FSell,
                            'fn': FNet, 
                            'tfb': FBuy,
                            'tfs': FSell       
                        }       
                                        
                        if self.__flag[ticker] == 0:
                            if any(field in self.fields for field in ['fn', 'fb', 'fs']):
                                lst_fields = list(set(self.fields + ['fn', 'fb', 'fs']))
                            else:
                                lst_fields = self.fields
                                
                            params = {
                                "access_token": self.access_token(),
                                "tickers": [ticker],
                                "by": self.by,
                                "fields": lst_fields,
                                "adjusted": self.adjusted
                            }
                            
                            if self.period is not None:
                                params["period"] = self.period 
                                params["from_date"] = None
                                params["to_date"] = None
                            else:
                                params["from_date"] = self.from_date
                                params["to_date"] = self.next_time_1M[ticker]

                            historical_data = GetBarData(**params).get(get_total_F=True).to_dataFrame()
                            
                            if not historical_data.empty:
        
                                ticker_data = historical_data[historical_data['ticker'] == ticker]
                                if not ticker_data.empty:
                                    ticker_data['ticker'] = ticker 

                                    self.df[ticker] = pd.concat([self.df[ticker], ticker_data], ignore_index=True)
                                    self.FB_temp[ticker] = self.df[ticker]['tfb'].iloc[-1]
                                    self.FS_temp[ticker] = self.df[ticker]['tfs'].iloc[-1]
                                    if self.df[ticker]['timestamp'].iloc[-1] == datetime.now().strftime('%Y-%m-%d %H:%M'):
                                        self.df[ticker] = self.df[ticker][:-1]
                                last_df = self.df[ticker].iloc[[-1]]
                                last_df['timestamp'] = pd.to_datetime(last_df['timestamp'], errors='coerce')
                                
                                if self.freq != "Daily":  
                                    minuteOrder = last_df['timestamp'].dt.hour * 60 + last_df['timestamp'].dt.minute - 540
                                    group = minuteOrder // self.multiplier
                                    timeStandard = group * self.multiplier + 540
                                    hoursStandard = (timeStandard // 60).astype(int).astype(str).str.zfill(2)
                                    minutesStandard = (timeStandard % 60).astype(int).astype(str).str.zfill(2)
                                    date = last_df['timestamp'].dt.date.astype(str)
                                    last_df['timestamp'] = date + ' ' + hoursStandard + ':' + minutesStandard 
                            
                                else:
                                    date = last_df['timestamp'].dt.date.astype(str)
                                    last_df['timestamp'] = date + ' 00:00'
                                self.__flag[ticker] = 1 
                                    
                        self.data_rt_temp[ticker] = pd.concat([self.data_rt_temp[ticker], pd.DataFrame([minutes_data])], ignore_index=True)          
                        self.data_rt_temp[ticker]['timestamp'] = pd.to_datetime(self.data_rt_temp[ticker]['timestamp'], errors='coerce')
                        
                        if self.freq != "Daily":  
                            minuteOrder = self.data_rt_temp[ticker]['timestamp'].dt.hour * 60 + self.data_rt_temp[ticker]['timestamp'].dt.minute - 540
                            group = minuteOrder // self.multiplier
                            timeStandard = group * self.multiplier + 540
                            hoursStandard = (timeStandard // 60).astype(int).astype(str).str.zfill(2)
                            minutesStandard = (timeStandard % 60).astype(int).astype(str).str.zfill(2)
                            date = self.data_rt_temp[ticker]['timestamp'].dt.date.astype(str)
                            self.data_rt_temp[ticker]['timestamp'] = date + ' ' + hoursStandard + ':' + minutesStandard 
                            
                        else:
                            date = self.data_rt_temp[ticker]['timestamp'].dt.date.astype(str)
                            self.data_rt_temp[ticker]['timestamp'] = date + ' 00:00'
                        
                        if self.first_check[ticker] == 0:
                            if self.df[ticker]['timestamp'].iloc[-1] == self.data_rt_temp[ticker]['timestamp'].iloc[-1]:
                                self.df[ticker] = self.df[ticker][:-1]
                                self.data_rt_temp[ticker] = pd.concat([last_df, self.data_rt_temp[ticker]], ignore_index=True)
                            self.first_check[ticker] = 1
                        
                        try:
                            if self.data_rt_temp[ticker]['timestamp'].iloc[-1][0:10] == self.data_rt_temp[ticker]['timestamp'].iloc[-2][0:10]:
                                self.data_rt_temp[ticker]['fb'].iloc[-1] = self.data_rt_temp[ticker]['tfb'].iloc[-1] - self.data_rt_temp[ticker]['tfb'].iloc[-2]
                                self.data_rt_temp[ticker]['fs'].iloc[-1] = self.data_rt_temp[ticker]['tfs'].iloc[-1] - self.data_rt_temp[ticker]['tfs'].iloc[-2]
                            else:
                                self.data_rt_temp[ticker]['fb'].iloc[-1] = self.data_rt_temp[ticker]['tfb'].iloc[-1] 
                                self.data_rt_temp[ticker]['fs'].iloc[-1] = self.data_rt_temp[ticker]['tfs'].iloc[-1]
                        except:
                            if self.data_rt_temp[ticker]['timestamp'].iloc[-1][0:10] == last_df['timestamp'].iloc[-1][0:10]:
                                self.data_rt_temp[ticker]['fb'].iloc[-1] = self.data_rt_temp[ticker]['tfb'].iloc[-1] - self.FB_temp[ticker]
                                self.data_rt_temp[ticker]['fs'].iloc[-1] = self.data_rt_temp[ticker]['tfs'].iloc[-1] - self.FS_temp[ticker]
                            else:
                                self.data_rt_temp[ticker]['fb'].iloc[-1] = self.data_rt_temp[ticker]['tfb'].iloc[-1]
                                self.data_rt_temp[ticker]['fs'].iloc[-1] = self.data_rt_temp[ticker]['tfs'].iloc[-1]
                        
                        self.data_rt_temp[ticker] = self.data_rt_temp[ticker].groupby('timestamp').agg(self.agg_funcs).reset_index()
                        
                        self.call_back_data[ticker] = pd.concat([self.df[ticker], self.data_rt_temp[ticker]], ignore_index=True)
                        # if self.call_back_data[ticker].iloc[-1]['timestamp'] == self.data_rt_temp[ticker]['timestamp'].iloc[-1]:
                        #     self.call_back_data[ticker] = self.call_back_data[ticker].groupby('timestamp').agg(self.agg_funcs).reset_index() 
                        if self.period is not None and len(self.call_back_data[ticker]) > self.period:
                            self.call_back_data[ticker].drop(index=self.call_back_data[ticker].index[:-self.period], inplace=True)
                        if 'fn' in self.fields:
                            self.call_back_data[ticker]['fn'] = self.call_back_data[ticker]['fb'] - self.call_back_data[ticker]['fs']
                        self.queue_callback[ticker].put(self.call_back_data[ticker])
                        # if self.callback: 
                        #     self.callback(BarDataUpdate(self.call_back_data[ticker], fields=self.fields))

            except Exception as e:
                print(f"Unexpected error: {e}")
                return            
            
    
    def _join_groups(self):
        if self.connected:
            self.tickers = sorted(self.tickers, key=len)
            time.sleep(2)
            for ticker in self.tickers:
                self.hub_connection.send("JoinGroup", [f"Realtime.{self._detect_code(ticker)}.{ticker}"])
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Joined group: {self._detect_code(ticker)}.{ticker}")
        else:
            raise ValueError("Cannot join groups, not connected.")
    
    def _build_connection(self): 
        
        connection = HubConnectionBuilder().with_url(
            self.url, options={"access_token_factory": lambda: self.access_token()}
        ).with_automatic_reconnect({
            "type": "raw", "keep_alive_interval": 10,
            "reconnect_interval": [1, 3, 5, 7, 11, 13]
        }).build()
        
        connection.on_reconnect(lambda: self._fetch_missing_data())
        return connection
    
    def _receive_message(self, message):
        try:
            ticker = message[0]['chanel'].split('.')[-1]
            if ticker:
                if ticker in self.message_queue:
                    self.message_queue[ticker].put(message)
                else:
                    print(f"Ticker {ticker} not in data.")
            else:
                print("No ticker in server data message:", message)
        except Exception as e:
            print("Error in receive_message:", e)
    
    def _message_worker_1(self, ticker):
        while not self._stop_event.is_set():
            try:
                message = self.message_queue[ticker].get(0.001)
            except queue.Empty:
                continue
            try:     
                self._data_handler_1(message)
            except Exception as e:
                print(f"Error processing message in worker for {ticker}: {e}")
            finally:
                self.message_queue[ticker].task_done()
                
    def _message_worker_2(self, ticker):
        while not self._stop_event.is_set():
            try:
                message = self.message_queue[ticker].get(timeout=0.001)
            except queue.Empty:
                continue
            try:
                self._data_handler_2(message)
       
            except Exception as e:
                print(f"Error processing message in worker for {ticker}: {e}")
            finally:
                self.message_queue[ticker].task_done()
        
    def _message_worker_3(self, ticker):
        while not self._stop_event.is_set():
            try:
                message = self.message_queue[ticker].get(0.001)    
            except queue.Empty:
                continue
            try:
                self._data_handler_3(message)
            except Exception as e:
                print(f"Error processing message in worker for {ticker}: {e}")
            finally:
                self.message_queue[ticker].task_done()
                
    def _callback_worker(self, ticker):
        while not self._stop_event.is_set():
            try:
                data = self.queue_callback[ticker].get(0.001)
                if data is not None and not data.empty:
                    current_time = time.time()
                    if current_time - self.lasted_time_callback[ticker] >= 1:
                        if self.callback:  
                            self.bardata[ticker]._update(data)
                            self.callback(self.bardata[ticker])
                            self.lasted_time_callback[ticker] = current_time
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing callback for {ticker}: {e}")
            finally:
                self.queue_callback[ticker].task_done()
                    
    def _handle_error(self, error):
        print(f"Error: {error}")
    
    def _on_connect(self):
        print("Connection established. Waiting for server processing...")
        reconnect_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')##
        self.connection_log.append(("Reconnected", reconnect_time))##
        time.sleep(5)  
        self.connected = True   
        self._join_groups()
    
    def _on_disconnect(self):
        self.connected = False
        if self.hub_connection:
            self.hub_connection.stop()
        disconnect_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.connection_log.append(("Disconnected", disconnect_time))
        print("Disconnected from the hub")

    def _get_log_messages(self):
        return self.custom_handler.get_logs()
    
    def _run(self):

        if self.hub_connection is not None and self.hub_connection.transport is not None:
            self.hub_connection.stop()
        self.hub_connection = self._build_connection()
        
        self.hub_connection.on("ReceiveMessage", self._receive_message)
        self.hub_connection.on_close(self._handle_error)
        self.hub_connection.on_open(self._on_connect)
        self.hub_connection.on_close(self._on_disconnect)
        self.hub_connection.on_close(self._handle_disconnect)
        
        self.hub_connection.start()
        
        while not self._stop_event.is_set():
            time.sleep(0.1)
            mess_error = self._get_log_messages()
            for message in mess_error:
                if "An unexpected error occurred invoking 'JoinGroup' on the server." in message:
                    print(message)
                if "Connection closed with an error" in message:
                    print(message)
                    
                    
            current_time = datetime.now()
            current_date = current_time.date()
            reset_time = datetime.combine(current_date, dt_time(0, 0))  
            if current_time >= reset_time and self._last_reset_date != current_date:
                
                for ticker in self.tickers:
                    if ticker in self.data_rt_temp and not self.data_rt_temp[ticker].empty:      
                        self.FB_temp[ticker] = 0
                        self.FS_temp[ticker] = 0
                        self.df[ticker] = pd.DataFrame(columns=self.df[ticker].columns)
                        self.data_rt_temp[ticker] = pd.DataFrame(columns=self.data_rt_temp[ticker].columns)
                        self.call_back_data[ticker] = pd.DataFrame(columns=self.call_back_data[ticker].columns)
                        self.data_rt_final[ticker] = pd.DataFrame(columns=self.data_rt_final[ticker].columns)
                        self.temp_data[ticker] = pd.DataFrame(columns=self.temp_data[ticker].columns)
                        self.first_check[ticker] = 0
                        self.__flag[ticker] = 0
                        self.__check[ticker] = 0
                        self.first_check[ticker] = 0
                self._last_reset_date = current_date

    def get_data(self):
        if not self.realtime:   
            if self.lasted:                    
                params = {
                    "access_token": self.access_token(),
                    "tickers": self.tickers,
                    "by": self.by,
                    "fields": self.fields,
                    "adjusted": self.adjusted
                }
                if self.period is not None:
                    params["period"] = self.period
                else:
                    params["from_date"] = self.from_date
                    params["to_date"] = self.to_date if self.to_date is not None else None
            
                data = GetBarData(**params).get(get_total_F = False).to_dataFrame()
                return data.drop(columns=['tfb', 'tfs'], errors='ignore')
            else:
                params = {
                    "access_token": self.access_token(),
                    "tickers": self.tickers,
                    "by": self.by,
                    "fields": self.fields,
                    "adjusted": self.adjusted
                }
                if self.period is not None:
                    params["period"] = self.period + 1
                    
                else:
                    params["from_date"] = self.from_date
                    params["to_date"] = self.to_date if self.to_date is not None else None
                data = GetBarData(**params).get(get_total_F = False).to_dataFrame()
                
                current_time = datetime.now()
                if self.freq != "Daily":
                    minuteOrder = current_time.hour * 60 + current_time.minute - 540
                    group = minuteOrder // self.multiplier
                    timeStandard = group * self.multiplier + 540
                    hoursStandard = str(timeStandard // 60).zfill(2)
                    minutesStandard = str(timeStandard % 60).zfill(2)
                    date = str(current_time.date())
                    current_time = date + ' ' + hoursStandard + ':' + minutesStandard 
                    group_df = data.groupby('ticker')
                    for ticker, df in group_df:
                        len_df = len(df) 
                        if df['timestamp'].iloc[-1] == current_time:
                            data = data.drop(data[data['ticker'] == ticker].index[-1])
                            len_df = len_df - 1    
                        if self.period is not None and len_df > self.period:
                            data = data.drop(data[data['ticker'] == ticker].index[0])
                else:
                    date = str(current_time.date())
                    current_time = date + ' 00:00'
                    if datetime.now() < datetime.now().replace(hour=15, minute=0, second=0):
                        group_df = data.groupby('ticker')
                        for ticker, df in group_df:
                            len_df = len(df) 
                            if df['timestamp'].iloc[-1] == current_time:
                                data = data.drop(data[data['ticker'] == ticker].index[-1])
                                len_df = len_df - 1
                            if self.period is not None and len_df > self.period:
                                data = data.drop(data[data['ticker'] == ticker].index[0])
                    else:
                        group_df = data.groupby('ticker')
                        for ticker, df in group_df:
                            if self.period is not None and len(df) > self.period:
                                data = data.drop(data[data['ticker'] == ticker].index[0])
                    
                return data.drop(columns=['tfb', 'tfs'], errors='ignore').reset_index(drop=True)
                
        else:
            self._stop_event.clear()
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
           

    def stop(self):    
        self._stop_event.set()
        if self.connected:
            print("Disconnecting...")
            self.hub_connection.stop()
            self._stop = True
        self.thread.join()

    def _fetch_missing_data(self):
        if self.last_received_time is None:
            return
        for ticker in self.tickers:
            self.__flag[ticker] = 0
            self.__check[ticker] = 0
            self.first_check[ticker] = 0
            self.data_rt_temp[ticker] = pd.DataFrame(columns=self.data_rt_temp[ticker].columns)
            self.df[ticker] = pd.DataFrame(columns=self.df[ticker].columns)
            
            # self.call_back_data[ticker] = pd.DataFrame(columns=self.call_back_data[ticker].columns)
            self.data_rt_final[ticker] = pd.DataFrame(columns=self.data_rt_final[ticker].columns)
            self.temp_data[ticker] = pd.DataFrame(columns=self.temp_data[ticker].columns)
        print("Fetching missing data...")
        # def fetch_data(ticker):
        #     if ticker not in self.last_received_time:
        #         return None
        #     # from_date = pd.to_datetime(self.last_received_time[ticker]).strftime('%Y-%m-%d %H:%M:%S')

        #     if self.period is None:
        #         from_date = self.from_date
        #         to_date = datetime.now()
        #         params = {
        #             "access_token": self.access_token(),
        #             "tickers": [ticker],
        #             "by": self.by,
        #             "fields": self.fields,
        #             "adjusted": self.adjusted,
        #             "from_date": from_date,
        #             "to_date": to_date
        #         }
        #     else:
        #         params = {
        #             "access_token": self.access_token(),
        #             "tickers": [ticker],
        #             "by": self.by,
        #             "fields": self.fields,
        #             "adjusted": self.adjusted,
        #             "period": self.period
        #         }

        #     missing_data = GetBarData(**params).get(get_total_F=True).to_dataFrame()

        #     if not missing_data.empty:
        #         return (ticker, missing_data)
        #     return None
        # with ThreadPoolExecutor(max_workers=len(self.tickers)) as executor:
        #     results = list(executor.map(fetch_data, self.tickers))
        # for result in results:
            # if result:
            #     ticker, missing_data = result
            #     self.df[ticker] = missing_data[missing_data['ticker'] == ticker]

    def _handle_disconnect(self):
        with self.connection_lock:
            self.connected = False
            while not self.connected and not self._stop_event.is_set():
                try:
                    if self.hub_connection:
                        self.hub_connection.stop()
                        self.hub_connection = None
                    time.sleep(3)
                    self.hub_connection = self._build_connection()
                    self.hub_connection.on("ReceiveMessage", self._receive_message)
                    self.hub_connection.on_open(self._on_connect)
                    self.hub_connection.on_close(self._on_disconnect)

                    self.hub_connection.on_close(self._handle_disconnect)
                    self.hub_connection.start()
                    time.sleep(5)
                    if self.hub_connection.transport is not None:   
                        self.connected = True
                        # print('Reconnected')
                        self._fetch_missing_data
                        # with ThreadPoolExecutor(max_workers=5) as executor:
                        #     executor.submit(self._fetch_missing_data)
                        #     executor.shutdown(wait=True) 

                except Exception as e:
                    print(f"Error in reconnection {e}")
                    time.sleep(5)                


