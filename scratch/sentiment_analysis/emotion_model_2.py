from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json
from collections import defaultdict


# !!!
import pandas as pd


def analyze_emotion(text, tokenizer, model, emotion_labels):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)

    predictions = torch.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(predictions, dim=-1)
    predicted_emotion = emotion_labels[predicted_class.item()]
    confidence_score = predictions[0][predicted_class.item()].item()

    return predicted_emotion, confidence_score


def run_analysis(file_path):
    """
    Load test data:
    """
    with open(file_path, "r") as file:
        data_json = json.load(file)

    """
    Load emotion detection model:
    """
    tokenizer = AutoTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-original")
    model = AutoModelForSequenceClassification.from_pretrained("monologg/bert-base-cased-goemotions-original")
    model_config = model.config
    emotion_labels = model_config.id2label


    """
Analyze emotion for each comment in the data:
"""
    for entry in data_json['ratings_data']:
        comment = entry['comments']
        emotion, score = analyze_emotion(comment, tokenizer, model, emotion_labels)

        entry['emotion'] = emotion
        entry['confidence_score'] = score

    summary = defaultdict(
        lambda: {'total_reviews': 0, 'total_quality': 0, 'total_difficulty': 0, 'emotion_counts': defaultdict(int),
             'total_confidence': 0})

    for entry in data_json['ratings_data']:
        key = data_json['professor_name']  # Only consider professor's name
        summary[key]['total_reviews'] += 1
        summary[key]['total_quality'] += float(entry['quality'])
        summary[key]['total_difficulty'] += float(entry['difficulty'])
        summary[key]['emotion_counts'][entry['emotion']] += 1
        summary[key]['total_confidence'] += entry['confidence_score']
        
        
        
    # !!!! changed    
    summary_list = []
    
    for key, value in summary.items():
        total_reviews = value['total_reviews']
        avg_quality = value['total_quality'] / total_reviews
        avg_difficulty = value['total_difficulty'] / total_reviews
        avg_confidence = value['total_confidence'] / total_reviews
        emotion_distribution = dict(value['emotion_counts'])
        
        print(f"Professor: {key}")
        print(f"  Total Reviews: {total_reviews}")
        print(f"  Average Quality: {avg_quality:.2f}")
        print(f"  Average Difficulty: {avg_difficulty:.2f}")
        print(f"  Average Confidence Score: {avg_confidence:.4f}")
        print(f"  Emotion Distribution: {emotion_distribution}")
        print()

        # Append to summary list
        summary_list.append({
            "Professor": key,
            "Total Reviews": total_reviews,
            "Average Quality": avg_quality,
            "Average Difficulty": avg_difficulty,
            "Average Confidence Score": avg_confidence,
            **emotion_distribution  # Flatten emotion distribution into columns
        })

    # Convert summary list to DataFrame
    df_summary = pd.DataFrame(summary_list)
    #print("Summary DataFrame:", df_summary)  
    return df_summary


        

if __name__ == "__main__":
    file_path = "../web_scraping/prof2302527scrape.json"
    with open(file_path, "r") as file:
        data_json = json.load(file)
    run_analysis(file_path)
