from datetime import datetime, timedelta
import random
import string
from . import get_db


# function to find an empty room if available else create an empty room
def findOrCreateEmptyRoom():
    # initialize cursor
    db = get_db()
    cursor = db.connection.cursor()

    # Get the current date and time
    current_time = datetime.now()

    # Add 30 minutes to the current time
    end_time = current_time + timedelta(minutes=30)

    # fetch the room_code that are expired
    query = """ 
        SELECT room_code
        FROM rooms 
        WHERE (%s) > end_time
        LIMIT 1;
    """
    cursor.execute(query, (current_time,))
    room_code = cursor.fetchone()

    # generating a new token for authentication
    token = str(''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=20)))

    # if no empty room found than creating a new room
    if room_code is None:
        # finding a room_code
        query = """
            SELECT MAX(room_code) FROM rooms;
        """
        cursor.execute(query)
        room_code = cursor.fetchone()[0] + 1

        query = """
            INSERT IGNORE INTO
            rooms (room_code, start_time, end_time, occupied, token) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (room_code, current_time, end_time, False, token))
        db.connection.commit()

    else:
        room_code = room_code[0]

        # updating the room time so that it can be used again
        query = """
            UPDATE rooms
            SET
            start_time = (%s),
            end_time = (%s),
            occupied = FALSE,
            token = (%s)
            WHERE room_code = (%s);     
        """
        cursor.execute(query, (current_time, end_time, token, room_code))
        db.connection.commit()

    return {
        "room_code": room_code,
        "token": token
    }


# function to join a player if room is empty otherwise returns false
def joinRoom(room_code):
    # initialize cursor
    db = get_db()
    cursor = db.connection.cursor()

    # Get the current date and time
    current_time = datetime.now()

    # check if room can be joined or not
    query = """ 
        SELECT token
        FROM rooms 
        WHERE room_code = (%s) AND (%s) < end_time AND occupied = FALSE
        LIMIT 1;
    """
    cursor.execute(query, (room_code, current_time))
    token = cursor.fetchone()

    if token is None:
        return False
    else:
        # set room occupied to true so that no other player will join the same room
        query = """
            UPDATE rooms
            SET occupied = TRUE
            WHERE room_code = (%s);    
        """
        cursor.execute(query, (room_code,))
        db.connection.commit()

        return token[0]


# function to check if room is expired or not
def isRoomValid(room_code, token):
    # initialize cursor
    db = get_db()
    cursor = db.connection.cursor()

    # Get the current date and time
    current_time = datetime.now()

    # fetch the room_code that are expired
    query = """ 
        SELECT room_code
        FROM rooms 
        WHERE token = (%s) AND room_code = (%s) AND (%s) < end_time
        LIMIT 1;
    """
    cursor.execute(query, (token, room_code, current_time))
    res = cursor.fetchone()

    if res is None:
        return False

    return True


# function to destroy the room session
def destroySession(room_code, token):
    if isRoomValid(room_code, token):
        # initialize cursor
        db = get_db()
        cursor = db.connection.cursor()

        # Get the current date and time
        current_time = datetime.now()

        # set the end_time to current time so that the room is treated as free as it is ended
        query = """
            UPDATE rooms
            SET
            end_time = (%s),
            occupied = FALSE
            WHERE room_code = (%s);    
        """
        cursor.execute(query, (current_time, room_code))
        db.connection.commit()

        return True

    # if token or room_code is invalid than return false
    return False
