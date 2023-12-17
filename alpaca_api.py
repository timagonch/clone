from alpaca_trade_api.rest import REST
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.stream import TradingStream
import config
import requests

#client = TradingClient(config.API_KEY, config.SECRET_KEY, paper=True)

# Initialize the Alpaca API client
#api = REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)

# Make a GET request to fetch historical bars for SPY
response = requests.get(config.endpoint, headers=config.headers)

if response.status_code == 200:
    # Data successfully retrieved
    historical_data = response.json()
    print(historical_data)  # Display the fetched data
else:
    # Handle errors if any
    print(f"Failed to fetch data. Status code: {response.status_code}")
    print(response.text)  # Display the error message if available
