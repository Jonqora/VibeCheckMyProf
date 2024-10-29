import json
import os
import random
import re
import sys


def modify_json(input_filename):
    """Read JSON file, add new fields, and save it under a new name."""
    if not os.path.exists(input_filename):
        print(f"File {input_filename} not found.")
        return

    # Extract the ID number from the input filename using regex
    match = re.search(r'(\d+)', input_filename)
    if not match:
        print("ID number not found in the filename.")
        return

    # Get the ID number and construct the output filename
    id_number = match.group(1)
    output_filename = f"sentiment_{id_number}.json"

    # Read the JSON file into a nested dict
    with open(input_filename, 'r') as infile:
        data = json.load(infile)

    # Update the dictionary with the new fields
    data = add_sentiment(data)

    # Write the modified dictionary to the new file
    with open(output_filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    print(f"Modified data saved to {output_filename}")


def add_sentiment(data):
    """Add random sentiment-related fields to the data."""
    emotions = [
        "admiration", "amusement", "anger", "annoyance", "approval",
        "caring", "confusion", "curiosity", "desire", "disappointment",
        "disapproval", "disgust", "embarrassment", "excitement", "fear",
        "gratitude", "grief", "joy", "love", "nervousness", "optimism",
        "pride", "realization", "relief", "remorse", "sadness", "surprise"
    ]
    sentiments = ["positive", "negative", "neutral", "mixed"]
    spelling_errors = [0, 0, 0, 0, 0, 0, 1, 1, 2, 3]

    for review in data["reviews"]:
        review["vcmp_polarity"] = round(random.random(), 4)
        review["vcmp_subjectivity"] = round(random.random(), 4)
        review["vcmp_emotion"] = random.choice(emotions)
        review["vcmp_sentiment"] = random.choice(sentiments)
        review["vcmp_spellingerrors"] = random.choice(spelling_errors)
        review["vcmp_spellingquality"] = round(random.uniform(0.85, 1), 4)

    return data


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_filename>")
    else:
        input_filename = sys.argv[1]
        modify_json(input_filename)
