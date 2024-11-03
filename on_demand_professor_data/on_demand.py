import json
import re

from shared.database import get_recent_data
from on_demand_professor_data.frontend import format

def lambda_handler(event, context):
    """Lambda handler function to handle on-demand requests."""
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
    professor_json = get_recent_data(professor_id)

    if professor_json:
        # Data is available in the database, return it
        return {
            "statusCode": 200,
            "body": json.dumps(format(professor_json))
        }
    else:
        # Data is not available, return a processing message
        return {
            "statusCode": 202,  # Accepted
            "body": json.dumps({
                "message": "Data is being processed. Please check back later.",
                "status": "processing",
                "professor_id": professor_id
            })
        }
