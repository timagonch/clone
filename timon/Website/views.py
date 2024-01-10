from flask import Blueprint, render_template
from reports.winner_looser import max_increase_stock, min_decrease_stock, max_increase_percentage, min_decrease_percentage


views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html", stock1=max_increase_stock, stock2=min_decrease_stock, 
                           change1=max_increase_percentage, change2=min_decrease_percentage)