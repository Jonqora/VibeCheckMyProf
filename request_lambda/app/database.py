# database.py
# Interacts with backend database

# ----------------------------------------------------------------------------#
# NOTE: this file contains function stubs. In order for our code to work
# together, the stub purpose and signatures must be followed. Feel free to
# define additional functions to do parts of the work, delegate as needed.
# ----------------------------------------------------------------------------#

from typing import Dict, Any

RECENT_INTERVAL_SECONDS = 86400  # seconds in a day, adjust as needed


# Check for recent data written to the database query table, where recent is
# any request for the given prof within the last e.g. RECENT_INTERVAL_SECONDS .
# - If recent data is found, load all dict-formatted prof/ratings data for the
# queried prof from the database. Also log the current request as a non-write-
# type one in the Requests table with the prof id. Finally, return the
# dict-formatted data.
# - If recent write data is not found, return empty dict.
def get_recent_data(professor_id: int) -> Dict[str, Any]:
    # TODO
    return {}


# Given dict-formatted prof/ratings data, save all the data into prof, ratings,
# sentiment, etc. data in the backend database.
# Afterwards, log the current request as a write-type one in Requests table
# with the given prof id.
def write_data(professor_json: Dict[str, Any]) -> None:
    # TODO
    return
