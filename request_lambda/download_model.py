import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# this code download the model and save it to app/models
model_name = "monologg/bert-base-cased-goemotions-original"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Ensure the directory exists
os.makedirs("app/models", exist_ok=True)

# Save to a local directory
tokenizer.save_pretrained("app/models/goemotions-tokenizer")
model.save_pretrained("app/models/goemotions-model")