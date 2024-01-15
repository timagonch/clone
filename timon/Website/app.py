#firts install flask with pip install Flask, plotly with pip install plotly, pandas with pip install pandas

from flask import Flask
from views import bp

#initialize the app
app = Flask(__name__)
app.register_blueprint(bp, url_prefix="/")

#automatically reload the app when code changes
if __name__ == '__main__':
    app.run(debug=True, port=8000)