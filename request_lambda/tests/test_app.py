# test_app.py

# ----------------------------------------------------------------------------#
# NOTE: this is a test file stub, generated by ChatGPT. The stub functions in
# your file may not be easy or even possible to test. Instead, use this file
# to test smaller functions and helper functions where you can.
# ----------------------------------------------------------------------------#

import json
from request_lambda.lambda1 import app


def test_lambda_handler_valid_url():
    event = {
        "url": "https://www.ratemyprofessors.com/professor/1835982"
    }
    context = {}  # Lambda context can be mocked
    response = app.lambda_handler(event, context)

    assert response['statusCode'] == 200


def test_lambda_handler_missing_url():
    event = {}
    context = {}
    response = app.lambda_handler(event, context)

    assert response['statusCode'] == 400
    assert "URL is missing" in json.loads(response['body'])['error']


def test_lambda_handler_invalid_url():
    event = {
        "url": "https://invalid.url/professor/invalid"
    }
    context = {}
    response = app.lambda_handler(event, context)

    assert response['statusCode'] == 400
    assert "Invalid URL format" in json.loads(response['body'])['error']


def test_lambda_handler_invalid_prof_id():
    event = {
        "url": "https://www.ratemyprofessors.com/professor/352689901"
    }
    context = {}
    response = app.lambda_handler(event, context)

    assert response['statusCode'] == 400
    assert "not found" in json.loads(response['body'])['error']
