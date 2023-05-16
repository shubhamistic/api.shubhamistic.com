from flask import Flask
from flask_cors import CORS
from routes.tictactoe.index import tictactoe_routes
from sockets.tictactoe.socket import socketio
from config.tictactoe.config import SECRET_KEY


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = SECRET_KEY  # put your secret key here (example: "any random string")
socketio.init_app(app, cors_allowed_origins="*", async_mode='gevent')


@app.route("/")
def landingPage():
    return {
        "message": "Welcome to api.shubhamistic.com",
        "routes": [
            {
                "/tictactoe": ["/generate-room-code", "/join-room", "/exit-room"]
            }
        ]
    }


# Register the admin_routes with /tictactoe/ URL prefix
app.register_blueprint(tictactoe_routes, url_prefix='/tictactoe')


if __name__ == "__main__":
    app.run()
    socketio.run(app)
