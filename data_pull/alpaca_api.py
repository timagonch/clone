# Import packages
from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd

# Parameters
BASE_URL = "https://paper-api.alpaca.markets"
KEY_ID = 'ADD YOURS'
SECRET_KEY = 'ADD YOURS'

# Instantiate REST API Connection
api = REST(key_id=KEY_ID,secret_key=SECRET_KEY,base_url="https://paper-api.alpaca.markets")

# Fetch 1Minute historical bars of Bitcoin
bars = api.get_crypto_bars("SHIB/USD", TimeFrame.Minute).df

bars.head()


# Graph the data with short and long moving averages
import plotly.graph_objects as go

# Calculate moving averages
short_ma = bars['close'].rolling(window=10).mean()
long_ma = bars['close'].rolling(window=30).mean()

# Create the plot
fig = go.Figure()

# Add traces for close, high, low prices
fig.add_trace(go.Scatter(x=bars.index, y=bars['close'], mode='lines', name='Close'))
fig.add_trace(go.Scatter(x=bars.index, y=bars['high'], mode='lines', name='High', line=dict(dash='dash')))
fig.add_trace(go.Scatter(x=bars.index, y=bars['low'], mode='lines', name='Low', line=dict(dash='dash')))

# Add traces for moving averages
fig.add_trace(go.Scatter(x=bars.index, y=short_ma, mode='lines', name='Short MA', line=dict(color='orange')))
fig.add_trace(go.Scatter(x=bars.index, y=long_ma, mode='lines', name='Long MA', line=dict(color='purple')))

# Update layout for a cleaner look
fig.update_layout(title='Crypto Price Data with Moving Averages', xaxis_title='Time', yaxis_title='Price', template="plotly_dark")

fig.show()

