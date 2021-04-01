# Services
## Database Creation
Run this command to create the database:
./bin/init.sh

## User Services
### Usage

All responses will have the form

'''
{
	"key":"Mixed type of data"
}
'''


Subsequent response definition will only detail the expected value of the 'data field'

### Create user
**Definition**
'POST /users'

**Arguments**
- '"username":string' a unique name for this account
- '"email":string' a valid email where we will verify the user
- '"password":string' a password that follows our requirments; used to login

**Response**
- '201 Created' on success
- '400 Bad Request' on fail 

'''
{
	"username-created": True
}
'''

### Authenticate User
**Definition**
'POST /users/login'

**Arguments**
- '"username":string' the unique username for this account
- '"password":string' matching password for account to gain access

**Response**
- '200 OK' on success
- '401 Unauthorized login' failed login

'''
{
	"authenticated": True
}
'''

### Add follower
**Definition**
'POST /users/_username_/followers'

**Arguments**
- '"username":string' the username of the current user
- '"user_followed":string' the username of the follower to add

**Response**
- '200 OK' on success
- '404 Not Found' if username or user_followed does not exist

'''
{
	"user-added": True
}
'''

### Remove follower
**Definition**
'DELETE /users/_username_/remove/_usernameToRemove_'

**Response**
- '200 No OK' on success
- '404 Not Found' if username or usernameToRemove does not exist

'''
{
	"removed":"True"
}
'''

# Timeline Services
### Get user timeline
**Definition**
'GET /timeline/_username_'

**Response**
- '200 OK' on success
- '404 Not Found' if  user doesn't exist

'''
{
	"posts": [{
	"post-id": 1,
	"post": "Hi",
	"time": "2021-1-3 09:10:00"
	},
	{
	"post-id": 34,
	"post": "How did I get here?",
	"time": "2021-8-5 12:10:00"
	}]
}
'''

### Get public timeline
**Definition**
'GET /timeline/'

**Response**
- '200 OK' on success
- '404 Not Found' if  user doesn't exist

'''
{
"data": [{
	"post_id": 5, 
	"username": "b.with.photos", 
	"post": "Look at this sweet picture", 
	"timestamp": "2021-1-3 15:10:23"
	}, 
	{
	"post_id": 4, 
	"username": "arny", 
	"post": "Hello from the magic tavern!", 
	"timestamp": "2021-1-3 09:12:54"
	}, 
	{
	"post_id": 3, 
	"username": "usidor_the_blue", 
	"post": "WIZARD OF THE 12TH REALM OF EPHYSIYIES \nMASTER OF LIGHT 	  AND SHADOW MANIPULATOR OF MAGICAL DELIGHTS \nDEVOURER OF CHAOS 	 CHAMPION OF THE GREAT HALLS OF TERRAKKAS\nTHE ELVES KNOW ME AS 	FIANG YALOK THE DWARES KNOW ME AS\nZOENEN HOOGSTANDJES I AM KNOWN 	  IN THE NORTHEAST AS GAISMUENAS MEISTAR\nAND THERE MAY BE OTHER 	 SECRET NAMES YOU DO NOT KNOW YET", 
	"timestamp": "2021-1-3 09:11:50"
	}, 
	{
	"post_id": 2, 
	"username": "chuntttttt", 
	"post": "Awh yea baby!", 
	"timestamp": "2021-1-3 09:10:23"
	}, 
	{
	"post_id": 1, 
	"username": "bubbly_snowflake", 
	"post": "Hello. This is my test post.", 
	"timestamp": "2021-1-3 09:10:00"
	}]
}
'''

### Get home timeline
**Definition**
'GET /timeline/_username_/home'

**Response**
- '200 OK' on success
- '404 Not Found' if user does not exist

'''
{
"followers": 3, 
"posts":
	[{
	"post_id": 10, 
	"username": "need_more_coffee", 
	"post": "...pls", 	   
	"timestamp": "2021-6-3 09:10:00"
	}, 
	{
	"post_id": 9, 
	"username": "need_more_coffee", 
	"post": "Bring me coffee...", 
	"timestamp": "2021-5-3 09:10:00"
	}]
}
'''

### Post tweet
**Definition**
'POST /timeline/_username_

**Arguments**
- '"username":string' the username that is writing the tweet

**Response**
- '201 Created' on success
- '404 Not found' if user does not exist

'''
{
	"posted": True
}
'''

