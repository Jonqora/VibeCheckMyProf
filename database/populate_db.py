""" Script to Bootstrap Database """
import os
from dotenv import load_dotenv
from query_runner import QueryRunner

# Load values from config.env file
load_dotenv("./infra/config.env")

# Set values from config.env file
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host_with_port = os.getenv("DB_HOST")
db_host = db_host_with_port.split(":")[0] \
    if ":" in db_host_with_port else db_host_with_port
db_port = int(os.getenv("DB_PORT"))
create_tables_file_path = "./database/sql_files/create_tables.sql"
sample_data_file_path_1 = "./database/sample_data/sentiment_output1.json"
read_data_file_path = "./database/sql_files/read_tables.sql"
drop_tables_file_path = "./database/sql_files/drop_tables.sql"

# Initialize DB connector/query executor
print("Starting to populate database...")
qr = QueryRunner(db_name, db_user, db_host, db_port, db_password)

# Run SQL commands to create app tables
print("Executing table scripts...")
qr.run_sql_script(drop_tables_file_path)
qr.run_sql_script(create_tables_file_path)

# Run SQL commands to load sample table data
print("Inserting sample data into tables...")
qr.insert_data_from_json(sample_data_file_path_1)

print("Database bootstrap complete!")
