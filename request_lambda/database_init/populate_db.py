""" Script to Bootstrap Database """
from request_lambda.app.config import Config
from request_lambda.app import database

env_file_path = "infra/config.env"
drop_tables_file_path = \
    "request_lambda/database_init/sql_files/drop_tables.sql"
create_tables_file_path = \
    "request_lambda/database_init/sql_files/create_tables.sql"
sample_data_file_path1 = \
    "request_lambda/database_init/sample_data/sentiment_output1.json"

print("Removing old tables from database...")
config = Config().from_file(env_file_path)
database.run_sql_file(drop_tables_file_path, config)

print("Creating tables...")
database.run_sql_file(create_tables_file_path, config)

print("Inserting sample data into tables...")
database.insert_data_from_json_file(sample_data_file_path1, config)
