from bottle import route, request, get, post, response, static_file, error, delete
import json
import datetime
import sqlite3
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