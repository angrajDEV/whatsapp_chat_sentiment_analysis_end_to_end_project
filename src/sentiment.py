import sys
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.logger import logging
from src.exception import CustomException

def analyze_sentiment(messages):
    try:
        analyzer = SentimentIntensityAnalyzer()
        
        messages['sentiment_score'] = messages['message'].apply(
            lambda x: analyzer.polarity_scores(str(x))['compound']
        )
        messages['sentiment'] = messages['sentiment_score'].apply(
            lambda x: 'Positive' if x > 0.05 else ('Negative' if x < -0.05 else 'Neutral')
        )
        
        logging.info('Sentiment analysis completed with VADER')
        return messages
    
    except Exception as e:
        raise CustomException(e, sys)