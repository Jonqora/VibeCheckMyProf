# app.py
# This lambda function delegates work to database, API, and sentiment
# analysis modules.

import json

from ..common import database
from . import sentiment


def lambda_handler(event, context):
    print("Received event: ", event)

    try:
        # Payload contains an 'id' field
        professor_json = event.get('data')
        
        if not isinstance(professor_json, dict) or not professor_json:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "No professor data provided"})
            }
        
        try:
            professor_id = professor_json["professor_id"]
        except KeyError:
            return {
                'statusCode': 400,
                'body': json.dumps(
                    {"error": "'professor_id' is missing from the data"}
                )
    }

        # Process data and have sentiment analysis added to it
        database.log_request(professor_id, analysis=True)
        professor_json = sentiment.analyze(professor_json)

        # Send data and sentiment to be stored in backend database
        database.write_data(professor_json)
        # database.log_request(professor_id, write=True)

        # Return a 200 OK response with the data
        return {
            'statusCode': 200,
            'body': json.dumps(professor_json)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }
