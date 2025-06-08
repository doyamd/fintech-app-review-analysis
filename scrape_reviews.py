from google_play_scraper import reviews, Sort
import pandas as pd
import os

# Create a directory to store CSVs
os.makedirs('data', exist_ok=True)

# App IDs from the Google Play Store
apps = {
    "Commercial Bank of Ethiopia": "com.combanketh.mobilebanking",
    "Bank of Abyssinia": "com.boa.boaMobileBanking",
    "Dashen Bank": "com.dashen.dashensuperapp"
}


def scrape_reviews(app_name, app_id, count=400):
    print(f"Scraping {app_name}...")
    result, _ = reviews(
        app_id,
        lang='en',
        country='et',
        sort=Sort.NEWEST,
        count=count
    )
    df = pd.DataFrame(result)
    df = df[['content', 'score', 'at']]
    df['bank'] = app_name
    return df

# Aggregate all reviews
all_reviews = pd.DataFrame()

for bank_name, app_id in apps.items():
    df = scrape_reviews(bank_name, app_id)
    df.to_csv(f"data/{bank_name.replace(' ', '_').lower()}_reviews.csv", index=False)
    all_reviews = pd.concat([all_reviews, df], ignore_index=True)

# Save combined file
all_reviews.to_csv("data/all_banks_reviews.csv", index=False)
print("Scraping complete. Files saved in /data.")
