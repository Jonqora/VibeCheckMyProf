# frontend.py
# formats and prepares professor data before it sending back in API response

# ----------------------------------------------------------------------------#
# NOTE: this file contains function stubs. In order for our code to work
# together, the stub purpose and signatures must be followed. Feel free to
# define additional functions to do parts of the work, delegate as needed.
# ----------------------------------------------------------------------------#

from typing import Dict, Any
from collections import defaultdict
import json
import os
import re
import sys


# Format the data for the response to the front end. This may include
# reorganization (into e.g. courses), calculating aggregate stats for prof and
# courses, and organizing the ratings under courses as well.
# NOTE: please preface all new fields with "vcmp_" in order to better
# distingish the original data from the data we are adding. Please also clean
# up any intermediate values stored (e.g. totals from calculating averages)
def format(professor_json: Dict[str, Any]) -> Dict[str, Any]:
    """Aggregate the data under courses and prof"""

    # Prepare the prof with tally/sum fields, course dict, and course list
    init_prof(professor_json)

    # For each review:
    for review in professor_json["reviews"]:
        # Add to the sum fields for prof
        sum_prof_from_review(professor_json, review)

        # If course not in course dict, create course with tally/sum fields
        course_name = review["class_name"]
        if course_name not in professor_json["course_dict"]:
            init_course(professor_json, course_name)

        # Add to the count tally and sum fields for course
        sum_course_from_review(professor_json, course_name, review)

    # For prof, calculate aggregates and remove sum fields
    calculate_prof_and_cleanup(professor_json)

    # Sort the courses by reverse count
    courses = sorted(
        professor_json["course_dict"].values(),
        key=lambda x: x["num_ratings"],
        reverse=True
        )
    professor_json["courses"] = []

    # For each course, calculate aggregates and remove sum fields
    for course in courses:
        calculate_course_and_cleanup(course)

        # Add the course to the course list
        professor_json["courses"].append(course)

    # Remove the reviews and the course_dict
    del professor_json["reviews"]
    del professor_json["course_dict"]

    return professor_json


def init_prof(data):
    """Prepare prof data structure with sum fields, course dict, and list"""
    data["sum_vcmp_polarity"] = 0
    data["sum_vcmp_subjectivity"] = 0
    data["sum_vcmp_emotion"] = defaultdict(int)
    data["sum_vcmp_sentiment"] = {
                    "positive": 0,
                    "negative": 0,
                    "neutral": 0,
                    "mixed": 0
                    }
    data["sum_vcmp_spellingerrors"] = 0
    data["sum_vcmp_spellingquality"] = 0
    data["course_dict"] = {}


def sum_prof_from_review(data, review):
    """Add data from a review to the prof sum fields"""
    data["sum_vcmp_polarity"] += review["vcmp_polarity"]
    data["sum_vcmp_subjectivity"] += review["vcmp_subjectivity"]
    data["sum_vcmp_emotion"][review["vcmp_emotion"]] += 1
    data["sum_vcmp_sentiment"][review["vcmp_sentiment"]] += 1
    data["sum_vcmp_spellingerrors"] += review["vcmp_spellingerrors"]
    data["sum_vcmp_spellingquality"] += review["vcmp_spellingquality"]


def init_course(data, course_name):
    """Prepare course data structure with tally/sum fields"""
    course_tracker = {
        "course_name": course_name,
        "num_ratings": 0,
        "sum_difficulty": 0,
        "sum_rating": 0,
        "sum_vcmp_polarity": 0,
        "sum_vcmp_subjectivity": 0,
        "sum_vcmp_emotion": defaultdict(int),
        "sum_vcmp_sentiment": {
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "mixed": 0
        },
        "sum_vcmp_spellingerrors": 0,
        "sum_vcmp_spellingquality": 0
        }
    data["course_dict"][course_name] = course_tracker


def sum_course_from_review(data, course_name, review):
    """Add data from a review to the course sum fields"""
    course = data["course_dict"][course_name]

    course["num_ratings"] += 1
    course["sum_difficulty"] += review["difficulty"]
    course["sum_rating"] += review["quality"]

    course["sum_vcmp_polarity"] += review["vcmp_polarity"]
    course["sum_vcmp_subjectivity"] += review["vcmp_subjectivity"]
    course["sum_vcmp_emotion"][review["vcmp_emotion"]] += 1
    course["sum_vcmp_sentiment"][review["vcmp_sentiment"]] += 1
    course["sum_vcmp_spellingerrors"] += review["vcmp_spellingerrors"]
    course["sum_vcmp_spellingquality"] += review["vcmp_spellingquality"]


def calculate_prof_and_cleanup(data):
    """Calculate aggregate data for prof and remove temp fields"""
    if data["num_ratings"] > 0:
        data["vcmp_polarity"] = round(
            data["sum_vcmp_polarity"] / data["num_ratings"], 4
            )
        data["vcmp_subjectivity"] = round(
            data["sum_vcmp_subjectivity"] / data["num_ratings"], 4
            )
        top_emotions = sorted(
            data["sum_vcmp_emotion"],
            key=lambda emotion: (-data["sum_vcmp_emotion"][emotion], emotion)
            )[:3]
        data["vcmp_emotion"] = [
            (emotion, data["sum_vcmp_emotion"][emotion])
            for emotion in top_emotions
            ]
        data["vcmp_sentiment"] = data["sum_vcmp_sentiment"]
        data["vcmp_spellingerrors"] = round(
            data["sum_vcmp_spellingerrors"] / data["num_ratings"], 4
            )
        data["vcmp_spellingquality"] = round(
            data["sum_vcmp_spellingquality"] / data["num_ratings"], 4
            )

    del data["sum_vcmp_polarity"]
    del data["sum_vcmp_subjectivity"]
    del data["sum_vcmp_emotion"]
    del data["sum_vcmp_sentiment"]
    del data["sum_vcmp_spellingerrors"]
    del data["sum_vcmp_spellingquality"]


def calculate_course_and_cleanup(course):
    """Calculate aggregate data for course and remove temp fields"""
    course["difficulty"] = round(
        course["sum_difficulty"] / course["num_ratings"], 2
        )
    course["rating"] = round(
        course["sum_rating"] / course["num_ratings"], 2
        )

    course["vcmp_polarity"] = round(
        course["sum_vcmp_polarity"] / course["num_ratings"], 4
        )
    course["vcmp_subjectivity"] = round(
        course["sum_vcmp_subjectivity"] / course["num_ratings"], 4
        )
    top_emotions = sorted(
        course["sum_vcmp_emotion"],
        key=lambda emotion: (-course["sum_vcmp_emotion"][emotion], emotion)
        )[:3]
    course["vcmp_emotion"] = [
        (emotion, course["sum_vcmp_emotion"][emotion])
        for emotion in top_emotions
        ]
    course["vcmp_sentiment"] = course["sum_vcmp_sentiment"]
    course["vcmp_spellingerrors"] = round(
        course["sum_vcmp_spellingerrors"] / course["num_ratings"], 4
        )
    course["vcmp_spellingquality"] = round(
        course["sum_vcmp_spellingquality"] / course["num_ratings"], 4
        )

    del course["sum_difficulty"]
    del course["sum_rating"]
    del course["sum_vcmp_polarity"]
    del course["sum_vcmp_subjectivity"]
    del course["sum_vcmp_emotion"]
    del course["sum_vcmp_sentiment"]
    del course["sum_vcmp_spellingerrors"]
    del course["sum_vcmp_spellingquality"]


def modify_json_file(input_filename):
    """Read JSON file, add new fields, and save it under a new name."""
    if not os.path.exists(input_filename):
        print(f"File {input_filename} not found.")
        return

    # Extract the ID number from the input filename using regex
    match = re.search(r'(\d+)', input_filename)
    if not match:
        print("ID number not found in the filename.")
        return

    # Get the ID number and construct the output filename
    id_number = match.group(1)
    output_filename = f"frontend_{id_number}.json"

    # Read the JSON file into a nested dict
    with open(input_filename, 'r') as infile:
        data = json.load(infile)

    # Update the dictionary with the new fields
    data = format(data)

    # Write the modified dictionary to the new file
    with open(output_filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    print(f"Modified data saved to {output_filename}")


if __name__ == "__main__":
    """Convert a sentiment file to a frontend file"""
    if len(sys.argv) != 2:
        print("Usage: python frontend.py <input_filename>")
    else:
        input_filename = sys.argv[1]
        modify_json_file(input_filename)
