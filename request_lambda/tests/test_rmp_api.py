# test rmp_api.py

# ----------------------------------------------------------------------------#
# NOTE: this is a test file stub, generated by ChatGPT. The stub functions in
# your file may not be easy or even possible to test. Instead, use this file
# to test smaller functions and helper functions where you can.
# ----------------------------------------------------------------------------#

from app import rmp_api


def test_get_prof_data():
    professor_id = 1835982
    prof_data = rmp_api.get_prof_data(professor_id)

    assert isinstance(prof_data, dict)
    assert prof_data["professor_id"] == 1835982
    assert prof_data["name"] == "Ben Williams"
    assert prof_data["department"] == "Mathematics"
    assert prof_data["school_id"] == 1413
    assert isinstance(prof_data["reviews"], list)
    assert prof_data["num_ratings"] == len(prof_data["reviews"])
    assert "quality" in prof_data["reviews"][0]
