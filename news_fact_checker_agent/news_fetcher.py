import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"

def fetch_trending_crypto_news(page_size=10):
    """
    Fetch trending crypto-related news using NewsAPI.
    """
    params = {
        "q": "crypto",
        "apiKey": NEWS_API_KEY,
        "pageSize": page_size 
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        articles = [
            {
                "id": idx + 1,
                "title": article["title"],
                "author" : article["author"],
                "description": article["description"],
                "content": article["content"],
                "source": article["source"]["name"],
                "urlToImage": article["urlToImage"],
                "url": article["url"]
            }
            for idx, article in enumerate(data.get("articles", []))
        ]

        return articles

    except requests.RequestException as e:
        print(f"Error while fetching news: {e}")
        return []
