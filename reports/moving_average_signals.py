import pandas as pd

# Load the data
data = pd.read_pickle('./pickle/dummy_processed.pkl')

# Ensure 'Time' column is in datetime format and sort the data
data['Time'] = pd.to_datetime(data['Time'])
data.sort_values(by=['Stock', 'Time'], inplace=True)

# Parameters for moving averages
short_window = 3
long_window = 10

# Calculate moving averages
data['Short_MA'] = data.groupby('Stock')['Close'].transform(lambda x: x.rolling(window=short_window, min_periods=1).mean())
data['Long_MA'] = data.groupby('Stock')['Close'].transform(lambda x: x.rolling(window=long_window, min_periods=1).mean())

# Track previous period's moving averages to help identify crossovers
data['Prev_Short_MA'] = data.groupby('Stock')['Short_MA'].shift(1)
data['Prev_Long_MA'] = data.groupby('Stock')['Long_MA'].shift(1)

# Generate trading signals based on moving average crossovers
data['Signal'] = 0  # Default to no signal
data['Signal'] = data.apply(lambda x: 1 if (x['Short_MA'] > x['Long_MA']) and (x['Prev_Short_MA'] <= x['Prev_Long_MA']) else (-1 if (x['Short_MA'] < x['Long_MA']) and (x['Prev_Short_MA'] >= x['Prev_Long_MA']) else 0), axis=1)

# Calculate the magnitude of the crossover as the absolute difference between short and long MAs
data['Crossover_Magnitude'] = abs(data['Short_MA'] - data['Long_MA'])

# Identify rows where a crossover occurs and exclude '0' signals
crossovers = data[(data['Signal'] != 0) & (data['Signal'] != data['Signal'].shift(1))]

# Sort the crossovers by time (most recent first) and by magnitude (largest magnitude first) to prioritize recent and strong signals
sorted_crossovers = crossovers.sort_values(by=['Time', 'Crossover_Magnitude', 'Signal'], ascending=[False, False, False])

# Select the top N recommendations for display or analysis
top_recommendations = sorted_crossovers.head(20)

# Display the top recommendations
print(top_recommendations[['Time', 'Stock', 'Close', 'Short_MA', 'Long_MA', 'Signal', 'Crossover_Magnitude']])

# Save the top recommendations to a new pickle file for further use or display in a UI
top_recommendations.to_pickle('./pickle/sorted_top_recommendations.pkl')
