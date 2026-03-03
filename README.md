# WhatsApp Chat Sentiment Analysis (End-to-End)

An end-to-end NLP-based web application that analyzes sentiment from WhatsApp chat exports using Python, VADER, and Flask.

## Features
- Upload WhatsApp `.txt` chat file
- Sentiment Analysis (Positive, Negative, Neutral) using VADER
- Overall sentiment distribution
- Per person sentiment analysis
- Message count per person
- WordCloud — most used words
- Per person WordCloud
- Top 10 most used emojis
- Most active hour and day
- Top 5 most positive and negative messages

## Tech Stack
- Python
- Flask
- NLTK / VADER
- Matplotlib / Seaborn
- WordCloud
- Pandas
- Docker

## Project Structure
```
whatsapp-sentiment/
├── app.py
├── requirements.txt
├── Dockerfile
├── src/
│   ├── parser.py
│   ├── sentiment.py
│   ├── visualize.py
│   └── utils.py
├── templates/
│   ├── index.html
│   └── result.html
└── static/
    └── images/
```

## Installation
```bash
git clone https://github.com/angrajDEV/whatsapp_chat_sentiment_analysis_end_to_end_project.git
cd whatsapp_chat_sentiment_analysis_end_to_end_project
pip install -r requirements.txt
python app.py
```

## Docker
```bash
docker build -t whatsapp-sentiment .
docker run -p 5000:5000 whatsapp-sentiment
```

## Usage
1. Export your WhatsApp chat as `.txt` file
2. Upload it on the web app
3. Get detailed sentiment analysis with visualizations