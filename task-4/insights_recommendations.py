import cx_Oracle
import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Connection and query
load_dotenv()
username = os.getenv('ORACLE_USERNAME')
password = os.getenv('ORACLE_PASSWORD')
dsn = os.getenv('ORACLE_DSN')
connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
cursor = connection.cursor()
query = """
    SELECT r.review_id, r.rating, r.review_date, r.sentiment_score, r.themes, b.bank_name
    FROM Reviews r JOIN Banks b ON r.bank_id = b.bank_id
    ORDER BY r.review_date
"""
cursor.execute(query)
df = pd.DataFrame(cursor.fetchall(), columns=['review_id', 'rating', 'review_date', 'sentiment_score', 'themes', 'bank_name'])
connection.close()

# Insights
drivers = df[df['sentiment_score'] > 0.7]['themes'].str.contains('navigation').sum()  # Evidence for fast navigation
pain_points = df[df['sentiment_score'] < 0.3]['themes'].str.contains('performance').sum()  # Evidence for crashes
bank_comparison = df.groupby('bank_name')['sentiment_score'].mean()

# Visualizations
df['review_date'] = pd.to_datetime(df['review_date'])
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='rating', bins=10, kde=True)
plt.title('Rating Distribution')
plt.savefig('rating_distribution.png')
plt.close()

plt.figure(figsize=(10, 6))
sentiment_trend = df.groupby(df['review_date'].dt.to_period('M'))['sentiment_score'].mean()
sentiment_trend.plot(marker='o')
plt.title('Sentiment Trend Over Time')
plt.xlabel('Month')
plt.ylabel('Average Sentiment Score')
plt.xticks(rotation=45)
plt.savefig('sentiment_trend.png')
plt.close()

# Report
with open('insights_report.md', 'w') as f:
    f.write("# Insights and Recommendations\n")
    f.write(f"- Drivers: Fast navigation ({drivers} reviews), Reliable transactions\n")
    f.write(f"- Pain Points: Crashes ({pain_points} reviews), Support delays\n")
    f.write(f"- Comparison: {bank_comparison.to_string()}\n")
    f.write("- Recommendations: Add budgeting tool, Improve crash handling\n")
    f.write("- Ethics: Potential negative skew bias\n")