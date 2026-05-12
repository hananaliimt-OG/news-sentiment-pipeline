def save_to_postgres(data):
    import psycopg2
    import os

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=5432
    )

    cursor = conn.cursor()

    for article in data:
        cursor.execute(
            """
            INSERT INTO news(title, description, published_at, sentiment, sentiment_label)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (title)
            DO UPDATE SET
                sentiment = EXCLUDED.sentiment,
                sentiment_label = EXCLUDED.sentiment_label;
            """,
            (
                article["title"],
                article["description"],
                article["published_at"],
                article["sentiment"],
                article["sentiment_label"]
            )
        )

    conn.commit()
    cursor.close()
    conn.close()

    print("Data saved to PostgreSQL")