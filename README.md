# User Services

## Usage

All responses will have the form

'''json
{
	"key":"Mixed type of data"
}
'''

Subsequent response definition will only detail the expected value of the 'data field'

### Create user
**Definition**
**Response**

'''json
{
	"key":"Mixed type of data"
}
'''

### Check password
**Definition**
**Response**

'''json
{
	"key":"Mixed type of data"
}
'''

### Add follower
**Definition**
**Response**

'''json
{
	"key":"Mixed type of data"
}
'''

### Remove follower
**Definition**
'DELETE /users/"username"/"usernameToRemove"'

**Response**
- '404 Not Found' if username or usernameToRemove does not exist
- '204 No Content' on success

'''json
{
	"removed":"True"
}
'''

# Timeline Services
### Get user timeline
**Definition**
'GET /users/"username"/posts'

**Response**
- '404 Not Found' if  user doesn't exist
- '200 OK' on success

'''json
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
**Response**

'''json
{
	"key":"Mixed type of data"
}
'''

### Get home timeline
**Definition**
**Response**

'''json
{
	"key":"Mixed type of data"
}
'''

### Post tweet
**Definition**
**Response**

'''json
{
	"key":"Mixed type of data"
}
'''
