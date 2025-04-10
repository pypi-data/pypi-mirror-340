# This code is encrypted and does not contain viruses or Trojans.
import stumpy
import numpy as np
import pandas as pd
from typing import Union
import os
import hashlib
import tempfile
import requests
import plotly.graph_objects as go
from .Aggregates import GetBarData
from sklearn.decomposition import PCA
from datetime import datetime, timedelta
from plotly.subplots import make_subplots
from dateutil.relativedelta import relativedelta
from sklearn.discriminant_analysis import StandardScaler
from concurrent.futures import ThreadPoolExecutor
import glob

data_path_1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1qSEZt0qQLRPDjBTjs4FZAhTotqkv-SQ3VnGVOCO4MzV0ow0RAkflz2f07nNh2g/pub?gid=2067535115&single=true&output=csv"
data_path_2 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1qSEZt0qQLRPDjBTjs4FZAhTotqkv-SQ3VnGVOCO4MzV0ow0RAkflz2f07nNh2g/pub?gid=1440944105&single=true&output=csv"
data_path_3 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1qSEZt0qQLRPDjBTjs4FZAhTotqkv-SQ3VnGVOCO4MzV0ow0RAkflz2f07nNh2g/pub?gid=1986692204&single=true&output=csv"
data_path_4 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1qSEZt0qQLRPDjBTjs4FZAhTotqkv-SQ3VnGVOCO4MzV0ow0RAkflz2f07nNh2g/pub?gid=1750139504&single=true&output=csv"
data_path_5 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1qSEZt0qQLRPDjBTjs4FZAhTotqkv-SQ3VnGVOCO4MzV0ow0RAkflz2f07nNh2g/pub?gid=1810538649&single=true&output=csv"
data_path_6 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1qSEZt0qQLRPDjBTjs4FZAhTotqkv-SQ3VnGVOCO4MzV0ow0RAkflz2f07nNh2g/pub?gid=1574033707&single=true&output=csv"
data_path_7 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1qSEZt0qQLRPDjBTjs4FZAhTotqkv-SQ3VnGVOCO4MzV0ow0RAkflz2f07nNh2g/pub?gid=1418871709&single=true&output=csv"

csv_urls = [data_path_1, data_path_2, data_path_3, data_path_4, data_path_5, data_path_6, data_path_7]
class SimilarChart(object):
    def __init__(self, access_token: callable)->None:   
        self.access_token = access_token
        self.current_time = datetime.now()
        self.current_hour = self.current_time.hour
        self.t1 = None
        self.t2 = None
        self.target_ticker = None

    def __fetch_data(self, Ticker: Union[str, list[str]], from_date: str) -> pd.DataFrame:
        if isinstance(Ticker, list):
            Ticker = Ticker[0]

        data = GetBarData(access_token=self.access_token(),
            tickers=Ticker,
            fields=['open','high','low','close', 'volume'],
            adjusted=True,
            by='1d',
            from_date=from_date
        ).get().to_dataFrame()
       
        return data
    
    def __get_max_date(self, Ticker: Union[str, list[str]], data: pd.DataFrame) -> str:
        if isinstance(Ticker, list):
            Ticker = Ticker[0]
        ticker_list = data["ticker"].unique().tolist()

        if Ticker in ticker_list:
            filtered_data = data[data["ticker"] == Ticker]
            filtered_data["date"] = pd.to_datetime(filtered_data["date"], format='mixed')
            max_date = (filtered_data["date"].max() + timedelta(days=1)).strftime("%Y-%m-%d")
            return max_date
        
        else:
            return

    def __data_prep(self, data):
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data['date'] = data['timestamp'].dt.date
        ticker_dfs = {}
        for ticker in data['ticker'].unique():
            ticker_dfs[ticker] = data[data['ticker'] == ticker]
        return ticker_dfs
    
    def __target_data(self, ticker_dfs):
        target_data = ticker_dfs[self.target_ticker][
            (pd.to_datetime(ticker_dfs[self.target_ticker]['date']) < pd.to_datetime(self.t2)) 
            & (pd.to_datetime(ticker_dfs[self.target_ticker]['date']) > pd.to_datetime(self.t1))
        ]
        return target_data
    
    def __find_top_similar_patterns(self,ticker_dfs, target_data, m, target_ticker, top_n=5):

        pca = PCA(n_components=1)
        

        similar_patterns = []
        
        print(f"\nSearching for patterns similar to {target_ticker}...")
        
        for ticker, df in ticker_dfs.items():
            # Skip the target ticker
            if ticker == target_ticker:
                continue
                
            print(f"\nProcessing ticker: {ticker}")
            
            # Transform the OHLC data of the current ticker
            df_ohlc = df[['open', 'high', 'low', 'close']]
            target_data_ohlc = target_data[['open', 'high', 'low', 'close']]
            
            # Scale the data first
            scaler = StandardScaler()
            df_scaled = scaler.fit_transform(df_ohlc)
            target_data_scaled = scaler.transform(target_data_ohlc)
            
            # Then apply PCA
            df_pca = pca.fit_transform(df_scaled)
            target_data_pca = pca.transform(target_data_scaled)
            print(f"PCA data shape for {ticker}:", df_pca.shape)
            # Compute the matrix profile using stumpy.mass
            mp = stumpy.mass(target_data_pca.flatten(), df_pca.flatten())
            print(f"Matrix profile shape for {ticker}:", mp.shape)
            
            # Find the minimum distance and its index
            min_index = np.argmin(mp)
            current_min_distance = mp[min_index]
            print(f"Minimum distance for {ticker}: {current_min_distance:.4f} at index {min_index}")

            # Store the pattern and its distance
            similar_patterns.append((current_min_distance, df.iloc[min_index:min_index + m], ticker))
        
        # Sort patterns by distance and get the top N
        similar_patterns.sort(key=lambda x: x[0])
        top_similar_patterns = similar_patterns[:top_n]

        for i, (distance, pattern, ticker) in enumerate(top_similar_patterns, start=1):
            print(f"\nTop {i} similar pattern found in {ticker} with distance {distance:.4f}")

        return top_similar_patterns
    
    def __plot_patterns_with_extension(self, ticker_dfs, target_data, similar_patterns, target_ticker, extension_length=30):
        # Create a subplot with 2 rows and 3 columns, using only 5 subplots
        fig = make_subplots(rows=2, cols=3, subplot_titles=(f"Target Pattern {target_ticker}", f"Similar pattern of {similar_patterns[0][2]}", f"Similar pattern of {similar_patterns[1][2]}", f"Similar pattern of {similar_patterns[2][2]}", f"Similar pattern of {similar_patterns[3][2]}", f"Similar pattern of {similar_patterns[4][2]}"))

        # Function to add candlestick and extension
        def add_pattern_with_extension(fig, data, ticker, row, col, name, add_extension=True):
            # Original pattern
            fig.add_trace(go.Candlestick(
                x=data['date'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                name=name,
                increasing_line_color='#26A69A',
                decreasing_line_color='#EF5350',
                increasing_fillcolor='#26A69A',
                decreasing_fillcolor='#EF5350',
                showlegend=False
            ), row=row, col=col)

            if add_extension:
                # Get the next 30 data points
                full_data = ticker_dfs[ticker]
                last_date = data['date'].iloc[-1]
                extended_data = full_data[full_data['date'] > last_date].head(extension_length)

                # Add the extension
                if not extended_data.empty:
                    fig.add_trace(go.Candlestick(
                        x=extended_data['date'],
                        open=extended_data['open'],
                        high=extended_data['high'],
                        low=extended_data['low'],
                        close=extended_data['close'],
                        name=f'{name} Extension',
                        increasing_line_color='rgba(38, 166, 154, 0.5)',
                        decreasing_line_color='rgba(239, 83, 80, 0.5)',
                        increasing_fillcolor='rgba(38, 166, 154, 0.5)',
                        decreasing_fillcolor='rgba(239, 83, 80, 0.5)',
                        showlegend=False
                    ), row=row, col=col)

                    # Dashed line separator
                    fig.add_shape(type="line",
                                x0=last_date, y0=min(data['low'].min(), extended_data['low'].min()),
                                x1=last_date, y1=max(data['high'].max(), extended_data['high'].max()),
                                line=dict(color="black", width=2, dash="dash"),
                                row=row, col=col)

        # Add the target pattern with blank extension
        def add_target_pattern_with_blank_extension(fig, data, row, col, name, extension_length):
            # Original pattern
            fig.add_trace(go.Candlestick(
                x=data['date'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                name=name,
                increasing_line_color='#26A69A',
                decreasing_line_color='#EF5350',
                increasing_fillcolor='#26A69A',
                decreasing_fillcolor='#EF5350',
                showlegend=False
            ), row=row, col=col)

            # Add blank space for extension
            last_date = data['date'].iloc[-1]
            blank_dates = pd.date_range(start=last_date, periods=extension_length + 1)[1:]
            fig.add_trace(go.Candlestick(
                x=blank_dates,
                open=[None] * extension_length,
                high=[None] * extension_length,
                low=[None] * extension_length,
                close=[None] * extension_length,
                showlegend=False
            ), row=row, col=col)

            # Dashed red line at the end of the target pattern
            fig.add_shape(type="line",
                          x0=last_date, y0=min(data['low'].min(), data['low'].min()),
                          x1=last_date, y1=max(data['high'].max(), data['high'].max()),
                          line=dict(color="red", width=2, dash="dash"),
                          row=row, col=col)

        # Add the target pattern with blank extension
        add_target_pattern_with_blank_extension(fig, target_data, 1, 1, 'Target Pattern', extension_length)

        # Add each similar pattern and its extension
        for i, (distance, pattern, ticker) in enumerate(similar_patterns, start=1):
            row = 1 if i <= 2 else 2
            col = i + 1 if i <= 2 else i - 2
            add_pattern_with_extension(fig, pattern, ticker, row, col, f'Similar Pattern {i} in {ticker}', add_extension=True)

        # Update layout for better visualization
        fig.update_layout(
            title='Candlestick Patterns with Extensions',
            plot_bgcolor='white',
            paper_bgcolor='white',
            yaxis=dict(gridcolor='#E0E0E0'),
            xaxis=dict(gridcolor='#E0E0E0'),
            width=1200,  # Adjusted width for 2x3 grid
            height=800,  # Adjusted height for better visualization
            showlegend=False
        )

        for i in range(1, 6):
            fig.update_xaxes(rangeslider_visible=False, row=(i-1)//3 + 1, col=(i-1)%3 + 1)

        fig.show()

    def __get_hashed_filename(self, url):
    
        month = datetime.now().strftime("%Y-%m")
        url_hash = hashlib.md5(url.encode()).hexdigest() 
        full_hash = hashlib.md5((url + month).encode()).hexdigest()
        temp_dir = tempfile.gettempdir()
        
        return os.path.join(temp_dir, f"{full_hash}.csv"), temp_dir, url_hash
    
    
    def plot(self, Ticker: Union[str, list[str]], t1: Union[str,None] = None, t2: Union[str,None] = None) -> None:
        def __download_csv(url):
            try:
                temp_file_path, temp_dir, url_hash = self.__get_hashed_filename(url)                
                for old_file in glob.glob(os.path.join(temp_dir, f"{url_hash}*.csv")):
                    if old_file != temp_file_path:  
                        os.remove(old_file)
                         
                if os.path.exists(temp_file_path):
                    return pd.read_csv(temp_file_path, decimal=",").dropna()
 
                response = requests.get(url, stream=True)
                response.raise_for_status()

                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(response.content)
               
                return pd.read_csv(temp_file_path, decimal=",").dropna()

            except Exception as e:
                print(f"Error reading data from {url}: {e}")
                return None
            # try:
    
            #     temp_dir = tempfile.gettempdir()
                
     
            #     url_hash = hashlib.md5(url.encode()).hexdigest() 
            #     temp_file_path = os.path.join(temp_dir, f"{url_hash}.csv") 

              
            #     if os.path.exists(temp_file_path):
            #         print(f"File already exists: {temp_file_path}")
            #         return pd.read_csv(temp_file_path, decimal=",").dropna()
                
               
            #     with requests.get(url, stream=True) as response:
            #         response.raise_for_status()
            #         with open(temp_file_path, "wb") as temp_file:
            #             for chunk in response.iter_content(chunk_size=8192):
            #                 temp_file.write(chunk)
                
            #     print(f"Downloaded: {temp_file_path}")
            #     return pd.read_csv(temp_file_path, decimal=",").dropna()

            # except Exception as e:
            #     print(f"Error reading data from {url}: {e}")
            #     return None
        if isinstance(Ticker, list):
            Ticker = Ticker[0]
        try:
            print('Reading data from FiinX')
            dataframes = []
            with ThreadPoolExecutor(max_workers=7) as executor:
                results = list(executor.map(__download_csv, csv_urls))

            dataframes = [df for df in results if df is not None]
            data_csv = pd.concat(dataframes, ignore_index=True) if dataframes else None
            data_csv['Date'] = pd.to_datetime(data_csv['Date'], format='mixed')
            # print(data_csv)
            columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in columns:
                data_csv[col] = (
                    data_csv[col]
                    .astype(str)
                    .str.replace(",", "", regex=True)  
                    .str.strip() 
                    .replace("", "0") 
                    .astype(float) 
    )
            # with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            #     temp_file_path = temp_file.name  

                
            #     with requests.get(csv_path, stream=True) as response:
            #         response.raise_for_status() 
            #         for chunk in response.iter_content(chunk_size=8192):
            #             temp_file.write(chunk) 
            #     data_csv = pd.read_csv(temp_file_path, decimal=",").dropna()
            #     print(data_csv)
        except:
            raise Exception("Error reading data from FiinX")
        
        if t1 is None:
            t1 = (datetime.now() - relativedelta(months=1)).strftime("%Y-%m-%d")
        if t2 is None:
            t2 =  datetime.now().strftime("%Y-%m-%d")
        
        data_csv = data_csv[["Ticker", "Date", "Open", "High", "Low", "Close", "Volume"]]
        data_csv = data_csv.rename(columns={
            "Ticker": "ticker", 
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        })
  

        max_date_of_csv = self.__get_max_date(Ticker=Ticker, data=data_csv)
        data_csv = data_csv.rename(columns={"date": "timestamp"})

        if max_date_of_csv is not None:
            data_realtime = self.__fetch_data(Ticker=Ticker, from_date=max_date_of_csv)
        else:
            data_realtime = self.__fetch_data(Ticker=Ticker, from_date=t1)
        
        data_realtime["timestamp"] = pd.to_datetime(data_realtime['timestamp']).dt.strftime('%Y-%m-%d')
        data = pd.concat([data_csv, data_realtime], ignore_index=True)
        self.t1, self.t2, self.target_ticker = t1, t2, Ticker

        ticker_dfs = self.__data_prep(data)
        target_data = self.__target_data(ticker_dfs)
        similar_patterns = self.__find_top_similar_patterns(ticker_dfs, target_data, 30, self.target_ticker, 5)
        self.__plot_patterns_with_extension(ticker_dfs, target_data, similar_patterns, self.target_ticker, 30)
