""" Script to Bootstrap Database """
import json
import os

from request_lambda.app import rmp_api
from request_lambda.app import sentiment


env_file_path = "infra/config.env"


def read_prof_ids(script_dir):
    in_file_path = os.path.join(script_dir, 'prof_ids.txt')
    try:
        # Open the file in read mode
        with open(in_file_path, 'r') as file:
            # Iterate over each line in the file
            for line in file:
                # Strip any leading/trailing whitespace and convert to integer
                prof_id = int(line.strip())
                # Process the integer
                process_prof_id(prof_id, script_dir)
    except FileNotFoundError:
        print(f"File {in_file_path} not found.")
    except ValueError:
        print(f"Error: Could not convert line to integer in {in_file_path}.")


def process_prof_id(professor_id: int, script_dir):
    # Get the data from RateMyProfessors
    try:
        professor_json = rmp_api.get_prof_data(professor_id)
    except ValueError:
        print(f"Professor with ID {professor_id} not found")

    # Analyze the data for sentiment
    professor_json = sentiment.analyze(professor_json)

    # Save prof data as a json file
    save_dict_to_json(professor_json, professor_id, script_dir)
    print(f"Saved {professor_json['name']} to a json file ({professor_id})")


def save_dict_to_json(prof_dict, prof_id, script_dir):
    # Save the dictionary as a JSON file
    folder_name = "prof_files"  # Specify the folder name
    folder_path = os.path.join(script_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"sent_{prof_id}.json")
    with open(file_path, 'w') as json_file:
        json.dump(prof_dict, json_file, indent=4)


print("Inserting sample data into files...")
script_dir = os.path.dirname(os.path.abspath(__file__))
read_prof_ids(script_dir)
