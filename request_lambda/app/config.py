import os

from dataclasses import field, dataclass
from dotenv import load_dotenv


@dataclass
class Config:
    """ Class to store database configuration attributes. """
    db_name: str = field(init=False)
    db_user: str = field(init=False)
    db_port: int = field(init=False)
    db_host: str = field(init=False)
    db_password: str = field(init=False)
    rec_int_sec: int = field(init=False)
    batch_size: int = field(init=False)

    @classmethod
    def from_env(cls) -> "Config":
        """ Factory method to initialize from environment variables. """
        obj = cls()
        obj.db_name = os.environ['DB_NAME']
        obj.db_user = os.environ['DB_USER']
        obj.db_port = int(os.environ['DB_PORT'])
        db_host_port = os.environ['DB_HOST']
        obj.db_host = db_host_port.split(":")[0] \
            if ":" in db_host_port else db_host_port
        obj.rec_int_sec = int(os.environ['SECOND_INTERVAL'])
        obj.db_password = os.environ["DB_PASSWORD"]
        obj.batch_size = int(os.environ['BATCH_SIZE'], 8)
        return obj

    @classmethod
    def from_file(cls, env_file_path: str) -> "Config":
        """ Factory method to initialize from configuration file. """
        load_dotenv(env_file_path)

        obj = cls()
        obj.db_name = os.getenv("DB_NAME")
        obj.db_user = os.getenv("DB_USER")
        obj.db_password = os.getenv("DB_PASSWORD")
        db_host_with_port = os.getenv("DB_HOST")
        obj.db_host = db_host_with_port.split(":")[0] \
            if ":" in db_host_with_port else db_host_with_port
        obj.rec_int_sec = int(os.getenv("SECOND_INTERVAL",
                                        604800))  # Default to 1 week
        obj.db_port = int(os.getenv("DB_PORT", "3306"))  # Default port 3306
        obj.batch_size = int(os.getenv("BATCH_SIZE", 8))
        return obj


@dataclass
class TSuiteConfig(Config):
    """ Class to store test db config attributes for test suite. """

    @classmethod
    def from_env(cls) -> "TSuiteConfig":
        """ Factory method to initialize from env for test suite. """
        obj = super().from_env()
        obj.db_name = f"""{obj.db_name}test"""
        return obj

    @classmethod
    def from_file(cls, env_file_path: str) -> "TSuiteConfig":
        """ Factory method to initialize from file for test suite. """
        obj = super().from_file(env_file_path)
        obj.db_name = f"""{obj.db_name}test"""
        return obj
