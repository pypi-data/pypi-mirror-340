# This code is encrypted and does not contain viruses or Trojans.
from typing import Union
from .Aggregates import GetBarData
import warnings
warnings.filterwarnings("ignore")

class GetDataPoint:
    def __init__(self, access_token: callable, 
                 ticker: str, 
                 field: str,  
                 by: str, 
                 candle_index: int,
                 adjusted: Union[bool, None] = True) -> None:
        
        self.access_token = access_token
        self.ticker = ticker
        self.field = [field] if isinstance(field, str) else field
        self.adjusted = adjusted
        self.by = by
        self.candle_index = candle_index
        self.data = self._get_data()

    def _get_data(self):
        data = GetBarData(
            access_token=self.access_token(),
            tickers=self.ticker,
            fields=self.field,
            adjusted=self.adjusted,
            by=self.by,
            period = self.candle_index+1).get().to_dataFrame()

        return data[f'{self.field[0]}'].values[-self.candle_index-1]

    def __repr__(self):
        return str(self.data)
    
    def __float__(self):
        return float(self.data)  

    def __int__(self):
        return int(self.data) 





