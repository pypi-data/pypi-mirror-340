# This code is encrypted and does not contain viruses or Trojans.
import pandas as pd
class RealTimeData:
    """RealTimeData is a class that represents a real-time data of a stock. This class is 
    a structure that contains all the information of a stock at a specific time. You can use 
    to_dataFrame() method to convert this class to a pandas DataFrame."""
    COLUMN_MAPPING = {
            'ReferenceIndex': 'Reference',
            'ReferencePrice': 'Reference',
            'OpenPrice': 'Open',
            'OpenIndex': 'Open',
            'ClosePrice': 'Close',
            'CloseIndex': 'Close',
            'HighestPrice': 'High',
            'HighestIndex': 'High',
            'LowestPrice': 'Low',
            'LowestIndex': 'Low',
            'PriceChange': 'Change',
            'IndexChange': 'Change',
            'PercentPriceChange': 'ChangePercent',
            'PercentIndexChange': 'ChangePercent',
            'VolumeBu': 'TotalBuyTradeVolume',
            'VolumeSd': 'TotalSellTradeVolume',
            'TotalBuyTradeVolume': 'TotalBuyTradeVolume',
            'TotalSellTradeVolume': 'TotalSellTradeVolume'
    }
    
    def __init__(self, data):
        data = data.rename(columns=self.COLUMN_MAPPING)

        data_converted = self._convert_data_types(data)
        self.__private_attribute = data_converted
        self.Ticker = data['Ticker'].values[0]
        self.TotalMatchVolume = data_converted['TotalMatchVolume'][0]
        self.MarketStatus = data_converted['MarketStatus'][0]
        self.TradingDate = data_converted['TradingDate'][0]
        self.ComGroupCode = data_converted['ComGroupCode'][0]
        self.Reference = data_converted['Reference'][0]
        self.Open = data_converted['Open'][0]
        self.Close = data_converted['Close'][0]
        self.High = data_converted['High'][0]
        self.Low = data_converted['Low'][0]
        self.Change = data_converted['Change'][0]
        self.ChangePercent = data_converted['ChangePercent'][0]
        self.MatchVolume = data_converted['MatchVolume'][0]
        self.MatchValue = data_converted['MatchValue'][0]
        self.TotalMatchValue = data_converted['TotalMatchValue'][0]
        self.TotalBuyTradeVolume = data_converted['TotalBuyTradeVolume'][0]
        self.TotalSellTradeVolume = data_converted['TotalSellTradeVolume'][0]
        self.TotalDealVolume = data_converted['TotalDealVolume'][0]
        self.TotalDealValue = data_converted['TotalDealValue'][0]
        self.ForeignBuyVolumeTotal = data_converted['ForeignBuyVolumeTotal'][0]
        self.ForeignBuyValueTotal = data_converted['ForeignBuyValueTotal'][0]
        self.ForeignSellVolumeTotal = data_converted['ForeignSellVolumeTotal'][0]
        self.ForeignSellValueTotal = data_converted['ForeignSellValueTotal'][0]
        self.Bu = data_converted['Bu'].values[0]
        self.Sd = data_converted['Sd'].values[0]
    def _normalize_columns(self, data):
        return data.rename(columns=self.COLUMN_MAPPING)       

    def _convert_data_types(self, data):
     
        def safe_convert(value, target_type, default=None):
            try:
                return target_type(value) if pd.notna(value) else default
            except (ValueError, TypeError):
                return default

        data_converted = {
            'Ticker': [data['Ticker'].values[0] if pd.notna(data['Ticker'].values[0]) else None],
            'TotalMatchVolume': [safe_convert(data['TotalMatchVolume'].values[0], int, default=0)],
            'MarketStatus': [data['MarketStatus'].values[0] if pd.notna(data['MarketStatus'].values[0]) else None],
            'TradingDate': [data['TradingDate'].values[0] if pd.notna(data['TradingDate'].values[0]) else None],
            'ComGroupCode': [data['ComGroupCode'].values[0] if pd.notna(data['ComGroupCode'].values[0]) else None],
            'Reference': [safe_convert(data['Reference'].values[0], float, default=0.0)],
            'Open': [safe_convert(data['Open'].values[0], float, default=0.0)],
            'Close': [safe_convert(data['Close'].values[0], float, default=0.0)],
            'High': [safe_convert(data['High'].values[0], float, default=0.0)],
            'Low': [safe_convert(data['Low'].values[0], float, default=0.0)],
            'Change': [safe_convert(data['Change'].values[0], float, default=0.0)],
            'ChangePercent': [safe_convert(data['ChangePercent'].values[0], float, default=0.0)],
            'MatchVolume': [safe_convert(data['MatchVolume'].values[0], int, default=0)],
            'MatchValue': [safe_convert(data['MatchValue'].values[0], float, default=0.0)],
            'TotalMatchValue': [safe_convert(data['TotalMatchValue'].values[0], float, default=0.0)],
            'TotalBuyTradeVolume': [safe_convert(data['TotalBuyTradeVolume'].values[0], int, default=0)],
            'TotalSellTradeVolume': [safe_convert(data['TotalSellTradeVolume'].values[0], int, default=0)],
            'TotalDealVolume': [safe_convert(data['TotalDealVolume'].values[0], int, default=0)],
            'TotalDealValue': [safe_convert(data['TotalDealValue'].values[0], float, default=0.0)],
            'ForeignBuyVolumeTotal': [safe_convert(data['ForeignBuyVolumeTotal'].values[0], int, default=0)],
            'ForeignBuyValueTotal': [safe_convert(data['ForeignBuyValueTotal'].values[0], float, default=0.0)],
            'ForeignSellVolumeTotal': [safe_convert(data['ForeignSellVolumeTotal'].values[0], int, default=0)],
            'ForeignSellValueTotal': [safe_convert(data['ForeignSellValueTotal'].values[0], float, default=0.0)],
            'Bu': [safe_convert(data['Bu'].values[0], int, default=0)],
            'Sd': [safe_convert(data['Sd'].values[0], int, default=0)]
            }
        
        return pd.DataFrame(data_converted)
    
    def to_dataFrame(self):
        return self.__private_attribute