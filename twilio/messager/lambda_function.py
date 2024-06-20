import json
import os
from messager.rest import Client


def lambda_handler(event, context):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    twilio_number = os.environ['TWILIO_PHONE_NUMBER']

    client = Client(account_sid, auth_token)

    to_number = event['to']
    message_body = event['message']

    message = client.messages.create(
        body=message_body,
        from_=twilio_number,
        to=to_number
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Message sent successfully!')
    }
