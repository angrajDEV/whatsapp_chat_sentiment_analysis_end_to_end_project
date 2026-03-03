import sys
import os
import emoji
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
from src.logger import logging
from src.exception import CustomException

def generate_visualizations(messages, save_path='static/images'):
    try:
        os.makedirs(save_path, exist_ok=True)

        # 1. Overall sentiment distribution
        plt.figure(figsize=(8,5))
        sns.countplot(x='sentiment', data=messages)
        plt.title('Overall Sentiment Distribution')
        plt.savefig(f'{save_path}/sentiment_distribution.png')
        plt.close()

        # 2. Per sender sentiment
        plt.figure(figsize=(10,5))
        sns.countplot(x='sender', hue='sentiment', data=messages)
        plt.title('Sentiment per Person')
        plt.savefig(f'{save_path}/sender_sentiment.png')
        plt.close()

        # 3. Message count per person
        plt.figure(figsize=(8,5))
        messages['sender'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Message Count per Person')
        plt.savefig(f'{save_path}/message_count.png')
        plt.close()

        # 4. WordCloud
        text = ' '.join(messages['message'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10,5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Most Used Words')
        plt.savefig(f'{save_path}/wordcloud.png')
        plt.close()

        # 5. Emoji Analysis
        all_emojis = []
        for msg in messages['message'].dropna():
            all_emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])
        
        if all_emojis:
            emoji_counts = Counter(all_emojis).most_common(10)
            emoji_labels, emoji_values = zip(*emoji_counts)
            plt.figure(figsize=(10,5))
            plt.bar(emoji_labels, emoji_values)
            plt.title('Top 10 Most Used Emojis')
            plt.savefig(f'{save_path}/emoji_analysis.png')
            plt.close()

        # 6. Most active hour
        if 'timestamp' in messages.columns:
            messages['hour'] = pd.to_datetime(messages['timestamp']).dt.hour
            plt.figure(figsize=(10,5))
            sns.countplot(x='hour', data=messages)
            plt.title('Most Active Hour of Day')
            plt.xlabel('Hour')
            plt.ylabel('Message Count')
            plt.savefig(f'{save_path}/active_hour.png')
            plt.close()

            # 7. Most active day
            messages['day'] = pd.to_datetime(messages['timestamp']).dt.day_name()
            day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            plt.figure(figsize=(10,5))
            sns.countplot(x='day', data=messages, order=day_order)
            plt.title('Most Active Day of Week')
            plt.savefig(f'{save_path}/active_day.png')
            plt.close()

        # 8. Top 5 Positive messages
        top_positive = messages[messages['sentiment']=='Positive'].nlargest(5, 'sentiment_score')[['sender','message','sentiment_score']]
        top_negative = messages[messages['sentiment']=='Negative'].nsmallest(5, 'sentiment_score')[['sender','message','sentiment_score']]

        # 9. Per person wordcloud
        senders = messages['sender'].unique()
        for sender in senders:
            sender_msgs = ' '.join(messages[messages['sender']==sender]['message'].dropna())
            if sender_msgs:
                wc = WordCloud(width=800, height=400, background_color='white').generate(sender_msgs)
                plt.figure(figsize=(10,5))
                plt.imshow(wc, interpolation='bilinear')
                plt.axis('off')
                plt.title(f'WordCloud - {sender}')
                plt.savefig(f'{save_path}/wordcloud_{sender.replace(" ","_")}.png')
                plt.close()

        logging.info('All visualizations generated successfully')
        return top_positive, top_negative, senders

    except Exception as e:
        raise CustomException(e, sys)