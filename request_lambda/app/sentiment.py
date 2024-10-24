# sentiment.py
# Process professor data and have sentiment analysis added to it

# ----------------------------------------------------------------------------#
# NOTE: this file contains function stub(s). In order for our code to work
# together, the stub purpose and signatures must be followed. Feel free to
# define additional functions to do parts of the work, delegate as needed.
# ----------------------------------------------------------------------------#

from typing import Dict, Any


# Compute and add sentiment fields into every professor rating. The only
# changes to the json input should be the addition of new fields on each of
# the ratings objects with associated values from analysis.
# NOTE: please preface all new fields with "vcmp_" in order to better
# distingish the original data from the data we are adding.
def analyze(professor_json: Dict[str, Any]) -> Dict[str, Any]:
    # TODO # for example...
    for review in professor_json["reviews"]:
        review["vcmp_sentiment"] = "placeholder"
        review["vcmp_emotion"] = "anger"
        review["vcmp_objectivity"] = 3.0

    return professor_json
