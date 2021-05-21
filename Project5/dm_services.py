import boto3
from boto3.dynamodb.conditions import Key
from bottle import route, request, get, post, response, static_file, error, delete, Bottle,default_app
import datetime
import json
import logging.config
import random

# app.config.load_config('./etc/gateway.ini')

#  app instance
defaultApp = default_app()
dmApp = Bottle()

# Mount app
defaultApp.mount("/directMessages", dmApp)

# Setting up log
defaultApp.config.load_config('./etc/gateway.ini')
logging.config.fileConfig(defaultApp.config['logging.config'])
logging.debug('DM logging enabled')

# get the service resource
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    aws_access_key_id='fakeMyKeyId',
    aws_secret_access_key='fakeMyKeyId',
    verify=False)

table = dynamodb.Table('DirectMessages')

@dmApp.post('/')
def sendDirectMessage():
    data = request.json

    if not("from" in data) or not("to" in data) or not("message" in data):
        response.status = 500
        return json.dumps({"success": False, "error": "to/from/message cannot be empty"})

    item = {
                'dmID': 'dm'+str(random.randrange(5,1000)),
                'sendingUsername': data["from"],
                'receivingUsername': data["to"],
                'message': { "quickReply": False, "text": data["message"]},
                'time-stamp': str(datetime.datetime.now())
            }
    if "quickReplies" in data:
        item["quickReplies"] = data["quickReplies"]
    try:
        table.put_item(
            Item = item
        )
    except Exception as e:
        response.status = 500
        logging.error(str(e))
        return json.dumps({"success": False, "error": "There was some problem in posting the message"})

    return json.dumps({"success": True, "message": "DM sent successfully"})


@dmApp.post('/<dmId>/reply')
def replyDirectMessage(dmId):
    data = request.json
    # return dict({"data": data})
    if not("message" in data):
        response.status = 500
        return json.dumps({"success": False, "error": "Message cannot be empty"})

    item = {
                'dmID': 'reply'+str(random.randrange(5,1000)),
                'message': data["message"],
                "in-reply-to": dmId,
                'time-stamp': str(datetime.datetime.now())
            }
    if "quickReplies" in data:
        item["quickReplies"] = data["quickReplies"]
    logging.debug(f"the message======{data['message']},ID= {item['dmID']}")

    try:
        table.put_item(
            Item = item
        )
    except Exception as e:
        response.status = 500
        logging.error(str(e))
        return json.dumps({"success": False, "error": "There was some problem in posting the message"})


    return json.dumps({"success": True, "message": "Reply posted successfully"})


@dmApp.get('/<username>')
def getAllDirectMessage(username):
    resp = table.query(
         IndexName='DmIndex',
         KeyConditionExpression=Key('sendingUsername').eq(username)
     )
    items = resp['Items']
    return json.dumps(items)

@dmApp.get('/<dmID>/reply')
def getDirectMessageReply(dmID):
    try:
        # query using dm reply index
        resp = table.query(
            IndexName = "DmReplyIndex",
            KeyConditionExpression = Key('in-reply-to').eq(dmID)
        )

        items = resp['Items']
        return json.dumps(items)
    except Exception as e:
        response.status = 404
        return json.dump({'success': False, 'error':'Replies were not found'})

@dmApp.get('/')
def getAllDirectMessage():
    response1 = table.scan()
    data1 = response1['Items']
    logging.debug(data1)
    return dict({"data":data1})
