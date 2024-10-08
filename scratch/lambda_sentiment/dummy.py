# dummy.py
# This is a dummy function to mock API functionality and return formatted data

import json
import re

def lambda_handler(event, context):
    # Parse the incoming request
    url = event.get('url')
    if not url:
        # Return a 400 Bad Request if URL is missing
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "URL is missing"})
        }

    # Regex to validate a professor URL from RateMyProfessors
    url_pattern = r"^https:\/\/(www\.)?ratemyprofessors\.com\/professor\/\d+$"
    
    if not re.match(url_pattern, url):
        # Return a 400 Bad Request if the URL is invalid
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "Invalid URL format. Must be a valid RateMyProfessors professor URL."})
        }

    # Prepare the response if the URL is valid
    scores = [0.52, 0.13, -0.22, 0.05, -0.43, 0.19, 0.21, -0.09, -0.27, 0.31]
    average = sum(scores) / len(scores)
    
    response = {
        "scores": scores,
        "average": round(average, 3),
        "professor_name": "Gregor Kiczales",
        "professor_id": 38077
    }

    # Return a 200 OK response with the data
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
