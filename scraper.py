import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL
url = "https://www.aljazeera.com/news/"

# Send a GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all headline elements (Inspect the site for correct tags)
    headlines = soup.find_all("h3", class_="gc__title")

    # Extract text and store in a list
    news_list = [headline.get_text(strip=True) for headline in headlines]

    # Convert to a DataFrame
    df = pd.DataFrame(news_list, columns=["Headline"])

    # Save to CSV
    df.to_csv("data/aljazeera_headlines.csv", index=False)

    print("Scraped", len(news_list), "headlines successfully!")
    print(df.head())

else:
    print("Failed to retrieve the webpage. Status Code:", response.status_code)
