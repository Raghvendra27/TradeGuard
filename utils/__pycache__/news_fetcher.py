# utils/news_fetcher.py
import requests

API_KEY = "f3b963758d2b49c788b58d29dc2e6cee"  # <-- Replace this with your actual API key

def get_newsapi_articles(query="indian export trade policy", max_items=5):
    try:
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={query}&"
            f"language=en&"
            f"sortBy=publishedAt&"
            f"apiKey={API_KEY}"
        )
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        news_list = []
        for article in articles[:max_items]:
            news_list.append({
                "title": article["title"],
                "link": article["url"],
                "summary": article["description"] or "No summary available."
            })
        return news_list
    except Exception as e:
        print("NewsAPI fetch failed:", e)
        return []
