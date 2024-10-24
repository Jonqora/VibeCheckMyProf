# test_database.py

# ----------------------------------------------------------------------------#
# NOTE: this is a test file stub, generated by ChatGPT. The stub functions in
# your file may not be easy or even possible to test. Instead, use this file
# to test smaller functions and helper functions where you can.
# ----------------------------------------------------------------------------#

from app import database


def test_get_recent_data():
    professor_id = 123456  # Mock the professor ID for test purposes
    data = database.get_recent_data(professor_id)

    assert isinstance(data, dict)  # Should return an empty dict or valid data
    # TODO can we even test this function without mocking?


def test_write_data():
    professor_json = {
        "professor_id": 123456,
        "name": "Test Professor",
        "reviews": []
    }
    result = database.write_data(professor_json)

    assert result is None  # Assuming write_data returns None
    # TODO assertions here that make sense, if any
