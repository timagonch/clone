#firts install flask with pip install Flask, plotly with pip install plotly, pandas with pip install pandas

from flask import Blueprint, render_template, request, redirect, url_for, Flask
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
import pickle

#initialize the app
app = Flask(__name__)

import sys
sys.path.append('./')
from reports.winner_looser import max_increase_stock, min_decrease_stock, max_increase_percentage, min_decrease_percentage

# Get a list of all 500 stocks
with open('./pickle/df_long.pkl', 'rb') as file:
    df_all = pickle.load(file)
    stocks = df_all['Stock'].unique()


@app.route("/", methods=["GET", "POST"])
def home():
      if request.method == 'POST':
        selected_option = request.form.get('dropdown')
    
        return redirect(url_for('display_graph', selected_option=selected_option))
       
      
      data_for_dropdown = [stocks[i] for i in range(0, len(stocks))]

      return render_template("index.html", stock1=max_increase_stock, stock2=min_decrease_stock, 
                           change1=f'{max_increase_percentage:.2f}%', change2=f'{min_decrease_percentage:.2f}%',
                           dropdown_data=data_for_dropdown)

@app.route('/display_graph', methods=["GET", "POST"])
def display_graph():
    
    selected_option = request.args.get('selected_option', None)
    #if selected_option == f'{selected_option}':
    graph_data = generate_graph1(selected_option)
    return render_template('graph1.html', selected_option=selected_option, graph_data=graph_data)
    #else:
       # return f'you have not selected {selected_option}'

    #return redirect(url_for('generate_graph', selected_option=selected_option, graph_data=graph_data))

    

def generate_graph1(pick):
    
    #selected_option = request.args.get('selected_option', None)
    with open('./pickle/df_long.pkl', 'rb') as file:
        df = pickle.load(file)
    df = df[df['Stock'] == pick]
    
    fig, ax = plt.subplots()
    # Plot lines for each category (High, Low, Middle)
    ax.plot(df['Date'], df['Close'], label='Close', marker='o')

    # Add labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title(f'Stock: {pick} Price Change Over a Month')

    # Add legend
    ax.legend()

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return f'<img src="data:image/png;base64,{plot_url}" alt="Line Graph">'

if __name__ == '__main__':
    app.run(host="0.0.0.0', port=8080")

