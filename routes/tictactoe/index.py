from flask import Blueprint, request, abort
import json
from models.tictactoe import database

# Create a blueprint for /tictactoe/ route
tictactoe_routes = Blueprint('tictactoe', __name__)


# Route for /tictactoe/
@tictactoe_routes.route('/')
def admin():
    # Logic to handle the /tictactoe/ request
    return {
        "message": "Welcome to tictactoe!",
        "routes": ["/generate-room-code GET", "/join-room POST", "/exit-room POST"]
    }


@tictactoe_routes.route('/generate-room-code', methods=['GET'])
def generateRoomCode():
    room = database.findOrCreateEmptyRoom()

    return {
        "message": "Request Successful!",
        "room_code": room["room_code"],
        "token": room["token"]
    }


@tictactoe_routes.route('/join-room', methods=['POST'])
def joinRoom():
    try:
        data = request.get_data().decode('utf-8')
        room_code = int(json.loads(data)['room_code'])

        # check in the database if room code is available or not
        token = database.joinRoom(room_code)
        if token:
            return {
                "message": "Joined Successfully!",
                "room_code": room_code,
                "token": token,
                "fulfilled": True
            }
        else:
            return {
                "message": "Exception: Room unavailable!",
                "room_code": room_code,
                "fulfilled": False
            }

    except ValueError:
        # if wrong input received from the user end
        abort(400, "Wrong data provided, room_code must be of type <int>!")


@tictactoe_routes.route('/exit-room', methods=['POST'])
def exitRoom():
    try:
        data = request.get_data().decode('utf-8')
        room_code = int(json.loads(data)['room_code'])
        token = json.loads(data)['token']

        # if exited successfully, below function will return true otherwise false
        if database.destroySession(room_code, token):
            return {
                "message": "Exited Successfully!",
                "data_received": [room_code, token],
                "fulfilled": True
            }
        else:
            return {
                "message": "Error: Invalid token or room code!",
                "data_received": [room_code, token],
                "fulfilled": False
            }

    except (ValueError, TypeError):
        # if wrong input received from the user end
        abort(400, "Wrong data provided, room_code and token must be of type <int> & <str> respectively!")
