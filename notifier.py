import requests
import os
from dotenv import load_dotenv
from collections import Counter

load_dotenv()

def send_slack_digest(brand: str, results: list[dict]) -> None:
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    total = len(results)
    sentiments = Counter(r["sentiment"] for r in results)
    categories = Counter(r["category"] for r in results)
    creator_signals = [r for r in results if r.get("creator_signal")]

    lines = [
        f"*CreatorPulse Daily Digest: {brand}*",
        f"_{total} articles analyzed_",
        "",
        "*Sentiment Breakdown*",
        f"  Positive: {sentiments['positive']}  |  Neutral: {sentiments['neutral']}  |  Negative: {sentiments['negative']}",
        "",
        "*Top Categories*",
        "  " + "  |  ".join(f"{cat}: {count}" for cat, count in categories.most_common(3)),
        "",
    ]

    if creator_signals:
        lines.append(f"*Creator/Influencer Signals ({len(creator_signals)} found)*")
        for r in creator_signals[:3]:
            lines.append(f"  • <{r['url']}|{r['title']}> — {r['summary']}")
    else:
        lines.append("_No creator/influencer signals detected today._")

    lines += [
        "",
        "*Recent Articles*",
    ]
    for r in results[:5]:
        emoji = {"positive": "🟢", "negative": "🔴", "neutral": "⚪"}.get(r["sentiment"], "⚪")
        lines.append(f"  {emoji} <{r['url']}|{r['title']}> ({r['source']})")

    payload = {"text": "\n".join(lines)}
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()
    print("Slack digest sent.")