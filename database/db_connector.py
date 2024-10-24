import mysql.connector
from mysql.connector import Error


class DatabaseConnector:
    def __init__(self):
        print("Database object initialized.")

    # Function to create a connection to the database
    def create_connection(self, host_name, user_name, user_password,
                          db_name, port):
        print("Creating connection.")
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                password=user_password,
                database=db_name,
                port=port)
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection

    # Function to execute a query (INSERT, UPDATE, DELETE)
    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    # Function to execute a SELECT query and fetch results
    def execute_read_query(self, connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
            return result
