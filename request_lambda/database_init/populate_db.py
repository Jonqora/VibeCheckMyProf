""" Script to Bootstrap Database """
import os

from request_lambda.app.config import Config
from request_lambda.app import database


env_file_path = "infra/config.env"
drop_tables_file_path = \
    "request_lambda/database_init/sql_files/drop_tables.sql"
create_tables_file_path = \
    "request_lambda/database_init/sql_files/create_tables.sql"
sample_data_file_path1 = \
    "request_lambda/database_init/sample_data/sentiment_output1.json"


def process_json_files_in_folder(folder_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, folder_name)

    # Ensure the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_name}' does not exist.")
        return

    # Iterate over all files in the specified folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Check if the file is a JSON file
        if filename.endswith('.json'):
            database.insert_data_from_json_file(file_path, config)
            print(f"Inserted data from {filename}")


print("Removing old tables from database...")
config = Config().from_file(env_file_path)
database.run_sql_file(drop_tables_file_path, config)

print("Creating tables...")
database.run_sql_file(create_tables_file_path, config)

print("Inserting sample data into tables...")
process_json_files_in_folder("prof_files")
