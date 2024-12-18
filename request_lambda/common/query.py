# flake8: noqa
import mysql.connector
from typing import Optional

from request_lambda.common.config import Config
from request_lambda.common.payload import Professor, Rating, Sentiment
from mysql.connector.connection import MySQLConnection, MySQLCursor

class QueryConnector:
    """ Class to manage database connection. """
    config: Config
    connection: MySQLConnection

    def __init__(self, config: Config):
        self.config = config
        self.connection = self.get_db_connector()

    def get_db_connector(self) -> mysql.connector.connect:
        """ Creates database connection and returns connector. """
        return mysql.connector.connect(host=self.config.db_host,
                                       user=self.config.db_user,
                                       password=self.config.db_password,
                                       database=self.config.db_name,
                                       port=self.config.db_port)

class QueryRunner:
    """ Class to run queries. """
    cursor: MySQLCursor

    def __init__(self, connection: MySQLConnection):
        self.cursor = connection.cursor()

    def insert_school(self, prof: Professor) -> None:
        """ Adds school to schools table. """
        query = """
            INSERT INTO schools (school_id, school_name) 
            VALUES (%s, %s) 
            ON DUPLICATE KEY UPDATE school_name = VALUES(school_name)
        """
        self.cursor.execute(query,(prof.school_id, prof.school_name))

    def insert_professor(self, prof: Professor) -> None:
        """ Adds professor to professors table. """
        query = """
            INSERT INTO professors (prof_id, prof_name, dept, avg_diff, avg_rating, 
                would_retake_rate, rating_count, school_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE prof_name=VALUES(prof_name), avg_diff=VALUES(avg_diff), 
                avg_rating=VALUES(avg_rating), would_retake_rate=VALUES(would_retake_rate), 
                rating_count=VALUES(rating_count)
        """
        self.cursor.execute(query,(prof.prof_id, prof.prof_name, prof.dept, prof.avg_diff,
                                   prof.avg_rating, prof.would_retake_rate, prof.rating_count, prof.school_id))

    def insert_request(self, prof_id: int, status: int) -> None:
        """ Adds/updates user request for prof data to requests table, where
                status 0 = in-progress,
                status 1 = complete. """
        query = """
        INSERT INTO requests (prof_id, status) 
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE write_date=CURRENT_TIMESTAMP, status=VALUES(status)"""
        self.cursor.execute(query,(prof_id, status))

    def delete_prof_reviews(self, prof: Professor) -> None:
        """ Removes stale reviews from ratings and sentiments tables. """
        self.cursor.execute("""DELETE FROM ratings WHERE prof_id = %s""", (prof.prof_id,))

    def get_course_record(self, course_name: str, school_id: int) -> Optional[tuple]:
        """ Returns course id from the course table, or None if course doesn't exist. """
        query = """
            SELECT course_id 
            FROM courses 
            WHERE course_name = %s 
                AND school_id = %s
        """
        self.cursor.execute(query,(course_name, school_id))
        return self.cursor.fetchone()

    def insert_course(self, course_name: str, school_id: int) -> None:
        """ Adds course to courses table. """
        query = """
            INSERT INTO courses (course_name, school_id) 
            VALUES (%s, %s)
        """
        self.cursor.execute(query,(course_name, school_id))

    def insert_rating(self, review: Rating) -> None:
        """ Adds review to ratings table. """
        query = """
            INSERT INTO ratings (prof_id, course_id, review_date, quality, difficulty, comment, take_again, 
                grade_achieved, thumbs_up, thumbs_down, online_class, for_credit, attendance_mand) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query,(review.prof_id, review.course_id, review.review_date,
                                   review.quality, review.difficulty, review.comment, review.take_again,
                                   review.grade_achieved, review.thumbs_up, review.thumbs_down,
                                   review.online_class, review.for_credit, review.attendance_mand))
        review.__add__(self.cursor.lastrowid)  # Capture rating id for sentiments record

    def insert_sentiment_analysis(self, sentiment: Sentiment) -> None:
        """ Adds analyzed review to sentiments table. """
        query = """
            INSERT INTO sentiments (rating_id, polarity, subjectivity, emotion, 
                sentiment, spell_error, spell_quality) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query,(sentiment.rating_id, sentiment.polarity,
                                   sentiment.subjectivity, sentiment.emotion, sentiment.sentiment,
                                   sentiment.spell_error, sentiment.spell_quality))

    def run_sql_commands(self, sql_commands: list[str]) -> None:
        """ Run each SQL command as query on database. """
        for command in sql_commands:
            # Avoid empty commands
            if command.strip():
                self.cursor.execute(command)

    def get_prof_request(self, professor_id: int) -> Optional[tuple]:
        """ Returns request record for given professor, or none if prof hasn't been processed. """
        query = """
            SELECT * 
            FROM requests 
            WHERE prof_id = %s
            ORDER BY write_date DESC
            LIMIT 1
        """
        self.cursor.execute(query,(professor_id,))
        query_result = self.cursor.fetchone()
        return query_result

    def get_prof_records(self, professor_id) -> list:
        """ Returns records matching the given professor and their analyzed ratings. """
        query = """
        SELECT 
            p.prof_id,
            p.prof_name,
            p.dept,
            p.avg_diff,
            p.avg_rating,
            p.would_retake_rate,
            p.rating_count,
            s.school_id,
            s.school_name,
            r.quality,
            r.difficulty,
            r.comment,
            r.grade_achieved,
            r.thumbs_up,
            r.thumbs_down,
            r.online_class,
            r.for_credit,
            r.attendance_mand,
            r.review_date,
            r.take_again,
            c.course_name,
            se.polarity,
            se.subjectivity,
            se.emotion,
            se.sentiment,
            se.spell_error,
            se.spell_quality
        FROM 
            professors p
        JOIN 
            ratings r ON p.prof_id = r.prof_id
        JOIN 
            schools s ON p.school_id = s.school_id
        JOIN 
            courses c ON r.course_id = c.course_id
        JOIN 
            sentiments se ON r.rating_id = se.rating_id
        WHERE 
            p.prof_id = %s;
        """
        self.cursor.execute(query, (professor_id,))
        query_results = self.cursor.fetchall()
        return query_results
