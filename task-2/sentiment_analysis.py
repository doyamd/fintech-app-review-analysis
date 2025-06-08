from transformers import pipeline
import pandas as pd

# Emoji to word mapping
emoji_map = {
    "😍": "love",
    "😘": "kiss",
    "👍": "thumbs up",
    "👌": "okay",
    "😡": "angry",
    "😢": "sad",
    # Add more if needed
}

# Function to replace emojis with words
def replace_emojis(text):
    for emoji, word in emoji_map.items():
        text = text.replace(emoji, f" {word} ")
    return text

# Load the sentiment model
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Load your preprocessed reviews
df = pd.read_csv("cleaned_data/cleaned_reviews.csv")

# Apply emoji replacement and sentiment classification
def classify_sentiment(review):
    cleaned = replace_emojis(str(review))[:512] 
    result = sentiment_pipeline(cleaned)[0]['label']
    return result.lower()

df['sentiment'] = df['review'].apply(classify_sentiment)

# Save the final dataset
df.to_csv("data/reviews_with_sentiment.csv", index=False)
