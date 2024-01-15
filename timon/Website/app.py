#firts install flask with pip install Flask, plotly with pip install plotly, pandas with pip install pandas

from flask import Flask
from views import views_bp
from graph1 import graph1_bp

#initialize the app
app = Flask(__name__)
app.register_blueprint(views_bp, url_prefix="/")
app.register_blueprint(graph1_bp, url_prefix='/graph1')

#automatically reload the app when code changes
if __name__ == '__main__':
    app.run(debug=True, port=8000)