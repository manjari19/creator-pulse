import csv
import os
from datetime import datetime
from dotenv import load_dotenv
from fetcher import fetch_articles
from analyzer import analyze_all
from notifier import send_slack_digest

load_dotenv()

def save_csv(results: list[dict], brand: str) -> str:
    os.makedirs("reports", exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"reports/{brand.lower()}_{date_str}.csv"

    fieldnames = ["title", "source", "published_at", "url", "sentiment", "category", "creator_signal", "summary"]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow({k: row.get(k, "") for k in fieldnames})

    print(f"Report saved to {filename}")
    return filename


def run():
    brand = os.getenv("BRAND", "Nike")
    print(f"Fetching articles for: {brand}")

    articles = fetch_articles(brand)
    print(f"Fetched {len(articles)} articles")

    print("Analyzing with Claude...")
    results = analyze_all(articles)
    print(f"Analyzed {len(results)} articles")

    filename = save_csv(results, brand)

    print("Sending Slack digest...")
    send_slack_digest(brand, results)

    print("Done.")


if __name__ == "__main__":
    run()