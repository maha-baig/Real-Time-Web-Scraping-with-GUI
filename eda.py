import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load cleaned data
df = pd.read_csv("data/cleaned_headlines.csv")

# Remove NaN values (if any)
df.dropna(inplace=True)

# Display basic stats
print("\nDataset Summary:")
print(df.describe())

print("\nFirst 5 Rows of Cleaned Data:")
print(df.head())

# Plot the most common words
all_text = " ".join(df["Cleaned_Headline"])

# Generate word cloud
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_text)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Most Frequent Words in News Headlines")
plt.show()

# Word frequency bar chart
word_list = all_text.split()
word_freq = pd.Series(word_list).value_counts()[:20]  # Top 20 words

plt.figure(figsize=(12, 6))
sns.barplot(x=word_freq.values, y=word_freq.index, palette="viridis")
plt.xlabel("Frequency")
plt.ylabel("Words")
plt.title("Top 20 Most Frequent Words in News Headlines")
plt.show()
