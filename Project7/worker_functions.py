import sqlite3
import time
import redis

connTimeline = sqlite3.connect('Project2-timeline.db')
cTimeline = connTimeline.cursor()

redisConn = redis.Redis()


def postTweet(post):
    print("Inside the queue")

    try:
        query=f"INSERT INTO user_posts(username, post, timestamp) VALUES ('{post['username']}', '{post['post']}', '{post['timestamp']}');"
        cTimeline.execute(query)
        connTimeline.commit()
    except Exception as e:
        print(e)


def analyzeHashTags(post):
    splitWords = post.split(" ")

    for word in splitWords:
        if word[0]=="#":
            redisConn.zincrby("hashtags", 1, word)


    print("Inside analyze hashtags")
    
    print(redisConn.zrevrange("hashtags", 0, -1, withscores=True))