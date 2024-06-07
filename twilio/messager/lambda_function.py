import json
import os
from messager.rest import Client


def lambda_handler(event, context):
    # Get the Twilio credentials from environment variables
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    twilio_number = os.environ['TWILIO_PHONE_NUMBER']

    # Initialize the Twilio client
    client = Client(account_sid, auth_token)

    # Get the input data from the event
    to_number = event['to']
    message_body = event['message']

    # Send the message
    message = client.messages.create(
        body=message_body,
        from_=twilio_number,
        to=to_number
    )

    # Return a success message
    return {
        'statusCode': 200,
        'body': json.dumps('Message sent successfully!')
    }
