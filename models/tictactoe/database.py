import sqlite3
from datetime import datetime, timedelta
import random
import string

# checkout database/__init__.py for more information.
conn = sqlite3.connect('models/tictactoe/database/database.sqlite', check_same_thread=False)
cur = conn.cursor()


# create table rooms
# cur.execute("""
#     CREATE TABLE rooms (
#         room_code INT PRIMARY KEY,
#         start_time DATE,
#         end_time DATE,
#         occupied BOOLEAN DEFAULT FALSE,
#         token TEXT
#     );
# """)
# conn.commit()


# function to find an empty room if available else create an empty room
def findOrCreateEmptyRoom():
    # Get the current date and time
    current_time = datetime.now()

    # Add 30 minutes to the current time
    end_time = current_time + timedelta(minutes=30)

    # fetch the room_code that are expired
    query = """ 
        SELECT room_code
        FROM rooms 
        WHERE (?) > end_time
        LIMIT 1;
    """
    cur.execute(query, (current_time,))
    room_code = cur.fetchone()

    # generating a new token for authentication
    token = str(''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=20)))

    # if no empty room found than creating a new room
    if room_code is None:
        # finding a room_code
        query = """
            SELECT MAX(room_code) FROM rooms;
        """
        cur.execute(query)
        room_code = cur.fetchone()[0] + 1

        query = """
            INSERT OR IGNORE 
            INTO rooms (room_code, start_time, end_time, occupied, token) 
            VALUES (?, ?, ?, ?, ?)
        """
        cur.execute(query, (room_code, current_time, end_time, False, token))
        conn.commit()

    else:
        room_code = room_code[0]

        # updating the room time so that it can be used again
        query = """
            UPDATE rooms
            SET
            start_time = (?),
            end_time = (?),
            occupied = FALSE,
            token = (?)
            WHERE room_code = (?);     
        """
        cur.execute(query, (current_time, end_time, token, room_code))
        conn.commit()

    return {
        "room_code": room_code,
        "token": token
    }


# function to join a player if room is empty otherwise return false
def joinRoom(room_code):
    # Get the current date and time
    current_time = datetime.now()

    # check if room can be joined or not
    query = """ 
        SELECT token
        FROM rooms 
        WHERE room_code = (?) AND (?) < end_time AND occupied = FALSE
        LIMIT 1;
    """
    cur.execute(query, (room_code, current_time))
    token = cur.fetchone()

    if token is None:
        return False
    else:
        # set room occupied to true so that no other player will join the same room
        query = """
            UPDATE rooms
            SET occupied = TRUE
            WHERE room_code = (?);    
        """
        cur.execute(query, (room_code,))
        conn.commit()

        return token[0]


# function to check if room is expired or not
def isRoomValid(room_code, token):
    # Get the current date and time
    current_time = datetime.now()

    # fetch the room_code that are expired
    query = """ 
        SELECT room_code
        FROM rooms 
        WHERE token = (?) AND room_code = (?) AND (?) < end_time
        LIMIT 1;
    """
    cur.execute(query, (token, room_code, current_time))
    res = cur.fetchone()

    if res is None:
        return False

    return True


# function to destroy the room session
def destroySession(room_code, token):
    if isRoomValid(room_code, token):
        # Get the current date and time
        current_time = datetime.now()

        # set the end_time to current time so that the room is treated as free as it is ended
        query = """
                   UPDATE rooms
                   SET
                   end_time = (?),
                   occupied = FALSE
                   WHERE room_code = (?);    
               """
        cur.execute(query, (current_time, room_code))
        conn.commit()

        return True

    # if token or room_code is invalid than return false
    return False
