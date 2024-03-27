from flask import Flask
from APIs.movie_api import movie_api
from APIs.cinema_api import cinema_api
from APIs.screening_api import screening_api
from APIs.user_api import user_api

app = Flask(__name__)

app.register_blueprint(movie_api)
app.register_blueprint(cinema_api)
app.register_blueprint(screening_api)
app.register_blueprint(user_api)

if __name__ == "__main__":
    app.run(debug=True)
