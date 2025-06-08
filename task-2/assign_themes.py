import pandas as pd

# Load reviews
df = pd.read_csv("data/reviews_with_sentiment.csv")

# Define themes and associated keywords (based on extracted TF-IDF keywords + manual grouping)
themes = {
    "User Interface & Experience": ["app", "nice", "good", "best", "amazing", "easy", "use", "interface"],
    "Account Access Issues": ["login", "work", "working", "doesn", "don", "update"],
    "Transaction Performance": ["transfer", "slow", "network", "time", "service"],
    "Customer Support": ["support", "response", "help"],
    "Positive Feedback": ["great", "excellent", "friendly", "wow", "super app"],
}


# Function to assign themes based on keyword match
def assign_review_themes(review):
    review = str(review).lower()
    matched_themes = [theme for theme, keywords in themes.items() if any(kw in review for kw in keywords)]
    return ', '.join(matched_themes) if matched_themes else 'Uncategorized'

# Apply to all reviews
df["themes"] = df["review"].apply(assign_review_themes)

# Save to CSV
df.to_csv("data/reviews_with_themes.csv", index=False)

print("Themes assigned and saved to data/reviews_with_themes.csv")
