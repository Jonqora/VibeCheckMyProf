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

client = boto3.client('lambda')


def lambda_handler(event, context):
    # Parse the incoming request and return an error if invalid
    url = event.get('url')
    count = event.get('count')

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
    prof_status = database.get_prof_status(professor_id)
    print(f"Received request for professor {professor_id}")

    # Case: valid data is in the database
    if prof_status == "complete":
        # Data is there, return it
        print("Database contains recent data for professor.")
        professor_json = database.get_prof_data(professor_id)
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

    # Case: request exists, but data is still being processed
    if prof_status == "in-progress":
        # Send a response to inform analysis is underway
        print("Analysis in progress for professor.")
        response = {
            "STATUS": "ANALYSIS_IN_PROGRESS",
            "PROF_NAME": professor_name,
        }
    # Case: request does not exist, or data is stale
    elif prof_status == "not-started":
        if count > 0:  # Request has timed out
            response = {
                "STATUS": "ANALYSIS_FAILED",
                "PROF_NAME": professor_name
            }
        else:
            # Start analysis and send a response to inform analysis has begun
            try:
                professor_name = rmp_api.get_prof_name(professor_id)
            except ValueError:
                return {
                    'statusCode': 400,
                    'body': json.dumps({"error": f"ID {professor_id} \
                                        not found."})
                }
            client.invoke(
                FunctionName=LAMBDA2_FUNCTION_NAME,  # Lambda fn to invoke
                InvocationType='Event',  # Asynchronous
                Payload=json.dumps({"id": professor_id})
            )
            print("No recent data and no recent analysis request")
            print(f"Invoked lambda {LAMBDA2_FUNCTION_NAME} for {professor_id}")
            response = {
                "STATUS": "ANALYSIS_REQUESTED",
                "PROF_NAME": professor_name
            }
    # Case: colleen's code fucked up or something
    else:
        print("Status = 'error'")
        response = {"error": "Unknown error with prof status"}

    # Return a 200 OK response
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
