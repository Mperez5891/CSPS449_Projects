import sqlite3
import time
connTimeline = sqlite3.connect('Project2-timeline.db')
cTimeline = connTimeline.cursor()


def postTweet(post):
    print("Inside the queue")

    try:
        query=f"INSERT INTO user_posts(username, post, timestamp) VALUES ('{post['username']}', '{post['post']}', '{post['timestamp']}');"
        cTimeline.execute(query)
        connTimeline.commit()
    except Exception as e:
        print(e)