
import bottle
from bottle import route, request, get, post, response, static_file, error, delete, Bottle,default_app
import datetime
import json
import sqlite3
import requests
# import services.user_services as userService


#  app instance
defaultApp = default_app()
timelineApp = Bottle()

# Mount app 
defaultApp.mount("/timeline", timelineApp)

timelineApp.config.load_config('./etc/microservice.ini')
# Allow JSON values to be loaded from app.config[key]
#
def json_config(key):
    value = timelineApp.config[key]
    return json.loads(value)

dbserver = json_config('dbserver.dblinks')

# set up DB connection--------------------------------------------
connTimeline = sqlite3.connect(dbserver["timeline"])

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
        response.status = 500
        return json.dumps({"success": False, "message": "Some problem occured while accessing the database"})
    
    c = conn.cursor()
    
    # check if username to remove exists
    # try:
    #     if (userService.validateUser(username)["exists"] != True): 
    #         raise KeyError
    
    # except KeyError:
    #     response.status = 404
    #     return {'user': 'Does Not exist'}
    
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
    try:
        cTimeline.execute(query)
        posts= cTimeline.fetchall()
    except Exception as e:
        response.status = 500
        return json.dumps({"success": False, "message": "Some problem occured while accessing the database"})
    return dict(posts=posts)

@timelineApp.get("/<username>/home")
def getHomeTimeline(username):
    # follow=request.query_string
    foll=request.GET.get('followers', '').strip()
    if len(foll)==0:
        return dict({"success": False, "message": "No followers sent", "followers": 0,"post": []})

    followersList1=foll.split(",")
    # Returns recent posts from all users that this user follows.

    # userExist= userService.validateUser(username)
    # if userExist["exists"] == False:
    #     response.status = 404
    #     return dict({ "error" : f"Username {username} does not exist"})
    
    # followersList1=userService.returnFriendsList(username)["followers"]
    


    query=""
    if len(followersList1) > 1:
        query= f"select * from user_posts where username in {tuple(followersList1)} order by timestamp desc;"
    else:
        query= f"select * from user_posts where username='{followersList1[0]}' order by timestamp desc;"

    try:
        cTimeline.execute(query)
        posts = cTimeline.fetchall()
    except Exception as e:
        response.status = 500
        return json.dumps({"success": False, "message": "Some problem occured while accessing the database"})

    return dict({"success": True,"followers": len(followersList1), "posts": posts})

@timelineApp.post("/<username>")
def postTweet(username):
    # name=request.forms.get("name")
    data=request.json
    try:
        post= data["text"]
    except:
        response.status = 422
        return dict({ "success" : False, "message" : "No text sent"})
    timestamp = datetime.datetime.now()
    # userExist= userService.validateUser(username)
    # if userExist["exists"] == False:
    #     response.status = 404
    #     return dict({ "error" : f"Username {username} does not exist"})
    try:
        query=f"INSERT INTO user_posts(username, post, timestamp) VALUES ('{username}', '{post}', '{timestamp}');"
        cTimeline.execute(query)
        connTimeline.commit()
    except Exception as e:
        response.status = 500
        return json.dumps({"success": False, "message": "Some problem occured while adding in database"})
    return dict({ "success" : True})

    # Post a new tweet.



