# flake8: noqa
# TODO: Ignore SQL-formatting lint issues in this scripting file for now

""" Class to Facilitate Interaction Between Database & Queries/Data Files """
import mysql.connector
import json

from datetime import datetime

class QueryRunner:
    db_name: str
    db_user: str
    db_host: str
    db_port: int
    db_password: str

    def __init__(self, db_name: str, db_user: str, db_host: str, db_port: int, db_password: str):
        self.db_name     = db_name
        self.db_user     = db_user
        self.db_host     = db_host
        self.db_port     = db_port
        self.db_password = db_password

    """ Creates database connection and returns connector """
    def get_db_connector(self) -> mysql.connector.connect:
        # Connect to the MySQL database
        return mysql.connector.connect(host=self.db_host,
                                       user=self.db_user,
                                       password=self.db_password,
                                       database=self.db_name,
                                       port=self.db_port)

    """ Executes MySQL commands from SQL file path """
    def run_sql_script(self, sql_file_path):
        # Connect to the MySQL database
        conn = self.get_db_connector()
        cursor = conn.cursor()

        # Read the SQL file
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()

        # Split commands by semicolon to execute them one by one
        commands = sql_script.split(';')

        try:
            # Execute each SQL command
            for command in commands:
                if command.strip():  # Avoid empty commands
                    cursor.execute(command)
            print("All commands executed successfully.")
        except mysql.connector.Error as e:
            print(f"An error occurred: {e}")
        finally:
            # Commit changes and close the connection
            conn.commit()
            cursor.close()
            conn.close()

    """ Executes MySQL commands parsed from JSON data file path """
    def insert_data_from_json(self, json_file_path):
        # Connect to the MySQL database
        conn = self.get_db_connector()
        cursor = conn.cursor()

        # Load JSON data
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        try:
            # Insert into schools table
            school_id = data["school_id"]
            school_name = data["school_name"]

            cursor.execute("""
                INSERT INTO schools (school_id, school_name) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE school_name = VALUES(school_name)
                """, (school_id, school_name))

            # Insert into professors table
            prof_id = data["professor_id"]
            prof_name = data["name"]
            dept = data["department"]
            avg_diff = data["difficulty"]
            avg_rating = data["rating"]
            would_retake_rate = data["would_take_again"]
            rating_count = data["num_ratings"]

            cursor.execute("""
                INSERT INTO professors (prof_id, prof_name, dept, avg_diff, avg_rating, 
                would_retake_rate, rating_count, school_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    avg_diff=VALUES(avg_diff), avg_rating=VALUES(avg_rating),  
                    would_retake_rate=VALUES(would_retake_rate), rating_count=VALUES(rating_count)
                """, (prof_id, prof_name, dept, avg_diff, avg_rating, would_retake_rate, rating_count, school_id))

            # Insert into requests table
            cursor.execute("""
                INSERT INTO requests (prof_id, resulted_in_write)
                VALUES (%s, %s)
                """, (prof_id, 1))

            # Insert into courses and ratings tables
            for review in data["reviews"]:
                # Insert course if it doesn't already exist
                course_name = review["class_name"]
                cursor.execute("SELECT course_id FROM courses WHERE course_name = %s AND school_id = %s",
                               (course_name, school_id))
                result = cursor.fetchone()

                # Check if the course already exists
                if result is None:
                    # Course does not exist, so insert it
                    cursor.execute("INSERT INTO courses (course_name, school_id) VALUES (%s, %s)",
                                   (course_name, school_id))
                    conn.commit()
                    course_id = cursor.lastrowid
                else:
                    # Course exists, use the existing course_id
                    course_id = result[0]

                # Insert sentiment details
                cursor.execute("""
                    INSERT INTO sentiments (polarity, subjectivity, emotion, sentiment, spell_error, spell_quality)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """, (review["vcmp_polarity"], review["vcmp_subjectivity"],
                          review["vcmp_emotion"], review["vcmp_sentiment"],
                          review["vcmp_spellingerrors"], review["vcmp_spellingquality"]))
                sent_id = cursor.lastrowid  # Retrieve the last inserted sentiment ID

                # Insert rating details
                cursor.execute("""
                    INSERT INTO ratings (prof_id, course_id, sent_id, review_date, quality, difficulty, 
                                         comment, take_again, grade_achieved, thumbs_up, thumbs_down, 
                                         online_class, for_credit, attendance_mand)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (prof_id, course_id, sent_id,
                          datetime.strptime(review["date"], "%Y-%m-%d %H:%M:%S"),
                          review["quality"], review["difficulty"], review["comment"],
                          review["take_again"], review["grade"], review["thumbs_up"],
                          review["thumbs_down"], review["online_class"], review["credit"],
                          review["attendance_mandatory"]))

            # Commit all changes
            conn.commit()
            print("Data insertion complete.")
        except mysql.connector.Error as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()
