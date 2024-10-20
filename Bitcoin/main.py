from flask import Flask, render_template_string
import plotly.express as px
import pandas as pd
import requests
import numpy as np

app = Flask(__name__)

# HTML template with enhanced styling, explanations, and hover tooltips
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bitcoin Price & KPI Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f4f8;
        color: #333;
        text-align: center;
        margin: 0;
    }
    h1 {
        color: #4CAF50;
        margin-top: 20px;
    }
    .kpis {
        margin: 20px auto;
        text-align: left;
        display: inline-block;
        background-color: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    .kpis h2 {
        color: #333;
    }
    .kpis ul {
        list-style: none;
        padding: 0;
    }
    .kpis ul li {
        padding: 8px 0;
    }
    .kpis ul li:hover {
        cursor: pointer;
        text-decoration: underline;
    }
    footer {
        margin-top: 50px;
        padding: 20px;
        background-color: #333;
        color: white;
    }

    /* Tooltip container */
    [data-tooltip] {
        position: relative;
        cursor: pointer;
    }

    /* Tooltip text */
    [data-tooltip]::after {
        content: attr(data-tooltip);
        position: absolute;
        background-color: #333;
        color: #fff;
        padding: 5px;
        border-radius: 4px;
        white-space: nowrap;
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.2s;
        transform: translate(-50%, -120%);
    }

    /* Show the tooltip on hover */
    [data-tooltip]:hover::after {
        opacity: 1;
        visibility: visible;
    }
</style>
</head>
<body>
    <h1>Bitcoin Price & Key KPIs (Last 30 Days)</h1>
    
    <!-- KPIs Section -->
    <div class="kpis">
        <h2>Your Key Bitcoin Stats:</h2>
        <ul>
            <li data-tooltip="This is the average price over the past 7 days. It helps smooth out daily price fluctuations.">💰 Last Week’s Average Price: ${{ kpis['MA7'] }}</li>
            <li data-tooltip="This is the average price over the past 30 days. It gives a longer-term view of the trend.">📉 Last Month’s Average Price: ${{ kpis['MA30'] }}</li>
            <li data-tooltip="How much the price has changed in percentage terms over the last 7 days. High change may indicate volatility.">📊 Change in the Last 7 Days: {{ kpis['price_change_7d'] }}%</li>
            <li data-tooltip="How much the price has changed over the last 30 days. Significant changes can be a sign of trends forming.">📈 Change in the Last 30 Days: {{ kpis['price_change_30d'] }}%</li>
            <li data-tooltip="A measure of how much the price has been moving up and down in the last 7 days.">⚡ Volatility (Last 7 Days): {{ kpis['volatility_7d'] }}</li>
            <li data-tooltip="The price's up-and-down movements over the last 30 days.">⚡ Volatility (Last 30 Days): {{ kpis['volatility_30d'] }}</li>
            <li data-tooltip="RSI tells us if the market is overbought (above 70) or oversold (below 30).">📊 RSI Score: {{ kpis['RSI_14'] }}</li>
            <li data-tooltip="How far the current price is from the highest price in the last 30 days.">⬆️ Price vs. 30-Day High: {{ kpis['price_vs_high'] }}%</li>
            <li data-tooltip="How far the current price is from the lowest price in the last 30 days.">⬇️ Price vs. 30-Day Low: {{ kpis['price_vs_low'] }}%</li>
            <li data-tooltip="Momentum compares the current price to the average price over the last 30 days. A high score indicates upward momentum.">🚀 Momentum Score: {{ kpis['momentum_score'] }}%</li>

        </ul>
        <h3>🧠 Final Call: {{ kpis['final_decision'] }} (Confidence: {{ kpis['confidence'] }}%)</h3>
    </div>
    
    <!-- Plot Section -->
    <div id="bitcoin-plot"></div>
    <script type="text/javascript">
        var plotData = {{ plot_data | safe }};
        Plotly.newPlot('bitcoin-plot', plotData.data, plotData.layout);
    </script>
    
    <footer>Keep an eye on Bitcoin and make those smart moves!</footer>
</body>
</html>
"""

# Fetch historical Bitcoin data and calculate moving averages
def get_historical_data(days=30):
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {'vs_currency': 'usd', 'days': days, 'interval': 'daily'}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Calculate 7-day and 30-day moving averages
        df['MA7'] = df['price'].rolling(window=7).mean()
        df['MA30'] = df['price'].rolling(window=30).mean()
        
        # Calculate price changes
        df['price_change'] = df['price'].pct_change() * 100
        
        # Calculate volatility
        df['volatility_7d'] = df['price_change'].rolling(window=7).std()
        df['volatility_30d'] = df['price_change'].rolling(window=30).std()
        
        # Calculate Relative Strength Index (RSI)
        delta = df['price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Calculate and round KPIs for better readability
def calculate_kpis(df):
    current_price = df['price'].iloc[-1]
    kpis = {}
    
    # Moving Averages
    kpis['MA7'] = round(df['MA7'].iloc[-1], 2)
    kpis['MA30'] = round(df['MA30'].iloc[-1], 2)
    
    # Price Change %
    kpis['price_change_7d'] = round((current_price - df['price'].iloc[-7]) / df['price'].iloc[-7] * 100, 2)
    kpis['price_change_30d'] = round((current_price - df['price'].iloc[0]) / df['price'].iloc[0] * 100, 2)
    
    # Volatility
    kpis['volatility_7d'] = round(df['volatility_7d'].iloc[-1], 2)
    kpis['volatility_30d'] = round(df['volatility_30d'].iloc[-1], 2)
    
    # RSI
    kpis['RSI_14'] = round(df['RSI'].iloc[-1], 2)
    
    # Price vs High/Low
    kpis['price_vs_high'] = round((current_price - df['price'].max()) / df['price'].max() * 100, 2)
    kpis['price_vs_low'] = round((current_price - df['price'].min()) / df['price'].min() * 100, 2)
    
    # Momentum Score
    kpis['momentum_score'] = round((current_price - df['MA30'].iloc[-1]) / df['MA30'].iloc[-1] * 100, 2)
    
    # Final Decision
    if kpis['RSI_14'] < 30 and kpis['momentum_score'] > 0:
        kpis['final_decision'] = "Time to Buy!"
        kpis['confidence'] = 80
    elif kpis['RSI_14'] > 70 and kpis['momentum_score'] < 0:
        kpis['final_decision'] = "Better Sell Now!"
        kpis['confidence'] = 80
    else:
        kpis['final_decision'] = "Hold Steady"
        kpis['confidence'] = 50

    return kpis

# Render the KPIs and chart
@app.route('/')
def index():
    df = get_historical_data(30)
    
    if df is None:
        return "Error fetching Bitcoin price data"
    
    # Calculate KPIs
    kpis = calculate_kpis(df)
    
 # Create Plotly figure for price, 7-day moving average, support, and resistance
    support_level = df['price'].min()  # Support is the lowest price
    resistance_level = df['price'].max()  # Resistance is the highest price
    
    fig = px.line(df, x='timestamp', y=['price', 'MA7'], 
                  labels={'value': 'Price (USD)', 'timestamp': 'Date', 'variable': 'Metric'})
    
    # Add Support and Resistance lines
    fig.add_shape(type='line', x0=df['timestamp'].min(), x1=df['timestamp'].max(), 
                  y0=support_level, y1=support_level,
                  line=dict(color='green', dash='dash'), name="Support")
    
    fig.add_shape(type='line', x0=df['timestamp'].min(), x1=df['timestamp'].max(), 
                  y0=resistance_level, y1=resistance_level,
                  line=dict(color='red', dash='dash'), name="Resistance")
    
    fig.update_layout(title="Bitcoin Price with Support and Resistance (Last 30 Days)", 
                      xaxis_title="Date", yaxis_title="Price (USD)")
    
    # Convert the Plotly figure to JSON for rendering
    plot_data = fig.to_json()
    
    # Render the HTML template with KPIs and plot data
    return render_template_string(html_template, kpis=kpis, plot_data=plot_data)

if __name__ == "__main__":
    app.run(debug=True)