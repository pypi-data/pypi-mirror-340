# This code is encrypted and does not contain viruses or Trojans.
import time
import requests
import pandas as pd
from .Aggregates import GetBarData

REBALANCE_URL = 'https://fiinquant.fiintrade.vn/TradingView/GetFreefloatMarketCapLimit'

class Rebalance(object):
    def __init__(self, access_token: callable)->None:
        self.access_token = access_token
        
    def _FiinXData(self):
        max_retries = 5
        url = REBALANCE_URL
        headers = {'Authorization': f'Bearer {self.access_token()}'}
        
        def __make_request(param):
            retries = 0
            while retries < max_retries:
                try: 
                    response = requests.get(url=url, params=param, headers=headers, timeout=30)
                    response.raise_for_status()
                    return response.json()
                
                except requests.exceptions.Timeout:
                    retries += 1
                    time.sleep(1)  

                except requests.exceptions.RequestException as e:
                    print(f"Request failed for GetFreefloatMarketCapLimit: {e}")
                    break

            raise Exception("Error reading data from FiinX.")
        
        param = {'ComGroupCode': self.ticker}
        res = __make_request(param)
        if len(res) == 0:
            raise Exception(f"{self.ticker} is not available for rebalance.")
        
        df = pd.DataFrame(res)
        df = df.rename(columns={
            'marketCapFLimit': 'MarketCapFLimit', 
            'outstandingShare': 'OutstandingShare', 
            'freeFloatRate': 'FreeFloatRate',
            'freeFloat':'FreeFloat'})
        
        return df

    def _StockConsump(self, data: pd.DataFrame, Coef: int):
        data["Stock Ratio"] = data["TotalCapitalization"] * Coef / data["TotalCapitalization"].min()
        data["Shares to Buy"] = data["Stock Ratio"].apply(lambda x: round(x, -2))
        data["Stock Value to Buy"] = data["Shares to Buy"] * data["close"]
        return data["Stock Value to Buy"].sum()

    def get(self, Budget: int, Ticker: str) -> pd.DataFrame:
        self.ticker = Ticker.upper()
        df_FiinX = self._FiinXData()
        self.Tickers = df_FiinX['ticker'].tolist()
        df_closeprice = GetBarData(
            access_token=self.access_token(),
            tickers=self.Tickers,
            fields=['close'],
            adjusted=True,
            period=1).get().to_dataFrame()
        
        df = pd.merge(left=df_closeprice, right=df_FiinX, how='left', on='ticker')
        df["TotalCapitalization"] = df["OutstandingShare"] * df["FreeFloatRate"] * df["MarketCapFLimit"]
        AdjustCoef = 0
        TotalConsump = 0
        while TotalConsump < Budget:
            df_copy = df.copy()
            AdjustCoef += 1
            TotalConsump =self._StockConsump(data=df_copy, Coef=AdjustCoef)
        
        TotalConsump = self._StockConsump(data=df, Coef=AdjustCoef - 1)
        return df
