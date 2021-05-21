# Services
## Database Creation
Use this command to run the DynamoDB in commandline:
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

Run this command to create the Dynamo database:
Python3 createDmDb.py

## Gateway
Run this comman to create 3 instances of timlines and 1 of gateway, users and direct messages

foreman start -m gatewayApi=1,userApi=1,timelineApi=3,dmApi=1

When using httpie to run the gateway at the end of every request add
--auth  "username:password"

ex: http GET http://localhost:5000/directMessages/chuntttttt --auth "chuntttttt:Password115"

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

**Example command**
http post http://localhost:5000/directMessages to="joey tribiani" from="joey tribiani" message="ddd" quickReplies:='[{"code": "1", "text": "yesss" }]'

Note: code sent should be a string

**Arguments**
- '"dmId": a unique ID for this account
- '"sendingUsername":string' a valid username to send a Message
- '"receivingUsername":string'  a valid username to receive a Message
- '"message":string' a text to send to users
- '"timestamp":a timestamp to show time and date of messages


**Response**
- '200 Ok' on success
- '500 Internal Server error' on fail 

'''
{
	'dmID': 'dm01',
        'sendingUsername': 'bubbly_snowflake',
        'receivingUsername': 'music_viking',
        'message': 'Dude, I freaken love your music!',
        'time-stamp': '2021-04-14 15:32:11.309128',
        'quickReplies' : [
                {
                    "code": "1",
                    "text": "yesss"
                }
            ]
}
'''

### Reply To Direct Messages
**Definition**
'POST /dmId/reply'

command example: http post http://localhost:5000/directMessages/dm136/reply  message:='{"quickReply": true, "text": "1"}' 

inside quickReply= true if its a quick reply code, false if it is just a text message.
Code and text message both will be in the field "text"

**Arguments**
- '"dmId": a unique ID for this account
- '"message":string' a text to send to users
- '"in-reply-to":a reply message to sender's dmId
- '"timestamp":a timestamp to show time and date of messages

**Response**
- '200 Ok' on success
- '500 Internal Server error' on fail 

'''
{
	'dmID': 'reply02',
        'message': ' {
                "quickReply": true,
                "text": "1"
            },
        'in-reply-to': 'dm01',
        'time-stamp': '2021-04-14 16:32:11.309128'
}
'''

### List All Direct Messages
**Definition**
'GET /username'

**Arguments**
- '"username":string' the username of the current user

**Response**
- '200 OK' on success
- '404 Not Found' if username or directMessages does not exist

'''
[
    {
        "dmID": "dm06",
        "message": "Are we doing the podcast tomorrow?",
        "receivingUsername": "arny",
        "sendingUsername": "chuntttttt",
        "time-stamp": "2021-04-15 15:32:11.309128"
    }
]

'''

### List ALL Direct Message Reply
**Definition**
'GET /dmID/reply'

**Response**
- '200 No OK' on success
- '404 Not Found' if username or replies does not exist

'''
[
    {
        "dmID": "reply08",
        "in-reply-to": "dm06",
        "message": "Dont sas me bro!",
        "time-stamp": "2021-04-14 15:32:11.309128"
    },
    {
        "dmID": "reply09",
        "in-reply-to": "dm06",
        "message": "Lets go bro!",
        "time-stamp": "2021-04-14 15:32:11.309128"
    },
    {
        "dmID": "reply07",
        "in-reply-to": "dm06",
        "message": "Why wouldnt we?",
        "time-stamp": "2021-04-14 15:32:11.309128"
    }
]

'''


##Note: Replies are optional, you can reply to a message using yes or no parameter in the auth function, It is separated by the "|" key in the Reply directMessage service. 
