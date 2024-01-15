from flask import Blueprint, render_template, request
import pandas as pd


import sys
sys.path.append('./reports')
from winner_looser import max_increase_stock, min_decrease_stock, max_increase_percentage, min_decrease_percentage


views_bp = Blueprint(__name__, "views")

@bp.route("/", methods=["GET", "POST"])
def home():
      if request.method == 'POST':
        selected_option = request.form.get('dropdown')
        # Process the selected option, e.g., generate graph data
        # You can redirect to the graph page passing the necessary data
        return render_template('graph1.html', selected_option=selected_option)

      
   
    
    data_for_dropdown = [f'{max_increase_stock}', 'Option 2', 'Option 3']

    return render_template("index.html", stock1=max_increase_stock, stock2=min_decrease_stock, 
                           change1=f'{max_increase_percentage:.2f}%', change2=f'{min_decrease_percentage:.2f}%',
                           dropdown_data=data_for_dropdown)