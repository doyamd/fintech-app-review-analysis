# extract_keywords.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load reviews
df = pd.read_csv("data/reviews_with_sentiment.csv")

# Initialize TF-IDF
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=1000)

bank_keywords = {}

# Loop through each bank
for bank in df['bank'].unique():
    bank_reviews = df[df['bank'] == bank]['review'].astype(str)
    tfidf_matrix = vectorizer.fit_transform(bank_reviews)
    scores = zip(vectorizer.get_feature_names_out(), tfidf_matrix.sum(axis=0).A1)
    top_keywords = sorted(scores, key=lambda x: x[1], reverse=True)[:30]
    bank_keywords[bank] = [kw for kw, _ in top_keywords]

# Display
for bank, keywords in bank_keywords.items():
    print(f"\nTop Keywords for {bank}:\n", ", ".join(keywords))

# Save to CSV
keywords_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in bank_keywords.items()]))
keywords_df.to_csv("data/bank_keywords.csv", index=False)
print("Top keywords saved to data/bank_keywords.csv.")
