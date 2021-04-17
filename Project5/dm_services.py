import boto3
from bottle import route, request, get, post, response, static_file, error, delete, Bottle,default_app
import datetime
import json

#  app instance
defaultApp = default_app()
dmApp = Bottle()

# Mount app 
defaultApp.mount("/directMessages", dmApp)

# get the service resource
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',   
    aws_access_key_id='fakeMyKeyId',
    aws_secret_access_key='fakeMyKeyId',
    verify=False)


table = dynamodb.Table('DirectMessages')
response = table.scan()
data = response['Items']

while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])

# print(data)


@dmApp.post('/')
def sendDirectMessage():
    data = request.json
    return json.dumps(data)