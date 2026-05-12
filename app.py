import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh
import os


# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="News Sentiment Dashboard", layout="wide")

st.title("📰 News Sentiment Dashboard")
st_autorefresh(interval=300000,
               key="dashboard_refresh")

# -------------------------------
# DB CONNECTION
# -------------------------------
@st.cache_resource
def get_connection():
    return psycopg2.connect(
    host="news-postgres.crkycwwa6j6q.ap-south-1.rds.amazonaws.com",
    database="postgres",
    user="postgres",
    password="postgres1818"
    )
    
        

conn = get_connection()

# -------------------------------
# LOAD DATA
# -------------------------------
def load_data():
    query = """
    SELECT title, published_at, sentiment, sentiment_label
    FROM news
    ORDER BY published_at DESC
    LIMIT 200;
    """
    df = pd.read_sql(query, conn)

    # Clean nulls
    df = df.dropna(subset=['sentiment', 'sentiment_label'])

    return df

df = load_data()

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("Filters")

sentiment_filter = st.sidebar.selectbox(
    "Select Sentiment",
    ["All", "POSITIVE", "NEGATIVE", "NEUTRAL"]
)

# Apply filter
if sentiment_filter != "All":
    df = df[df["sentiment_label"] == sentiment_filter]

# -------------------------------
# METRICS
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

total_news = len(df)
positive_count = (df['sentiment_label'] == 'POSITIVE').sum()
negative_count = (df['sentiment_label'] == 'NEGATIVE').sum()
neutral_count = (df['sentiment_label'] == 'NEUTRAL').sum()

col1.metric("Total News", total_news)
col2.metric("Positive", positive_count)
col3.metric("Negative", negative_count)
col4.metric("Neutral", neutral_count)

st.markdown("---")

# -------------------------------
# TABLE
# -------------------------------
st.subheader("📋 Latest News")

st.dataframe(
    df,
    use_container_width=True,
    height=400
)

# -------------------------------
# SENTIMENT DISTRIBUTION (BAR)
# -------------------------------
st.subheader("📊 Sentiment Distribution")

sentiment_counts = df['sentiment_label'].value_counts()

fig, ax = plt.subplots()
sentiment_counts.plot(kind='bar', ax=ax)
ax.set_xlabel("Sentiment")
ax.set_ylabel("Count")
ax.set_title("Sentiment Distribution")

st.pyplot(fig)

# -------------------------------
# SENTIMENT OVER TIME
# -------------------------------
st.subheader("📈 Sentiment Trend Over Time")

df['published_at'] = pd.to_datetime(df['published_at'],
                                    errors='coerce')
df=df.dropna(subset=['published_at'])

# Group by hour/day
trend_df = df.groupby(
    pd.Grouper(key='published_at', freq='h')
)['sentiment'].mean()

fig2, ax2 = plt.subplots()
trend_df.plot(ax=ax2)
ax2.set_title("Average Sentiment Over Time")
ax2.set_xlabel("Time")
ax2.set_ylabel("Sentiment Score")

st.pyplot(fig2)

# -------------------------------
# TOP POSITIVE & NEGATIVE NEWS
# -------------------------------
st.subheader("🔥 Top Insights")

col1, col2 = st.columns(2)

with col1:
    st.write("### 🟢 Most Positive News")
    top_positive = df.sort_values(by='sentiment', ascending=False).head(5)
    st.write(top_positive[['title', 'sentiment']])

with col2:
    st.write("### 🔴 Most Negative News")
    top_negative = df.sort_values(by='sentiment').head(5)
    st.write(top_negative[['title', 'sentiment']])