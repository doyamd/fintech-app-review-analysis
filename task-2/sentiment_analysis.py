# sentiment_and_preprocess.py
import pandas as pd
from transformers import pipeline

# Emoji-to-word mapping
emoji_map = {
    "😍": "love", "😘": "kiss", "👍": "thumbs up", "👌": "okay",
    "😡": "angry", "😢": "sad", "❤️": "love", "😭": "cry",
    "😃": "happy", "😠": "mad", "😞": "disappointed", "😆": "laugh"
}

def replace_emojis(text):
    for emoji, word in emoji_map.items():
        text = text.replace(emoji, f" {word} ")
    return text

# Load reviews
df = pd.read_csv("cleaned_data/cleaned_reviews.csv")

# Replace emojis
df['review'] = df['review'].astype(str).apply(replace_emojis)

# Load model
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Analyze sentiment (truncate long reviews to 512 tokens)
df['sentiment_label'] = df['review'].apply(lambda x: sentiment_pipeline(x[:512])[0]['label'].lower())
df['sentiment_score'] = df['review'].apply(lambda x: sentiment_pipeline(x[:512])[0]['score'])

# Save results
df.to_csv("data/reviews_with_sentiment.csv", index=False)
print("Sentiment analysis completed and saved to data/reviews_with_sentiment.csv.")
