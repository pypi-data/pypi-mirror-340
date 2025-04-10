# This code is encrypted and does not contain viruses or Trojans.

import numpy as np
import pandas as pd

class _FiinIndicator:
    _instance = None
    _authorized = False

    def __new__(cls, *args, **kwargs):
        if not cls._authorized:
            raise RuntimeError("Access denied: FiinIndicator can only be created by FiinSession.")
        
        if cls._instance is None:
            cls._instance = super(_FiinIndicator, cls).__new__(cls)
        return cls._instance

    @classmethod
    def _authorize(cls):
        cls._authorized = True

    @classmethod
    def _deauthorize(cls):
        cls._authorized = False

    class trend:
        class EMA:
            def __init__(self, column: pd.Series, window: int):
                self.column = column
                self.window = window
                
            def ema(self):                
                ema = self.column.ewm(span=self.window, min_periods=self.window, adjust=False).mean()
                return ema
            
        class SMA:
            def __init__(self, column: pd.Series, window: int):
                self.column = column
                self.window = window
                
                
            def sma(self):               
                sma = self.column.rolling(window=self.window, min_periods=self.window).mean()
                return sma

        class WMA:
            def __init__(self, column: pd.Series, window: int = 9):
                self.column = column
                self.window = window
            
            def wma(self):
                weights = np.arange(1, self.window + 1)
                wma = self.column.rolling(window=self.window).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)
                return wma

        class MACD:
            def __init__(self, column: pd.Series, window_slow: int = 26, window_fast: int = 12, window_sign: int = 9):
                self.column = column
                self.window_slow = window_slow
                self.window_fast = window_fast
                self.window_sign = window_sign
                
            def macd(self):
                ema_slow = _FiinIndicator.trend.EMA(self.column, self.window_slow).ema()
                ema_fast = _FiinIndicator.trend.EMA(self.column, self.window_fast).ema()
                macd = ema_fast - ema_slow      
                return macd
            
            def macd_signal(self):
                macd_signal = _FiinIndicator.trend.EMA(self.macd(), self.window_sign).ema()
                return macd_signal
            
            def macd_diff(self):
                macd_diff = self.macd() - self.macd_signal()
                return macd_diff

        class ADX:
            def __init__(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14):
                self.high = high
                self.low = low
                self.close = close
                self.window = window

            def _true_range(self):
                high_low = self.high - self.low
                high_close = (self.high - self.close.shift(1)).abs()
                low_close = (self.low - self.close.shift(1)).abs()
                true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
                return true_range

            def _directional_movement(self):
                plus_dm = self.high.diff()
                minus_dm = -self.low.diff()

                for i in range(plus_dm.shape[0]):
                    p = plus_dm[i]
                    m = minus_dm[i]
                    plus_dm[i] = max(p, 0) if p > m else 0
                    minus_dm[i] = max(m, 0) if m > p else 0

                plus_dm = np.nan_to_num(plus_dm, nan=0.0)
                minus_dm = np.nan_to_num(minus_dm, nan=0.0)
                return plus_dm, minus_dm

            def calculate_adx_pos(self): 
                true_range = self._true_range()
                plus_dm, _ = self._directional_movement()
                smoothed_tr = [np.nan] * self.window
                smoothed_plus_dm = [np.nan] * self.window

                smoothed_tr.append(true_range[1:self.window+1].sum())
                for i in range(self.window + 1, true_range.shape[0]):
                    smoothed_tr.append(smoothed_tr[i - 1] - smoothed_tr[i - 1] / self.window + true_range[i])

                smoothed_tr = pd.Series(smoothed_tr)

                smoothed_plus_dm.append(plus_dm[1:self.window+1].sum())
                for i in range(self.window + 1, plus_dm.shape[0]):
                    smoothed_plus_dm.append(smoothed_plus_dm[i - 1] - smoothed_plus_dm[i - 1] / self.window + plus_dm[i])
                
                smoothed_plus_dm = pd.Series(smoothed_plus_dm)

                adx_pos = 100 * (smoothed_plus_dm / smoothed_tr)
                return adx_pos
            
            def calculate_adx_neg(self):
                true_range = self._true_range()
                _, minus_dm = self._directional_movement()

                smoothed_tr = [np.nan] * self.window
                smoothed_minus_dm = [np.nan] * self.window

                smoothed_tr.append(true_range[1:self.window+1].sum())
                for i in range(self.window + 1, true_range.shape[0]):
                    smoothed_tr.append(smoothed_tr[i - 1] - smoothed_tr[i - 1] / self.window + true_range[i])

                smoothed_tr = pd.Series(smoothed_tr)

                smoothed_minus_dm.append(minus_dm[1:self.window+1].sum())
                for i in range(self.window + 1, minus_dm.shape[0]):
                    smoothed_minus_dm.append(smoothed_minus_dm[i - 1] - smoothed_minus_dm[i - 1] / self.window + minus_dm[i])
                smoothed_minus_dm = pd.Series(smoothed_minus_dm)
                adx_neg = 100 * (smoothed_minus_dm / smoothed_tr)
                return adx_neg
            
            def adx_pos(self):
                adx_pos = self.calculate_adx_pos()
                adx_pos[self.window] = np.nan
                return adx_pos
            
            def adx_neg(self):
                adx_neg = self.calculate_adx_neg()
                adx_neg[self.window] = np.nan
                return adx_neg

            def adx(self):                
                adx_pos = self.calculate_adx_pos()
                adx_neg = self.calculate_adx_neg()

                dx = 100 * ((adx_pos - adx_neg).abs() / (adx_pos + adx_neg))
                adx = [np.nan] * (self.window * 2 - 1)

                adx.append(dx[self.window : self.window * 2].mean())
                for i in range(self.window * 2, dx.shape[0]):
                    adx.append((adx[i - 1] * (self.window - 1) + dx[i]) / self.window)

                adx = pd.Series(adx)
                return adx
            
        class PSAR:
            def __init__(self, high: pd.Series, low: pd.Series, close: pd.Series, 
                         step: float = 0.02, max_step = 0.2):
                self.high = high
                self.low = low
                self.close = close
                self.step = step
                self.max_step = max_step

            def psar(self):               
                up_trend = True
                af = self.step
                up_trend_high = self.high.iloc[0]
                down_trend_low = self.low.iloc[0]

                psar = self.close.copy()
                psar_up = pd.Series(index=psar.index, dtype="float64")
                psar_down = pd.Series(index=psar.index, dtype="float64")

                for i in range(2, len(self.close)):
                    reversal = False

                    max_high = self.high.iloc[i]
                    min_low = self.low.iloc[i]

                    if up_trend:
                        psar.iloc[i] = psar.iloc[i - 1] + (af * (up_trend_high - psar.iloc[i - 1]))

                        if min_low < psar.iloc[i]:
                            reversal = True
                            psar.iloc[i] = up_trend_high
                            down_trend_low = min_low
                            af = self.step
                        else:
                            if max_high > up_trend_high:
                                up_trend_high = max_high
                                af = min(af + self.step, self.max_step)

                            low1 = self.low.iloc[i - 1]
                            low2 = self.low.iloc[i - 2]
                            if low2 < psar.iloc[i]:
                                psar.iloc[i] = low2
                            elif low1 < psar.iloc[i]:
                                psar.iloc[i] = low1
                    else:
                        psar.iloc[i] = psar.iloc[i - 1] - (af * (psar.iloc[i - 1] - down_trend_low))

                        if max_high > psar.iloc[i]:
                            reversal = True
                            psar.iloc[i] = down_trend_low
                            up_trend_high = max_high
                            af = self.step
                        else:
                            if min_low < down_trend_low:
                                down_trend_low = min_low
                                af = min(af + self.step, self.max_step)

                            high1 = self.high.iloc[i - 1]
                            high2 = self.high.iloc[i - 2]
                            if high2 > psar.iloc[i]:
                                psar[i] = high2
                            elif high1 > psar.iloc[i]:
                                psar.iloc[i] = high1

                    up_trend = up_trend != reversal  # XOR

                    if up_trend:
                        psar_up.iloc[i] = psar.iloc[i]
                    else:
                        psar_down.iloc[i] = psar.iloc[i]
                        
                return psar

        class Ichimoku:
            def __init__(self, high: pd.Series, low: pd.Series, close: pd.Series,
                         window1: int = 9, window2: int = 26, window3: int = 52):
                self.high = high
                self.low = low
                self.close = close
                self.window1 = window1
                self.window2 = window2
                self.window3 = window3

            def conversion_line(self):               
                ph = self.high.rolling(window=self.window1).max()
                pl = self.low.rolling(window=self.window1).min()
                conversion_line = (ph + pl) / 2
                return conversion_line

            def base_line(self):               
                ph = self.high.rolling(window=self.window2).max()
                pl = self.low.rolling(window=self.window2).min()
                base_line = (ph + pl) / 2
                return base_line
            
            def leading_span_a(self):               
                leading_span_a = ((self.conversion_line() + self.base_line()) / 2)
                leading_span_a = leading_span_a.shift(self.window2)
                return leading_span_a
        
            def leading_span_b(self):               
                ph = self.high.rolling(window=self.window3).max()
                pl = self.low.rolling(window=self.window3).min()
                leading_span_b = ((ph + pl) / 2)
                leading_span_b = leading_span_b.shift(self.window2)
                return leading_span_b
            
            def lagging_span(self):
                lagging_span = self.close.shift(-self.window2)
                return lagging_span

        class CCI:
            def __init__(self, high: pd.Series, low: pd.Series, close: pd.Series,
                         window: int = 20, constant: float = 0.015):
                self.high = high
                self.low = low
                self.close = close
                self.window = window
                self.constant = constant

            def cci(self):
                typical_price = (self.high + self.low + self.close) / 3
                sma_tp = typical_price.rolling(window=self.window).mean()
                mean_deviation = typical_price.rolling(window=self.window).apply(
                    lambda x: abs(x - x.mean()).mean(), raw=True
                )
                cci = (typical_price - sma_tp) / (self.constant * mean_deviation)
                return cci

        class Aroon:
            def __init__(self, high: pd.Series, low: pd.Series, window: int = 25):
                self.high = high
                self.low = low
                self.window = window

            def aroon_up(self):               
                rolling_high = self.high.rolling(self.window + 1, min_periods=self.window + 1)
                aroon_up = rolling_high.apply(lambda x: float(np.argmax(x)) / self.window * 100, raw=True)
                return aroon_up

            def aroon_down(self):               
                rolling_low = self.low.rolling(self.window + 1, min_periods=self.window + 1)
                aroon_down = rolling_low.apply(lambda x: float(np.argmin(x)) / self.window * 100, raw=True)
                return aroon_down

            def aroon(self):
                aroon_diff = self.aroon_up() - self.aroon_down()
                return aroon_diff

    class momentum:
        class RSI:
            def __init__(self, column: pd.Series, window: int = 14):
                self.column = column
                self.window = window
                
            def rsi(self):
                self.column = self.column.astype(float)
                delta = self.column.diff()
                gain = delta.where(delta > 0, 0) 
                loss = -delta.where(delta < 0, 0) 
                avg_gain = gain.ewm(com=self.window - 1, min_periods=self.window, adjust=False).mean()
                avg_loss = loss.ewm(com=self.window - 1, min_periods=self.window, adjust=False).mean()
                rs = avg_gain / avg_loss.abs() 
                rsi = 100 - (100 / (1 + rs)) 
                rsi[(avg_loss == 0) | (avg_loss == -avg_gain)] = 100  
                return rsi
            
        class Stochastic:
            def __init__(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14, smooth_window: int = 3):
                self.high = high
                self.low = low
                self.close = close
                self.window = window
                self.smooth_window = smooth_window
                
            def stoch(self):               
                lowest_low = self.low.rolling(window=self.window).min()
                highest_high = self.high.rolling(window=self.window).max()
                stoch = 100 * (self.close - lowest_low) / (highest_high - lowest_low)
                return stoch
            
            def stoch_signal(self):
                stochSi = _FiinIndicator.trend.SMA(self.stoch(), self.smooth_window).sma()
                return stochSi

    class volatility:
        class BollingerBands:
            def __init__(self, column: pd.Series, window: int = 20, window_dev: int = 2):
                self.column = column
                self.window = window
                self.window_dev = window_dev
                
            def mavg(self):
                return _FiinIndicator.trend.SMA(self.column, self.window).sma()
            
            def std(self):
                try:
                    rolling_windows = np.lib.stride_tricks.sliding_window_view(self.column, self.window)
                    stds = np.std(rolling_windows, axis=1)
                    stds = np.concatenate([np.full(self.window - 1, np.nan), stds])
                    std = pd.Series(stds, index=self.column.index)
                except:
                    std = pd.Series([np.nan] * self.column.shape[0])
                    
                return std

            def bollinger_hband(self):      
                hband = self.mavg() + (self.window_dev * self.std())
                return hband 
            
            def bollinger_lband(self):      
                lband = self.mavg() - (self.window_dev * self.std())
                return lband 
            
        class Supertrend:
            def __init__(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14, multiplier: float = 3.0):
                self.high = high
                self.low = low
                self.close = close
                self.window = window
                self.multiplier = multiplier
                self.upper_band, self.lower_band = self._calculate_bands()
                self.supertrend_line = self.supertrend()
            def _calculate_bands(self):
                atr = _FiinIndicator.volatility.ATR(self.high, self.low, self.close, self.window).atr()
                hl2 = (self.high + self.low) / 2
                upper_band = hl2 + (atr * self.multiplier)
                lower_band = hl2 - (atr * self.multiplier)
                return upper_band, lower_band
            def supertrend(self):
                supertrend = pd.Series(index=self.close.index)
                in_uptrend = True

                for i in range(self.window, len(self.close)):
                    if self.close[i] <= self.upper_band[i]:
                        in_uptrend = False
                    else:
                        in_uptrend = True

                    if in_uptrend:
                        supertrend[i] = self.lower_band[i]
                    else:
                        supertrend[i] = self.upper_band[i]

                return supertrend

            def supertrend_hband(self):
                atr = _FiinIndicator.volatility.ATR(self.high, self.low, self.close, self.window).atr()
                hl2 = (self.high + self.low) / 2
                upper_band = hl2 + (atr * self.multiplier)
                return upper_band

            def supertrend_lband(self):
                atr = _FiinIndicator.volatility.ATR(self.high, self.low, self.close, self.window).atr()
                hl2 = (self.high + self.low) / 2
                lower_band = hl2 - (atr * self.multiplier)
                return lower_band

        class ATR:
            def __init__(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14):
                self.high = high
                self.low = low
                self.close = close
                self.window = window

            def atr(self):
                tr1 = self.high - self.low
                tr2 = abs(self.high - self.close.shift(1))
                tr3 = abs(self.low - self.close.shift(1))
                tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)   
                atr = _FiinIndicator.trend.SMA(column=tr, window=self.window).sma()
                for i in range(self.window, len(tr)):
                    atr.iloc[i] = (atr.iloc[i-1] * (self.window - 1) + tr.iloc[i]) / self.window
                return atr

    class volume:
        class MFI:
            def __init__(self, high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, window: int = 14):
                self.high = high
                self.low = low
                self.close = close
                self.volume = volume
                self.window = window
                self.typical_price = self._calculate_typical_price()
                self.money_flow = self._calculate_money_flow()
                self.positive_money_flow = self._calculate_positive_money_flow()
                self.negative_money_flow = self._calculate_negative_money_flow()
            
            def _calculate_typical_price(self):
                return (self.high + self.low + self.close) / 3

            def _calculate_money_flow(self):
                return self.typical_price * self.volume

            def _calculate_positive_money_flow(self):
                prev_typical_price = self.typical_price.shift(1)
                return self.money_flow.where(self.typical_price > prev_typical_price, 0)

            def _calculate_negative_money_flow(self):
                prev_typical_price = self.typical_price.shift(1)
                return self.money_flow.where(self.typical_price < prev_typical_price, 0)

            def mfi(self):
                pos_flow_sum = self.positive_money_flow.rolling(window=self.window, min_periods=self.window).sum()
                neg_flow_sum = self.negative_money_flow.rolling(window=self.window, min_periods=self.window).sum()
                money_flow_ratio = pos_flow_sum / neg_flow_sum.replace(0, pd.NA)
                mfi = 100 - (100 / (1 + money_flow_ratio))
                return mfi

        class OBV:
            def __init__(self, column: pd.Series, volume: pd.Series):
                self.column = column
                self.volume = volume
            
            def obv(self):
                obv = pd.Series(index=self.column.index)
                obv.iloc[0] = self.volume.iloc[0]

                for i in range(1, len(self.column)):
                    if self.column.iloc[i] > self.column.iloc[i - 1]:
                        obv.iloc[i] = obv.iloc[i - 1] + self.volume.iloc[i]
                    elif self.column.iloc[i] < self.column.iloc[i - 1]:
                        obv.iloc[i] = obv.iloc[i - 1] - self.volume.iloc[i]
                    else:
                        obv.iloc[i] = obv.iloc[i - 1]
                return obv

        class VWAP:
            def __init__(self, high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, window: int = 14):
                self.high = high
                self.low = low
                self.close = close
                self.volume = volume
                self.window = window

            def vwap(self):
                volume_weighted_price = ((self.high + self.low + self.close) / 3) * self.volume
                cumulative_volume_weighted_price = volume_weighted_price.rolling(window=self.window, min_periods=self.window).sum()
                cumulative_volume = self.volume.rolling(window=self.window, min_periods=self.window).sum()
                vwap = cumulative_volume_weighted_price / cumulative_volume.replace(0, np.NAN)
                return vwap
            
    class smart_money_concepts:
        class FVG:
            def __init__(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, join_consecutive: bool = True):
                self.open = open
                self.high = high
                self.low = low
                self.close = close
                self.join_consecutive = join_consecutive
                self.ohlc = pd.DataFrame(self.open, self.high, self.low, self.close)
                self.fvg_values, self.top, self.bottom, self.mitigatedIndex = self._calc_fvg()

            def _calc_fvg(self):
                
                fvg = np.where(((self.high.shift(1) < self.low.shift(-1)) & (self.close > self.open)) 
                            | ((self.low.shift(1) > self.high.shift(-1)) & (self.close < self.open)),
                            np.where(self.close > self.open, 1, -1), np.nan)
                
                top = np.where(
                    ~np.isnan(fvg),
                    np.where(
                        self.close > self.open,
                        self.low.shift(-1),
                        self.low.shift(1),
                    ),
                    np.nan,
                )

                bottom = np.where(
                    ~np.isnan(fvg),
                    np.where(
                        self.close > self.open,
                        self.high.shift(1),
                        self.high.shift(-1),
                    ),
                    np.nan,
                )

                if self.join_consecutive:
                    for i in range(len(fvg) - 1):
                        if fvg[i] == fvg[i + 1]:
                            top[i + 1] = max(top[i], top[i + 1])
                            bottom[i + 1] = min(bottom[i], bottom[i + 1])
                            fvg[i] = top[i] = bottom[i] = np.nan

                mitigated_index = np.zeros(len(self.ohlc), dtype=np.int32)
                for i in np.where(~np.isnan(fvg))[0]:
                    mask = np.zeros(len(self.ohlc), dtype=np.bool_)
                    if fvg[i] == 1:
                        mask = self.low[i + 2 :] <= top[i]
                    elif fvg[i] == -1:
                        mask = self.high[i + 2 :] >= bottom[i]
                    if np.any(mask):
                        j = np.argmax(mask) + i + 2
                        mitigated_index[i] = j

                mitigated_index = np.where(np.isnan(fvg), np.nan, mitigated_index)
                return fvg, top, bottom, mitigated_index
            
            def fvg(self):
                return self.fvg_values
            
            def fvg_top(self):
                return self.top
            
            def fvg_bottom(self):
                return self.bottom
            
            def fvg_mitigatedIndex(self):
                return self.mitigatedIndex

        class Swing_Highs_Lows:
            def __init__(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, swing_length: int = 50):
                self.open = open
                self.high = high
                self.low = low
                self.close = close
                self.swing_length = swing_length
                self.ohlc = pd.DataFrame(self.open, self.high, self.low, self.close)
                self.swing_highs_lows_value, self.level_value = self._calc_swing_highs_lows()

            def _calc_swing_highs_lows(self):
                self.swing_length *= 2
                swing_highs_lows = np.where(
                    self.high == self.high.shift(-(self.swing_length // 2)).rolling(self.swing_length).max(), 1,
                    np.where(
                        self.low == self.low.shift(-(self.swing_length // 2)).rolling(self.swing_length).min(), -1,
                        np.nan,
                    ),
                )

                while True:
                    positions = np.where(~np.isnan(swing_highs_lows))[0]

                    if len(positions) < 2:
                        break

                    current = swing_highs_lows[positions[:-1]]
                    next = swing_highs_lows[positions[1:]]

                    highs = self.high.iloc[positions[:-1]].values
                    lows = self.low.iloc[positions[:-1]].values

                    next_highs = self.high.iloc[positions[1:]].values
                    next_lows = self.low.iloc[positions[1:]].values

                    index_to_remove = np.zeros(len(positions), dtype=bool)

                    consecutive_highs = (current == 1) & (next == 1)
                    index_to_remove[:-1] |= consecutive_highs & (highs < next_highs)
                    index_to_remove[1:] |= consecutive_highs & (highs >= next_highs)

                    consecutive_lows = (current == -1) & (next == -1)
                    index_to_remove[:-1] |= consecutive_lows & (lows > next_lows)
                    index_to_remove[1:] |= consecutive_lows & (lows <= next_lows)

                    if not index_to_remove.any():
                        break

                    swing_highs_lows[positions[index_to_remove]] = np.nan

                positions = np.where(~np.isnan(swing_highs_lows))[0]

                if len(positions) > 0:
                    if swing_highs_lows[positions[0]] == 1:
                        swing_highs_lows[0] = -1
                    if swing_highs_lows[positions[0]] == -1:
                        swing_highs_lows[0] = 1
                    if swing_highs_lows[positions[-1]] == -1:
                        swing_highs_lows[-1] = 1
                    if swing_highs_lows[positions[-1]] == 1:
                        swing_highs_lows[-1] = -1

                level = np.where(
                    ~np.isnan(swing_highs_lows),
                    np.where(swing_highs_lows == 1, self.high, self.low),
                    np.nan,
                )

                return swing_highs_lows, level
            
            def swing_HL(self):
                return self.swing_highs_lows_value
            
            def swing_level(self):
                return self.level_value
            
        class Break_Of_Struture_And_Change_Of_Character:
            def __init__(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, close_break: bool = True, swing_length: int = 50):
                self.open = open
                self.high = high
                self.low = low
                self.close = close
                self.close_break = close_break
                self.swing_length = swing_length
                self.ohlc = pd.DataFrame(self.open, self.high, self.low, self.close)
                self.bos_value, self.choch_value, self.level_value, self.broken_value = self._calc_bos_choch()

            def _calc_bos_choch(self):
                swing_highs_lows = _FiinIndicator.smart_money_concepts.Swing_Highs_Lows(self.open, self.high, self.low, self.close, self.swing_length)
                highlow = swing_highs_lows.swing_HL()
                level = swing_highs_lows.swing_level()

                level_order = []
                highs_lows_order = []

                bos = np.zeros(len(self.ohlc), dtype=np.int32)
                choch = np.zeros(len(self.ohlc), dtype=np.int32)
                level = np.zeros(len(self.ohlc), dtype=np.float32)

                last_positions = []

                for i in range(len(highlow)):
                    if not np.isnan(highlow[i]):
                        level_order.append(level[i])
                        highs_lows_order.append(highlow[i])
                        if len(level_order) >= 4:
                            # bullish bos
                            bos[last_positions[-2]] = (
                                1
                                if (
                                    np.all(highs_lows_order[-4:] == [-1, 1, -1, 1])
                                    and np.all(
                                        level_order[-4]
                                        < level_order[-2]
                                        < level_order[-3]
                                        < level_order[-1]
                                    )
                                )
                                else 0
                            )
                            level[last_positions[-2]] = (
                                level_order[-3] if bos[last_positions[-2]] != 0 else 0
                            )

                            # bearish bos
                            bos[last_positions[-2]] = (
                                -1
                                if (
                                    np.all(highs_lows_order[-4:] == [1, -1, 1, -1])
                                    and np.all(
                                        level_order[-4]
                                        > level_order[-2]
                                        > level_order[-3]
                                        > level_order[-1]
                                    )
                                )
                                else bos[last_positions[-2]]
                            )
                            level[last_positions[-2]] = (
                                level_order[-3] if bos[last_positions[-2]] != 0 else 0
                            )

                            # bullish choch     
                            choch[last_positions[-2]] = (
                                1
                                if (
                                    np.all(highs_lows_order[-4:] == [-1, 1, -1, 1])
                                    and np.all(
                                        level_order[-1]
                                        > level_order[-3]
                                        > level_order[-4]
                                        > level_order[-2]
                                    )
                                )
                                else 0
                            )
                            level[last_positions[-2]] = (
                                level_order[-3]
                                if choch[last_positions[-2]] != 0
                                else level[last_positions[-2]]
                            )

                            # bearish choch
                            choch[last_positions[-2]] = (
                                -1
                                if (
                                    np.all(highs_lows_order[-4:] == [1, -1, 1, -1])
                                    and np.all(
                                        level_order[-1]
                                        < level_order[-3]
                                        < level_order[-4]
                                        < level_order[-2]
                                    )
                                )
                                else choch[last_positions[-2]]
                            )
                            level[last_positions[-2]] = (
                                level_order[-3]
                                if choch[last_positions[-2]] != 0
                                else level[last_positions[-2]]
                            )

                        last_positions.append(i)

                broken = np.zeros(len(self.ohlc), dtype=np.int32)
                for i in np.where(np.logical_or(bos != 0, choch != 0))[0]:
                    mask = np.zeros(len(self.ohlc), dtype=np.bool_)
                    if bos[i] == 1 or choch[i] == 1:
                        mask = self.ohlc["close" if self.close_break else "high"][i + 2 :] > level[i]
                    elif bos[i] == -1 or choch[i] == -1:
                        mask = self.ohlc["close" if self.close_break else "low"][i + 2 :] < level[i]
                    if np.any(mask):
                        j = np.argmax(mask) + i + 2
                        broken[i] = j
                        for k in np.where(np.logical_or(bos != 0, choch != 0))[0]:
                            if k < i and broken[k] >= j:
                                bos[k] = 0
                                choch[k] = 0
                                level[k] = 0

                for i in np.where(np.logical_and(np.logical_or(bos != 0, choch != 0), broken == 0))[0]:
                    bos[i] = 0
                    choch[i] = 0
                    level[i] = 0

                bos = np.where(bos != 0, bos, np.nan)
                choch = np.where(choch != 0, choch, np.nan)
                level = np.where(level != 0, level, np.nan)
                broken = np.where(broken != 0, broken, np.nan)
                return bos, choch, level, broken
            
            def break_of_structure(self):
                return self.bos_value
            
            def chage_of_charactor(self):
                return self.choch_value
            
            def bos_choch_level(self):
                return self.level_value

            def broken_index(self):
                return self.broken_value
        
        class Order_Blocks:
            def __init__(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, close_mitigation: bool = False, swing_length: int = 50):
                self.open = open
                self.high = high
                self.low = low
                self.close = close
                self.volume = volume
                self.close_mitigation = close_mitigation
                self.swing_length = swing_length
                self.ohlc = pd.DataFrame(self.open, self.high, self.low, self.close, self.volume)
                self.ob_value, self.top_value, self.bottom_value, self.obVolume_value, self.mitigated_index_value, self.percentage_value = self._calc_ob()

            def _calc_ob(self):
                swing_highs_lows = _FiinIndicator.smart_money_concepts.Swing_Highs_Lows(self.open, self.high, self.low, self.close, self.swing_length)
                highlow = swing_highs_lows.swing_HL()
                ohlc_len = len(self.ohlc)

                _open = self.open.values
                _high = self.high.values
                _low = self.low.values
                _close = self.close.values
                _volume = self.volume.values
                _swing_high_low = highlow

                crossed = np.full(len(self.ohlc), False, dtype=bool)
                ob = np.zeros(len(self.ohlc), dtype=np.int32)
                top = np.zeros(len(self.ohlc), dtype=np.float32)
                bottom = np.zeros(len(self.ohlc), dtype=np.float32)
                obVolume = np.zeros(len(self.ohlc), dtype=np.float32)
                lowVolume = np.zeros(len(self.ohlc), dtype=np.float32)
                highVolume = np.zeros(len(self.ohlc), dtype=np.float32)
                percentage = np.zeros(len(self.ohlc), dtype=np.int32)
                mitigated_index = np.zeros(len(self.ohlc), dtype=np.int32)
                breaker = np.full(len(self.ohlc), False, dtype=bool)

                for i in range(ohlc_len):
                    close_index = i
                    if len(ob[ob == 1]) > 0:
                        for j in range(len(ob) - 1, -1, -1):
                            if ob[j] == 1:
                                currentOB = j
                                if breaker[currentOB]:
                                    if _high[close_index] > top[currentOB]:
                                        ob[j] = top[j] = bottom[j] = obVolume[j] = lowVolume[j] = (
                                            highVolume[j]
                                        ) = mitigated_index[j] = percentage[j] = 0.0

                                elif (
                                    not self.close_mitigation and _low[close_index] < bottom[currentOB]
                                ) or (
                                    self.close_mitigation
                                    and min(_open[close_index], _close[close_index]) < bottom[currentOB]
                                ):
                                    breaker[currentOB] = True
                                    mitigated_index[currentOB] = close_index - 1

                    last_top_indices = np.where(
                        (_swing_high_low == 1)
                        & (np.arange(len(highlow)) < close_index)
                    )[0]

                    if last_top_indices.size > 0:
                        last_top_index = np.max(last_top_indices)
                    else:
                        last_top_index = None

                    if last_top_index is not None:

                        swing_top_price = _high[last_top_index]
                        if _close[close_index] > swing_top_price and not crossed[last_top_index]:
                            crossed[last_top_index] = True
                            obBtm = _high[close_index - 1]
                            obTop = _low[close_index - 1]
                            obIndex = close_index - 1
                            for j in range(1, close_index - last_top_index):
                                obBtm = min(
                                    _low[last_top_index + j],
                                    obBtm,
                                )
                                if obBtm == _low[last_top_index + j]:
                                    obTop = _high[last_top_index + j]
                                obIndex = (
                                    last_top_index + j
                                    if obBtm == _low[last_top_index + j]
                                    else obIndex
                                )

                            ob[obIndex] = 1
                            top[obIndex] = obTop
                            bottom[obIndex] = obBtm
                            obVolume[obIndex] = (
                                _volume[close_index]
                                + _volume[close_index - 1]
                                + _volume[close_index - 2]
                            )
                            lowVolume[obIndex] = _volume[close_index - 2]
                            highVolume[obIndex] = _volume[close_index] + _volume[close_index - 1]
                            percentage[obIndex] = (
                                np.min([highVolume[obIndex], lowVolume[obIndex]], axis=0)
                                / np.max([highVolume[obIndex], lowVolume[obIndex]], axis=0)
                                if np.max([highVolume[obIndex], lowVolume[obIndex]], axis=0) != 0
                                else 1
                            ) * 100.0

                for i in range(len(self.ohlc)):
                    close_index = i
                    close_price = _close[close_index]

                    if len(ob[ob == -1]) > 0:
                        for j in range(len(ob) - 1, -1, -1):
                            if ob[j] == -1:
                                currentOB = j
                                if breaker[currentOB]:
                                    if _low[close_index] < bottom[currentOB]:

                                        ob[j] = top[j] = bottom[j] = obVolume[j] = lowVolume[j] = (
                                            highVolume[j]
                                        ) = mitigated_index[j] = percentage[j] = 0.0

                                elif (
                                    not self.close_mitigation and _high[close_index] > top[currentOB]
                                ) or (
                                    self.close_mitigation
                                    and max(
                                        _open[close_index],
                                        _close[close_index],
                                    )
                                    > top[currentOB]
                                ):
                                    breaker[currentOB] = True
                                    mitigated_index[currentOB] = close_index

                    last_btm_indices = np.where(
                        (highlow == -1)
                        & (np.arange(len(highlow)) < close_index)
                    )[0]
                    if last_btm_indices.size > 0:
                        last_btm_index = np.max(last_btm_indices)
                    else:
                        last_btm_index = None

                    if last_btm_index is not None:
                        swing_btm_price = _low[last_btm_index]
                        if close_price < swing_btm_price and not crossed[last_btm_index]:
                            crossed[last_btm_index] = True
                            obBtm = _low[close_index - 1]
                            obTop = _high[close_index - 1]
                            obIndex = close_index - 1
                            for j in range(1, close_index - last_btm_index):
                                obTop = max(_high[last_btm_index + j], obTop)
                                obBtm = (
                                    _low[last_btm_index + j]
                                    if obTop == _high[last_btm_index + j]
                                    else obBtm
                                )
                                obIndex = (
                                    last_btm_index + j
                                    if obTop == _high[last_btm_index + j]
                                    else obIndex
                                )

                            ob[obIndex] = -1
                            top[obIndex] = obTop
                            bottom[obIndex] = obBtm
                            obVolume[obIndex] = (
                                _volume[close_index]
                                + _volume[close_index - 1]
                                + _volume[close_index - 2]
                            )
                            lowVolume[obIndex] = _volume[close_index] + _volume[close_index - 1]
                            highVolume[obIndex] = _volume[close_index - 2]
                            percentage[obIndex] = (
                                np.min([highVolume[obIndex], lowVolume[obIndex]], axis=0)
                                / np.max([highVolume[obIndex], lowVolume[obIndex]], axis=0)
                                if np.max([highVolume[obIndex], lowVolume[obIndex]], axis=0) != 0
                                else 1
                            ) * 100.0

                ob = np.where(ob != 0, ob, np.nan)
                top = np.where(~np.isnan(ob), top, np.nan)
                bottom = np.where(~np.isnan(ob), bottom, np.nan)
                obVolume = np.where(~np.isnan(ob), obVolume, np.nan)
                mitigated_index = np.where(~np.isnan(ob), mitigated_index, np.nan)
                percentage = np.where(~np.isnan(ob), percentage, np.nan)
        
                return ob, top, bottom, obVolume, mitigated_index, percentage

            def ob(self):
                return self.ob_value
        
            def ob_top(self):
                return self.top_value
        
            def ob_bottom(self):
                return self.bottom_value
        
            def ob_volume(self):
                return self.obVolume_value
        
            def ob_mitigated_index(self):
                return self.mitigated_index_value
        
            def ob_percetage(self):
                return self.percentage_value

        class Liquidity:
            def __init__(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, range_percent: float = 0.01, swing_length: int = 50):
                self.open = open
                self.high = high
                self.low = low
                self.close = close
                self.range_percent = range_percent
                self.swing_length = swing_length
                self.ohlc = pd.DataFrame(self.open, self.high, self.low, self.close)
                self.liquidity_value, self.liquidity_level_value, self.liquidity_end_value, self.liquidity_swept_value = self._calc_liquidity()
                
            def _calc_liquidity(self):
                swing_highs_lows = _FiinIndicator.smart_money_concepts.Swing_Highs_Lows(self.open, self.high, self.low, self.close, self.swing_length)
                highlow = swing_highs_lows.swing_HL()
                level = swing_highs_lows.swing_level()
                pip_range = (max(self.high) - min(self.low)) * self.range_percent
                liquidity = np.zeros(len(self.ohlc), dtype=np.int32)
                liquidity_level = np.zeros(len(self.ohlc), dtype=np.float32)
                liquidity_end = np.zeros(len(self.ohlc), dtype=np.int32)
                liquidity_swept = np.zeros(len(self.ohlc), dtype=np.int32)

                for i in range(len(self.ohlc)):
                    if highlow[i] == 1:
                        high_level = level[i]
                        range_low = high_level - pip_range
                        range_high = high_level + pip_range
                        temp_liquidity_level = [high_level]
                        end = i
                        swept = 0
                        for c in range(i + 1, len(self.ohlc)):
                            if (
                                highlow[c] == 1
                                and range_low <= level[c] <= range_high
                            ):
                                end = c
                                temp_liquidity_level.append(level[c])
                                # swing_highs_lows.loc[c] = 0
                                swing_highs_lows.swing_highs_lows_value[c] = 0
                                
                            if self.high.iloc[c] >= range_high:
                                swept = c
                                break
                        if len(temp_liquidity_level) > 1:
                            average_high = sum(temp_liquidity_level) / len(temp_liquidity_level)
                            liquidity[i] = 1
                            liquidity_level[i] = average_high
                            liquidity_end[i] = end
                            liquidity_swept[i] = swept

                for i in range(len(self.ohlc)):
                    if highlow[i] == -1:
                        low_level = level[i]
                        range_low = low_level - pip_range
                        range_high = low_level + pip_range
                        temp_liquidity_level = [low_level]
                        start = i
                        end = i
                        swept = 0
                        for c in range(i + 1, len(self.ohlc)):
                            if (
                                highlow[c] == -1
                                and range_low <= level[c] <= range_high
                            ):
                                end = c
                                temp_liquidity_level.append(level[c])
                                # swing_highs_lows.loc[c] = 0
                                swing_highs_lows.swing_highs_lows_value[c] = 0
                            if self.low.iloc[c] <= range_low:
                                swept = c
                                break
                        if len(temp_liquidity_level) > 1:
                            average_low = sum(temp_liquidity_level) / len(temp_liquidity_level)
                            liquidity[i] = -1
                            liquidity_level[i] = average_low
                            liquidity_end[i] = end
                            liquidity_swept[i] = swept

                liquidity = np.where(liquidity != 0, liquidity, np.nan)
                liquidity_level = np.where(~np.isnan(liquidity), liquidity_level, np.nan)
                liquidity_end = np.where(~np.isnan(liquidity), liquidity_end, np.nan)
                liquidity_swept = np.where(~np.isnan(liquidity), liquidity_swept, np.nan)
                return liquidity, liquidity_level, liquidity_end, liquidity_swept
            
            def liquidity(self):
                return self.liquidity_value
            
            def liquidity_level(self):
                return self.liquidity_level_value
            
            def liquidity_end(self):
                return self.liquidity_end_value
            
            def liquidity_swept(self):
                return self.liquidity_swept_value



    ###### Function 
    #### Trend

    # EMA
    def ema(self, column: pd.Series, window: int):
        return _FiinIndicator.trend.EMA(column=column, window=window).ema()
    
    # SMA
    def sma(self, column: pd.Series, window: int):
        return _FiinIndicator.trend.SMA(column=column, window=window).sma()
    
    # WMA
    def wma(self, column: pd.Series, window: int):
        return _FiinIndicator.trend.WMA(column=column, window=window).wma()
    
    # MACD
    def macd(self, column: pd.Series, window_slow: int = 26, window_fast: int = 12):
        return _FiinIndicator.trend.MACD(
            column=column, 
            window_slow=window_slow, 
            window_fast=window_fast
        ).macd()
    
    def macd_signal(self, column: pd.Series, window_slow: int = 26, window_fast: int = 12, window_sign: int = 9):
        return _FiinIndicator.trend.MACD(
            column=column, 
            window_slow=window_slow, 
            window_fast=window_fast, 
            window_sign=window_sign,
        ).macd_signal()
    
    def macd_diff(self, column: pd.Series, window_slow: int = 26, window_fast: int = 12, window_sign: int = 9):
        return _FiinIndicator.trend.MACD(
            column=column, 
            window_slow=window_slow, 
            window_fast=window_fast, 
            window_sign=window_sign,
        ).macd_diff()
    
    # ADX
    def adx(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14):
        return _FiinIndicator.trend.ADX(
            high=high,
            low=low,
            close=close,
            window=window
        ).adx()
    
    def adx_pos(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14):
        return _FiinIndicator.trend.ADX(
            high=high,
            low=low,
            close=close,
            window=window
        ).adx_pos()
    
    def adx_neg(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14):
        return _FiinIndicator.trend.ADX(
            high=high,
            low=low,
            close=close,
            window=window
        ).adx_neg()
    
    # PSAR
    def psar(self, high: pd.Series, low: pd.Series, close: pd.Series, step: float = 0.02, max_step: float = 0.2):
        return _FiinIndicator.trend.PSAR(
            high=high, 
            low=low, 
            close=close, 
            step=step, 
            max_step=max_step
        ).psar()

    # Ichimoku
    def ichimoku_a(self, high: pd.Series, low: pd.Series, close: pd.Series, window1: int = 9, window2: int = 26, window3: int = 52):      
        return _FiinIndicator.trend.Ichimoku(
            high=high, 
            low=low, 
            close=close,
            window1=window1, 
            window2=window2, 
            window3=window3
        ).leading_span_a()

    def ichimoku_b(self, high: pd.Series, low: pd.Series, close: pd.Series, window1: int = 9, window2: int = 26, window3: int = 52):
        return _FiinIndicator.trend.Ichimoku(
            high=high, 
            low=low, 
            close=close,
            window1=window1, 
            window2=window2, 
            window3=window3
        ).leading_span_b()
    
    def ichimoku_base_line(self, high: pd.Series, low: pd.Series, close: pd.Series, window1: int = 9, window2: int = 26, window3: int = 52):
        return _FiinIndicator.trend.Ichimoku(
            high=high, 
            low=low, 
            close=close,
            window1=window1, 
            window2=window2,
            window3=window3
        ).base_line()
    
    def ichimoku_conversion_line(self, high: pd.Series, low: pd.Series, close: pd.Series, window1: int = 9, window2: int = 26, window3: int = 52):
        return _FiinIndicator.trend.Ichimoku(
            high=high, 
            low=low, 
            close=close,
            window1=window1, 
            window2=window2, 
            window3=window3
        ).conversion_line()
    
    def ichimoku_lagging_line(self, high: pd.Series, low: pd.Series, close: pd.Series, window1: int = 9, window2: int = 26, window3: int = 52):
        return _FiinIndicator.trend.Ichimoku(
            high=high, 
            low=low, 
            close=close,
            window1=window1, 
            window2=window2, 
            window3=window3
        ).lagging_span()

    # CCI
    def cci(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 20, constant: float = 0.015):
        return _FiinIndicator.trend.CCI(
            high = high, 
            low = low, 
            close = close, 
            window = window, 
            constant = constant
        ).cci()
    
    # Aroon
    def aroon(self, high: pd.Series, low: pd.Series, window: int = 25):
        return _FiinIndicator.trend.Aroon(
            high=high, 
            low=low, 
            window=window
        ).aroon()
    
    def aroon_up(self, high: pd.Series, low: pd.Series, window: int = 25):
        return _FiinIndicator.trend.Aroon(
            high=high, 
            low=low, 
            window=window
        ).aroon_up()
    
    def aroon_down(self, high: pd.Series, low: pd.Series, window: int = 25):
        return _FiinIndicator.trend.Aroon(
            high=high, 
            low=low, 
            window=window
        ).aroon_down()

    #### Momentum

    # RSI
    def rsi(self, column: pd.Series, window: int = 14):
        return _FiinIndicator.momentum.RSI(
            column=column, 
            window=window
        ).rsi()

    # Stochastic
    def stoch(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14):
        return _FiinIndicator.momentum.Stochastic(
            high=high, 
            low=low, 
            close=close, 
            window=window
        ).stoch()
    
    def stoch_signal(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14, smooth_window: int = 3):
        return _FiinIndicator.momentum.Stochastic(
            high=high, 
            low=low, 
            close=close, 
            window=window, 
            smooth_window=smooth_window
        ).stoch_signal()
    
    #### Volatility

    # Bollinger
    def bollinger_hband(self, column: pd.Series, window: int = 20, window_dev: int = 2):
        return _FiinIndicator.volatility.BollingerBands(
            column=column, 
            window=window, 
            window_dev=window_dev
        ).bollinger_hband()
    
    def bollinger_lband(self, column: pd.Series, window: int = 20, window_dev: int = 2):
        return _FiinIndicator.volatility.BollingerBands(
            column=column, 
            window=window, 
            window_dev=window_dev
        ).bollinger_lband()
    
    # Suppertrend
    def supertrend(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14, multiplier: float = 3.0):
        return _FiinIndicator.volatility.Supertrend(
            high=high, 
            low=low, 
            close=close, 
            window=window, 
            multiplier=multiplier
        ).supertrend()
    
    def supertrend_hband(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14, multiplier: float = 3.0):
        return _FiinIndicator.volatility.Supertrend(
            high=high, 
            low=low, 
            close=close, 
            window=window, 
            multiplier=multiplier
        ).supertrend_hband()
    
    def supertrend_lband(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14, multiplier: float = 3.0):
        return _FiinIndicator.volatility.Supertrend(
            high=high, 
            low=low, 
            close=close, 
            window=window, 
            multiplier=multiplier
        ).supertrend_lband()
    
    # ATR
    def atr(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14):
        return _FiinIndicator.volatility.ATR(
            high=high, 
            low=low, 
            close=close, 
            window=window
        ).atr()
    
    #### Volume

    # MFI
    def mfi(self, high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, window: int = 14):
        return _FiinIndicator.volume.MFI(
            high=high, 
            low=low, 
            close=close, 
            volume=volume, 
            window=window
        ).mfi()
    
    # OBV
    def obv(self, column: pd.Series, volume: pd.Series):
        return _FiinIndicator.volume.OBV(
            column=column, 
            volume=volume
        ).obv()
    
    # VWAP
    def vwap(self, high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, window: int = 14):
        return _FiinIndicator.volume.VWAP(
            high=high, 
            low=low, 
            close=close, 
            volume=volume, 
            window=window
        ).vwap()
    
    #### smart_money_concepts

    # FVG
    def fvg(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, join_consecutive: bool = True):
        return _FiinIndicator.smart_money_concepts.FVG(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            join_consecutive=join_consecutive
        ).fvg()
    
    def fvg_top(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, join_consecutive: bool = True):
        return _FiinIndicator.smart_money_concepts.FVG(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            join_consecutive=join_consecutive
        ).fvg_top()
    
    def fvg_bottom(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, join_consecutive: bool = True):
        return _FiinIndicator.smart_money_concepts.FVG(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            join_consecutive=join_consecutive
        ).fvg_bottom()
    
    def fvg_mitigatedIndex(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, join_consecutive: bool = True):
        return _FiinIndicator.smart_money_concepts.FVG(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            join_consecutive=join_consecutive
        ).fvg_mitigatedIndex()
    
    def swing_HL(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, swing_length: int = 50):
        
        return _FiinIndicator.smart_money_concepts.Swing_Highs_Lows(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            swing_length=swing_length
        ).swing_HL()
    
    def swing_level(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, swing_length: int = 50):
        return _FiinIndicator.smart_money_concepts.Swing_Highs_Lows(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            swing_length=swing_length
        ).swing_level()
    
    # BOS & CHoCH
    def break_of_structure(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, close_break: bool = True, swing_length: int = 50): 
        return _FiinIndicator.smart_money_concepts.Break_Of_Struture_And_Change_Of_Character(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            close_break=close_break, 
            swing_length=swing_length
        ).break_of_structure()
    
    def chage_of_charactor(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, close_break: bool = True, swing_length: int = 50):
        return _FiinIndicator.smart_money_concepts.Break_Of_Struture_And_Change_Of_Character(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            close_break=close_break, 
            swing_length=swing_length
        ).chage_of_charactor()
    
    def bos_choch_level(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, close_break: bool = True, swing_length: int = 50):
        return _FiinIndicator.smart_money_concepts.Break_Of_Struture_And_Change_Of_Character(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            close_break=close_break, 
            swing_length=swing_length
        ).bos_choch_level()
        
    def broken_index(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, close_break: bool = True, swing_length: int = 50):
        return _FiinIndicator.smart_money_concepts.Break_Of_Struture_And_Change_Of_Character(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            close_break=close_break, 
            swing_length=swing_length
        ).broken_index()
    
    # OB
    def ob(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, close_mitigation: bool = False, swing_length: int = 50):
        return _FiinIndicator.smart_money_concepts.Order_Blocks(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            volume=volume, 
            close_mitigation=close_mitigation, 
            swing_length=swing_length
        ).ob()
    
    def ob_top(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, close_mitigation: bool = False, swing_length: int = 50):  
        return _FiinIndicator.smart_money_concepts.Order_Blocks(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            volume=volume, 
            close_mitigation=close_mitigation, 
            swing_length=swing_length
        ).ob_top()
    
    def ob_bottom(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, close_mitigation: bool = False, swing_length: int = 50):
        return _FiinIndicator.smart_money_concepts.Order_Blocks(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            volume=volume, 
            close_mitigation=close_mitigation, 
            swing_length=swing_length
        ).ob_bottom()
    
    def ob_volume(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, close_mitigation: bool = False, swing_length: int = 50):
        return _FiinIndicator.smart_money_concepts.Order_Blocks(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            volume=volume, 
            close_mitigation=close_mitigation, 
            swing_length=swing_length
        ).ob_volume()
        
    def ob_mitigated_index(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, close_mitigation: bool = False, swing_length: int = 50):
        return _FiinIndicator.smart_money_concepts.Order_Blocks(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            volume=volume, 
            close_mitigation=close_mitigation, 
            swing_length=swing_length
        ).ob_mitigated_index()
    
    def ob_percetage(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, close_mitigation: bool = False, swing_length: int = 50):
        return _FiinIndicator.smart_money_concepts.Order_Blocks(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            volume=volume, 
            close_mitigation=close_mitigation, 
            swing_length=swing_length
        ).ob_percetage()

    # Liquidity  
    def liquidity(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, range_percent: float = 0.01, swing_length: int = 50):
        return _FiinIndicator.smart_money_concepts.Liquidity(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            range_percent=range_percent, 
            swing_length=swing_length
        ).liquidity()

    def liquidity_level(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, range_percent: float = 0.01, swing_length: int = 50):
        return _FiinIndicator.smart_money_concepts.Liquidity(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            range_percent=range_percent, 
            swing_length=swing_length
        ).liquidity_level()
    
    def liquidity_end(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, range_percent: float = 0.01, swing_length: int = 50):
        return _FiinIndicator.smart_money_concepts.Liquidity(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            range_percent=range_percent, 
            swing_length=swing_length
        ).liquidity_end()
    
    def liquidity_swept(self, open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series, range_percent: float = 0.01, swing_length: int = 50):
        return _FiinIndicator.smart_money_concepts.Liquidity(
            open=open, 
            high=high, 
            low=low, 
            close=close, 
            range_percent=range_percent, 
            swing_length=swing_length
        ).liquidity_swept()
      