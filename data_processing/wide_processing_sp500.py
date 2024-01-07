# Importing common python packages
import pandas as pd
import numpy as np
import pickle
import ta

# Import the DataFrame from fetch_data.py
df = pd.read_pickle('/Users/lilygoncharov/Documents/Z/code/AI-Trading/data_processing/df_long.pkl')

# Calculate Daily Price Spread (Candlestick Range)
df['Spread'] = df['High'] - df['Low']

# Calculate True Range
df['True_Range'] = np.maximum(df['High'] - df['Low'], 
                              np.maximum(np.abs(df['High'] - df['Close'].shift(1)), 
                                         np.abs(df['Low'] - df['Close'].shift(1))))

# Calculate Price Change (Absolute and Percentage)
df['Price_Change'] = df['Close'] - df['Open']
df['Price_Change_Percent'] = ((df['Close'] - df['Open']) / df['Open']) * 100

# Initialize and calculate RSI, BB, SMA and EMA indicators
indicator_rsi = ta.momentum.RSIIndicator(close=df['Close'], window=14)
indicator_bb = ta.volatility.BollingerBands(close=df['Close'], window=20, window_dev=2)
indicator_sma = ta.trend.SMAIndicator(close=df['Close'], window=20)
indicator_ema = ta.trend.EMAIndicator(close=df['Close'], window=20)

df['RSI'] = indicator_rsi.rsi()
df['BB_Upper'] = indicator_bb.bollinger_hband()
df['BB_Lower'] = indicator_bb.bollinger_lband()
df['SMA_20'] = indicator_sma.sma_indicator()
df['EMA_20'] = indicator_ema.ema_indicator()

# Calculate Momentum Indicators (using stochasic oscillator)
stoch = ta.momentum.StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'], window=14, smooth_window=3)
df['Stoch_%K'] = stoch.stoch()
df['Stoch_%D'] = stoch.stoch_signal()

# Calculate On-Balance Volume (OBV)
df['OBV'] = ta.volume.OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume']).on_balance_volume()

# Calculate Average True Range Indicator
df['ATR'] = ta.volatility.AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close'], window=14).average_true_range()

# Calculate Trend - Moving Average Convergence Divergence (MACD) Indicator
macd = ta.trend.MACD(close=df['Close'], window_slow=26, window_fast=12, window_sign=9)
df['MACD'] = macd.macd()
df['MACD_Signal'] = macd.macd_signal()
df['MACD_Diff'] = macd.macd_diff()

# Pickle the DataFrame
df.to_pickle('/Users/lilygoncharov/Documents/Z/code/AI-Trading/data_processing/df_with_indicators.pkl')