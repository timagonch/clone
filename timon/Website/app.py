#firts install flask with pip install Flask

from flask import Flask
from views import views

#initialize the app
app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

#automatically reload the app when code changes
if __name__ == '__main__':
    app.run(debug=True, port=8000)