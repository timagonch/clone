import requests
import pandas as pd

# Your API key
api_key = 'dc63d528-027a-4e5f-a0eb-6cfffee74609'

# Endpoint URL
url = 'https://api.livecoinwatch.com/coins/list'

# Headers including your API key
headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key,
}

# Request body with parameters
data = {
    "currency": "USD",
    "sort": "rank",
    "order": "ascending",
    "offset": 0,
    "limit": 50,
    "meta": True
}

# Make the POST request
response = requests.post(url, headers=headers, json=data)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    coins_data = response.json()
    # Process the data as needed
    print(coins_data)
else:
    print("Failed to fetch data:", response.status_code)

df = pd.DataFrame(coins_data)

# Assuming 'df' is your DataFrame with all the columns
clean_df = df[['name', 'symbol', 'rate', 'volume', 'cap', 'delta']].copy()

# Saving the clean DataFrame to a pickle file
clean_df.to_pickle('./data/crypto_coins_list_data.pkl')