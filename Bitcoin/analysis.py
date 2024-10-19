# analysis.py

def add_moving_averages(df, short_window=7, long_window=30):
    df['MA7'] = df['price'].rolling(window=short_window).mean()
    df['MA30'] = df['price'].rolling(window=long_window).mean()
    return df

def calculate_volatility(df):
    df['price_change'] = df['price'].pct_change()
    df['volatility'] = df['price_change'].rolling(window=7).std() * 100
    return df

def calculate_rsi(df, window=14):
    delta = df['price'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df