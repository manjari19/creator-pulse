import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyze_article(article: dict) -> dict:
    prompt = f"""You are a brand intelligence analyst. Analyze this news article about a brand and return ONLY a JSON object with no markdown, no backticks, no explanation.

Article title: {article['title']}
Article description: {article['description']}
Source: {article['source']}

Return this exact JSON structure:
{{
    "sentiment": "positive" | "negative" | "neutral",
    "category": "product launch" | "controversy" | "partnership" | "financial" | "campaign" | "general",
    "creator_signal": true | false,
    "summary": "one sentence summary of the article"
}}

creator_signal should be true if the article mentions influencers, creators, ambassadors, sponsorships, or social media campaigns."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    return json.loads(raw)


def analyze_all(articles: list[dict]) -> list[dict]:
    results = []
    for article in articles:
        try:
            analysis = analyze_article(article)
            results.append({**article, **analysis})
        except Exception as e:
            print(f"Skipping article due to error: {e}")
    return results