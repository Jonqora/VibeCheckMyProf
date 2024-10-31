""" Script to Clean Up Database """
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
drop_tables_file_path = "./database/sql_files/drop_tables.sql"

# Initialize DB connector/query executor
print("Starting to clean up database...")
qr = QueryRunner(db_name, db_user, db_host, db_port, db_password)

# Run SQL commands to drop app tables
print("Dropping tables...")
qr.run_sql_script(drop_tables_file_path)

print("Database clean up complete!")
