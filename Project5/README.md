# Services
## Database Creation
Run this command to create the Dynamo database:
Python3 createDmDb.py

Use this command to run the DynamoDB in commandline:
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

## Gateway
Run this comman to create 3 instances of timlines and 1 of gateway, users and direct messages

foreman start -m gatewayApi=1,userApi=1,timelineApi=3,dmApi=1


## Direct Messaging Services
### Usage

All responses will have the form

'''
{
	"key":"Mixed type of data"
}
'''


Subsequent response definition will only detail the expected value of the 'data field'

### Send Direct Message service
**Definition**
'POST /'

**Arguments**
- '"dmId": a unique ID for this account
- '"sendingUsername":string' a valid username to send a Message
- '"receivingUsername":string'  a valid username to receive a Message
- '"message":string' a text to send to users
- '"timestamp":a timestamp to show time and date of messages

**Response**
- '200 Ok' on success
- '500 Server error' on fail 

'''
{
	'dmID': 'dm01',
        'sendingUsername': 'bubbly_snowflake',
        'receivingUsername': 'music_viking',
        'message': 'Dude, I freaken love your music!',
        'time-stamp': '2021-04-14 15:32:11.309128'
}
'''

### Reply To Direct Messages
**Definition**
'POST /<dmId>/reply'

**Arguments**
- '"dmId": a unique ID for this account
- '"message":string' a text to send to users
- '"in-reply-to":a reply message to sender's dmId
- '"timestamp":a timestamp to show time and date of messages

**Response**
- '200 Ok' on success
- '500 Server error' on fail 

'''
{
	'dmID': 'reply02',
        'message': 'Thanks, I appreciate it.',
        'in-reply-to': 'dm01',
        'time-stamp': '2021-04-14 16:32:11.309128'
}
'''

### List All Direct Messages
**Definition**
'GET /<username>'

**Arguments**
- '"username":string' the username of the current user

**Response**
- '200 OK' on success
- '404 Not Found' if username or directMessages does not exist

'''
{
	'dmID': 'dm01',
        'sendingUsername': 'bubbly_snowflake',
        'receivingUsername': 'music_viking',
        'message': 'Dude, I freaken love your music!',
        'time-stamp': '2021-04-14 15:32:11.309128'
}
'''

### List ALL Direct Message Reply
**Definition**
'GET /<dmID>/reply'

**Response**
- '200 No OK' on success
- '404 Not Found' if username or replies does not exist

'''
{	'dmID': 'dm01',
        'sendingUsername': 'bubbly_snowflake',
        'receivingUsername': 'music_viking',
        'message': 'Dude, I freaken love your music!',
        'time-stamp': '2021-04-14 15:32:11.309128'
}
'''


###Note: Replies are optional, you can reply to a message using yes or no parameter in the auth function, It is separated by the "|" key in the Reply directMessage service. 
