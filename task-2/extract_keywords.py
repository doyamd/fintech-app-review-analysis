import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path

# Load sentiment-tagged review data
data_path = Path("data/reviews_with_sentiment.csv")
df = pd.read_csv(data_path)

# Prepare TF-IDF vectorizer
vectorizer = TfidfVectorizer(
    stop_words='english',
    ngram_range=(1, 2),  
    max_features=1000    
)

# Store keywords by bank
bank_keywords = {}

for bank in df['bank'].unique():
    print(f"Processing bank: {bank}")
    bank_reviews = df[df['bank'] == bank]['review'].astype(str)
    
    if bank_reviews.empty:
        print(f"Warning: No reviews found for {bank}. Skipping.")
        continue

    tfidf_matrix = vectorizer.fit_transform(bank_reviews)
    tfidf_scores = zip(vectorizer.get_feature_names_out(), tfidf_matrix.sum(axis=0).A1)

    top_keywords = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)[:30]
    bank_keywords[bank] = [kw for kw, _ in top_keywords]

for bank, keywords in bank_keywords.items():
    print(f"\nTop Keywords for {bank}:\n", ", ".join(keywords))

# Optional: Save results to a file
output_dir = Path("results")
output_dir.mkdir(exist_ok=True)

keywords_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in bank_keywords.items()]))
keywords_df.to_csv(output_dir / "tfidf_top_keywords.csv", index=False)
