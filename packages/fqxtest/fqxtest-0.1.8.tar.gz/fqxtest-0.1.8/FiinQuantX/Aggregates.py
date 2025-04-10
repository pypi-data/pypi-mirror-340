# This code is encrypted and does not contain viruses or Trojans.
import gzip
import time
import json
import base64
import requests
import warnings
import numpy as np
import pandas as pd
from typing import Union
from threading import Lock
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
warnings.filterwarnings('ignore')

## Product API
HISTORICAL_ADJ_API = "https://fiinquant.fiintrade.vn/TradingView/GetStockChartData"
HISTORICAL_UNADJ_API = "https://fiinquant.fiintrade.vn/TradingView/GetStockChartDataUnAdjust"
HISTORICAL_BUSD_API = "https://fiinquant.fiintrade.vn/TradingView/GetIndicatorBuSd"
HISTORICAL_FOREIGN_API = "https://fiinquant.fiintrade.vn/TradingView/GetIndicatorForeign"

# ### Staging API
# HISTORICAL_ADJ_API = "https://fiinquant-staging.fiintrade.vn/TradingView/GetStockChartData"
# HISTORICAL_UNADJ_API = "https://fiinquant-staging.fiintrade.vn/TradingView/GetStockChartDataUnAdjust"
# HISTORICAL_BUSD_API = "https://fiinquant-staging.fiintrade.vn/TradingView/GetIndicatorBuSd"
# HISTORICAL_FOREIGN_API = "https://fiinquant-staging.fiintrade.vn/TradingView/GetIndicatorForeign"

class GetBarData:
    def __init__(self, 
                 access_token: str, 
                 tickers: Union [str, list[str]], 
                 by: str = '1m',  
                 from_date: Union [str, datetime, None] = None,  
                 to_date: Union [str, datetime, None] = None,          
                 adjusted: bool = True,
                 fields: list[str] = None,
                 period: Union[int, None] = None):
        
        # Params
        self.access_token = access_token
        self.tickers = [tickers] if isinstance(tickers, str) else tickers
        self.by = by
        self.from_date = self._format_date(from_date)     
        self.to_date = self._format_date(to_date) 
        self.adjusted = adjusted
        if fields == ['full']:
            self.fields = ['open', 'high', 'low', 'close', 'volume', 'bu', 'sd', 'fb', 'fs', 'fn']
        else:
            self.fields = fields 
        self.period = period
        
        # API Links
        self.url_adj = HISTORICAL_ADJ_API
        self.url_unadj = HISTORICAL_UNADJ_API
        self.url_busd = HISTORICAL_BUSD_API
        self.url_foreign = HISTORICAL_FOREIGN_API
        
        # Initation
        self.header = {'Authorization': f'Bearer {self.access_token}'}
        self.lock = Lock()
        
        self.from_to_mode = 1
        self.period_mode = 0
        self.flag_OHLCV = 0
        self.flag_BUSD = 0
        self.flag_FOREIGN = 0
        self.api_list = []
        self.data_dict = {}
        self.check_api = True
        self.not_authorization = []
      
        # self.maxPageSize = min(self._calculate_pagesize(), 5000) if self.from_to_mode else self.period * 2
        self.df = pd.DataFrame()
     
        # Dict
        self.TIME_FORMATS = [
            '%Y-%m-%d %H:%M:%S', 
            '%Y-%m-%d %H:%M', 
            '%Y-%m-%d', 
            '%Y-%m', 
            '%Y'
        ]

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

        self.FIELD_FORMATS = {
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume',
            'bu': 'bu',
            'sd': 'sd',
            'fn': 'fn',
            'fb': 'fb',
            'fs': 'fs'
        }

    def _decode_jwt(self):
        header_b64, payload_b64, _ = self.access_token.split('.')
        header = json.loads(base64.urlsafe_b64decode(header_b64 + '=='))
        payload = json.loads(base64.urlsafe_b64decode(payload_b64 + '=='))
        return header, payload

    def _decode_list_api(self,compressed_data):
        compressed_bytes = base64.b64decode(compressed_data)
        decompressed_bytes = gzip.decompress(compressed_bytes)
        return decompressed_bytes.decode('utf-8')
    
    def _is_valid_api(self):
        
        _, payload = self._decode_jwt()

        if 'list_api' in payload:
            list_api_decoded = self._decode_list_api(payload['list_api'])
        else:
            list_api_decoded = ""
            print("No api list!")
        return list_api_decoded
    
    def _calculate_pagesize(self):
        try:
            from_date_obj = datetime.strptime(self.from_date, "%Y-%m-%d")
        except:
            from_date_obj = pd.to_datetime(self.from_date)
        
        try:
            to_date_obj = datetime.strptime(self.to_date, "%Y-%m-%d")
        except:
            to_date_obj = pd.to_datetime(self.to_date)
        
        delta = to_date_obj - from_date_obj
        number_of_days = delta.days if delta.days > 0 else 1
        
        if self.by == '1m':
            return number_of_days * 360
        elif self.by == '5m':
            return number_of_days * 72
        elif self.by == '15m':
            return number_of_days * 24
        elif self.by == '30m':
            return number_of_days * 12
        elif self.by == '1h':
            return number_of_days * 6
        elif self.by == '2h':
            return number_of_days * 3
        elif self.by == '4h':
            return number_of_days * 2
        elif self.by == '1d':
            return number_of_days

    def _format_date(self, date):
        if isinstance(date, datetime):
            return date.strftime('%Y-%m-%d %H:%M:%S')
        return date
    
    def _is_valid_date(self, date, fmt):
        try:
            datetime.strptime(date, fmt)
            return True
        except ValueError:
            return False

    def _validate(self):       
        # Tickers
        if not self.tickers:
            raise ValueError('Tickers cannot be left blank')
        
        # By
        if self.by in self.VALID_BY:
            self.freq = self.VALID_BY[self.by]
        else:
            raise ValueError('Invalid value for "by". Must be one of: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d')
        
        # Fields
        if not self.fields:
            raise ValueError('Fields cannot be left blank')

        self.invalid_fields = [field for field in self.fields if field not in self.FIELD_FORMATS]

        if self.invalid_fields:
            valid_fields = "', '".join(self.FIELD_FORMATS.keys())
            raise ValueError(
                f"Invalid fields: {', '.join(self.invalid_fields)}. Must be one of: '{valid_fields}'"
            )

        # From_date, To_date, Period
        if not self.from_date and not self.to_date:
            if self.period is None:
                raise ValueError("From_date and To_date cannot be left blank")
            else:
                self.to_date = datetime.now().strftime('%Y-%m-%d %H:%M')
                self.period_mode = 1
                self.from_to_mode = 0

        elif not self.from_date and self.to_date:
            raise ValueError("From_date cannot be left blank")
        
        elif self.from_date and self.period is not None:
            raise ValueError("From_date, To_date, and Period cannot coexist")
        
        elif self.from_date and not self.to_date and self.period is None:
            self.to_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        if self.from_to_mode == 1:
            for date, label in [(self.from_date, "from_date"), (self.to_date, "to_date")]:
                if not any(self._is_valid_date(date, fmt) for fmt in self.TIME_FORMATS):
                    valid_formats = "', '".join(self.TIME_FORMATS)
                    raise ValueError(f"Invalid '{label}': '{date}'. Must be one of '{valid_formats}'")

        if self.period_mode == 1 and not (isinstance(self.period, int) and self.period > 0):
            raise ValueError("Period must be a positive integer")
    
    def _detect_code(self, code):
        if code in ['VNMID', 'VNHEAL', 'HNXINDEX', 'VNDIAMOND', 'VNREAL', 'VNMAT', 
                    'VNX50', 'VNIT', 'VNSI', 'VNIND', 'VNENE', 'VNCOND', 'VNXALL', 
                    'VN30', 'VNALL', 'VNUTI', 'VNFIN', 'VNSML', 'HNX30', 'VN100', 
                    'VNCONS', 'UPCOMINDEX', 'VNFINLEAD', 'VNFINSELECT', 'VNINDEX']:
            return 'Index'
        
        elif len(code) == 3:
            return 'Stock'
            
        elif len(code) == 8:
            if code[0] == 'C':
                return 'CW'
            else:
                return 'Stock'
            
        elif len(code) == 7 or len(code) == 9:
            return 'Derivative'

    def _process_fields(self):
        field_mapping = {
            "OHLCV": (['open', 'high', 'low', 'close', 'volume'], "flag_OHLCV", self.url_adj if self.adjusted else self.url_unadj),
            "BUSD": (['bu', 'sd'], "flag_BUSD", self.url_busd),
            "FOREIGN": (['fn', 'fb', 'fs'], "flag_FOREIGN", self.url_foreign),
        }

        for fields, flag, url in field_mapping.values():
            if getattr(self, flag) == 0 and any(field in self.fields for field in fields):
                setattr(self, flag, 1)
                self.api_list.append(url)              

    def _fetch_data_parallel(self):        
        self.maxPageSize = min(self._calculate_pagesize(), 1000) if self.from_to_mode else min(self.period,1000)        
        list_api = self._is_valid_api()
        
        def fetch_url(ticker, url):
            if 'GetIndicatorBuSd' in url:
                field = 'BUSD'
                if url.split('/')[-1] not in list_api:
                    self.check_api = False
                    self.not_authorization.append('BUSD')

            elif 'GetIndicatorForeign' in url:
                field = 'FOREIGN'
                if url.split('/')[-1] not in list_api:
                    self.check_api = False
                    self.not_authorization.append('FOREIGN')

            elif 'GetStockChartDataUnAdjust' in url:
                field = 'OHLCV'
                if url.split('/')[-1] not in list_api:
                    self.check_api = False
                    self.not_authorization.append('OHLCV with adjusted=False')

            else:
                field = 'OHLCV'
                if url.split('/')[-1] not in list_api:
                    self.check_api = False
                    self.not_authorization.append('OHLCV with adjusted')

            self.data_dict[ticker][field] = {}
            to_date = self.to_date
            period = self.period
            page = 1
            max_retries = 14
            def make_request(param):
                retries = 0
                while retries < max_retries:
                    try: 
                        response = requests.get(url=url, params=param, headers=self.header, timeout=30, verify=False)
                        response.raise_for_status()
                        return response.json()
      
                    except requests.exceptions.Timeout:
                        retries += 1
                        time.sleep(1)  
                    except requests.exceptions.HTTPError as e:
                        if response.status_code == 429:
                            retries += 1
                            time.sleep(5)
                        else:
                            print(e)
                            break
                    except requests.exceptions.RequestException as e:
                        try:
                            error_message = str(e).split(" for url: ")[0] 
                            # print(response.json())
                            print(f"Request failed for {ticker}: {error_message}, {response.json().get('errors')[0]}")
                            break
                        except:
                            break
                print(f"Failed to fetch data for {ticker}.")
                raise Exception()

            try:
                if self.from_to_mode == 1:
                    param = {
                        'Code': ticker,
                        'Type': self._detect_code(ticker),
                        'Frequency': self.freq,
                        'From': self.from_date,
                        'To': to_date,
                        'PageSize': self.maxPageSize
                    }
                    
                    while True:  
                        res = make_request(param) 
                        data = pd.DataFrame(res.get('items', []))
                        if data.empty:
                            break
                        self.data_dict[ticker][field][page] = data

                        param['To'] = datetime.strptime(data['t'].iloc[-1], "%Y-%m-%dT%H:%M:%S") - timedelta(minutes=1)
                        page += 1

                else:
                    while True:
                        # pagesize = min(self.maxPageSize,period)
                        param = {
                            'Code': ticker,
                            'Type': self._detect_code(ticker),
                            'Frequency': self.freq,
                            'To': to_date,
                            'PageSize': self.maxPageSize
                        }
                        
                        res = make_request(param)
                        data = pd.DataFrame(res.get('items', []))
                        period -= data.shape[0]
                        self.data_dict[ticker][field][page] = data
                        if period <= 0:
                            break
                        to_date = datetime.strptime(data['t'].iloc[-1], "%Y-%m-%dT%H:%M:%S") - timedelta(minutes=1)
                        page += 1
                
            except Exception as e:
                raise(f"Error fetching data {url.split('/')[-1][3:]} for {ticker}")

        def fetch_single_ticker(ticker):
            self.data_dict[ticker] = {}
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {executor.submit(fetch_url, ticker, url): url for url in self.api_list}
                for future in as_completed(futures):
                    futures[future]
                    try:
                        future.result()
                    except Exception as e:
                        pass

            return ticker

        with ThreadPoolExecutor(max_workers=7) as executor:
            futures = {executor.submit(fetch_single_ticker, ticker): ticker for ticker in self.tickers}
            for future in as_completed(futures):
                futures[future]
                try:
                    future.result()
                except Exception as e:
                    pass
        return self.data_dict
    
    def _fetch_data_parallel_unlimited(self):        
        self.maxPageSize = min(self._calculate_pagesize(), 1000) if self.from_to_mode else min(self.period,1000)        
        list_api = self._is_valid_api()
        
        def fetch_url(ticker, url):
            if 'GetIndicatorBuSd' in url:
                field = 'BUSD'
                if url.split('/')[-1] not in list_api:
                    self.check_api = False
                    self.not_authorization.append('BUSD')

            elif 'GetIndicatorForeign' in url:
                field = 'FOREIGN'
                if url.split('/')[-1] not in list_api:
                    self.check_api = False
                    self.not_authorization.append('FOREIGN')

            elif 'GetStockChartDataUnAdjust' in url:
                field = 'OHLCV'
                if url.split('/')[-1] not in list_api:
                    self.check_api = False
                    self.not_authorization.append('OHLCV with adjusted=False')

            else:
                field = 'OHLCV'
                if url.split('/')[-1] not in list_api:
                    self.check_api = False
                    self.not_authorization.append('OHLCV with adjusted')

            self.data_dict[ticker][field] = {}
            to_date = self.to_date
            period = self.period
            page = 1
            max_retries = 14
            def make_request(param):
                
                retries = 0
                while retries < max_retries:
                    try: 
                        response = requests.get(url=url, params=param, headers=self.header, timeout=30, verify=False)
                        response.raise_for_status()
                        return response.json()
      
                    except requests.exceptions.Timeout:
                        retries += 1
                        time.sleep(1)  
                    except requests.exceptions.HTTPError as e:
                        if response.status_code == 429:
                         
                            while True:
                                time.sleep(5)
                                try:
                                    response = requests.get(url=url, params=param, headers=self.header, timeout=30, verify=False)
                                    response.raise_for_status()
                                    return response.json()
                                except requests.exceptions.HTTPError as e:
                                    if response.status_code != 429:
                                        print(e)
                                        break
                        else:
                            print(e)
                            break
                    except requests.exceptions.RequestException as e:
                        try:
                            error_message = str(e).split(" for url: ")[0] 
                            # print(response.json())
                            print(f"Request failed for {ticker}: {error_message}, {response.json().get('errors')[0]}")
                            break
                        except:
                            break
                print(f"Failed to fetch data for {ticker}.")
                raise Exception()

            try:
                if self.from_to_mode == 1:
                    param = {
                        'Code': ticker,
                        'Type': self._detect_code(ticker),
                        'Frequency': self.freq,
                        'From': self.from_date,
                        'To': to_date,
                        'PageSize': self.maxPageSize
                    }
                    
                    while True:  
                        res = make_request(param) 
                        data = pd.DataFrame(res.get('items', []))
                        if data.empty:
                            break
                        self.data_dict[ticker][field][page] = data

                        param['To'] = datetime.strptime(data['t'].iloc[-1], "%Y-%m-%dT%H:%M:%S") - timedelta(minutes=1)
                        page += 1

                else:
                    while True:
                        # pagesize = min(self.maxPageSize,period)
                        # pagesize = min(1000,period)
                        
                        param = {
                            'Code': ticker,
                            'Type': self._detect_code(ticker),
                            'Frequency': self.freq,
                            'To': to_date,
                            'PageSize': self.maxPageSize
                        }
                       
                        res = make_request(param)
                        data = pd.DataFrame(res.get('items', []))
                        period -= data.shape[0]
                        self.data_dict[ticker][field][page] = data
                        if period <= 0:
                            break
                        to_date = datetime.strptime(data['t'].iloc[-1], "%Y-%m-%dT%H:%M:%S") - timedelta(minutes=1)
                        page += 1
                
            except Exception as e:
                raise(f"Error fetching data {url.split('/')[-1][3:]} for {ticker}")

        def fetch_single_ticker(ticker):
            self.data_dict[ticker] = {}
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {executor.submit(fetch_url, ticker, url): url for url in self.api_list}
                for future in as_completed(futures):
                    futures[future]
                    try:
                        future.result()
                    except Exception as e:
                        pass

            return ticker

        with ThreadPoolExecutor(max_workers=7) as executor:
            futures = {executor.submit(fetch_single_ticker, ticker): ticker for ticker in self.tickers}
            for future in as_completed(futures):
                futures[future]
                try:
                    future.result()
                except Exception as e:
                    pass
                
        return self.data_dict
    
    def _combine_data(self,data_dict):
        merged_data_dict = {**data_dict}
        combined_results = []
        
        for ticker, ticker_data in merged_data_dict.items():
            try:
                ohlcv_combined = pd.concat(ticker_data.get('OHLCV', {}).values(), axis=0) if 'OHLCV' in ticker_data and ticker_data['OHLCV'] else None
                busd_combined = pd.concat(ticker_data.get('BUSD', {}).values(), axis=0) if 'BUSD' in ticker_data and ticker_data['BUSD'] else None
                foreign_combined = pd.concat(ticker_data.get('FOREIGN', {}).values(), axis=0) if 'FOREIGN' in ticker_data and ticker_data['FOREIGN'] else None
                
                merged_data = next((df for df in [ohlcv_combined, busd_combined, foreign_combined] if df is not None), None)

                if merged_data is not None:
                    if ohlcv_combined is not None and not merged_data.equals(ohlcv_combined):
                        merged_data = pd.merge(merged_data, ohlcv_combined, on = 't', how='outer')
                    if busd_combined is not None and not merged_data.equals(busd_combined):
                        merged_data = pd.merge(merged_data, busd_combined, on = 't', how='outer')
                    if foreign_combined is not None and not merged_data.equals(foreign_combined):
                        merged_data = pd.merge(merged_data, foreign_combined, on ='t', how='outer')

                    merged_data['ticker'] = ticker

                    merged_data = merged_data.sort_values(by='t').reset_index(drop=True)
                    if self.period_mode:
                        merged_data = merged_data.tail(self.period)
                        
                    combined_results.append(merged_data)
                    
            except Exception as e:
                print(f"Error processing {ticker}: {e}")
        
        final_dataframe = pd.concat(combined_results, ignore_index=True) if combined_results else pd.DataFrame()
        return final_dataframe

    def _process_data(self):
        rename_mapping = {
                "t": "timestamp",
                "o": "open",
                "l": "low",
                "h": "high",
                "c": "close",
                "v": "volume",
                "b": "bu",
                "s": "sd",
                "fn": "fn",
                "fb": "fb",
                "fs": "fs",
                "tfb": "tfb",
                "tfs": "tfs"
            }
   
        valid_rename_mapping = {col: rename_mapping[col] for col in self.df.columns if col in rename_mapping}
        self.df = self.df.rename(columns=valid_rename_mapping)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], errors='coerce')
        self.df['timestamp'] = self.df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        processed_data = []
        grouped = self.df.groupby('ticker')
        
        for _, df_ticker in grouped:
            processed_data.append(df_ticker.sort_values(by='timestamp').reset_index(drop=True))

        combined_df = pd.concat(processed_data, ignore_index=True)
        
        if self.get_total_F:
            ordered_values = ['ticker', 'timestamp'] + [self.FIELD_FORMATS[field] for field in self.fields] + ['tfb', 'tfs']
        else: 
            ordered_values = ['ticker', 'timestamp'] + [self.FIELD_FORMATS[field] for field in self.fields]
            
        try:
            combined_df = combined_df[ordered_values]
        except:   
            for col in ordered_values:
                if col not in combined_df.columns:
                    combined_df[col] = np.nan
            combined_df = combined_df[ordered_values]
        
        return combined_df

    def get(self, get_total_F: bool = False):
        self.get_total_F = get_total_F
        self._validate()
        self._process_fields()
        if not self.get_total_F and self.freq == 'Daily':
            dict_data = self._fetch_data_parallel_unlimited()
        else:
            dict_data = self._fetch_data_parallel()
        
        if self.check_api == False:
            raise KeyError(f"You are not authorized for some fields: {', '.join(self.not_authorization)}")
        self.df = self._combine_data(dict_data)
        
        try:
            self.df = self._process_data()  
        except:
            self.df = pd.DataFrame(columns=['ticker', 'timestamp', *self.FIELD_FORMATS.values()])
        
        return BarData(self.df)
        
class BarData:
    def __init__(self, data):
        self.__private_attribute = data
        for col in data.columns:
            setattr(self, col, data[col])
        
    def to_dataFrame(self):
        return self.__private_attribute
        

# class BarDataUpdate:
#     def __init__(self, data, fields):
        
#         selected_columns = [field for field in fields]
#         self.__private_attribute = data[['ticker', 'timestamp'] + selected_columns]
#         # self.__private_attribute = pd.DataFrame(columns=['ticker', 'timestamp'] + selected_columns)
#         # for col in self.__private_attribute.columns:
#         #     setattr(self, col, self.__private_attribute[col])
#         col_map = {selected_columns[i]: fields[i] for i in range(len(selected_columns))}
#         for col in self.__private_attribute.columns:
#             setattr(self, col_map.get(col, col), self.__private_attribute[col])
            
#     # def _update_data(self, data, fields):
#     #     selected_columns = [field for field in fields if field in data.columns]
#     #     self.__private_attribute = data[['ticker', 'timestamp'] + selected_columns]
#     #     for col in self.__private_attribute.columns:
#     #         setattr(self, col, self.__private_attribute[col])
            
#     def to_dataFrame(self):
#         return self.__private_attribute

# class BarDataUpdate:
#     def __init__(self, data, fields):
#         columns = ['ticker', 'timestamp'] + [field for field in fields if field in data.columns]
#         self.__private_attribute = data[columns]
#         self.ticker = self.__private_attribute['ticker']
#         self.timestamp = self.__private_attribute['timestamp']
#         for field in fields:
#             if field in self.__private_attribute.columns:
#                 setattr(self, field, self.__private_attribute[field])
    
#     def to_dataFrame(self):
#         return self.__private_attribute

class BarDataUpdate:
    def __init__(self, fields):
        self.fields = fields
        self.__private_attribute = None
        self.ticker = None
        self.timestamp = None
    
    def _update(self, data):
        columns = ['ticker', 'timestamp'] + [field for field in self.fields if field in data.columns]
        self.__private_attribute = data[columns]
        self.ticker = self.__private_attribute['ticker']
        self.timestamp = self.__private_attribute['timestamp']
        for field in self.fields:
            if field in self.__private_attribute.columns:
                setattr(self, field, self.__private_attribute[field])
    
    def to_dataFrame(self):
        return self.__private_attribute

    
