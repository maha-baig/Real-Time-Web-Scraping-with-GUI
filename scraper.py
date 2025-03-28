import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re

# Download stopwords if not available
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """Cleans and preprocesses text."""
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W+', ' ', text)  # Remove special characters
    words = text.split()
    words = [word for word in words if word not in stop_words]  # Remove stopwords
    return ' '.join(words)

# Define the URL
url = "https://www.aljazeera.com/news/"

# Send a GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all headline elements
    headlines = soup.find_all("h3", class_="gc__title")

    # Extract text and store in a list
    news_list = [headline.get_text(strip=True) for headline in headlines]

    # Convert to a DataFrame
    df = pd.DataFrame(news_list, columns=["Headline"])

    # Apply text cleaning
    df["Cleaned_Headline"] = df["Headline"].apply(clean_text)

    # Save both raw and cleaned data
    df.to_csv("data/cleaned_headlines.csv", index=False)

    print("Scraped", len(news_list), "headlines successfully!")
    print("\nCleaned Data Sample:")
    print(df.head())

else:
    print("Failed to retrieve the webpage. Status Code:", response.status_code)
