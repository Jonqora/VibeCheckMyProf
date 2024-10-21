import json
import pandas as pd
from flair.data import Sentence
from flair.models import TextClassifier
from collections import Counter



def analyze_sentiment(comment, classifier):
    
    # Flair Sentence
    sentence = Sentence(comment)
    
    # Predict sentiment
    classifier.predict(sentence)
    
    # Return the sentiment label and score
    return sentence.labels[0].value, sentence.labels[0].score




def run_analysis(file_path):
    # Load JSON file
    with open(file_path, "r") as file:
        data_json = json.load(file)
        
    # Load Flair Sentiment Classifier
    classifier = TextClassifier.load('sentiment')
    
    # Summary dictionary
    summary = {}
    
    # Run analysis for each comment
    for entry in data_json['ratings_data']:
        comment = entry['comments']
        sentiment_label, sentiment_score = analyze_sentiment(comment, classifier)
        entry['sentiment_label'] = sentiment_label
        entry['sentiment_score'] = sentiment_score
        
        print(f"Sentiment: {sentiment_label}, Score: {sentiment_score}")
        
        # Professor's name
        professor_name = data_json['professor_name']
        
        if professor_name not in summary:
            summary[professor_name] = {
                'total_reviews': 0,
                'total_quality': 0,
                'total_difficulty': 0,
                'sentiment_scores': [],
                'sentiment_labels': []
            }
        
        # Update summary for the professor
        summary[professor_name]['total_reviews'] += 1
        summary[professor_name]['total_quality'] += float(entry['quality'])
        summary[professor_name]['total_difficulty'] += float(entry['difficulty'])
        summary[professor_name]['sentiment_scores'].append(sentiment_score)
        summary[professor_name]['sentiment_labels'].append(sentiment_label)
        
        
    # Create summary DataFrame
    summary_list = []
    for professor, value in summary.items():
        total_reviews = value['total_reviews']
        avg_quality = value['total_quality'] / total_reviews
        avg_difficulty = value['total_difficulty'] / total_reviews
        avg_sentiment_score = sum(value['sentiment_scores']) / total_reviews
        
        # Highest counted label
        sentiment_counter = Counter(value['sentiment_labels'])
        highest_count_label = sentiment_counter.most_common(1)[0][0]
        
        summary_list.append({
            "Professor": professor,
            "Total Reviews": total_reviews,
            "Avg Quality": avg_quality,
            "Avg Difficulty": avg_difficulty,
            "Avg Sentiment Score": avg_sentiment_score,
            "Highest Count Label": highest_count_label
        })
    
    summary_df = pd.DataFrame(summary_list)
    return summary_df




