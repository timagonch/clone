import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from data_fetcher import get_historical_data
from analysis import add_moving_averages, calculate_volatility, calculate_rsi

# Function to display moving averages
def display_moving_averages():
    historical_data = get_historical_data(30)
    historical_data = add_moving_averages(historical_data)
    
    # Plot the moving averages and price
    plt.figure(figsize=(10,6))
    plt.plot(historical_data['timestamp'], historical_data['price'], label='Price')
    plt.plot(historical_data['timestamp'], historical_data['MA7'], label='7-Day MA')
    plt.plot(historical_data['timestamp'], historical_data['MA30'], label='30-Day MA')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title('Bitcoin Price with Moving Averages')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to display RSI analysis
def display_rsi():
    historical_data = get_historical_data(30)
    historical_data = calculate_rsi(historical_data)

    # Plot the RSI
    plt.figure(figsize=(10,6))
    plt.plot(historical_data['timestamp'], historical_data['RSI'], label='RSI', color='purple')
    plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
    plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.title('Bitcoin Relative Strength Index (RSI)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to display volatility
def display_volatility():
    historical_data = get_historical_data(30)
    historical_data = calculate_volatility(historical_data)

    # Plot the volatility
    plt.figure(figsize=(10,6))
    plt.plot(historical_data['timestamp'], historical_data['volatility'], label='Volatility', color='orange')
    plt.xlabel('Date')
    plt.ylabel('Volatility (%)')
    plt.title('Bitcoin Price Volatility')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to suggest buy/sell decisions based on RSI
def buy_sell_suggestion():
    historical_data = get_historical_data(30)
    historical_data = calculate_rsi(historical_data)

    # Get the latest RSI value
    latest_rsi = historical_data['RSI'].iloc[-1]

    # Suggest buy/sell decision based on RSI
    if latest_rsi < 30:
        messagebox.showinfo("Decision", f"RSI is {latest_rsi:.2f}. Suggestion: BUY (RSI < 30)")
    elif latest_rsi > 70:
        messagebox.showinfo("Decision", f"RSI is {latest_rsi:.2f}. Suggestion: SELL (RSI > 70)")
    else:
        messagebox.showinfo("Decision", f"RSI is {latest_rsi:.2f}. Suggestion: HOLD")

# Main GUI window
def create_gui():
    window = tk.Tk()
    window.title("Bitcoin Analysis Dashboard")

    # Add buttons for each analysis
    ma_button = tk.Button(window, text="Moving Averages", command=display_moving_averages, width=25, height=2)
    rsi_button = tk.Button(window, text="RSI Analysis", command=display_rsi, width=25, height=2)
    volatility_button = tk.Button(window, text="Volatility", command=display_volatility, width=25, height=2)
    suggestion_button = tk.Button(window, text="Buy/Sell Suggestion", command=buy_sell_suggestion, width=25, height=2)

    # Place buttons in the window
    ma_button.pack(pady=10)
    rsi_button.pack(pady=10)
    volatility_button.pack(pady=10)
    suggestion_button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_gui()