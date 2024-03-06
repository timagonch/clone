#firts install flask with pip install Flask, plotly with pip install plotly, pandas with pip install pandas

from flask import Blueprint, render_template, request, redirect, url_for, Flask
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
import pickle
from datetime import datetime 

#initialize the app
app = Flask(__name__)

import sys
sys.path.append('./')
from reports.winner_looser import max_increase_stock, min_decrease_stock, max_increase_percentage, min_decrease_percentage

# Get a list of all 500 stocks
with open('./pickle/df_long.pkl', 'rb') as file:
    df_all = pickle.load(file)
    stocks = df_all['Stock'].unique()
    # Find the yearliest date in the data
    update = df_all['Date'].max()
    last_update = update.strftime("%m/%d/%Y")
    


@app.route("/", methods=["GET", "POST"])
def home():
      if request.method == 'POST':
        selected_option = request.form.get('dropdown')
    
        return redirect(url_for('display_graph', selected_option=selected_option))
       
      
      data_for_dropdown = [stocks[i] for i in range(0, len(stocks))]
      graph1= generate_graph1(max_increase_stock,6,4)
      graph2= generate_graph1(min_decrease_stock,6,4)

      return render_template("index.html", graph1=graph1, graph2=graph2,stock1=max_increase_stock, stock2=min_decrease_stock, 
                           change1=f'{max_increase_percentage:.2f}%', change2=f'{min_decrease_percentage:.2f}%',
                           dropdown_data=data_for_dropdown, last_update=last_update)

@app.route('/display_graph', methods=["GET", "POST"])
def display_graph():
    
    selected_option = request.args.get('selected_option', None)
    #if selected_option == f'{selected_option}':
    graph_data = generate_graph1(selected_option,10,8)
    return render_template('graph1.html', selected_option=selected_option, graph_data=graph_data, last_update=last_update)
 
    

def generate_graph1(pick, h,w):
    
    #selected_option = request.args.get('selected_option', None)
    with open('./pickle/df_long.pkl', 'rb') as file:
        df = pickle.load(file)
    df = df[df['Stock'] == pick]

    fig, ax = plt.subplots()

    # Plot lines with custom styling
    ax.plot(df['Date'], df['Close'], label='Close', linestyle='-', color='blue', marker='o', markersize=8, linewidth=2)

    # Customize background and grid
    ax.grid(True)
    ax.set_facecolor('#f0f0f0')  # Set a light gray background color

    # Customize title and labels
    ax.set_xlabel('Date', fontsize=10)
    ax.set_ylabel('Price', fontsize=10)
    ax.set_title(f'Price of - {pick}', fontsize=20, fontweight='bold')

    # Customize legend
    ax.legend(loc='upper left', fontsize=10)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Creating a secondary y-axis for volume
    ax2 = ax.twinx()
    ax2.bar(df['Date'], df['Volume'], color='gray', alpha=0.3)
    ax2.set_ylabel('Volume')

    # Adjust figure size
    fig.set_size_inches(h, w)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return f'<img src="data:image/png;base64,{plot_url}" alt="Line Graph">'


if __name__ == '__main__':
    app.run(host="0.0.0.0', port=8080")

