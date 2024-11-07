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
                'body': json.dumps(
                    {"error": "'id' is missing from the data"}
                )
            }
        professor_id = int(professor_id)

        # Fetch professor data and analyze sentiment
        try:
            print(f"About to get RMP data for {professor_id}")
            professor_json = rmp_api.get_prof_data(professor_id)
        except ValueError:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": f"{professor_id} not in RMP."})
            }
        professor_json = sentiment.analyze(professor_json)

        # Send data and sentiment to be stored in backend database
        database.write_data(professor_json)

        # Return a 200 OK response with the data
        return {
            'statusCode': 200,
            'body': json.dumps(professor_json)
        }

    except Exception as e:
        print("error", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({"error": "Internal server error"})
        }
