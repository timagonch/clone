from flask import Flask, render_template
import pandas as pd
import plotly.express as px
from data_fetcher import get_historical_data
from analysis import add_moving_averages, calculate_volatility, calculate_rsi

app = Flask(__name__)

@app.route("/")
def index():
    # Fetch historical data
    historical_data = get_historical_data(30)
    
    # Perform analysis
    historical_data = add_moving_averages(historical_data)
    historical_data = calculate_volatility(historical_data)
    historical_data = calculate_rsi(historical_data)

    # Create a Plotly line chart for Bitcoin price and moving averages
    fig = px.line(historical_data, x="timestamp", y=["price", "MA7", "MA30"], 
                  labels={"value": "Price (USD)", "timestamp": "Date"}, 
                  title="Bitcoin Price with Moving Averages")
    
    # Convert Plotly figure to JSON to pass to the HTML template
    graph_json = fig.to_json()

    # Pass data and graph to the HTML template
    return render_template("index.html", graph_json=graph_json)

if __name__ == "__main__":
    app.run(debug=True)
