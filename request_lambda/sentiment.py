# sentiment.py
# Process professor data and have sentiment analysis added to it

# ----------------------------------------------------------------------------#
# NOTE: this file contains function stub(s). In order for our code to work
# together, the stub purpose and signatures must be followed. Feel free to
# define additional functions to do parts of the work, delegate as needed.
# ----------------------------------------------------------------------------#

from typing import Dict, Any


# Compute and add sentiment field into every professor rating
def analyze(professor_json: Dict[str, Any]) -> Dict[str, Any]:
    # TODO
    for review in professor_json["reviews"]:
        review["sentiment"] = "placeholder"

    return professor_json
