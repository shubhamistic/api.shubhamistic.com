from flask import Flask
from flask_cors import CORS
from os import environ
from routes.tictactoe.index import tictactoe_routes
from sockets.tictactoe.socket import socketio


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')  # put your secret key here (example: "any random string")
socketio.init_app(app, cors_allowed_origins="*", async_mode='gevent')


@app.route("/")
def landingPage():
    return {
        "message": "Welcome to api.shubhamistic.com",
        "routes": [
            {
                "/tictactoe": ["/generate-room-code GET", "/join-room POST", "/exit-room POST"]
            }
        ]
    }


# Register the admin_routes with /tictactoe/ URL prefix
app.register_blueprint(tictactoe_routes, url_prefix='/tictactoe')


if __name__ == "__main__":
    app.run()
    socketio.run(app)
