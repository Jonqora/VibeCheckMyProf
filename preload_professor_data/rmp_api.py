# rmp_api.py
# Gets the professor and ratings data using RateMyProfessorAPI
# When run as __main__, outputs a json file for a given prof_id
# see documentation at https://github.com/Nobelz/RateMyProfessorAPI/blob/master/ratemyprofessor/professor.py  # noqa: E501

import ratemyprofessor

import json
import sys
from datetime import datetime


def get_prof_data(professor_id: int):
    professor = ratemyprofessor.Professor(professor_id)

    prof_data = {
        "professor_id": professor_id,
        "name": professor.name,
        "department": professor.department,
        "difficulty": professor.difficulty,
        "rating": professor.rating,
        "would_take_again": professor.would_take_again,
        "num_ratings": professor.num_ratings,
        "school_id": professor.school.id,
        "school_name": professor.school.name,
        "reviews": []
    }

    for rating in professor.get_ratings():
        review = {
            "quality": rating.rating,
            "difficulty": rating.difficulty,
            "comment": rating.comment,
            "class_name": rating.class_name,
            "date": (
                rating.date.strftime('%Y-%m-%d %H:%M:%S')
                if isinstance(rating.date, datetime)
                else str(rating.date)
            ),
            "take_again": rating.take_again,
            "grade": rating.grade,
            "thumbs_up": rating.thumbs_up,
            "thumbs_down": rating.thumbs_down,
            "online_class": rating.online_class,
            "credit": rating.credit,
            "attendance_mandatory": rating.attendance_mandatory
        }
        prof_data["reviews"].append(review)

    return prof_data


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rmp_api.py <prof_id>")
        sys.exit(1)

    prof_id = int(sys.argv[1])

    data = get_prof_data(prof_id)

    with open(f'prof_data_{prof_id}.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
