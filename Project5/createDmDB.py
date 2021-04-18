import boto3

# get the service resource
# dynamodb = boto3.resource(
#     'dynamodb',
#     endpoint_url='http://localhost:8000',
#     aws_access_key_id='fakeMyKeyId',
#     aws_secret_access_key='fakeMyKeyId',
#     verify=False)

# Manny's way
dynamodb = boto3.resource(service_name='dynamodb', endpoint_url='http://localhost:8000')

# get the table and delete
table = dynamodb.Table('DirectMessages')
table.delete()

# create the dynamboDB table
try:
    table = dynamodb.create_table(
        TableName = 'DirectMessages',
        KeySchema = [
            {
                'AttributeName':'dmID',
                'KeyType':'HASH'
            }
        ],
        AttributeDefinitions = [
            {
                'AttributeName': 'dmID',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput = {
            'ReadCapacityUnits': 20,
            'WriteCapacityUnits': 20
        }
    )

except Exception as e:
    print(e)
    response.status = 500

# wait until the table exists
table.meta.client.get_waiter('table_exists').wait(TableName='DirectMessages')

# fill test DB
table.put_item(
   Item = {
        'dmID': 'dm01',
        'sendingUsername': 'bubbly_snowflake',
        'receivingUsername': 'music_viking',
        'message': 'Dude, I freaken love your music!',
        'time-stamp': '2021-04-14 15:32:11.309128'
    }
)
table.put_item(
   Item = {
        'dmID': 'reply02',
        'message': 'Thanks, I appreciate it.',
        'in-reply-to': 'dm01',
        'time-stamp': '2021-04-14 16:32:11.309128'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm03',
        'sendingUsername': 'stealtheddefender',
        'receivingUsername': 'rage_quitter1',
        'message': 'Why did you quit?',
        'time-stamp': '2021-04-14 17:32:11.309128'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm04',
        'sendingUsername': 'blaze assault',
        'receivingUsername': 'readingpro',
        'message': 'Hi',
        'time-stamp': '2021-04-14 18:32:11.309128'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm05',
        'sendingUsername': 'need_more_coffee',
        'receivingUsername': 'dravenfact',
        'message': 'Do you like coffee?',
        'time-stamp': '2021-04-15 15:32:11.309128'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm06',
        'sendingUsername': 'chuntttttt',
        'receivingUsername': 'arny',
        'message': 'Are we doing the podcast tomorrow?',
        'time-stamp': '2021-04-15 15:32:11.309128'
    }
)
table.put_item(
   Item = {
        'dmID': 'reply07',
        'message': 'Why wouldnt we?',
        'in-reply-to': 'dm06',
        'time-stamp': '2021-04-14 15:32:11.309128'
    }
)
table.put_item(
   Item = {
        'dmID': 'reply08',
        'message': 'Dont sas me bro!',
        'in-reply-to': 'dm07',
        'time-stamp': '2021-04-14 15:32:11.309128'
    }
)
table.put_item(
   Item = {
        'dmID': 'reply09',
        'message': 'Lets go bro!',
        'in-reply-to': 'dm08',
        'time-stamp': '2021-04-14 15:32:11.309128'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm10',
        'sendingUsername': 'usidor_the_blue',
        'receivingUsername': 'chuntttttt',
        'message': 'STOP FIGHTING!!!',
        'time-stamp': '2021-04-14 15:32:11.309128'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm11',
        'sendingUsername': 'usidor_the_blue',
        'receivingUsername': 'chuntttttt',
        'message': 'STOP FIGHTING!!!',
        'time-stamp': '2021-04-14 15:32:11.309128'
    }
)

# need dynamo client to update table
client = boto3.client(service_name='dynamodb', endpoint_url='http://localhost:8000')


# Create the secondary index
try:
    resp = client.update_table(
        TableName = "DirectMessages",

        AttributeDefinitions = [
            {
                "AttributeName": "in-reply-to",
                "AttributeType": "S"
            },
        ],
        GlobalSecondaryIndexUpdates = [
            {
                "Create": {
                    "IndexName": "DmReplyIndex",
                    "KeySchema": [
                    {
                        "AttributeName": "in-reply-to",
                        "KeyType": "HASH"
                    }
                    ],
                    "Projection":
                    {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput":
                    {
                        "ReadCapacityUnits": 20,
                        "WriteCapacityUnits": 20,
                    }
                }
            }
        ],
    )

except Exception as e:
    print("Error updating table:")
    print(e)
    response.status = 500
# # example of getting an item
# response = table.get_item(
#     Key={
#         'dmID': 'dm01',
#         'sendingUsername': 'Jane'
#     }
# )
# item = response['Item']
# print(item)
#
# # example of deleting item
# table.delete_item(
#     Key={
#         'dmID': 'dm01',
#         'sendingUsername': 'Jane'
#     }
# )
#
