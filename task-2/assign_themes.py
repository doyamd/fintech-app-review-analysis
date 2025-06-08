# assign_themes.py
import pandas as pd

# Define theme keyword sets
themes = {
    "User Experience": ["app", "interface", "design", "easy use", "layout", "navigation", "nice"],
    "Reliability": ["crash", "fail", "bug", "slow", "network", "hang", "freeze"],
    "Transaction": ["transfer", "send", "receive", "deposit", "withdraw", "payment", "money"],
    "Customer Support": ["support", "help", "service", "assist", "response"],
    "Access Issues": ["login", "update", "register", "otp", "password", "access"]
}

# Load data
df = pd.read_csv("data/reviews_with_sentiment.csv")

def detect_themes(text):
    text = str(text).lower()
    matched = []
    for theme, keywords in themes.items():
        if any(keyword in text for keyword in keywords):
            matched.append(theme)
    return ", ".join(matched) if matched else "Other"

# Assign themes
df['themes'] = df['review'].apply(detect_themes)

# Save results
df.to_csv("data/reviews_with_themes.csv", index=False)
print("Themes assigned and saved to data/reviews_with_themes.csv.")
