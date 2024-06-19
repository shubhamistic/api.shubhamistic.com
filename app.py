from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
from os import environ
from sockets.tictactoe import socketio
# import the routes
from routes.tictactoe import tictactoe_routes


app = Flask(__name__)

# configure secret key
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

# configure MySQL
app.config['MYSQL_USER'] = environ.get('DB_USER')
app.config['MYSQL_PASSWORD'] = environ.get('DB_PASS')
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_DB'] = "tictactoe"

# define extensions
CORS(app)  # cors
socketio.init_app(app, cors_allowed_origins="*", async_mode='gevent')  # socket
mysql = MySQL(app)  # MySQL

# define the routes
app.register_blueprint(tictactoe_routes, url_prefix='/tictactoe')


@app.route("/")
def index():
    return {
        "message": "Welcome to api.shubhamistic.com!",
        "routes": [{
            "/tictactoe": [
                "/generate-room-code [GET]",
                "/join-room [POST]",
                "/exit-room [POST]"
            ]
        }]
    }


if __name__ == "__main__":
    app.run(port=5000)
    socketio.run(app)
