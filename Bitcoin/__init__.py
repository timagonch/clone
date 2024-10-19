# __init__.py

# Importing standard libraries
import os
import sys
import logging

# Importing external dependencies (add more as you install)
import requests

# Setting up logging for the package
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define version of your package (optional)
__version__ = "0.1.0"

# Add any global constants here
DEFAULT_TIMEOUT = 30  # Timeout for external requests in seconds

# Optionally, you can import functions from data_fetcher and analysis here
from .data_fetcher import get_historical_data
from .analysis import add_moving_averages, calculate_volatility, calculate_rsi

# Example of a utility function that you can still use in main.py
def get_bitcoin_price():
    """
    Function to get the current price of Bitcoin using CoinGecko API.
    """
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'bitcoin',
        'vs_currencies': 'usd'
    }
    
    try:
        response = requests.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        price = data['bitcoin']['usd']
        logger.info(f"Bitcoin Price fetched: ${price}")
        return price
    except requests.RequestException as e:
        logger.error(f"Error fetching Bitcoin price: {e}")
        return None