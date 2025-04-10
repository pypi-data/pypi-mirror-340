# This code is encrypted and does not contain viruses or Trojans.
import os
import time
import requests
from typing import Union
from datetime import datetime
from dotenv import load_dotenv
from .Rebalance import Rebalance
from .SimilarChart import SimilarChart
from .DateCorr import FindDateCorrelation
from .FiinIndicator import _FiinIndicator
from .Fetch_Trading_Data import Fetch_Trading_Data
from .Trading_Data_Stream import Trading_Data_Stream
from .GetDataPoint import GetDataPoint

### Staging API
# TOKEN_URL = "http://42.112.22.11:9900/connect/token"
# GRANT_TYPE = 'password'
# CLIENT_ID = 'FiinGroup.FiinQuant.ClientDev'
# CLIENT_SECRET = 'fgFQ2)@5)1'
# SCOPE = 'openid FiinGroup.FiinQuant'

### Product API
TOKEN_URL = 'https://auth.fiingroup.vn/connect/token'
GRANT_TYPE = 'password'
CLIENT_ID = 'FiinGroup.FiinQuant.Client'
CLIENT_SECRET = 'fgFQ2)@5)1'
SCOPE = 'openid FiinGroup.FiinQuant'

env_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(env_path):
    load_dotenv(env_path)
    _USERNAME = os.getenv("_USERNAME")
    _PASSWORD = os.getenv("_PASSWORD")

else:
    _USERNAME =''
    _PASSWORD =''

class FiinSession:
    
    """
    This class is used to create a session to access FiinQuant.
    """
    
    def __init__(self, username=_USERNAME, password=_PASSWORD):
        self.username = username
        self.password = password
        self.is_login = False
        self.access_token = None
        self.expired_token = None
        self.urlGetToken = TOKEN_URL
        self._indicator = None
        self.bodyGetToken = {
            'grant_type': GRANT_TYPE,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'scope': SCOPE,
            'username': self.username,
            'password': self.password
        }

    def _is_valid_token(self):
        return self.access_token and time.time() < self.expired_token 
    
    def _get_token(self):
        if not self._is_valid_token():
            self.login()
        return self.access_token    
        
    def login(self):
        if self._is_valid_token():
            self.is_login = True
            return self
        else:
            self.bodyGetToken['username'] = self.username
            self.bodyGetToken['password'] = self.password
            try:
                response = requests.post(self.urlGetToken, data=self.bodyGetToken)
                if response.status_code == 200:
                    res = response.json()
                    self.access_token = res['access_token']
                    self.expired_token = res['expires_in'] + int(time.time()) - 30
                    self.is_login = True
                    return self
                else:
                    res = response.json()
                    print(res['error_description'])
                    self.is_login = False  
                    raise NameError("Login failed")
                
            except:
                self.is_login = False
                return self
    
    def FiinIndicator(self):

        """
        FiinIndicator class is used to calculate technical indicators for stock market data.
        """

        if not self.is_login:
            raise PermissionError("Access denied: Please log in first.")
        if self.is_login and not self._is_valid_token():
            self.login()
        if self._indicator is None:
            # Authorize, create, and deauthorize
            _FiinIndicator._authorize()
            self._indicator = _FiinIndicator()
            self._indicator._deauthorize()
        return self._indicator
        
    def Trading_Data_Stream(self, tickers: Union[list[str], str], callback: callable):

        """
        Using this class to stream real-time stock market matching data. Using start() to start streaming and stop() to stop streaming.
        The variable _stop is used to check if the streaming is stopped or not.
        """

        if self.is_login:
            if not self._is_valid_token():
                self.login()
            return Trading_Data_Stream(self._get_token, tickers, callback)
        else:
            raise NameError("Please login before calling data")
    
    def Fetch_Trading_Data(self, 
                        realtime: bool, 
                        tickers: Union[list[str], str],
                        fields: list, 
                        adjusted: Union[bool,None] = True,
                        period: Union[int, None] = None,  
                        by: str ='1m',  
                        from_date: Union [str, datetime, None] = None, 
                        to_date: Union [str, datetime, None] = None,
                        callback: callable = None,
                        wait_for_full_timeFrame: bool = False,
                        lasted: Union[bool,None] = None):
   
        if self.is_login:
            if not self._is_valid_token():
                self.login()
            return Fetch_Trading_Data(self._get_token, realtime, tickers, fields, adjusted,
                                   period, by, from_date, to_date, callback, wait_for_full_timeFrame, lasted)
        else:
            raise NameError("Please login before calling data")
        
    def FindDateCorrelation(self):

        """
        Using this class to find the correlation between today data and the past data.
        """

        if self.is_login:
            if not self._is_valid_token():
                self.login()
            return FindDateCorrelation(self._get_token)
        else:
            raise NameError("Please login before calling data")

    def Rebalance(self):
        if self.is_login:
            if not self._is_valid_token():
                self.login()
            return Rebalance(self._get_token)
        else:
            raise NameError("Please login before calling data")
    
    def SimilarChart(self):
        if self.is_login:
            if not self._is_valid_token():
                self.login()
            return SimilarChart(self._get_token)
        else:
            raise NameError("Please login before calling data")
    def GetDataPoint(self, ticker: str, field: str, by: str, candle_index: int, adjusted: Union[bool,None]=True):
        if self.is_login:
            if not self._is_valid_token():
                self.login()
            return GetDataPoint(self._get_token, ticker, field, by, candle_index, adjusted)
        else:
            raise NameError("Please login before calling data")
