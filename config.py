# ALPACA Keys

API_KEY = 'PK6BG8Z29QYTCK1C4EMD'
SECRET_KEY = '8YVgyawkNvdtw3FF4CKSHXwfwIF9CRyEXEmDamye'
BASE_URL='https://paper-api.alpaca.markets'

headers = {
    'APCA-API-KEY-ID': API_KEY,
    'APCA-API-SECRET-KEY': SECRET_KEY,
}

symbol = 'AAPL'
# Endpoint URL for fetching historical bars
endpoint = f'https://data.alpaca.markets/v2/stocks/{symbol}/bars?timeframe=1D'