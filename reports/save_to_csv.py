import pandas as pd

# Import the DataFrame from fetch_data.py
sp500_data = pd.read_pickle('sp500_data.pkl')

# Define the file path where you want to save the CSV file
file_path = '/Users/lilygoncharov/Documents/Z/data/sp500_historical_data.csv'

# Save the DataFrame containing historical data to a CSV file
sp500_data.to_csv(file_path)

print(f"Data saved to {file_path}")