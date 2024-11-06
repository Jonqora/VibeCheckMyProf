""" Script to Clean Up Database """
from request_lambda.common.config import Config
from request_lambda.common import database

env_file_path = "infra/config.env"
drop_tables_file_path = \
    "request_lambda/database_init/sql_files/drop_tables.sql"

print("Dropping tables...")
config = Config().from_file(env_file_path)
database.run_sql_file(drop_tables_file_path, config)
print("Database clean up complete!")
