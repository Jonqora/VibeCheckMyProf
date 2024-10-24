import json
from collections import defaultdict
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def analyze_sentiment(comment, analyzer):
    sentiment_dict = analyzer.polarity_scores(comment)
    return sentiment_dict



def run_analysis(file_path):
    
    # Loading Json File
    with open(file_path, "r") as file:
        data_json = json.load(file)
        
    
    # Load VADER-Sentiment-Analysis Model
    analyzer = SentimentIntensityAnalyzer()
    
    
    # Summary dict
    summary = {}
    
    
    # Run analysis for each comment
    for entry in data_json['ratings_data']:
        comment = entry['comments']
        sentiment_scores = analyze_sentiment(comment, analyzer)
        entry['sentiment_scores'] = sentiment_scores
        
        print(sentiment_scores)
        professor_name = data_json['professor_name']
        
        
    summary = defaultdict(
        lambda: {
            'total_reviews': 0,
            'total_quality': 0,
            'total_difficulty': 0,
            'vader_compound_scores': [],
            'vader_positive_scores': [],
            'vader_negative_scores': [],
            'vader_neutral_scores': []
        }
    )
            
    
    # Update summary for the professor
    for entry in data_json['ratings_data']:
        key = data_json['professor_name']
        summary[key]['total_reviews'] += 1
        summary[key]['total_quality'] += float(entry['quality'])
        summary[key]['total_difficulty'] += float(entry['difficulty'])

        
        # Append VADER sentiment scores
        summary[key]['vader_compound_scores'].append(sentiment_scores['compound'])
        summary[professor_name]['vader_positive_scores'].append(sentiment_scores['pos'])
        summary[professor_name]['vader_negative_scores'].append(sentiment_scores['neg'])
        summary[professor_name]['vader_neutral_scores'].append(sentiment_scores['neu'])
        
        
    # New dict
    summary_list = []
        
    for professor, value in summary.items():
        total_reviews = value['total_reviews']
        avg_quality = value['total_quality'] / total_reviews
        avg_difficulty = value['total_difficulty'] / total_reviews
        avg_vader_compound = sum(value['vader_compound_scores']) / total_reviews
        avg_vader_positive = sum(value['vader_positive_scores']) / total_reviews
        avg_vader_negative = sum(value['vader_negative_scores']) / total_reviews
        avg_vader_neutral = sum(value['vader_neutral_scores']) / total_reviews
            
            
        # taking average of all the scores
        summary_list.append({
            "Professor": professor,
            "Total Reviews": total_reviews,
            "Avg Quality": avg_quality,
            "Avg Difficulty": avg_difficulty,
            "Avg VADER Compound Score": avg_vader_compound,
            "Avg VADER Positive Score": avg_vader_positive,
            "Avg VADER Negative Score": avg_vader_negative,
            "Avg VADER Neutral Score": avg_vader_neutral
        })
            
            
    summary_df = pd.DataFrame(summary_list)
    return summary_df
        