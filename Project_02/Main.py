# Authors: 
# Abhishek Sunil Gujamagdi
# Divya Barsode
# Manuel Perez
#
# Project description: 
#
# Date: 3/9/2021
#

# User services:
# ========================================================
def createUser(username, email, password):
# Registers a new user account. Returns true if 
# username is available, email address is valid, 
# and password meets complexity requirements.

def checkPassword(username, password):
# Returns true if the password parameter matches 
# the password stored for the username.

def addFollower(username, usernameToFollow):
# Start following a new user.

def removeFollower(username, usernameToRemove):
# Stop following a user.

# Timelines service:
# ========================================================
def getUserTimeline(username):
# Returns recent posts from a user.

def getPublicTimeline():
#Returns recent posts from all users.

def getHomeTimeline(username):
# Returns recent posts from all users that this user follows.

def postTweet(username, text):
# Post a new tweet.

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()
