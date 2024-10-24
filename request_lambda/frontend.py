# frontend.py
# formats and prepares professor data before it sending back in API response

# ----------------------------------------------------------------------------#
# NOTE: this file contains function stubs. In order for our code to work
# together, the stub purpose and signatures must be followed. Feel free to
# define additional functions to do parts of the work, delegate as needed.
# ----------------------------------------------------------------------------#

from typing import Dict, Any


# Format the data for the response to the front end. This may include 
# reorganization (into e.g. courses), calculating aggregate stats for prof and
# courses, and organizing the ratings under courses as well.
# NOTE: please preface all new fields with "vcmp_" in order to better 
# distingish the original data from the data we are adding. Please also clean
# up any intermediate values stored (e.g. totals from calculating averages)
def format(professor_json: Dict[str, Any]) -> Dict[str, Any]:
    # TODO
    return professor_json
