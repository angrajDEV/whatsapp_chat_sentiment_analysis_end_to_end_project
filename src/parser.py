# %%
import pandas as pd
import numpy as np

data = pd.read_csv('WhatsApp-Chat.csv')
data.head()

# %%
data['31/08/23, 12:52 pm - Messages and calls are end-to-end encrypted. Only people in this chat can read, listen to, or share them. Learn more.']

# %%
data = data['31/08/23, 12:52 pm - Messages and calls are end-to-end encrypted. Only people in this chat can read, listen to, or share them. Learn more.'].str.split('-')

# %%
messages = pd.DataFrame(data.str[1:2])
messages.rename(columns={'31/08/23, 12:52 pm - Messages and calls are end-to-end encrypted. Only people in this chat can read, listen to, or share them. Learn more.':'sender and message'},inplace=True)
messages.head()

# %%
messages['sender and message'] = messages['sender and message'].astype(str)
messages[['sender', 'message']] = messages['sender and message'].str.strip('[]').str.split(': ', n=1, expand=True)
print(messages.head())

# %%
messages.drop(columns='sender and message')

# %%
from textblob import TextBlob

messages['sentiment_score'] = messages['message'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
messages['sentiment'] = messages['sentiment_score'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))

messages.head()

# %%
messages[messages['sentiment']=='Positive']

# %%
import matplotlib.pyplot as plt
import seaborn as sns

# Overall sentiment distribution
plt.figure(figsize=(8,5))
sns.countplot(x='sentiment', data=messages)
plt.title('Overall Sentiment Distribution')
plt.show()

# Per sender sentiment
plt.figure(figsize=(10,5))
sns.countplot(x='sender', hue='sentiment', data=messages)
plt.title('Sentiment per Person')
plt.show()


