import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_articles(brand: str, page_size: int = 10) -> list[dict]:
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": brand,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": os.getenv("NEWS_API_KEY")
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    articles = response.json().get("articles", [])
    return [
        {
            "title": a["title"],
            "description": a["description"] or "",
            "source": a["source"]["name"],
            "url": a["url"],
            "published_at": a["publishedAt"]
        }
        for a in articles
        if a["title"] and a["title"] != "[Removed]"
    ]