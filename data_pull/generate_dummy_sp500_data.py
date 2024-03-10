import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load symbols from the pickle file
sp500_symbols = pd.read_pickle('./pickle/sp500_symbols.pkl')

# Parameters for dummy data generation
hours_of_data = 5  # Number of hours of data to generate
interval_minutes = 15  # Interval in minutes
data_points = int((60 / interval_minutes) * hours_of_data)  # Calculate total data points

# Generate a date range for the timestamps
end_time = datetime.now().replace(second=0, microsecond=0)
start_time = end_time - timedelta(hours=hours_of_data)
timestamps = pd.date_range(start=start_time, end=end_time, periods=data_points)

# Initialize an empty DataFrame to store dummy data
dummy_data = pd.DataFrame(index=timestamps)

# Function to generate random price data
def generate_price_data(start_price=100, percent_change=0.10, n=data_points):
    prices = [start_price]
    for _ in range(n - 1):
        change_percent = np.random.uniform(-percent_change, percent_change)
        prices.append(prices[-1] * (1 + change_percent))
    return prices

# Generate dummy data for each symbol
for symbol in sp500_symbols:
    open_prices = generate_price_data()
    close_prices = generate_price_data(start_price=open_prices[-1])  # Ensure continuity
    high_prices = [max(open_price, close_price) * np.random.uniform(1.0, 1.1) for open_price, close_price in zip(open_prices, close_prices)]
    low_prices = [min(open_price, close_price) * np.random.uniform(0.9, 1.0) for open_price, close_price in zip(open_prices, close_prices)]
    volumes = [np.random.randint(100000, 1000000) for _ in range(data_points)]

    # Combine the generated data into a DataFrame
    symbol_data = pd.DataFrame({
        f'{symbol}_Open': open_prices,
        f'{symbol}_High': high_prices,
        f'{symbol}_Low': low_prices,
        f'{symbol}_Close': close_prices,
        f'{symbol}_Volume': volumes
    }, index=timestamps)

    # Concatenate with the main DataFrame
    dummy_data = pd.concat([dummy_data, symbol_data], axis=1)

# Display the first few rows of the dummy data
print(dummy_data.head())

# Pickle the DataFrame
dummy_data.to_pickle('./pickle/dummy_intraday_data.pkl')

# Save the dummy data to CSV for later use
dummy_data.to_csv('./data/dummy_intraday_data.csv')
