import pandas as pd
import sys
import pickle
sys.path.append('./parameters')

#import parameters.params as params
from parameters.params import *

# Open the file in binary read mode
with open(sp500_data, 'rb') as file:
    # Load the contents from the file and de-serialize it
    data = pickle.load(file)

# Calculate daily percentage changes for each stock
daily_percentage_changes = data.pct_change().dropna()

# Calculate the standard deviation of daily percentage changes for the last week
volatility_last_week = daily_percentage_changes.std() * 100

# Find the stock with the highest volatility
most_volatile_stock = volatility_last_week.idxmax()
highest_volatility = volatility_last_week[most_volatile_stock]

print(f"The most volatile stock for the specified period: {most_volatile_stock}")
print(f"Volatility (standard deviation of daily % changes): {highest_volatility:.2f}%")