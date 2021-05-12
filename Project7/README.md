# Services
## How to run
Run this command to create 3 instances of timlines and 1 of gateway, users and direct messages

foreman start -m gatewayApi=1,userApi=1,timelineApi=3,dmApi=1

## Message Queueing
For Implementing Message Queueing function, Firstly you need to install an Redis Queue, a message queueing service based on Redis a key-value data store and its libraries.

## Asynchronus Posting
Created a worker function python file which will post a new tweet and will be directly updated on the timeline database file and also analyze the posted tweet by splitting it into words by '#', also gives a range of words and count of words using zrevrange function from the posted tweet.

When using httpie to run the gateway at the end of every request add
--auth  "username:password"

ex: http GET http://localhost:5000/directMessages/chuntttttt --auth "chuntttttt:Password115"

### Usage

All responses will have the form

'''
{
	"key":"Mixed type of data"
}
'''


Subsequent response definition will only detail the expected value of the 'data field'

### Post Tweet
**Definition**
'POST /'

**Arguments**
- '"username":string' a valid username 
- '"post": A tweet posted by users
- '"timestamp":a timestamp to show time and date of messages

**Response**
- '200 Ok' on success
- '500 Internal Server error' on fail 

'''
{
        'sendingUsername': 'bubbly_snowflake',
        'post': 'Dude, I freaken love your music!',
        'time-stamp': '2021-04-14 15:32:11.309128'
}
'''
### Analyze Hashtags

Using Dependency injection function, Create a second queue and then add a second worker function to service that queue. In the route for postTweet enqueue calls to both your database worker function and new background worker function.The second worker function is added to the timeline file to access the previous worker function which was using timeline database and also to use the background services of timeline.
It will identify the words beginning with '#', then count those words in Redis using ZINCRBY and a Sorted Set. 


### Trending 

Adding a route Timelines microservice for the URL /trending which gives a range(0,24) of words by splitting it using hastags and also the count of words (using zrevrange function) 

**Definition**
'GET /trending'

**Arguments**
- posted tweet in the first worker function

**Response**
- '200 OK' on success
- '500 Internal Server error' on fail 

'''
### Accessing the timeline function to get the function running 
Ex: http GET http://localhost:5000/directMessages/trending/username:"chuntttttt"password:Password115" --unsorted

[
    data:[
    		{
        		"#one":1.0,
			"#two":1.0,
			"#three":1.0,
			"#five":2.0,
			"#one":1.0,
			"#two":1.0,
			"#three":1.0,
			"#five":2.0,
		}
	]
]

'''
Use the --unsorted function on the command line to get the range of words in an ascending order.
