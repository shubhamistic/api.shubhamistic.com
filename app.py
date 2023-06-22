from flask import Flask
from flask_cors import CORS
from os import environ
from sockets.tictactoe.socket import socketio

# import the routes
from routes.tictactoe.index import tictactoe_routes
from routes.shubhamistic.index import shubhamistic_routes


# define the app
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')  # put your secret key here (example: "any random string")
socketio.init_app(app, cors_allowed_origins="*", async_mode='gevent')


# define the routes
app.register_blueprint(tictactoe_routes, url_prefix='/tictactoe')
app.register_blueprint(shubhamistic_routes, url_prefix='/shubhamistic')


@app.route("/")
def landingPage():
    return {
        "message": "Welcome to api.shubhamistic.com!",
        "routes": [
            {
                "/tictactoe": [
                    "/generate-room-code GET",
                    "/join-room POST",
                    "/exit-room POST"
                ]
            },
            {
                "/shubhamistic": [
                    "/projects GET",
                    "/experience GET",
                    "/skills GET",
                    "/achievements GET",
                    "/contact POST"
                ]
            }
        ]
    }


if __name__ == "__main__":
    app.run(debug=True)
    socketio.run(app)
