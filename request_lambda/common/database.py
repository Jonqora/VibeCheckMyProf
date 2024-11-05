# database.py
# Interacts with backend database
# noqa: E501
import json
import mysql.connector
import time

from typing import Dict, Any
from datetime import datetime, timezone, timedelta
from request_lambda.common.config import Config
from request_lambda.common.payload import Professor, Rating, Sentiment
from request_lambda.common.query import QueryConnector, QueryRunner

SECONDS_RECENT_ANALYSIS = 300


def has_recent_data(professor_id: int) -> bool:
    """Returns True if a prof has a write request within recent time limit"""
    return False


def has_recent_analysis_request(professor_id: int) -> bool:
    """Returns True if a prof has a very recent analysis request"""
    return False


def log_standard_request(professor_id: int):
    pass


def log_analysis_request(professor_id: int):
    pass


def log_write_request(professor_id: int):
    pass


def get_recent_data(professor_id: int) -> Dict[str, Any]:
    """ Returns dict of recently analyzed professor reviews,
        empty if ratings are stale. """
    
    dummy_response = {
        "professor_id": 2971924,
        "name": "Maryam Aliabadi",
        "department": "Computer Science",
        "difficulty": 3.2,
        "rating": 4,
        "would_take_again": 80,
        "num_ratings": 5,
        "school_id": 1413,
        "school_name": "University of British Columbia",
        "reviews": [
            {
                "quality": 4,
                "difficulty": 4,
                "comment": "I have learnt alot in this course.",
                "class_name": "CPSC436C",
                "date": "2024-03-18 18:36:05",
                "take_again": True,
                "grade": "A+",
                "thumbs_up": 0,
                "thumbs_down": 0,
                "online_class": False,
                "credit": True,
                "attendance_mandatory": False,
                "vcmp_polarity": 0.0,
                "vcmp_subjectivity": 0.0,
                "vcmp_emotion": "neutral",
                "vcmp_sentiment": "positive",
                "vcmp_spellingerrors": 2,
                "vcmp_spellingquality": 0.7142857142857143
            },
            {
                "quality": 5,
                "difficulty": 3,
                "comment": "Maryam is one of the most caring teachers that I ever had. I liked the guest speakers who were invited to the course. She did her best to bring the industrial experience of professionals to the course which was a great complementary to what we had learnt in this course. ",
                "class_name": "CPSC436C",
                "date": "2024-03-18 18:32:15",
                "take_again": True,
                "grade": "A",
                "thumbs_up": 0,
                "thumbs_down": 0,
                "online_class": False,
                "credit": True,
                "attendance_mandatory": True,
                "vcmp_polarity": 0.7250000000000001,
                "vcmp_subjectivity": 0.5875,
                "vcmp_emotion": "admiration",
                "vcmp_sentiment": "positive",
                "vcmp_spellingerrors": 3,
                "vcmp_spellingquality": 0.94
            },
            {
                "quality": 5,
                "difficulty": 4,
                "comment": "This course was very practical and it helps a lot to get a job ",
                "class_name": "CPSC436C",
                "date": "2024-01-17 20:40:30",
                "take_again": True,
                "grade": "A",
                "thumbs_up": 0,
                "thumbs_down": 0,
                "online_class": False,
                "credit": True,
                "attendance_mandatory": True,
                "vcmp_polarity": 0.2,
                "vcmp_subjectivity": 0.3,
                "vcmp_emotion": "approval",
                "vcmp_sentiment": "positive",
                "vcmp_spellingerrors": 0,
                "vcmp_spellingquality": 1.0
            },
            {
                "quality": 5,
                "difficulty": 3,
                "comment": "I truely appreciate Maryam for her awesome course. CPSC 436C was one of the most useful courses that I ever had in my academic life. It included lots of practical assignments that made me feel confident to start a career in cloud computing. Highly recommend it to UBC students from different disciplines. ",
                "class_name": "CPSC436C",
                "date": "2024-01-17 20:20:02",
                "take_again": True,
                "grade": "A+",
                "thumbs_up": 0,
                "thumbs_down": 0,
                "online_class": False,
                "credit": True,
                "attendance_mandatory": True,
                "vcmp_polarity": 0.35125,
                "vcmp_subjectivity": 0.5154166666666666,
                "vcmp_emotion": "admiration",
                "vcmp_sentiment": "positive",
                "vcmp_spellingerrors": 9,
                "vcmp_spellingquality": 0.8269230769230769
            },
            {
                "quality": 1,
                "difficulty": 2,
                "comment": "Dr. Aliabadi is honestly a very knowledgeable and engaging lecturer and the lectures are good, but the class is incredibly disorganized and her behaviours are questionable. She blames TAs for not proofreading labs/assignments/quizzes/exams. Labs and assignments are poorly documented. Nobody responds on Piazza. Overall, not recommended. ",
                "class_name": "CPSC436C",
                "date": "2024-01-06 01:16:30",
                "take_again": None,
                "grade": "A",
                "thumbs_up": 1,
                "thumbs_down": 0,
                "online_class": False,
                "credit": True,
                "attendance_mandatory": True,
                "vcmp_polarity": 0.18571428571428575,
                "vcmp_subjectivity": 0.5857142857142856,
                "vcmp_emotion": "disapproval",
                "vcmp_sentiment": "negative",
                "vcmp_spellingerrors": 11,
                "vcmp_spellingquality": 0.7608695652173914
            }
        ]
    }

    return dummy_response

    start_time = time.perf_counter()
    config = Config().from_env()
    payload = get_data_from_db(professor_id, config)
    stop_time = time.perf_counter()

    get_data_time = stop_time - start_time
    print(f"Time to get recent data from DB: {(get_data_time):.4f} seconds.")
    return payload


def get_data_from_db(professor_id: int, config: Config) -> Dict[str, Any]:
    qc = QueryConnector(config)
    qr = QueryRunner(qc.connection)
    current_time_utc = datetime.now(timezone.utc)
    data_freshness_cutoff = (current_time_utc
                             - timedelta(seconds=config.rec_int_sec))

    try:
        last_prof_write = qr.get_prof_request_date(professor_id)
        if last_prof_write is None:
            payload = {}
        elif (last_prof_write[0].replace(tzinfo=timezone.utc)
              <= data_freshness_cutoff):
            payload = {}
        else:
            recent_data = qr.get_prof_records(professor_id)
            if not recent_data:
                raise ValueError(f"""Failed query for {professor_id}.""")
            payload = get_formatted_as_dict(recent_data)
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
        payload = {}
    except ValueError as ve:
        print(f"An error occurred: {ve}")
        payload = {}
    finally:
        qr.cursor.close()
        qc.connection.close()
    return payload


def get_formatted_as_dict(rows: list) -> Dict[str, Any]:
    """ Returns dictionary of rows formatted for frontend. """
    result = {
        "professor_id": rows[0][0],
        "name": rows[0][1],
        "department": rows[0][2],
        "difficulty": float(rows[0][3]),
        "rating": float(rows[0][4]),
        "would_take_again": float(rows[0][5]),
        "num_ratings": rows[0][6],
        "school_id": rows[0][7],
        "school_name": rows[0][8],
        "reviews": []
    }

    for row in rows:
        review = {
            "quality": float(row[9]),
            "difficulty": float(row[10]),
            "comment": row[11],
            "class_name": row[20],
            "date": row[18].strftime("%Y-%m-%d %H:%M:%S"),
            "take_again": bool(row[19]),
            "grade": row[12],
            "thumbs_up": row[13],
            "thumbs_down": row[14],
            "online_class": bool(row[15]),
            "credit": bool(row[16]),
            "attendance_mandatory": bool(row[17]),
            "vcmp_polarity": row[21],
            "vcmp_subjectivity": row[22],
            "vcmp_emotion": row[23],
            "vcmp_sentiment": row[24],
            "vcmp_spellingerrors": row[25],
            "vcmp_spellingquality": float(row[26])
        }
        result["reviews"].append(review)

    return result


def write_data(professor_dict: Dict[str, Any]) -> None:
    """ Parses and writes dictionary data to database. """
    start_time = time.perf_counter()
    config = Config().from_env()
    insert_data_from_dict(professor_dict, config)
    stop_time = time.perf_counter()

    write_data_time = stop_time - start_time
    print(f"Time to write data to DB: {(write_data_time):.4f} seconds.")


def insert_data_from_dict(professor_dict: Dict[str, Any],
                          config: Config) -> None:
    """ Parses and writes dictionary data to database. """
    qc = QueryConnector(config)
    qr = QueryRunner(qc.connection)
    try:
        prof = Professor(professor_dict)
        qr.insert_school(prof)
        qr.insert_professor(prof)
        qr.insert_request(prof)  # TODO edit this one
        qr.delete_prof_reviews(prof)

        for review in prof.reviews:
            # Query courses table for course
            query_result = qr.get_course_record(review["class_name"],
                                                prof.school_id)

            if query_result is None:
                # Course doesn't exist, so add it to courses table
                qr.insert_course(review["class_name"], prof.school_id)
                qc.connection.commit()
                course_id = qr.cursor.lastrowid  # Grab for rating record
            else:
                # Course exists, so use the existing course_id
                course_id = query_result[0]

            rating = Rating(review, prof.prof_id, course_id)
            qr.insert_rating(rating)

            sentiment = Sentiment(review, rating.rating_id)
            qr.insert_sentiment_analysis(sentiment)

        qc.connection.commit()
        print("Data insertion complete.")
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
    finally:
        qr.cursor.close()
        qc.connection.close()

    return


def insert_data_from_json_file(json_file_path: str, config: Config) -> None:
    """ Inserts data from JSON file into database. """
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    insert_data_from_dict(data, config)


def run_sql_file(sql_file_path: str, config: Config) -> None:
    """ Runs SQL file commands on database. """
    qc = QueryConnector(config)
    qr = QueryRunner(qc.connection)

    with open(sql_file_path, 'r') as file:
        sql_script = file.read()
    sql_commands = sql_script.split(';')
    try:
        qr.run_sql_commands(sql_commands)
        print("All commands executed successfully.")
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
    finally:
        qc.connection.commit()
        qr.cursor.close()
        qc.connection.close()
