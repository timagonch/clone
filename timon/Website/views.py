from flask import Blueprint, render_template
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

import sys
sys.path.append('./reports')
from reports.winner_looser import max_increase_stock, min_decrease_stock, max_increase_percentage, min_decrease_percentage


pickle_file_path = './pickle/df_long.pkl'
df = pd.read_pickle(pickle_file_path)

csv_file_path = './data/df_long.csv'
df.to_csv(csv_file_path, index=False)

df = pd.read_csv(csv_file_path)

df = df[df['Stock'] == max_increase_stock]

bp = Blueprint(__name__, "views")

@bp.route("/")
def home():
      # Create a box plot
    fig, ax = plt.subplots()
     # Plot lines for each category (High, Low, Middle)
    ax.plot(df['Date'], df['High'], label='High', marker='o')
    ax.plot(df['Date'], df['Low'], label='Low', marker='o')
    ax.plot(df['Date'], df['Close'], label='Close', marker='o')

    # Add labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title(f'Stock: {max_increase_stock} Price Change Over a Month')

    # Add legend
    ax.legend()

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("index.html", stock1=max_increase_stock, stock2=min_decrease_stock, 
                           change1=f'{max_increase_percentage:.2f}%', change2=f'{min_decrease_percentage:.2f}%', plot_url=plot_url)