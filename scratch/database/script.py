import os
from database import Database

# Database connection details
db_endpoint = "vibe-check-my-prof.c38g806w4spe.ca-central-1.rds.amazonaws.com"
db_name = "vibe-check-my-prof"
db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_port = 3306
db = Database()

# Create connection
connection = db.create_connection(host_name=db_endpoint, user_name=db_user, user_password=db_password,
                                  db_name=db_name, port=db_port)

if connection:
    # Example: Create a table (if it doesn't exist already)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT, 
        name VARCHAR(100) NOT NULL, 
        age INT, 
        PRIMARY KEY (id)
    );
    """
    db.execute_query(connection, create_table_query)

    # Example: Insert data into the table
    insert_query = """
    INSERT INTO users (name, age)
    VALUES ('John Doe', 28), ('Jane Smith', 22);
    """
    db.execute_query(connection, insert_query)

    # Example: Select data from the table
    select_query = "SELECT * FROM users;"
    rows = db.execute_read_query(connection, select_query)

    # Print the results
    for row in rows:
        print(row)

# Close the connection when done
if connection:
    connection.close()
