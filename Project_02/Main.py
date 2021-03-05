# Authors: 
# Abhishek Sunil Gujamagdi
# Divya Barsode
# Manuel Perez
#
# Project: 
#
# Date: 3/9/2021
#


from bottle import route, request, get, post, response, static_file, error, delete
import datetime
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

# Timelines service:
# ========================================================
@get('/timeline/<username>')
def getUserTimeline(username):
    # open DB connection
    try:
        conn = sqlite3.connect('Project2-timeline.db')
    except sqlite3.OperationalError as e:
        print(e)
    
    c = conn.cursor()
    
    # check if the username exists
    # open DB connection
    try:
        temp_conn = sqlite3.connect('Project2-users.db')
    except sqlite3.OperationalError as e:
        print(e)
    
    temp_c = temp_conn.cursor()
    
    # get all posts for a user
    s = (username,)
    temp_c.execute(''' SELECT count(username) 
                    FROM users 
                    WHERE username = ?''', s)

    try:
        if temp_c.fetchone()[0] != 1: 
            raise KeyError
    
    except KeyError:
        response.status = 404
        return {'removed': False}
        
    temp_conn.close()
    
    # get all posts for a user
    s = (username,)
    c.execute('SELECT * FROM user_posts WHERE username = ?', s)
    rows = c.fetchall()
    
    # create the list of posts
    post_list = []
    for row in rows:
        post_list.append({'post-ID':row[0], 'post': row[2], 'time': row[3]})
    
    # close DB connection
    conn.close()
    
    # set some headers
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    
    # Returns recent posts from a user in json  
    return json.dumps({'posts': post_list})


@get("/timeline")
def getPublicTimeline():
    #Returns recent posts from all users.
    query= "select * from user_posts order by timestamp desc;"
    cTimeline.execute(query)
    posts= cTimeline.fetchall()
    return dict(data=posts)

@get("/timeline/<username>/home")
def getHomeTimeline(username):
    # Returns recent posts from all users that this user follows.

    cUsers.execute(f"select * from users where username='{username}';")
    user = cUsers.fetchone()
    if user == None :
        return dict({ "error" : f"Username {username} does not exist"})
    
    cUsers.execute(f"select user_followed from following where username='{username}';")
    followers = cUsers.fetchall()
    if len(followers) == 0 :
        return dict({"followers": 0 , "posts": []})

    followersList=[]
    for follow in followers:
        followersList.append(follow["user_followed"])
    
    query= f"select * from user_posts where username in {tuple(followersList)} order by timestamp desc;"
    cTimeline.execute(query)
    posts = cTimeline.fetchall()
    return dict({"followers": len(followers), "posts": posts})

@post("/timeline/<username>")
def postTweet(username):
    # name=request.forms.get("name")
    data=request.json
    post= data["text"]
    timestamp = datetime.datetime.now()
    cUsers.execute(f"select * from users where username='{username}';")
    user = cUsers.fetchone()
    if user == None :
        return dict({ "posted": False ,"error" : f"Username {username} does not exist"})

    query=f"INSERT INTO user_posts(username, post, timestamp) VALUES ('{username}', '{post}', '{timestamp}');"
    cTimeline.execute(query)
    connTimeline.commit()
    return dict({ "posted" : True})

    # Post a new tweet.

@post("/doform")
def doform():
    name=request.forms.get("name")
    return f"saved your name {name}"
