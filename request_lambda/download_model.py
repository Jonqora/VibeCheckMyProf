import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# this code download the model and save it to app/models
# model_name = "jitesh/emotion-english"
model_name = "monologg/bert-base-cased-goemotions-original"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Define the base directory relative to the script file location
base_dir = os.path.join(os.path.dirname(__file__), "lambda2/models")

# Ensure the directory exists
os.makedirs(base_dir, exist_ok=True)

# Save tokenizer and model in the base directory
tokenizer.save_pretrained(os.path.join(base_dir, "goemotions-tokenizer"))
model.save_pretrained(os.path.join(base_dir, "goemotions-model"))
