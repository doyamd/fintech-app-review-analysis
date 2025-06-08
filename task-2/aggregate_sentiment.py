import pandas as pd
df = pd.read_csv("data/reviews_with_sentiment.csv")

sentiment_summary = df.groupby(['bank', 'rating'])['sentiment'].value_counts(normalize=True).unstack().fillna(0)
print(sentiment_summary)
