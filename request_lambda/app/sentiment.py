# sentiment.py
# Process professor data and have sentiment analysis added to it

# ----------------------------------------------------------------------------#
# NOTE: this file contains function stub(s). In order for our code to work
# together, the stub purpose and signatures must be followed. Feel free to
# define additional functions to do parts of the work, delegate as needed.
# ----------------------------------------------------------------------------#

from typing import Dict, Any

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from textblob import TextBlob
import boto3
from spellchecker import SpellChecker


class SentimentAnalyzer:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-original")
        self.model = AutoModelForSequenceClassification.from_pretrained("monologg/bert-base-cased-goemotions-original")
        self.emotion_labels = self.model.config.id2label
        self.comprehend = boto3.client('comprehend', region_name="ca-central-1")
        self.spellchecker = SpellChecker()

    def analyze_sentiment_textblob(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        return polarity, subjectivity

    def analyze_emotion_goemotions(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        predictions = torch.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(predictions, dim=-1).item()
        predicted_emotion = self.emotion_labels[predicted_class]
        return predicted_emotion

    def analyze_spelling_and_grammar(self, text):
        misspelled_words = self.spellchecker.unknown(text.split())
        quality = 1 - (len(misspelled_words) / len(text.split())) if len(text.split()) > 0 else 1
        return quality, len(misspelled_words)

    def analyze_sentiment_comprehend(self, text):
        response = self.comprehend.detect_sentiment(Text=text, LanguageCode='en')
        return response['Sentiment']


# Compute and add sentiment fields into every professor rating. The only
# changes to the json input should be the addition of new fields on each of
# the ratings objects with associated values from analysis.
# NOTE: please preface all new fields with "vcmp_" in order to better
# distingish the original data from the data we are adding.
def analyze(professor_json: Dict[str, Any]) -> Dict[str, Any]:
    sentiment_analyzer = SentimentAnalyzer()

    for review in professor_json["reviews"]:
        comment = review["comment"]

        tb_polarity, tb_subjectivity = sentiment_analyzer.analyze_sentiment_textblob(comment)
        emotion = sentiment_analyzer.analyze_emotion_goemotions(comment)
        comprehend_sentiment = sentiment_analyzer.analyze_sentiment_comprehend(comment)
        spelling_quality, spelling_errors = sentiment_analyzer.analyze_spelling_and_grammar(comment)

        review["vcmp_polarity"] = tb_polarity
        review["vcmp_subjectivity"] = tb_subjectivity
        review["vcmp_emotion"] = emotion
        review["vcmp_sentiment"] = comprehend_sentiment
        review["vcmp_spellingerrors"] = spelling_errors
        review["vcmp_spellingquality"] = spelling_quality

    return professor_json
