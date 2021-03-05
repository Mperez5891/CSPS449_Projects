from bottle import route, request, get, post, response, static_file, error, delete
import json
import sqlite3
import re

connUsers = sqlite3.connect('Project2-users.db')
connTimeline = sqlite3.connect('Project2-timeline.db')
cUsers = connUsers.cursor()

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d 

connUsers.row_factory=dict_factory
cUsers = connUsers.cursor()

connTimeline.row_factory=dict_factory
cTimeline = connTimeline.cursor()

@post('/users/')
def create_users():
    data = request.json

    username = request.get("username")
    email = request.get("email")
    password = request.get("password")

    # validate given input
    if username == "":
        return f"Enter valid Username!"

    if password == "" or len(password) < 6:
        return f"Passowrd is less than 6 characters. Enter a strong password!"

    regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$'
    if email == "" or not re.search(regex, email):
        return f"Enter a email in correct format!"
    try:
        with connUsers:
            cUsers.execute("INSERT into user (username, email, password) values (?,?,?)", (username, email, password))
            connUsers.commit()
            
    except sqlite3.IntegrityError as ie:
        connUsers.rollback()
        connUsers.close()
        return f"UserName already exists!"
    
    except Exception as e:
        connUsers.rollback()
        connUsers.close()
        return f"Problem while connecting to database"
    
    # Create json object that needs to be returned
    userdata = {
        'username': username,
        'email': email,
        'password': password
    }
    return json.dumps(userdata)


@post('/users/login')
def checkPassword():
    username = request.json.get('username')
    password = request.json.get('password')
    try:
        with connUsers:
            # Retrieve user from user table.
            cUsers.execute("SELECT * FROM user WHERE username = ?", (username,))
            user = cUsers.fetchone()
            connUsers.commit()
    except Exception as e:
        connUsers.rollback()
        connUsers.close()
        return f"Problem while executing query!"

    if user and check_password_hash(user[1], password):
        return f"Login successful!"
    else:
        return f"Unauthorized Login!"

@post('/users/addFollower')
def followers():
    # extract values from json
    username = request.json.get("username")
    user_followed = request.json.get("user_followed")
    userdata = {
        'username': username,
        'user_followed': user_followed
    }
    # connect to databse
    try:
        with connUsers:
            # Check if user already has this follower
            cUsers.execute("SELECT * FROM following WHERE username = ? AND user_followed = ?",
                           (username, user_followed))
            result = cUsers.fetchall()
            if result:
                return json.dumps(userdata)
            cUsers.execute('pragma foreign_keys = ON')
            cUsers.execute("INSERT into followers (username, user_followed) values (?,?)", (username,
                                                                                            usernameToFollow))
            cUsers.commit()
    except Exception as e:
        cUsers.rollback()
        cUsers.close()
        return json.dumps("Problem while executing query!")

    return json.dumps(userdata)

# Stop following a user.
@delete('/users/<username>/<usernameToRemove>')
def removeFollower(username, usernameToRemove):
    # open DB connection
    try:
        conn = sqlite3.connect('Project2-users.db')
    except sqlite3.OperationalError as e:
        print(e)
    
    c = conn.cursor()
    
    # check if username exists
    s = (username,)
    c.execute(''' SELECT count(username) 
                    FROM users 
                    WHERE username = ?''', s)

    try:
        if c.fetchone()[0] != 1: 
            raise KeyError
    
    except KeyError:
        response.status = 404
        return {'removed': False}

    # check if username to remove exists
    s = (usernameToRemove,)
    c.execute(''' SELECT count(username) 
                    FROM users 
                    WHERE username = ?''', s)

    try:
        if c.fetchone()[0] != 1: 
            raise KeyError
    
    except KeyError:
        response.status = 404
        return {'removed': False}
    
    # remove user
    s = (username, usernameToRemove)
    c.execute('''DELETE FROM following 
                WHERE username = ? 
                AND user_followed = ?''', s)
    
    # commit
    conn.commit()
    
    # close DB connection
    conn.close()
    
    return {'removed': True}
