import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import re

# Download required nltk data
nltk.download("vader_lexicon")
nltk.download("punkt")

# Load cleaned data
df = pd.read_csv("data/cleaned_headlines.csv")

# Remove NaN values (if any)
df.dropna(inplace=True)

# Display basic stats
print("\nDataset Summary:")
print(df.describe())

print("\nFirst 5 Rows of Cleaned Data:")
print(df.head())

# Word Frequency Analysis
all_text = " ".join(df["Cleaned_Headline"])

word_list = all_text.split()
word_freq = Counter(word_list)
common_words = word_freq.most_common(20)  # Top 20 words

# Convert to DataFrame for visualization
word_df = pd.DataFrame(common_words, columns=["Word", "Frequency"])

# Plot word frequency bar chart
plt.figure(figsize=(12, 6))
sns.barplot(x=word_df["Frequency"], y=word_df["Word"], palette="magma")
plt.xlabel("Frequency")
plt.ylabel("Words")
plt.title("Top 20 Most Frequent Words in News Headlines")
plt.show()

# Generate and display Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Most Frequent Words in News Headlines")
plt.show()

### **3️⃣ Sentiment Analysis**
sia = SentimentIntensityAnalyzer()

def get_sentiment(text):
    """Returns sentiment polarity score (-1 to +1)"""
    return sia.polarity_scores(text)["compound"]

df["Sentiment_Score"] = df["Cleaned_Headline"].apply(get_sentiment)

# Categorizing sentiment
df["Sentiment_Label"] = df["Sentiment_Score"].apply(lambda x: "Positive" if x > 0.2 else ("Negative" if x < -0.2 else "Neutral"))

# Sentiment Distribution
plt.figure(figsize=(8, 5))
sns.countplot(x=df["Sentiment_Label"], palette="coolwarm")
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.title("Distribution of Sentiments in News Headlines")
plt.show()

print("\nSentiment Breakdown:")
print(df["Sentiment_Label"].value_counts())

### **4️⃣ Length Analysis**
df["Word_Count"] = df["Cleaned_Headline"].apply(lambda x: len(x.split()))

plt.figure(figsize=(10, 5))
sns.histplot(df["Word_Count"], bins=20, kde=True, color="blue")
plt.xlabel("Word Count")
plt.ylabel("Frequency")
plt.title("Distribution of Word Count in Headlines")
plt.show()

print("\nHeadline Length Stats:")
print(df["Word_Count"].describe())

# Save enhanced data with Sentiment Scores
df.to_csv("data/enhanced_headlines.csv", index=False)
