import requests
import pandas as pd

def get_historical_data(days=30):
    """
    Fetch historical Bitcoin data for the past `days` from the CoinGecko API.
    Returns a DataFrame with 'timestamp' and 'price'.
    """
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': 'daily'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse the JSON response and convert it to a DataFrame
        data = response.json()
        prices = data['prices']  # List of [timestamp, price] entries
        
        # Convert to DataFrame
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert to readable timestamp
        
        return df
    
    except requests.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return None
