# app.py
# This lambda function delegates work to database, API, and sentiment
# analysis modules.

import json

from ..common import database
from ..common import rmp_api
from . import sentiment


def lambda_handler(event, context):
    print("Received event: ", event)

    try:
        # Payload contains an 'id' field
        professor_id = event.get('id')
        
        if professor_id is None:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "No professor ID provided"})
            }
        
        # Get professor and review data from RMP
        try:
            professor_json = rmp_api.get_prof_data(professor_id)
        except ValueError:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": f"ID {professor_id} not found."})
            }

        # Process data and have sentiment analysis added to it
        database.log_analysis_request(professor_id)
        professor_json = sentiment.analyze(professor_json)

        # Send data and sentiment to be stored in backend database
        database.write_data(professor_json)
        database.log_write_request(professor_id)

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
