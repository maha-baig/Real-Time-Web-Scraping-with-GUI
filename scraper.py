import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape Al Jazeera
def scrape_aljazeera():
    url = "https://www.aljazeera.com/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("article")
    news_data = []

    for article in articles:
        headline = article.find("h3")
        if headline:
            news_data.append(["Al Jazeera", headline.text.strip(), url])

    return news_data

# Function to scrape BBC
def scrape_bbc():
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("h3")  # Modify selector based on site structure
    news_data = []

    for article in articles:
        if article.a:
            headline = article.text.strip()
            news_data.append(["BBC", headline, url])

    return news_data

# Function to scrape CNN
def scrape_cnn():
    url = "https://edition.cnn.com/world"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("span", class_="container__headline")
    news_data = []

    for article in articles:
        headline = article.text.strip()
        news_data.append(["CNN", headline, url])

    return news_data

# Combine all scraped data
news_sources = [scrape_aljazeera(), scrape_bbc(), scrape_cnn()]
all_news = [item for source in news_sources for item in source]

# Convert to DataFrame and save to CSV
df = pd.DataFrame(all_news, columns=["Source", "Headline", "URL"])
df.to_csv("data/latest_news.csv", index=False)

print("News scraping completed successfully.")
