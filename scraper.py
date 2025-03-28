import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

URL = "https://www.aljazeera.com/news/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_news():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("article")

    news_data = []
    for article in articles:
        headline = article.find("h3")
        if headline:
            title = headline.text.strip()
            link = "https://www.aljazeera.com" + article.find("a")["href"]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Add timestamp
            news_data.append([title, link, timestamp])

    # Convert to DataFrame and save
    df = pd.DataFrame(news_data, columns=["Headline", "URL", "Timestamp"])
    df.to_csv("data/latest_news.csv", index=False)
    print("✅ News Data Updated!")

if __name__ == "__main__":
    scrape_news()
