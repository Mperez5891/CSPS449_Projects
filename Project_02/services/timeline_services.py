
import bottle
from bottle import route, request, get, post, response, static_file, error, delete, Bottle,default_app
import datetime
import json
import sqlite3
import requests
import services.user_services as userService


#  app instance

defaultApp = default_app()
timelineApp = Bottle()

# Mount app 
defaultApp.mount("/timeline", timelineApp)

# set up DB connection--------------------------------------------
connTimeline = sqlite3.connect('Project2-timeline.db')

# helper function for Divya
def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d 

connTimeline.row_factory=dict_factory
cTimeline = connTimeline.cursor()

# Timelines service:
# ======================================================================================================

@timelineApp.get('/<username>')
def getUserTimeline(username):
    # open DB connection
    try:
        conn = sqlite3.connect('Project2-timeline.db')
    except sqlite3.OperationalError as e:
        print(e)
    
    c = conn.cursor()
    
    # check if username to remove exists
    try:
        if (userService.validateUser(usernameToRemove)["exists"] != True): 
            raise KeyError
    
    except KeyError:
        response.status = 404
        return {'user': 'Does Not exist'}
    
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


@timelineApp.get("/")
def getPublicTimeline():
    #Returns recent posts from all users.
    query= "select * from user_posts order by timestamp desc;"
    cTimeline.execute(query)
    posts= cTimeline.fetchall()
    return dict(data=posts)

@timelineApp.get("/<username>/home")
def getHomeTimeline(username):
    # Returns recent posts from all users that this user follows.

    userExist= userService.validateUser(username)
    if userExist["exists"] == False:
        response.status = 404
        return dict({ "error" : f"Username {username} does not exist"})
    
    followersList1=userService.returnFriendsList(username)["followers"]
   
    if len(followersList1) == 0 :
        return dict({"follows": 0 , "posts": []})


    query= f"select * from user_posts where username in {tuple(followersList1)} order by timestamp desc;"
    cTimeline.execute(query)
    posts = cTimeline.fetchall()
    return dict({"followers": len(followersList1), "posts": posts})

@timelineApp.post("/<username>")
def postTweet(username):
    # name=request.forms.get("name")
    data=request.json
    post= data["text"]
    timestamp = datetime.datetime.now()
    userExist= userService.validateUser(username)
    if userExist["exists"] == False:
        response.status = 404
        return dict({ "error" : f"Username {username} does not exist"})
    query=f"INSERT INTO user_posts(username, post, timestamp) VALUES ('{username}', '{post}', '{timestamp}');"
    cTimeline.execute(query)
    connTimeline.commit()
    return dict({ "posted" : True})

    # Post a new tweet.



