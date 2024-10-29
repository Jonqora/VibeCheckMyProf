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

from . import database
from . import frontend
from . import rmp_api
from . import sentiment


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
    professor_json = database.get_recent_data(professor_id)  # TODO

    pre_sentiment = {}
    if not professor_json:
        # Get prof and ratings data using RateMyProfessorAPI
        try:
            professor_json = rmp_api.get_prof_data(professor_id)
        except ValueError:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": f"ID {professor_id} not found."})
            }
        
        pre_sentiment = professor_json.copy()
        # Process data and have sentiment analysis added to it
        professor_json = sentiment.analyze(professor_json)  # TODO

        # Send data and sentiment to be stored in backend database
        database.write_data(professor_json)  # TODO

    # Format the data for the response to the front end
    if pre_sentiment != professor_json:
        response = frontend.format(professor_json)  # TODO
    else:
        # # # # # # # # # dummy code is below # # # # # # # # #
        # # #  remove when sentiment & frontend complete  # # #
        response = {
            "professor_id": 1835982,
            "name": "Ben Williams",
            "department": "Mathematics",
            "difficulty": 3.7,
            "rating": 3.6,
            "would_take_again": 76.1905,
            "num_ratings": 26,
            "school_id": 1413,
            "school_name": "University of British Columbia",
            "vcmp_polarity": 0.369,
            "vcmp_subjectivity": 0.5198,
            "vcmp_emotion": [
                [
                    "approval",
                    4
                ],
                [
                    "nervousness",
                    3
                ],
                [
                    "realization",
                    3
                ]
            ],
            "vcmp_sentiment": {
                "positive": 2,
                "negative": 9,
                "neutral": 11,
                "mixed": 4
            },
            "vcmp_spellingerrors": 0.6923,
            "vcmp_spellingquality": 0.9438,
            "courses": [
                {
                    "course_name": "MATH221",
                    "num_ratings": 15,
                    "difficulty": 3.4,
                    "rating": 3.87,
                    "vcmp_polarity": 0.3575,
                    "vcmp_subjectivity": 0.5097,
                    "vcmp_emotion": [
                        [
                            "nervousness",
                            3
                        ],
                        [
                            "approval",
                            2
                        ],
                        [
                            "realization",
                            2
                        ]
                    ],
                    "vcmp_sentiment": {
                        "positive": 1,
                        "negative": 5,
                        "neutral": 7,
                        "mixed": 2
                    },
                    "vcmp_spellingerrors": 0.8,
                    "vcmp_spellingquality": 0.9407
                },
                {
                    "course_name": "MATH220",
                    "num_ratings": 5,
                    "difficulty": 4.0,
                    "rating": 3.0,
                    "vcmp_polarity": 0.3374,
                    "vcmp_subjectivity": 0.572,
                    "vcmp_emotion": [
                        [
                            "approval",
                            2
                        ],
                        [
                            "anger",
                            1
                        ],
                        [
                            "fear",
                            1
                        ]
                    ],
                    "vcmp_sentiment": {
                        "positive": 1,
                        "negative": 2,
                        "neutral": 2,
                        "mixed": 0
                    },
                    "vcmp_spellingerrors": 0.6,
                    "vcmp_spellingquality": 0.9506
                },
                {
                    "course_name": "MATH427",
                    "num_ratings": 2,
                    "difficulty": 4.5,
                    "rating": 4.5,
                    "vcmp_polarity": 0.1845,
                    "vcmp_subjectivity": 0.2369,
                    "vcmp_emotion": [
                        [
                            "confusion",
                            1
                        ],
                        [
                            "disappointment",
                            1
                        ]
                    ],
                    "vcmp_sentiment": {
                        "positive": 0,
                        "negative": 0,
                        "neutral": 1,
                        "mixed": 1
                    },
                    "vcmp_spellingerrors": 0.0,
                    "vcmp_spellingquality": 0.9442
                },
                {
                    "course_name": "MATH105",
                    "num_ratings": 1,
                    "difficulty": 3.0,
                    "rating": 5.0,
                    "vcmp_polarity": 0.5404,
                    "vcmp_subjectivity": 0.3826,
                    "vcmp_emotion": [
                        [
                            "grief",
                            1
                        ]
                    ],
                    "vcmp_sentiment": {
                        "positive": 0,
                        "negative": 1,
                        "neutral": 0,
                        "mixed": 0
                    },
                    "vcmp_spellingerrors": 1.0,
                    "vcmp_spellingquality": 0.9211
                },
                {
                    "course_name": "MATH527",
                    "num_ratings": 1,
                    "difficulty": 4.0,
                    "rating": 5.0,
                    "vcmp_polarity": 0.3549,
                    "vcmp_subjectivity": 0.8683,
                    "vcmp_emotion": [
                        [
                            "fear",
                            1
                        ]
                    ],
                    "vcmp_sentiment": {
                        "positive": 0,
                        "negative": 0,
                        "neutral": 1,
                        "mixed": 0
                    },
                    "vcmp_spellingerrors": 2.0,
                    "vcmp_spellingquality": 0.9644
                },
                {
                    "course_name": "MATH308",
                    "num_ratings": 1,
                    "difficulty": 5.0,
                    "rating": 4.0,
                    "vcmp_polarity": 0.3068,
                    "vcmp_subjectivity": 0.8376,
                    "vcmp_emotion": [
                        [
                            "confusion",
                            1
                        ]
                    ],
                    "vcmp_sentiment": {
                        "positive": 0,
                        "negative": 0,
                        "neutral": 0,
                        "mixed": 1
                    },
                    "vcmp_spellingerrors": 0.0,
                    "vcmp_spellingquality": 0.9571
                },
                {
                    "course_name": "184",
                    "num_ratings": 1,
                    "difficulty": 5.0,
                    "rating": 1.0,
                    "vcmp_polarity": 0.9736,
                    "vcmp_subjectivity": 0.4465,
                    "vcmp_emotion": [
                        [
                            "disappointment",
                            1
                        ]
                    ],
                    "vcmp_sentiment": {
                        "positive": 0,
                        "negative": 1,
                        "neutral": 0,
                        "mixed": 0
                    },
                    "vcmp_spellingerrors": 0.0,
                    "vcmp_spellingquality": 0.9459
                }
            ]
        }
        # # # # # # # # #  end of dummy code  # # # # # # # # #


    # Return a 200 OK response with the data
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
