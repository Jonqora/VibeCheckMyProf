# flake8: noqa
# test_database.py
import mysql.connector

from request_lambda.common.config import TSuiteConfig
from request_lambda.common.database import (insert_data_from_json_file,
                                            get_data_from_db,
                                            run_sql_file)


class TestDatabaseFunctions:
    """ Class for testing behavior of database functions.

        REQUIRES: DB instance created in AWS using terraform.
                  AWS credentials configured.

        To run test suite, type 'pytest' in terminal.
        Tests may take a few minutes to run."""

    @classmethod
    def setup_class(cls):
        """ Sets up database dependencies for testing environment. """
        # Create connection for test database
        cls.config = TSuiteConfig.from_file("infra/config.env")
        cls.connection = mysql.connector.connect(
            host=cls.config.db_host,
            user=cls.config.db_user,
            password=cls.config.db_password,
            port=cls.config.db_port
        )
        cls.cursor = cls.connection.cursor()

        # Create a test schema
        cls.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {cls.config.db_name}")
        cls.cursor.execute(f"USE {cls.config.db_name}")

        # Commit changes
        cls.connection.commit()

        # Create tables in test schema
        run_sql_file("request_lambda/database_init/sql_files/create_tables.sql",
                     cls.config)

        # Insert sample data for tests
        insert_data_from_json_file(
            "request_lambda/tests/valid_payloads/analyzed_prof_1835982.json",
            cls.config)
        insert_data_from_json_file(
            "request_lambda/tests/valid_payloads/analyzed_prof_2302527.json",
            cls.config)
        insert_data_from_json_file(
            "request_lambda/tests/valid_payloads/analyzed_prof_511007.json",
            cls.config)

    @classmethod
    def teardown_class(cls):
        """ Removes testing environment. """
        run_sql_file("request_lambda/database_init/sql_files/drop_tables.sql", cls.config)
        cls.cursor.execute(f"DROP DATABASE IF EXISTS {cls.config.db_name}")
        cls.cursor.close()
        cls.connection.close()

    def setup_method(self):
        """ Starts a transaction before each test to isolate changes. """
        self.connection.start_transaction()

    def teardown_method(self):
        """ Rolls back any changes made during each test. """
        self.connection.rollback()

    def test_get_recent_data_prof1(self):
        """ Tests database.get_recent_data returns a dict with the correct data in it. """
        professor_id = 1835982
        result = get_data_from_db(professor_id, self.config)

        assert isinstance(result, dict), "Result should be a dictionary"
        assert result["professor_id"] == 1835982, "Professor ID should match the inserted record"
        assert result["name"] == "Ben Williams", "Professor name should match the inserted record"
        assert result["school_id"] == 1413, "School ID should match the inserted record"
        assert result["school_name"] == "University of British Columbia", \
            "School name should match the inserted record"
        assert result["reviews"][0]["class_name"] == "MATH221", \
            "Course name for 1st review should match the inserted record"
        assert result["reviews"][4]["class_name"] == "MATH220", \
            "Course name for 3rd review should match the inserted record"
        assert result["reviews"][25]["class_name"] == "MATH221", \
            "Course name for 26th review should match the inserted record"

    def test_get_recent_data_prof2(self):
        professor_id = 2302527
        result = get_data_from_db(professor_id, self.config)

        assert isinstance(result, dict), "Result should be a dictionary"
        assert result["professor_id"] == 2302527, "Professor ID should match the inserted record"
        assert result["name"] == "Cinda Heeran", "Professor name should match the inserted record"
        assert result["school_id"] == 1413, "School ID should match the inserted record"
        assert result["school_name"] == "University of British Columbia", \
            "School name should match the inserted record"
        assert result["reviews"][0]["class_name"] == "CPSC221", \
            "Course name for 1st review should match the inserted record"
        assert result["reviews"][1]["class_name"] == "CPSC203", \
            "Course name for 2nd review should match the inserted record"

    def test_get_recent_data_prof3(self):
        professor_id = 511007
        result = get_data_from_db(professor_id, self.config)

        assert isinstance(result, dict), "Result should be a dictionary"
        assert result["professor_id"] == 511007, "Professor ID should match the inserted record"
        assert result["name"] == "Cinda Heeran", "Professor name should match the inserted record"
        assert result["school_id"] == 1112, "School ID should match the inserted record"
        assert result["school_name"] == "University Of Illinois at Urbana - Champaign", \
            "School name should match the inserted record"
        assert result["reviews"][0]["class_name"] == "CS121", \
            "Course name for 1st review should match the inserted record"

    def test_double_write_no_duplicates_prof1(self):
        """ Tests repeat writes of the same prof data does not result in duplicates. """
        # Insert Williams 3 times
        insert_data_from_json_file("request_lambda/tests/valid_payloads/analyzed_prof_1835982.json",
                                   self.config)
        insert_data_from_json_file("request_lambda/tests/valid_payloads/analyzed_prof_1835982.json",
                                   self.config)

        # Query for inserted data
        self.cursor.execute("SELECT * FROM professors WHERE prof_id = 1835982")
        result = self.cursor.fetchall()

        assert result is not None, "Professor data should be inserted into the table."
        assert result[0][1] == "Ben Williams", "Professor name should match the inserted record"

    def test_double_write_no_duplicates_prof2(self):
        # Insert each Cinda 2 times
        insert_data_from_json_file("request_lambda/tests/valid_payloads/analyzed_prof_511007.json",
                                   self.config)
        insert_data_from_json_file("request_lambda/tests/valid_payloads/analyzed_prof_2302527.json",
                                   self.config)

        # Query for inserted data
        self.cursor.execute("SELECT * FROM professors WHERE prof_id = 511007")
        result = self.cursor.fetchall()

        # Should return Cinda's record for University of Illinois
        assert result is not None, "Professor data should be inserted into the table."
        assert result[0][1] == "Cinda Heeran", "Professor name should match the inserted record"
        assert result[0][7] == 1112, "Professor school_id should match inserted record"

        # Query for inserted data
        self.cursor.execute(f"SELECT * FROM professors WHERE prof_name = 'Cinda Heeran'")
        result = self.cursor.fetchall()

        assert result is not None, "Professor data should be inserted into the table."
        assert len(result) == 2, "There should be 2 records in the table."

    def test_changed_data_captured(self):
        """ Tests table counts reflect changed professor record. """
        # Insert updated version of Williams
        insert_data_from_json_file(
            "request_lambda/tests/valid_payloads/analyzed_prof_1835982_updated.json",
            self.config)

        # Query for inserted data
        self.cursor.execute("SELECT * FROM professors WHERE prof_id = 1835982")
        result = self.cursor.fetchall()

        # Should return updated William's record only
        assert result is not None, "Professor data should be inserted into the table."
        assert len(result) == 1, "There should be 1 record in the table."
        assert result[0][3] == 2.0, "Professor difficulty rating should be updated."

        # Query for inserted data
        self.cursor.execute(f"SELECT count(*) FROM ratings WHERE prof_id = 1835982")
        result = self.cursor.fetchall()

        assert result is not None, "Rating data should be inserted into the table."
        assert len(result) == 1, "There should be 1 rating in the table."

    def test_table_counts_correct(self):
        """ Tests table counts correct after multiple inserts of duplicate data. """
        # Insert updated version of Williams
        insert_data_from_json_file(
            "request_lambda/tests/valid_payloads/analyzed_prof_1835982_updated.json",
            self.config)
        # Re-insert Cindas
        insert_data_from_json_file(
            "request_lambda/tests/valid_payloads/analyzed_prof_511007.json",
            self.config)
        insert_data_from_json_file(
            "request_lambda/tests/valid_payloads/analyzed_prof_2302527.json",
            self.config)

        # Check school table record count
        self.cursor.execute(f"SELECT * FROM schools")
        result = self.cursor.fetchall()
        assert len(result) == 2, "There should be 2 schools in the school table."

        # Check professors table record count
        self.cursor.execute(f"SELECT * FROM professors")
        result = self.cursor.fetchall()
        assert len(result) == 3, "There should be 3 profs in the professors table."

        # Check requests table record count
        self.cursor.execute(f"SELECT * FROM requests")
        result = self.cursor.fetchall()
        assert len(result) == 3, "There should be 3 records in the requests table."

        # Check courses table record count
        self.cursor.execute(f"SELECT * FROM courses")
        result = self.cursor.fetchall()
        assert len(result) == 10, "There should be 10 records in the courses table."

        # Check ratings table record count
        self.cursor.execute(f"SELECT * FROM ratings")
        result = self.cursor.fetchall()
        assert len(result) == 4, "There should be 4 records in the ratings table."

        # Check sentiments table record count
        self.cursor.execute(f"SELECT * FROM sentiments")
        result = self.cursor.fetchall()
        assert len(result) == 4, "There should be 4 records in the sentiments table."
