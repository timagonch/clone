# main.py

# Import directly, since you're inside the same folder
from data_fetcher import get_historical_data
from analysis import add_moving_averages, calculate_volatility, calculate_rsi

if __name__ == "__main__":
    # Fetch historical data (e.g., last 30 days)
    historical_data = get_historical_data(30)
    
    # Perform analysis
    historical_data = add_moving_averages(historical_data)
    historical_data = calculate_volatility(historical_data)
    historical_data = calculate_rsi(historical_data)

    # Display results (for now, just print the last few rows)
    print(historical_data.tail())