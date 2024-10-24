import subprocess
import warnings
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalysis:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.tokenizer = AutoTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-original")
        self.model = AutoModelForSequenceClassification.from_pretrained("monologg/bert-base-cased-goemotions-original")
        self.emotion_labels = self.model.config.id2label
        self.data_json = self.load_json()
        self.tool = self.initialize_language_tool()

    def load_json(self):
        with open(self.json_file_path, "r") as file:
            return json.load(file)

    def initialize_language_tool(self):
        try:
            subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT)
            import language_tool_python
            return language_tool_python.LanguageTool('en-US')
        except (subprocess.CalledProcessError, FileNotFoundError):
            warnings.warn("Java is not installed or not found. Spelling and grammar analysis will be skipped.")
            return None

    def analyze_sentiment_textblob(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        return polarity, subjectivity

    def analyze_sentiment_vader(self, text):
        scores = self.vader_analyzer.polarity_scores(text)
        return scores['compound'], scores['pos'], scores['neu'], scores['neg']

    def analyze_emotion_goemotions(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        predictions = torch.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(predictions, dim=-1).item()
        predicted_emotion = self.emotion_labels[predicted_class]
        confidence_score = predictions[0][predicted_class].item()
        return predicted_emotion, confidence_score

    def analyze_spelling_and_grammar(self, text):
        if self.tool is None:
            return 1, 0, []
        matches = self.tool.check(text)
        misspelled_words = []
        for match in matches:
            if len(match.replacements) > 0:
                misspelled_words.append((text[match.offset: match.offset + match.errorLength], match.replacements[0]))
        seriousness = 1 - (len(misspelled_words) / len(text.split())) if len(text.split()) > 0 else 1
        return seriousness, len(misspelled_words), misspelled_words

    def process_data(self):
        for entry in self.data_json['ratings_data']:
            comment = entry['comments']

            tb_polarity, tb_subjectivity = self.analyze_sentiment_textblob(comment)
            vader_polarity, vader_pos, vader_neu, vader_neg = self.analyze_sentiment_vader(comment)
            emotion, confidence = self.analyze_emotion_goemotions(comment)
            seriousness, misspelled_count, incorrect_words = self.analyze_spelling_and_grammar(comment)

            entry['textblob_polarity'] = tb_polarity
            entry['textblob_subjectivity'] = tb_subjectivity
            entry['vader_polarity'] = vader_polarity
            entry['vader_positive'] = vader_pos
            entry['vader_neutral'] = vader_neu
            entry['vader_negative'] = vader_neg
            entry['goemotions_emotion'] = emotion
            entry['goemotions_confidence'] = confidence
            entry['spelling_seriousness'] = seriousness

        for entry in self.data_json['ratings_data']:
            print(entry)

def main():
    json_file_path = '../web_scraping/prof2302527scrape.json'
    sentiment_analysis = SentimentAnalysis(json_file_path)
    sentiment_analysis.process_data()

if __name__ == "__main__":
    main()


