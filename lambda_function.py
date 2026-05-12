import json
import os
from datetime import datetime
import requests
import psycopg2

from storage.s3 import upload_to_s3
from db.postgres import save_to_postgres

# Environment variable
API_KEY = os.getenv("NEWS_API_KEY")

# API URL
URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"


# -------- SIMPLE SENTIMENT FUNCTION --------
def get_sentiment(text):
    positive_words = [
        "good", "great", "excellent", "positive", "growth",
        "profit", "success", "win", "increase", "improve", "best", "strong"
    ]

    negative_words = [
        "bad", "poor", "negative", "loss", "fail",
        "drop", "decline", "fall", "crisis", "worst", "risk", "weak"
    ]

    text = text.lower()
    score = 0

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    if score > 0:
        return score, "POSITIVE"
    elif score < 0:
        return score, "NEGATIVE"
    else:
        return score, "NEUTRAL"


def run_pipeline():
    print("Starting pipeline...")

    # -------- CALL API --------
    response = requests.get(URL)

    if response.status_code != 200:
        raise Exception(f"API failed: {response.status_code} - {response.text}")

    data = response.json()

    # -------- SET TIME --------
    now = datetime.now()

    folder_path = f"/tmp/data/{now.year}/{now.month:02d}/{now.day:02d}"
    os.makedirs(folder_path, exist_ok=True)

    # -------- SAVE RAW DATA --------
    raw_filename = f"{folder_path}/news_raw_{now.strftime('%H-%M-%S')}.json"

    with open(raw_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Raw data saved:", raw_filename)

    # -------- PROCESS DATA --------
    articles = data.get("articles", [])
    cleaned_articles = []

    for article in articles:
        title = article.get("title")
        description = article.get("description") or "No Description"
        published_at_raw = article.get("publishedAt")

        if not title:
            continue

        published_at = None

        if published_at_raw:
            try:
                published_at = datetime.strptime(
                    published_at_raw, "%Y-%m-%dT%H:%M:%SZ"
                )
            except Exception as e:
                print("Date parsing error:", published_at_raw, e)

        # -------- SENTIMENT (LOCAL) --------
        text = title + " " + description
        sentiment_score, sentiment_label = get_sentiment(text)

        # -------- FINAL DATA --------
        cleaned_articles.append({
            "title": title,
            "description": description,
            "published_at": published_at,
            "sentiment": sentiment_score,
            "sentiment_label": sentiment_label
        })

    # -------- SAVE PROCESSED DATA --------
    processed_filename = f"{folder_path}/processed_{now.strftime('%H-%M-%S')}.json"

    with open(processed_filename, "w", encoding="utf-8") as f:
        json.dump(cleaned_articles, f, indent=4, default=str)

    print("Processed data saved:", processed_filename)

    # -------- UPLOAD TO S3 --------
    upload_to_s3(processed_filename, "news-pipeline-bucket-awshanan")

    # -------- SAVE TO POSTGRES --------
    save_to_postgres(cleaned_articles)

    print("Pipeline completed successfully")


# -------- LAMBDA ENTRY POINT --------
def lambda_handler(event, context):
    run_pipeline()

    return {
        "statusCode": 200,
        "body": json.dumps("Pipeline executed successfully")
    }