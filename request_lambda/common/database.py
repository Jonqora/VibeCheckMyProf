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


def has_recent_request_entry(professor_id: int, analysis=False) -> bool:
    """Returns True if a prof has a request within recent time limit"""
    config = Config().from_env()
    qc = QueryConnector(config)
    qr = QueryRunner(qc.connection)
    current_time_utc = datetime.now(timezone.utc)
    if analysis:
        recency_cutoff = (current_time_utc
                                - timedelta(seconds=SECONDS_RECENT_ANALYSIS))
    else:
        recency_cutoff = (current_time_utc
                                - timedelta(seconds=config.rec_int_sec))

    try:
        if analysis:
            last_prof_write = qr.get_prof_request_date(professor_id, analysis=True)
        else:
            last_prof_write = qr.get_prof_request_date(professor_id, write=True)
        if last_prof_write is None:
            response = False
        elif (last_prof_write[0].replace(tzinfo=timezone.utc)
              <= recency_cutoff):
            response = False
        else:
            response = True
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
        response = False
    except ValueError as ve:
        print(f"An error occurred: {ve}")
        response = False
    finally:
        qr.cursor.close()   
        qc.connection.close()
    return response


def log_request(professor_id: int, write = False, analysis = False):
    """Logs a request, optionally if resulted in write or analysis request"""
    config = Config().from_env()
    qc = QueryConnector(config)
    qr = QueryRunner(qc.connection)
    try:
        qr.insert_request(professor_id, write, analysis)
        qc.connection.commit()
        print(f"Logged request with write={write} and analysis={analysis}.")
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
    finally:
        qr.cursor.close()
        qc.connection.close()


def get_recent_data(professor_id: int) -> Dict[str, Any]:
    """ Returns dict of recently analyzed professor reviews,
        given that recent data exists. """

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
    
    try:
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
        # qr.insert_request(prof.prof_id, True, False)  # TODO edit this one
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
