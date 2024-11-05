# app.py
# This lambda function delegates work to database, API, and
# frontend formatting modules.

import boto3
import json
import re

from ..common import database
from . import frontend
from ..common import rmp_api

LAMBDA2_FUNCTION_NAME = "vibe-check-my-prof-lambda2"


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
    if database.has_recent_data(professor_id):
        # Get, format and send the data
        print(f"Database contains recent data for prof")
        professor_json = database.get_recent_data(professor_id)
        database.log_standard_request(professor_id)
        response = {
            "STATUS": "DATA_RETRIEVED",
            "DATA": frontend.format(professor_json)
        }
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    
    # Get the professor name from RMP API for responses
    try:
        professor_name = rmp_api.get_prof_name(professor_id)
    except ValueError:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": f"ID {professor_id} not found."})
        }
        
    if database.has_recent_analysis_request(professor_id):
        # Send a response to inform analysis already requested
        print(f"Recent analysis request found")
        database.log_standard_request(professor_id)
        response = {
            "STATUS": "ANALYSIS_IN_PROGRESS",
            "PROF_NAME": professor_name
        }
    else:
        # Start analysis and
        # Send a response to inform analysis has begun
        client = boto3.client('lambda')
        client.invoke(
            FunctionName=LAMBDA2_FUNCTION_NAME,  # Lambda function to invoke
            InvocationType='Event',       # Asynchronous
            Payload=json.dumps({"id": professor_id})
        )
        print(f"No recent data and no recent analysis request")
        print(f"Invoked lambda function {LAMBDA2_FUNCTION_NAME}")
        response = {
            "STATUS": "ANALYSIS_REQUESTED",
            "PROF_NAME": professor_name
        }

    # Return a 200 OK response
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
