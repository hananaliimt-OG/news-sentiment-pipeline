# 📰 News Sentiment Pipeline

A real-time cloud-based news sentiment analysis pipeline built using AWS and Python.

This project automatically collects news articles, performs sentiment analysis, stores processed data in cloud storage and databases, and visualizes insights through a live Streamlit dashboard deployed using Docker and Amazon ECS.

---

# 🚀 Project Overview

The pipeline performs the following workflow automatically:

1. Fetches live news articles using News API
2. Processes and cleans article data
3. Performs sentiment analysis using Python
4. Stores raw and processed data in Amazon S3
5. Inserts processed results into PostgreSQL (Amazon RDS)
6. Triggers automated execution using AWS Lambda and EventBridge
7. Displays live analytics through a Streamlit dashboard
8. Deploys the dashboard container using Docker + Amazon ECS Fargate

---

# 🏗️ Architecture

News API  
↓  
AWS Lambda  
↓  
Sentiment Analysis (Python)  
↓  
Amazon S3 + Amazon RDS PostgreSQL  
↓  
Streamlit Dashboard  
↓  
Docker Container  
↓  
Amazon ECS Fargate

---

# ⚙️ Technologies Used

## Cloud Services
- AWS Lambda
- Amazon EventBridge
- Amazon ECS Fargate
- Amazon ECR
- Amazon RDS PostgreSQL
- Amazon S3
- CloudWatch

## Backend & Data
- Python
- Pandas
- Psycopg2
- PostgreSQL

## Visualization
- Streamlit
- Matplotlib

## DevOps
- Docker
- GitHub

---

# 📊 Dashboard Features

- Live sentiment monitoring
- Positive / Negative / Neutral classification
- Sentiment trend visualization
- Real-time database updates
- Interactive news table
- Auto-refresh dashboard every 5 minutes

---

# 🔄 Automation Flow

EventBridge automatically triggers the AWS Lambda function every 5 minutes.

The Lambda function:
- Fetches latest news
- Processes sentiment
- Uploads JSON files to S3
- Stores structured data in PostgreSQL

The Streamlit dashboard then visualizes the updated data in real time.

---

# 🐳 Docker Deployment

The Streamlit application was containerized using Docker and deployed to Amazon ECS Fargate for scalable cloud hosting.

---

# 📁 Project Structure

```bash
news-sentiment-pipeline/
│
├── db/
├── storage/
├── app.py
├── lambda_function.py
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 🔐 Security

Sensitive credentials and API keys are managed using environment variables and are excluded from GitHub using `.gitignore`.

---

# 📌 Future Improvements

- Add advanced NLP models
- Implement Kafka streaming
- Add authentication system
- Deploy CI/CD pipeline
- Add historical analytics dashboard
- Add alerting system for sentiment spikes

---

# 👨‍💻 Author

Built by Hanan Ali  
Cloud Data Analytics & MLOps Enthusiast
