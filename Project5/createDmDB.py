import boto3

# get the service resource
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',   
    aws_access_key_id='fakeMyKeyId',
    aws_secret_access_key='fakeMyKeyId',
    verify=False)

# get the table and delete
table = dynamodb.Table('DirectMessages')
table.delete()

# create the dynamboDB table
table = dynamodb.create_table(
    TableName = 'DirectMessages',
    KeySchema = [
        {
            'AttributeName':'dmID',
            'KeyType':'HASH'
        },
        {
            'AttributeName':'sendingUsername',
            'KeyType':'RANGE'
        }
    ],
    AttributeDefinitions = [
        {
            'AttributeName': 'dmID',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'sendingUsername',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput = {
        'ReadCapacityUnits': 20,
        'WriteCapacityUnits': 20
    }
)

# wait until the table exists
table.meta.client.get_waiter('table_exists').wait(TableName='DirectMessages')

# fill test DB
table.put_item(
   Item = {
        'dmID': 'dm01',
        'sendingUsername': 'bubbly_snowflake',
        'receivingUsername': 'music_viking',
        'message': 'Dude, I freaken love your music!',
        'time-stamp': '2021-01-23T20:18:29Z'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm02',
        'sendingUsername': 'music_viking',
        'receivingUsername': 'bubbly_snowflake',
        'message': 'Thanks, I appreciate it.',
        'in-reply-to': 'dm01',
        'time-stamp': '2021-01-23T20:19:00Z'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm03',
        'sendingUsername': 'stealtheddefender',
        'receivingUsername': 'rage_quitter1',
        'message': 'Why did you quit?',
        'time-stamp': '2021-01-24T20:19:00Z'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm04',
        'sendingUsername': 'blaze assault',
        'receivingUsername': 'readingpro',
        'message': 'Hi',
        'time-stamp': '2021-02-09T08:18:29Z'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm05',
        'sendingUsername': 'need_more_coffee',
        'receivingUsername': 'dravenfact',
        'message': 'Do you like coffee?',
        'time-stamp': '2021-02-10T03:18:55Z'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm06',
        'sendingUsername': 'chuntttttt',
        'receivingUsername': 'arny',
        'message': 'Are we doing the podcast tomorrow?',
        'time-stamp': '2021-04-23T20:18:29Z'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm07',
        'sendingUsername': 'arny',
        'receivingUsername': 'chuntttttt',
        'message': 'Why wouldnt we?',
        'in-reply-to': 'dm06',
        'time-stamp': '2021-04-23T20:18:29Z'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm08',
        'sendingUsername': 'chuntttttt',
        'receivingUsername': 'arny',
        'message': 'Dont sas me bro!',
        'in-reply-to': 'dm07',
        'time-stamp': '2021-04-23T20:18:29Z'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm09',
        'sendingUsername': 'arny',
        'receivingUsername': 'chuntttttt',
        'message': 'Lets go bro!',
        'in-reply-to': 'dm08',
        'time-stamp': '2021-04-23T20:18:29Z'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm10',
        'sendingUsername': 'usidor_the_blue',
        'receivingUsername': 'chuntttttt',
        'message': 'STOP FIGHTING!!!',
        'time-stamp': '2021-04-23T20:18:29Z'
    }
)
table.put_item(
   Item = {
        'dmID': 'dm11',
        'sendingUsername': 'usidor_the_blue',
        'receivingUsername': 'chuntttttt',
        'message': 'STOP FIGHTING!!!',
        'time-stamp': '2021-04-23T20:18:29Z'
    }
)
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
