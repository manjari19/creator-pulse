# CreatorPulse

Automated brand intelligence pipeline that monitors news mentions, analyzes sentiment and creator signals using Claude AI, and delivers a daily Slack digest with a structured CSV report.

## What it does

1. **Fetches** recent news articles about a brand via NewsAPI
2. **Analyzes** each article with Claude — sentiment, category, creator/influencer signal, and a one-sentence summary
3. **Reports** results to a timestamped CSV in `/reports`
4. **Notifies** a Slack channel with a formatted daily digest
5. **Runs automatically** every day at 9am UTC via GitHub Actions

## Business impact

Replaces manual brand monitoring workflows. A marketing or ops team member checking news mentions manually across sources takes 1-2 hours daily — this pipeline does it in under 60 seconds with consistent, structured output.

## Tech stack

- **Python** — pipeline orchestration
- **NewsAPI** — article ingestion
- **Anthropic Claude API** — LLM analysis with prompt-engineered JSON outputs
- **Slack Incoming Webhooks** — automated digest delivery
- **GitHub Actions** — daily scheduling and CI/CD

## Setup

1. Clone the repo
2. Install dependencies:
```bash
   pip install anthropic requests python-dotenv
```
3. Create a `.env` file:
```NEWS_API_KEY=your_key
    ANTHROPIC_API_KEY=your_key
    SLACK_WEBHOOK_URL=your_webhook_url
    BRAND=Nike
```
4. Run manually:
```bash
   python main.py
```

## Output example

**Slack digest:**
- Sentiment breakdown across all articles
- Top categories (product launch, financial, campaign, etc.)
- Flagged creator/influencer signals with links
- Recent article summaries with source attribution

**CSV report** (`reports/nike_2026-06-24.csv`):

| title | source | sentiment | category | creator_signal | summary |
|---|---|---|---|---|---|
| Nike Names New CFO | Financial Post | neutral | financial | False | Nike appointed... |

## Automated scheduling

Runs daily via GitHub Actions cron (`0 9 * * *`). Can also be triggered manually from the Actions tab. All credentials stored as GitHub repository secrets.