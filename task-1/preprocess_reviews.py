import pandas as pd
from datetime import datetime
import os

# Load raw scraped data
df = pd.read_csv("data/all_banks_reviews.csv")

# Rename columns for consistency
df = df.rename(columns={
    "content": "review",
    "score": "rating",
    "at": "date"
})

# Add source column
df["source"] = "Google Play"

# Normalize date format
df["date"] = pd.to_datetime(df["date"], errors='coerce')
df["date"] = df["date"].dt.strftime('%Y-%m-%d')

# Drop missing values
df = df.dropna(subset=["review", "rating", "date", "bank"])

# Drop duplicates
df = df.drop_duplicates(subset=["review", "bank"])

# Keep only required columns
df = df[["review", "rating", "date", "bank", "source"]]

# Save cleaned file
os.makedirs("cleaned_data", exist_ok=True)
df.to_csv("cleaned_data/cleaned_reviews.csv", index=False)

print(f"✅ Preprocessing complete. {len(df)} reviews saved to cleaned_data/cleaned_reviews.csv")
