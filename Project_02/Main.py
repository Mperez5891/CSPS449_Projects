# Authors: 
# Abhishek Sunil Gujamagdi
# Divya Barsode
# Manuel Perez
#
# Project Description: 
#
# Date: 3/9/2021
#
import sqlite3
import json
from bottle import request, response
from bottle import post, get, put, delete

#app = bottle.default_app()

# User services:
# ========================================================
#def createUser(username, email, password):
# Registers a new user account. Returns true if 
# username is available, email address is valid, 
# and password meets complexity requirements.

#def checkPassword(username, password):
# Returns true if the password parameter matches 
# the password stored for the username.

#def addFollower(username, usernameToFollow):
# Start following a new user.

# Stop following a user.
@delete('/users/<username>/<usernameToRemove>')
def removeFollower(username, usernameToRemove):
    # open DB connection
    try:
        conn = sqlite3.connect('users_services.db')
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
@get('/users/<username>/posts')
def getUserTimeline(username):
    # open DB connection
    try:
        conn = sqlite3.connect('timeline_services.db')
    except sqlite3.OperationalError as e:
        print(e)
    
    c = conn.cursor()
    
    # get all posts for a user
    s = (username,)
    c.execute('SELECT * FROM user_posts WHERE username = ?', s)
    rows = c.fetchall()
        
    # close DB connection
    conn.close()
    
    # create the list of posts
    post_list = []
    for row in rows:
        post_list.append({'post-ID':row[0], 'post': row[2], 'time': row[3]})
    
    # set some headers
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    
    # Returns recent posts from a user in json  
    return json.dumps({'posts': post_list})


#def getPublicTimeline():
#Returns recent posts from all users.

#def getHomeTimeline(username):
# Returns recent posts from all users that this user follows.

#def postTweet(username, text):
# Post a new tweet.
    
if __name__ == '__main__':
    bottle.run(host = '127.0.0.1', port = 8000)
