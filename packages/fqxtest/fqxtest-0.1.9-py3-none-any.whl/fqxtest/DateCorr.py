# This code is encrypted and does not contain viruses or Trojans.
import pandas
import numpy
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from .Aggregates import GetBarData
from datetime import datetime
from dateutil.relativedelta import relativedelta
from itertools import islice
from typing import Union, Optional
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

class FindDateCorrelation(object):
    def __init__(self, access_token: callable) -> None:
        
        self.access_token = access_token
        self.processed_data = None
        self.similarity_scores = {}
        self.past_data = []
        self.t2 = datetime.strptime("15:00:00", "%H:%M:%S").time()
        self.method = None
    
    def __normalize_prices(self, past_data: pandas.DataFrame, actual_data: pandas.DataFrame) -> pandas.DataFrame:
        start_price = past_data['close'].iloc[0]
        normalized_start_price = actual_data['close'].iloc[0]
        
        # Calculate the scaling factor
        scaling_factor = normalized_start_price / start_price
        
        # Scale the 'close' prices
        past_data['close'] = past_data['close'] * scaling_factor
        
        return past_data
    
    def __filter_data(self, data: pandas.DataFrame, t1: int) -> pandas.DataFrame:
        start_exclude = pandas.to_datetime('11:30', format='%H:%M').time()
        end_exclude = pandas.to_datetime('13:00', format='%H:%M').time()

        t1 = pandas.to_datetime(t1, format='%H:%M:%S').time()

        if t1 <= start_exclude:
            return data[((data['Timestamp(Hour)'] >= t1) & (data['Timestamp(Hour)'] < start_exclude)) | (data['Timestamp(Hour)'] > end_exclude)]
        else:
            return data[data['Timestamp(Hour)'] >= t1]

    def __time_to_minutes_since_t1_skip(self, time_obj: datetime, t1: datetime) -> int:
        total_minutes = (time_obj.hour - t1.hour) * 60 + (time_obj.minute - t1.minute)
    
        # Only skip if t1 is before 11:30 AM
        if t1 < pandas.to_datetime('11:30', format='%H:%M').time() and time_obj >= pandas.to_datetime('11:30', format='%H:%M').time():
            total_minutes -= 90  # Skip noon
        return total_minutes

    def __format_minutes_to_hhmm_skip(self, x, pos, t1) -> str:
        # Calculate the minutes from t1 to 11:30 AM
        minutes_to_1130 = (11 * 60 + 30) - (t1.hour * 60 + t1.minute)
        
        # Only adjust if t1 is before 11:30 AM
        if t1 < pandas.to_datetime('11:30', format='%H:%M').time() and x >= minutes_to_1130:
            x += 90  # Add 90 minutes to skip the 11:30 AM to 1:00 PM gap
        
        hours = int(x // 60) + t1.hour
        minutes = int(x % 60)
        return f"{hours:02d}:{minutes:02d}"

    def __fetch_data(self, Tickers: Union[str, list[str]], From: str, Timeframe: str) -> pandas.DataFrame:
        print(f"Fetching data of Ticker {Tickers}\n--------------------------------\n")
        data = GetBarData(
            access_token=self.access_token(),
            tickers=Tickers,
            fields=['close'],
            adjusted=True,
            by=Timeframe,
            from_date=From
        ).get().to_dataFrame()
        
        return data
    
    def __preprocess_data(self, data: pandas.DataFrame) -> pandas.DataFrame:
        print(f"Preprocessing data \n--------------------------------\n")
        data["timestamp"] = pandas.to_datetime(data["timestamp"], format="%Y-%m-%d %H:%M")
        data["Timestamp(Hour)"] = data["timestamp"].dt.strftime("%H:%M")
        data["Transaction_Day"] = data["timestamp"].dt.date
        data.drop(columns=["timestamp"], inplace=True)
        data['Timestamp(Hour)'] = pandas.to_datetime(data['Timestamp(Hour)'], format='%H:%M').dt.time
        data['Transaction_Day'] = pandas.to_datetime(data['Transaction_Day'])
        return data
    
    def __get_interval_data(self, data: pandas.DataFrame, transaction_day: str, t1: datetime, t2: datetime) -> pandas.DataFrame:
        print(f"Getting interval for original data\n--------------------------------\n")
        data_filtered = data[data['Transaction_Day'] == transaction_day]
        real_time_data = data_filtered[(data_filtered['Timestamp(Hour)'] >= t1) & (data_filtered['Timestamp(Hour)'] <= t2)]
        return real_time_data
    
    def __get_past_interval_data(self, data: pandas.DataFrame, transaction_day: str, t1: datetime, t2: datetime) -> list:
        print(f"Getting past data after being splitted\n--------------------------------\n")
        # Set default t1 based on the current time
        interval_data = []
        df_filtered = data[data['Transaction_Day'] < transaction_day]
        grouped_df = df_filtered.groupby('Transaction_Day')
        
        for group in grouped_df:
            interval_data.append(group[1][(group[1]['Timestamp(Hour)'] >= t1) & (group[1]['Timestamp(Hour)'] <= t2)])
        
        return interval_data
    
    def __compute_similarity(self, real_time_data: pandas.DataFrame, past_interval_data: list, method: int) -> Optional[dict]:
        print(f"Computing similarity\n--------------------------------\n")
        real_time_array = real_time_data['close'].to_numpy().flatten()
    
        if real_time_array.size == 0:
            print("Warning: Past data is empty.")
            return self.similarity_scores

        real_time_normalized = real_time_array

        for past_data in past_interval_data:
            transaction_day = past_data['Transaction_Day'].iloc[0]
            past_data_array = past_data['close'].to_numpy().flatten()
            
            if past_data_array.size == 0:
                print(".")
                continue
            
            past_data_normalized_df = self.__normalize_prices(past_data=past_data, actual_data=real_time_data)
            past_data_normalized = past_data_normalized_df['close'].to_numpy().flatten()
            
            min_length = min(len(real_time_normalized), len(past_data_normalized))
            real_time_normalized = real_time_normalized[:min_length]
            past_data_normalized = past_data_normalized[:min_length]
            
            if method == '1' or method =='euclidean distance' or method == 'ed':
                distance = euclidean(real_time_normalized, past_data_normalized)
                self.method = "Euclidean Distance"
            elif method == '2' or method == 'dynamic time warping' or method == 'dtw':
                distance, _ = fastdtw(real_time_normalized, past_data_normalized, dist=2)
                self.method = "Dynamic Time Wrapping"
            elif method == '3' or method == 'pearson correlation' or method == 'pc':
                distance = 1 - numpy.corrcoef(real_time_normalized, past_data_normalized)[0, 1]
                self.method = "Pearson Correlation"
            elif method == '4' or method == 'cosine similarity' or method == 'cp': 
                distance = 1 - numpy.dot(real_time_normalized, past_data_normalized) / (numpy.linalg.norm(real_time_normalized) * numpy.linalg.norm(past_data_normalized))
                self.method = "Cosine"
            else:
                raise ValueError("Invalid method. Choose one of [euclidean distance, ed, 1], or one of [dynamic time warping, dtw, 2], or one of [pearson correlation, pc, 3], or one of[cosine similarity, cp, 4].")
            
            self.similarity_scores[transaction_day] = distance
        
        return self.similarity_scores
    
    def __dates_correlation(self, Tickers: Union[str, list], From: str, Timeframe: str, transaction_day: str, t1: datetime, t2: datetime, method: str) -> Union[dict, str]:
        rawl_data = self.__fetch_data(Tickers=Tickers, From=From, Timeframe=Timeframe)
        self.processed_data = self.__preprocess_data(data=rawl_data)
        real_time_data = self.__get_interval_data(data=self.processed_data, transaction_day=transaction_day, t1=t1, t2=t2)
        past_interval_data = self.__get_past_interval_data(data=self.processed_data, transaction_day=transaction_day, t1=t1, t2=t2)
        similarity_scores = self.__compute_similarity(real_time_data=real_time_data, past_interval_data=past_interval_data, method=method)
        print(f"Finding 5 most correlated dates\n--------------------------------\n")
        sorted_similarity_scores = dict(sorted(similarity_scores.items(), key=lambda x: x[1]))
        result_dates = dict(islice(sorted_similarity_scores.items(), 5))
        return result_dates
    
    def intraday_Correlation(self, Ticker: Union[str, list[str]], Timeframe: str, t1:Union[str,None] = None, t2:Union[str,None]=None, method: str = '1', year: int=1) -> None:
        
        """
        Plot the normalized price of a stock over time, comparing the current day to the past days.
            method (str, optional): Distance measurement. Defaults to "pearson correlation".
            For simple, use '1' for euclidean distance, '2' for dynamic time warping, '3' for pearson correlation, '4' for cosine similarity.
        """
        if t1 is None:
            t1 = datetime.strptime("09:00:00", "%H:%M:%S").time() if datetime.now().hour < 12 else datetime.strptime("13:00:00", "%H:%M:%S").time()
        else:
            t1 = datetime.strptime(t1, "%H:%M:%S").time()
    
        if t2 is None:
            t2 = datetime.now().replace(microsecond=0).time()
        else:
            t2 = datetime.strptime(t2, "%H:%M:%S").time()
        From = (datetime.now() - relativedelta(years=year)).strftime("%Y-%m-%d 09:00:00")
        transaction_day = datetime.now().strftime("%Y-%m-%d")
        result_dates = self.__dates_correlation(Tickers=Ticker, From=From, Timeframe=Timeframe, transaction_day=transaction_day, t1=t1, t2=t2, method=method)
        for past_day in result_dates.keys():
            self.past_data.append(self.__get_interval_data(data=self.processed_data, transaction_day=past_day.strftime("%Y-%m-%d"), t1=t1, t2=self.t2))
        
        actual_day = self.__get_interval_data(data=self.processed_data, transaction_day=transaction_day, t1=t1, t2=t2)
        filtered_actual_day = self.__filter_data(data=actual_day, t1=t1)

        filtered_past_day = []
        for past_day in self.past_data:
            filtered_past_day.append(self.__filter_data(data=self.__normalize_prices(past_data=past_day, actual_data=actual_day), t1=t1))
        
        print(f"Plotting chart\n--------------------------------\n")
        plt.figure(figsize=(12, 6))

        # Plot the actual day
        minutes_since_9am_actual = filtered_actual_day['Timestamp(Hour)'].apply(self.__time_to_minutes_since_t1_skip, t1=t1)
        plt.plot(minutes_since_9am_actual, filtered_actual_day['close'], label=f'{transaction_day}', linestyle='-', linewidth=2)

        # Plot each past day
        for index, ((result_date, value), past_day) in enumerate(zip(result_dates.items(), filtered_past_day)):
            minutes_since_9am_past = past_day['Timestamp(Hour)'].apply(self.__time_to_minutes_since_t1_skip, t1=t1)
            if method in [1, 2]:
                plt.plot(minutes_since_9am_past, past_day['close'], label=f'{result_date.strftime("%Y-%m-%d")} ({value:.2f})', linestyle='--', linewidth=1)
            else:
                plt.plot(minutes_since_9am_past, past_day['close'], label=f'{result_date.strftime("%Y-%m-%d")} ({1 - value:.2f})', linestyle='--', linewidth=1)

        # Format the plot
        ax = plt.gca()
        ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: self.__format_minutes_to_hhmm_skip(x, pos, t1)))

        plt.xlim(left=0)
        plt.xticks(rotation=90)

        plt.title(f'Corretion Dates of Ticker {Ticker} on {datetime.now().strftime("%d/%m/%Y")} by using method {self.method}')
        plt.xlabel('Trading Date')
        plt.ylabel('Normalized close price')
        plt.legend()
        plt.grid(False)
        plt.tight_layout()
        plt.show()
