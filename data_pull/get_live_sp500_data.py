import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

# Parameters to specify the interval and the number of hours of data to fetch
minute_interval = '15m'  # Interval between data points, e.g., '1m', '5m', '15m', etc.
hours_of_data = 1  # Number of hours of data to fetch from the end of the trading day

# Define your symbol mapping and import sp500_symbols as before
symbol_mapping = {
    'BRK.B': 'BRK-B',
    'BF.B': 'BF-B',
}
sp500_symbols = pd.read_pickle('./pickle/sp500_symbols.pkl')

# Calculate the start time based on the hours_of_data parameter
end_time = datetime.now()  # Assuming script is run after trading hours
start_time = end_time - timedelta(hours=hours_of_data)

# Format the start and end times as strings in 'YYYY-MM-DD HH:MM' format
start_time_str = start_time.strftime('%Y-%m-%d %H:%M')
end_time_str = end_time.strftime('%Y-%m-%d %H:%M')

# Create an empty DataFrame to store the intraday data
intraday_data = pd.DataFrame()

# Loop through each symbol in the S&P 500 list and fetch intraday data
for symbol in sp500_symbols:
    # Apply symbol mapping if necessary
    symbol_to_fetch = symbol_mapping.get(symbol, symbol)

    try:
        # Fetch intraday data within the specified time range
        stock_data = yf.download(symbol_to_fetch, start=start_time_str, end=end_time_str, interval=minute_interval)

        # Check if data is not empty and rename columns
        if not stock_data.empty:
            stock_data = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']].rename(
                columns={'Open': f'{symbol}_Open', 'High': f'{symbol}_High', 'Low': f'{symbol}_Low',
                         'Close': f'{symbol}_Close', 'Volume': f'{symbol}_Volume'})
            # Concatenate the fetched data
            intraday_data = pd.concat([intraday_data, stock_data], axis=1)

    except Exception as e:
        print(f"Error fetching data for {symbol_to_fetch}: {e}")

# Define the directory path and file name for saving
directory = './data'
file_name = os.path.join(directory, f"intraday_data_last_{hours_of_data}_hours_{minute_interval}_min.csv")

# Save the DataFrame to a CSV file
intraday_data.to_csv(file_name)

print(f"Intraday data for the last {hours_of_data} hours saved to {file_name}")