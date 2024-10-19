from flask import Flask, render_template_string, jsonify
import plotly.express as px
from data_fetcher import get_historical_data
from analysis import add_moving_averages, calculate_volatility, calculate_rsi

app = Flask(__name__)

# HTML template directly embedded in Python
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bitcoin Analysis Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            text-align: center;
        }
        header {
            background-color: #333;
            color: white;
            padding: 10px 0;
            font-size: 24px;
        }
        button {
            margin: 20px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }
        #plot {
            width: 80%;
            margin: 20px auto;
        }
    </style>
    <!-- Plotly JS -->
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <header>Bitcoin Analysis Dashboard</header>

    <button onclick="fetchPlotData('moving_averages')">Moving Averages</button>
    <button onclick="fetchPlotData('rsi')">RSI</button>
    <button onclick="fetchPlotData('volatility')">Volatility</button>
    <button onclick="fetchPlotData('buy_sell')">Buy/Sell Suggestion</button>

    <div id="plot"></div>

    <script type="text/javascript">
        function fetchPlotData(endpoint) {
            fetch('/' + endpoint)
                .then(response => response.json())
                .then(data => {
                    console.log("Received data:", data); // Log data to the console for debugging
                    if (data.plot) {
                        Plotly.newPlot('plot', data.plot.data, data.plot.layout);
                    } else if (data.message) {
                        alert(data.message);  // For buy/sell suggestion
                    } else {
                        alert("No data available for this request.");
                    }
                })
                .catch(error => {
                    console.error("Error fetching data:", error);
                    alert("Error fetching data. Check console for details.");
                });
        }
    </script>
</body>
</html>
"""

# Debugging helper function
def print_debug_info(label, data):
    print(f"--- {label} Data ---")
    if data is None:
        print(f"{label}: No data returned.")
    else:
        print(f"{label} head:\n", data.head())

# Moving Averages Endpoint
@app.route('/moving_averages')
def moving_averages():
    try:
        historical_data = get_historical_data(30)
        print_debug_info("Moving Averages Raw", historical_data)

        if historical_data is None or len(historical_data) < 7:  # Rolling window of 7 requires at least 7 data points
            return jsonify({"message": "Not enough data for moving averages."})
        
        historical_data = add_moving_averages(historical_data)
        print_debug_info("Moving Averages Calculated", historical_data)

        # Create Plotly chart for Moving Averages
        fig = px.line(historical_data, x="timestamp", y=["price", "MA7", "MA30"], 
                      labels={"value": "Price (USD)", "timestamp": "Date"}, 
                      title="Bitcoin Price with Moving Averages")
        return jsonify(plot=fig.to_dict())
    except Exception as e:
        print(f"Error in /moving_averages: {e}")
        return jsonify({"message": "Error generating moving averages plot."})

# RSI Endpoint
@app.route('/rsi')
def rsi():
    try:
        historical_data = get_historical_data(30)
        print_debug_info("RSI Raw", historical_data)

        if historical_data is None or len(historical_data) < 14:  # Rolling window of 14 requires at least 14 data points
            return jsonify({"message": "Not enough data for RSI."})

        historical_data = calculate_rsi(historical_data)
        print_debug_info("RSI Calculated", historical_data)

        # Create Plotly chart for RSI
        fig = px.line(historical_data, x="timestamp", y="RSI", 
                      labels={"RSI": "RSI", "timestamp": "Date"}, 
                      title="Bitcoin Relative Strength Index (RSI)")
        return jsonify(plot=fig.to_dict())
    except Exception as e:
        print(f"Error in /rsi: {e}")
        return jsonify({"message": "Error generating RSI plot."})

# Volatility Endpoint
@app.route('/volatility')
def volatility():
    try:
        historical_data = get_historical_data(30)
        print_debug_info("Volatility Raw", historical_data)

        if historical_data is None or len(historical_data) < 7:  # Volatility calculation requires at least 7 data points
            return jsonify({"message": "Not enough data for volatility."})

        historical_data = calculate_volatility(historical_data)
        print_debug_info("Volatility Calculated", historical_data)

        # Create Plotly chart for Volatility
        fig = px.line(historical_data, x="timestamp", y="volatility", 
                      labels={"volatility": "Volatility (%)", "timestamp": "Date"}, 
                      title="Bitcoin Price Volatility")
        return jsonify(plot=fig.to_dict())
    except Exception as e:
        print(f"Error in /volatility: {e}")
        return jsonify({"message": "Error generating volatility plot."})

# Buy/Sell Suggestion Endpoint
@app.route('/buy_sell')
def buy_sell():
    try:
        historical_data = get_historical_data(30)
        print_debug_info("Buy/Sell Raw", historical_data)

        if historical_data is None:
            return jsonify({"message": "No data available for buy/sell suggestion."})
        
        historical_data = calculate_rsi(historical_data)

        # Get the latest RSI value
        latest_rsi = historical_data['RSI'].iloc[-1]
        if latest_rsi < 30:
            message = f"RSI is {latest_rsi:.2f}. Suggestion: BUY (RSI < 30)"
        elif latest_rsi > 70:
            message = f"RSI is {latest_rsi:.2f}. Suggestion: SELL (RSI > 70)"
        else:
            message = f"RSI is {latest_rsi:.2f}. Suggestion: HOLD"

        return jsonify(message=message)
    except Exception as e:
        print(f"Error in /buy_sell: {e}")
        return jsonify({"message": "Error generating buy/sell suggestion."})

if __name__ == "__main__":
    app.run(debug=True)