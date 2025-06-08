# Fintech App Review Analysis

---
This repository analyzes user reviews of Ethiopian banking apps to uncover sentiment trends and key themes affecting user satisfaction. The workflow includes scraping reviews from the Google Play Store, preprocessing the text, performing sentiment analysis using NLP models, and extracting thematic insights through keyword clustering.

---

## Tools & Technologies

- **Python** 🐍
- **google-play-scraper** – Collect app reviews
- **pandas** – Data manipulation
- **transformers** – Sentiment classification (BERT)
- **scikit-learn** – TF-IDF vectorization
- **spaCy** – Text preprocessing and lemmatization
- **matplotlib / seaborn** – (Optional) Data visualization

---

## Project Structure

```
.
├── cleaned_data/
│   └── cleaned_reviews.csv               # Preprocessed review dataset
├── data/
│   ├── reviews_with_sentiment.csv        # Reviews with sentiment labels
│   ├── keywords_per_bank.csv             # Top keywords per bank
│   └── reviews_with_themes.csv           # Final structured output
├── sentiment_and_preprocess.py           # Preprocessing and sentiment classification
├── extract_keywords.py                   # TF-IDF keyword extraction
├── assign_themes.py                      # Manual/rule-based theme assignment
├── requirements.txt
└── README.md
```

---

## Features

- **Scraping Reviews:** Collects real reviews from the Google Play Store for:
  - Commercial Bank of Ethiopia
  - Bank of Abyssinia
  - Dashen Bank

- **Preprocessing:**
  - Emoji normalization (e.g., "😍" → "love")
  - Lowercasing, punctuation removal, optional lemmatization
  - Stopword filtering

- **Sentiment Analysis:**
  - Uses `distilbert-base-uncased-finetuned-sst-2-english` transformer model
  - Assigns each review a label: positive or negative
  - Results saved to `reviews_with_sentiment.csv`

- **Keyword Extraction:**
  - Identifies top keywords and bigrams per bank using TF-IDF
  - Saved to `keywords_per_bank.csv`

- **Thematic Clustering:**
  - Groups related keywords into themes such as:
    - Account Access
    - App Performance
    - User Interface
    - Customer Support
  - Themes appended to reviews for deeper insight

---

## Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/fintech-review-analysis.git
   cd fintech-review-analysis
   ```

2. **Set Up the Environment**
   Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the Pipeline**
   Ensure `cleaned_reviews.csv` exists in the `cleaned_data` folder, then run:
   ```bash
   python sentiment_analysis.py
   python extract_keywords.py
   python assign_themes.py
   ```
   Output files will be generated in the `data/` directory.

---

## Insights

This analysis helps fintech stakeholders to:
- Identify pain points in app performance and reliability
- Understand what users value (e.g., ease of use, speed)
- Prioritize feature improvements based on user sentiment
