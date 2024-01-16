from flask import Blueprint, render_template, request, redirect, url_for

import sys
sys.path.append('./')
from reports.winner_looser import max_increase_stock, min_decrease_stock, max_increase_percentage, min_decrease_percentage


views_bp = Blueprint(__name__, "views")

@views_bp.route("/", methods=["GET", "POST"])
def home():
      if request.method == 'POST':
        selected_option = request.form.get('dropdown')
    
        return redirect(url_for('graph1.display_graph', selected_option=selected_option))

      
   
    
      data_for_dropdown = [f'{max_increase_stock}', 'Option 2', 'Option 3']

      return render_template("index.html", stock1=max_increase_stock, stock2=min_decrease_stock, 
                           change1=f'{max_increase_percentage:.2f}%', change2=f'{min_decrease_percentage:.2f}%',
                           dropdown_data=data_for_dropdown)