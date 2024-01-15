import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import pickle

# Define a mapping dictionary to handle discrepancies
symbol_mapping = {
    'BRK.B': 'BRK-B',
    'BF.B': 'BF-B',
}

# Import the DataFrame from fetch_data.py
sp500_symbols = pd.read_pickle('./pickle/sp500_symbols.pkl')

# Calculate the start and end dates for the last week
end_date = datetime.now()  # Current date
start_date = end_date - timedelta(days=7)  # Subtract 7 days to get the start date for last week

# Format the dates as strings in 'YYYY-MM-DD' format
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Create an empty DataFrame to store the historical data
weekly_sp500_data = pd.DataFrame()

# Loop through each symbol in the S&P 500 list and fetch historical data
for symbol in sp500_symbols:
    # Check if the symbol needs to be converted using the mapping dictionary
    if symbol in symbol_mapping:
        symbol_to_fetch = symbol_mapping[symbol]
    else:
        symbol_to_fetch = symbol

    try:
        stock_data = yf.download(symbol_to_fetch, start=start_date_str, end=end_date_str)
        if not stock_data.empty:
            stock_data = stock_data[['Adj Close']].rename(columns={'Adj Close': symbol})
            weekly_sp500_data = pd.concat([weekly_sp500_data, stock_data], axis=1)
    except Exception as e:
        print(f"Error fetching data for {symbol_to_fetch}: {e}")

# Pickle the DataFrame
weekly_sp500_data.to_pickle('./pickle/weekly_sp500_data.pkl')

# Save DataFrame to a CSV file with proper headers for each stock
file_name = f"sp500_weekly_data_{start_date_str}_{end_date_str}.csv"

# Define the directory path where you want to save the file
directory = './data'

# Specify the file path within the directory
file_name = os.path.join(directory, f"sp500_weekly_data_{start_date_str}_{end_date_str}.csv")

# Save DataFrame to a CSV file with proper headers for each stock
with open(file_name, 'w') as file:
    file.write(f"Weekly data from {start_date_str} to {end_date_str}\n")
    weekly_sp500_data.to_csv(file, header=True)

