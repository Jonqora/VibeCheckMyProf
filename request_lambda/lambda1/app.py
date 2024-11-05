# app.py
# This lambda function delegates work to database, API, sentiment analysis and
# frontend formatting modules.

# The json format output by these functions
#     database.get_recent_data
#     rmp_api.get_prof_data
#     sentiment.analyze
# ...and consumed by these functions
#     sentiment.analyze
#     database.write_data
#     frontend.format
# is demonstrated in prof_data_1835982.json

import json
import re

from ..common import database
from . import frontend
from ..common import rmp_api


def lambda_handler(event, context):
    # Parse the incoming request and return an error if invalid
    url = event.get('url')
    if not url:
        # Return a 400 Bad Request if URL is missing
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "URL is missing"})
        }
    url_pattern = r"^https:\/\/(www\.)?ratemyprofessors\.com\/professor\/\d+$"
    if not re.match(url_pattern, url):
        # Return a 400 Bad Request if the URL is invalid
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "Invalid URL format. Must be a valid "
                                "RateMyProfessors professor URL."})
        }

    # Get the professor id
    professor_id = int(url.split('/')[-1])

    # Check for recent data in our database (return data if present else None)
    professor_json = database.get_recent_data(professor_id)

    if not professor_json:
        # Get prof and ratings data using RateMyProfessorAPI
        try:
            professor_json = rmp_api.get_prof_data(professor_id)
        except ValueError:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": f"ID {professor_id} not found."})
            }

        # Process data and have sentiment analysis added to it
        professor_json = sentiment.analyze(professor_json)

        # Send data and sentiment to be stored in backend database
        database.write_data(professor_json)

    response = frontend.format(professor_json)

    # Return a 200 OK response with the data
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
