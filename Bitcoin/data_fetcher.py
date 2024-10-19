# data_fetcher.py
import requests
import pandas as pd

def get_historical_data(days=30):
    """
    Fetches historical data for Bitcoin in USD for the given number of days.
    Args:
        days (int): Number of days of historical data to fetch.
    Returns:
        pd.DataFrame: Historical price data as a pandas DataFrame.
    """
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': 'daily'
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None