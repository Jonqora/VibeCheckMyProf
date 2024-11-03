import json

from preload_professor_data.rmp_api import get_prof_data
from preload_professor_data.sentiment import analyze
from shared.database import write_data

def lambda_handler(event, context):
    """Lambda handler function to preload professor data."""
    professor_ids = [13305, 42342, 2053524]

    for prof_id in professor_ids:
        try:
            prof_json = get_prof_data(prof_id)
            analyzed_prof_json = analyze(prof_json)
            write_data(analyzed_prof_json)
        except Exception as e:
            print(e)

    return {
        "statusCode": 200,
        "body": json.dumps("Professor data successfully preloaded.")
    }