import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob import TextBlob
from datetime import datetime

NEWS_SOURCES = {
    "Al Jazeera": "https://www.aljazeera.com/news/",
    "BBC": "https://www.bbc.com/news",
    "CNN": "https://edition.cnn.com/world"
}

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_aljazeera_news():
    response = requests.get(NEWS_SOURCES["Al Jazeera"], headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")
    
    news_data = []
    for article in articles:
        headline_tag = article.find("h3")
        if headline_tag:
            title = headline_tag.text.strip()
            link = "https://www.aljazeera.com" + article.find("a")["href"]
            news_data.append(["Al Jazeera", title, link])
    return news_data

def get_bbc_news():
    response = requests.get(NEWS_SOURCES["BBC"], headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select("h3 a")
    
    news_data = []
    for article in articles:
        title = article.text.strip()
        link = "https://www.bbc.com" + article["href"]
        news_data.append(["BBC", title, link])
    return news_data

def get_cnn_news():
    response = requests.get(NEWS_SOURCES["CNN"], headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select("h3 a")
    
    news_data = []
    for article in articles:
        title = article.text.strip()
        link = "https://edition.cnn.com" + article["href"]
        news_data.append(["CNN", title, link])
    return news_data

def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity  # Returns a value between -1 (negative) to +1 (positive)

def scrape_news():
    all_news = get_aljazeera_news() + get_bbc_news() + get_cnn_news()
    df = pd.DataFrame(all_news, columns=["Source", "Headline", "URL"])
    
    # Add sentiment score
    df["Sentiment"] = df["Headline"].apply(analyze_sentiment)
    df["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save to CSV
    df.to_csv("data/latest_news.csv", index=False)
    print("✅ News Data Updated!")

if __name__ == "__main__":
    scrape_news()
