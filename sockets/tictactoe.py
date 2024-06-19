from flask import request
from . import socketio
import random
from models import tictactoe as ttt_db


namespace = '/tictactoe'

# information about which player joined in which room
# syntax:rooms = {room_code: [host request.sid, guest request.sid], ...}
rooms = {}

# information about player
# syntax:info: {room_code: {host :{marker: X or 0}, guest: {marker: X or 0}, board: list[3][3], turn: host or guest, box_filled: 1 to 9}, ...}
info = {}


@socketio.on("connect", namespace=namespace)
def handleConnect():
    pass


@socketio.on("join-room", namespace=namespace)
def handleJoinRoom(data):
    global rooms, info

    room_code = data["room_code"]
    token = data["token"]
    participant_type = data["participant_type"]

    # check if provided room data is valid or not
    if ttt_db.isRoomValid(room_code, token):
        # handle host join event
        if participant_type == "host":
            # assign a marker ("X" or "O") to the player
            marker = "X" if random.randint(0, 1) else "O"

            # add information about the host
            # player with "X" marker will always move first
            ttt_board = [
                [None, None, None],
                [None, None, None],
                [None, None, None]
            ]
            info[room_code] = {
                "board": ttt_board,
                "turn": "host" if marker == "X" else "guest",
                "box_filled": 0,
                "host": {
                    "marker": marker,
                    "sid": request.sid
                },
                "guest": {
                    "marker": "O" if marker == "X" else "X",
                    "sid": None
                }
            }

            # add host to room
            rooms[room_code] = [request.sid, None]
            socketio.emit(
                'host-joined',
                {
                    "message": "Host Joined Successfully!",
                    "marker": marker
                },
                namespace=namespace
            )

        # handle guest join event
        if participant_type == "guest":
            # add guest to room
            rooms[room_code][1] = request.sid

            # add information about the guest
            info[room_code]["guest"]["sid"] = request.sid

            # emit guest joined message to host
            socketio.emit(
                'guest-joined',
                {
                    "message": "Guest Joined Successfully!",
                    "marker": info[room_code]["guest"]["marker"]
                },
                namespace=namespace,
                room=rooms[room_code]
            )

    else:
        # emit the join-failed message
        socketio.emit(
            'error',
            {
                "message": "Error in joining: Invalid room code or token provided!",
                "error_code": 401
            },
            namespace=namespace
        )


@socketio.on("exit-room", namespace=namespace)
def handleExitRoom(data):
    global rooms, info

    room_code = data["room_code"]
    token = data["token"]
    participant_type = data["participant_type"]

    # check if the connected client is allowed to play or not
    if request.sid in rooms[room_code]:
        # delete room data from rooms{}
        rooms.pop(room_code)

        # if the host left the game
        if participant_type == "host":
            # delete the room from info{} and emit guest that host left the game
            socketio.emit(
                'host-left',
                {
                    "message": "host left the game!"
                },
                namespace=namespace,
                room=info.pop(room_code)["guest"]["sid"]
            )

        # if guest left the game
        if participant_type == "guest":
            # delete the room from info{} and emit host that guest left the game
            socketio.emit(
                'guest-left',
                {
                    "message": "guest left the game!"
                },
                namespace=namespace,
                room=info.pop(room_code)["host"]["sid"]
            )


# game execution handler
@socketio.on("place-marker", namespace=namespace)
def placeMarker(data):
    global rooms, info

    room_code = data["room_code"]
    token = data["token"]
    participant_type = data["participant_type"]
    box_id = data["box_id"]

    # check if the connected client is allowed to play or not
    if request.sid in rooms[room_code]:
        room = info[room_code]

        # player with "X" marker will always move first
        # check if the correct participant got the turn
        if participant_type == info[room_code]["turn"]:
            # check if marker is already places there or not
            if room["board"][int(box_id[0])][int(box_id[1])] is not None:
                # cannot place marker as there is already a marker present there
                return

            # box_id: "00" -> [0][0], (box_id is of type <str>)
            room["board"][int(box_id[0])][int(box_id[1])] = room[participant_type]["marker"]
            room["box_filled"] += 1
            socketio.emit(
                'marker-placed',
                {
                    "message": "marker is placed!",
                    "marker": room[participant_type]["marker"],
                    "box_id": box_id
                },
                namespace=namespace,
                room=rooms[room_code]
            )

            # set turn to another player
            room["turn"] = "guest" if participant_type == "host" else "host"

            # check for the winner
            # cover all possible cases
            winner_marker = None
            winning_line = []  # syntax: ["00", "01", "02"]
            if room["board"][0][0] == room["board"][0][1] == room["board"][0][2] is not None:
                winner_marker = room["board"][0][0]
                winning_line = ["00", "01", "02"]
            elif room["board"][1][0] == room["board"][1][1] == room["board"][1][2] is not None:
                winner_marker = room["board"][1][0]
                winning_line = ["10", "11", "12"]
            elif room["board"][2][0] == room["board"][2][1] == room["board"][2][2] is not None:
                winner_marker = room["board"][2][0]
                winning_line = ["20", "21", "22"]
            elif room["board"][0][0] == room["board"][1][0] == room["board"][2][0] is not None:
                winner_marker = room["board"][0][0]
                winning_line = ["00", "10", "20"]
            elif room["board"][0][1] == room["board"][1][1] == room["board"][2][1] is not None:
                winner_marker = room["board"][0][1]
                winning_line = ["01", "11", "21"]
            elif room["board"][0][2] == room["board"][1][2] == room["board"][2][2] is not None:
                winner_marker = room["board"][0][2]
                winning_line = ["02", "12", "22"]
            elif room["board"][0][0] == room["board"][1][1] == room["board"][2][2] is not None:
                winner_marker = room["board"][0][0]
                winning_line = ["00", "11", "22"]
            elif room["board"][0][2] == room["board"][1][1] == room["board"][2][0] is not None:
                winner_marker = room["board"][0][2]
                winning_line = ["02", "11", "20"]

            # check if someone has won or if all box are filled.
            if (winner_marker is not None) or (room["box_filled"] == 9):
                # if the host won
                if winner_marker == room["host"]["marker"]:
                    socketio.emit(
                        'host-won',
                        {
                            "message": "Host Won!",
                            "winning_line": winning_line
                        },
                        namespace=namespace,
                        room=rooms.pop(room_code)
                    )

                # if guest won
                if winner_marker == room["guest"]["marker"]:
                    socketio.emit(
                        'guest-won',
                        {
                            "message": "Guest Won!",
                            "winning_line": winning_line
                        },
                        namespace=namespace,
                        room=rooms.pop(room_code)
                    )

                # if all boxes are filled (match draw)
                if (room["box_filled"] == 9) and (winner_marker is None):
                    socketio.emit(
                        'match-draw',
                        {
                            "message": "Match Draw!"
                        },
                        namespace=namespace,
                        room=rooms.pop(room_code)
                    )

                # delete the room session from a database also
                ttt_db.destroySession(room_code, token)

                # also delete it from the info{}
                info.pop(room_code)


@socketio.on('disconnect', namespace=namespace)
def handle_disconnect():
    global rooms, info

    # search the room code of the client
    for room_code, client_info in rooms.items():
        if request.sid in client_info:
            # if a client gets disconnected than delete the room
            socketio.emit(
                'room-expired',
                {
                    "message": "Room is Expired!"
                },
                namespace=namespace,
                room=rooms.pop(room_code))

            # also delete it from the info{}
            info.pop(room_code)

            break
