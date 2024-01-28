#firts install flask with pip install Flask, plotly with pip install plotly, pandas with pip install pandas
'''
from flask import Blueprint, render_template, request, redirect, url_for, Flask
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
import pickle
from parse import Parse

Parse.initialize(
    "2f0c8e56-081e-477e-8b44-e455ad8aed8b",
    "https://clone-gpzo2ob6.b4a.run/",
    "20vKMcCsM896RqdfTwl4PElekqbwErio7fRS74VQ"
)

#initialize the app
app = Flask(__name__)


import sys
sys.path.append('./')
from reports.winner_looser import max_increase_stock, min_decrease_stock, max_increase_percentage, min_decrease_percentage


@app.route("/", methods=["GET", "POST"])
def home():
      if request.method == 'POST':
        selected_option = request.form.get('dropdown')
    
        return redirect(url_for('display_graph', selected_option=selected_option))
        #return f'you have selected {selected_option}'
      
   
    
      data_for_dropdown = [f'{max_increase_stock}', 'Option 2', 'Option 3']

      return render_template("index.html", stock1=max_increase_stock, stock2=min_decrease_stock, 
                           change1=f'{max_increase_percentage:.2f}%', change2=f'{min_decrease_percentage:.2f}%',
                           dropdown_data=data_for_dropdown)

@app.route('/display_graph', methods=["GET", "POST"])
def display_graph():
    
    selected_option = request.args.get('selected_option', None)
    if selected_option == f'{max_increase_stock}':
        graph_data = generate_graph1(selected_option)
        return render_template('graph1.html', selected_option=selected_option, graph_data=graph_data)
    #else:
       # return f'you have not selected {selected_option}'

    return redirect(url_for('generate_graph', selected_option=selected_option, graph_data=graph_data))

    

def generate_graph1(pick):
    
    selected_option = request.args.get('selected_option', None)
    with open('./pickle/df_long.pkl', 'rb') as file:
        df = pickle.load(file)
    df = df[df['Stock'] == pick]
    
    fig, ax = plt.subplots()
    # Plot lines for each category (High, Low, Middle)
    ax.plot(df['Date'], df['High'], label='High', marker='o')
    ax.plot(df['Date'], df['Low'], label='Low', marker='o')
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
   
   

#automatically reload the app when code changes
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
    '''
    
from flask import Flask
from parse import Parse

Parse.initialize(
    "2f0c8e56-081e-477e-8b44-e455ad8aed8b",
    "https://clone-gpzo2ob6.b4a.run/",
    "20vKMcCsM896RqdfTwl4PElekqbwErio7fRS74VQ"
)

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, guys!'

if __name__ == '__main__':
    app.run(debug=True)