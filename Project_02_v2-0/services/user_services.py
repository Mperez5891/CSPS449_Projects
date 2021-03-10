
import bottle
from bottle import route, request, get, post, response, static_file, error, delete, Bottle,default_app
import datetime
import json
import sqlite3
import re

# create apps 1 and 2
defaultApp=default_app()
userApp = Bottle()

defaultApp.mount("/users", userApp)
#app2.mount('/timeline/', userApp)

# set up DB connection
connUsers = sqlite3.connect('Project2-users.db')


# helper function for Divya
def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d 

connUsers.row_factory=dict_factory
cUsers = connUsers.cursor()


# User Service: 
# ======================================================================================================
        
@userApp.post('/')
def create_users():
    userdata = request.json

    username = userdata["username"]
    email = userdata["email"]
    password = userdata["password"]

    # validate given input
    if username == "":
        return ({"Incorrect": "Enter valid Username!"})

    if password == "" or len(password) < 6:
        return ({"Passowrd is less than 6 characters.": "Enter a strong password!"})

    regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$'
    if email == "" or not re.search(regex, email):
        return json.dumps({"Invalid": "Enter a email in correct format!"})

    try:
        with connUsers:
            cUsers.execute("INSERT into users (username, email, password) values (?,?,?)", (username, email, password))
            connUsers.commit()

    except sqlite3.IntegrityError as ie:
        connUsers.close()
        return ({"UserName already exists!": "Enter different username"})

    except Exception as e:
        connUsers.close()
        return ({"error": "Problem while connecting to database"})

    # Create json object that needs to be returned
    userdata = {
        'username': username,
        'email': email,
        'password': password
    }
    return json.dumps({'userdata': userdata})

@userApp.post('/login')
def checkPassword():
    username = request.json.get('username')
    password = request.json.get('password')
    try:
    	with connUsers:
            # Retrieve user from user table.
            cUsers.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cUsers.fetchone()
            connUsers.commit()
    except Exception as e:
        connUsers.close()
        return ({"error":"Problem while executing query!"})
    if username in user and password(users.get(username),password):
        return json.dumps({"authenticate": True})
    else:
        return json.dumps({"authenticate": False})

@userApp.post('/<username>/followers')
def followers(username):
    # extract values from json
        user_followed = request.json.get("user_followed")
        userdata = {
            'username': username,
            'user_followed': user_followed
        }
        # connect to database
        try:
            with connUsers:
            # Check if user already has this follower
            	cUsers.execute("SELECT * FROM following WHERE username = ? AND user_followed = ?", (username, user_followed))
            	result = cUsers.fetchall()
            if result:
                return json.dumps({'userdata': userdata})
            cUsers.execute('PRAGMA foreign_keys = ON')
            cUsers.execute("INSERT INTO following (username, user_followed) values (?,?)", (username, user_followed))
            cUsers.commit()
        except Exception as e:
            cUsers.rollback()
            cUsers.close()
            return ({"error": "Problem while executing query!"})

        return json.dumps({'userdata': userdata})

# Stop following a user.
@userApp.delete('/<username>/remove/<usernameToRemove>')
def removeFollower(username, usernameToRemove):
    # open DB connection
    try:
        conn = sqlite3.connect('Project2-users.db')
    except sqlite3.OperationalError as e:
        print(e)
    
    c = conn.cursor()
    
    # check if username exists
    try:
        if (validateUser(username)["exists"] != True): 
            raise KeyError
    
    except KeyError:
        response.status = 404
        return {'removed': False, "message": f"User {usernameToRemove} does not exist"}

    # check if username to remove exists
    try:
        if (validateUser(usernameToRemove)["exists"] != True): 
            raise KeyError
    
    except KeyError:
        response.status = 404
        return {'removed': False, "message": f"The follower {usernameToRemove} which you want to remove does not exist"}
    
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
    
# user service helper functions
@userApp.get("/validate/<username>")
def validateUser(username):
    cUsers.execute(f"select * from users where username='{username}';")
    user = cUsers.fetchone()
    if user == None:
        return dict({"exists":False})
    return dict({"exists":True})

@userApp.get("/<username>/followers")
def returnFriendsList(username):
    userExists = validateUser(username)
    if(userExists["exists"] == False):
        response.status = 404
        return dict({"success": False, "message": "User does not exist"})
    cUsers.execute(f"select user_followed from following where username='{username}';")
    followers = cUsers.fetchall()
    if len(followers) == 0 :
        return dict({"followers": 0 , "posts": []})

    followersList=[]
    for follow in followers:
        followersList.append(follow["user_followed"])
        
    return dict({"followers": followersList})

# user service end =====================================================================================
