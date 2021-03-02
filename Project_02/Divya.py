

from bottle import route, request, get, post, response, static_file, error
import sqlite3
conn = sqlite3.connect('CPSC449-P2.db')

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d 
conn.row_factory=dict_factory
c = conn.cursor()

c.execute('SELECT * FROM users')
users = c.fetchall()


@get("/hello")
def hello():
    msg= {"msg": "hello there"}
    return dict(data=users)

@get("/posts/all")
def getPublicTimeline():
    query= "select username, post, timestamp from user_posts inner join users on user_posts.user_id = users.user_id order by timestamp desc;"
    c.execute(query)
    posts= c.fetchall()
    return dict(data=posts)

@get("/posts/home/<username>")
def getHomeTimeline(username):
    queryGetUserid = f"select * from users where username='{username}';"
    c.execute(queryGetUserid)
    user=c.fetchone()
    print("==============", user["user_id"])
    return username
# Returns recent posts from all users that this user follows.