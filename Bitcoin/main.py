from flask import Flask, render_template_string, jsonify
import plotly.express as px
from data_fetcher import get_historical_data
import traceback  # For detailed error logging

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

    <button onclick="fetchPlotData('price')">Show Bitcoin Prices</button>

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
                        alert(data.message);  // For error messages
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

# Debugging helper function to print detailed errors
def log_error(label, error):
    print(f"--- Error in {label} ---")
    print(error)
    print(traceback.format_exc())

# Basic Price Endpoint
@app.route('/price')
def price():
    try:
        # Fetch historical data (30 days)
        historical_data = get_historical_data(30)
        
        if historical_data is None:
            return jsonify({"message": "No data available for price plot."})
        
        # Log the raw data
        print(f"Fetched Data:\n{historical_data.head()}")

        # Create Plotly chart for the raw price data
        fig = px.line(historical_data, x="timestamp", y="price", 
                      labels={"price": "Price (USD)", "timestamp": "Date"}, 
                      title="Bitcoin Price (Last 30 Days)")
        return jsonify(plot=fig.to_dict())
    except Exception as e:
        log_error("Price Plot", e)
        return jsonify({"message": "Error generating price plot."})

if __name__ == "__main__":
    app.run(debug=True)