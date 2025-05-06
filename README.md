# 🧠 AI Agents Backend — Crypto Market Intelligence API

Welcome to the **AI Agents Backend**, the core API service powering our Crypto Market Intelligence Dashboard. This backend handles market data fetching, AI-generated market summaries, fact-checking crypto news articles, and digest reporting — all powered by LLM-based agents.

---

## 📌 Project Overview

This FastAPI-based backend exposes endpoints for interacting with AI agents responsible for summarizing market trends, verifying crypto news, and generating daily or on-demand digest reports. It integrates with external APIs for real-time market data and language models for intelligent text generation and validation.

---

## 🚀 Features Implemented

### 📝 Market Summary Agent

- Fetches a predefined list of available cryptocurrencies.
- Accepts user-selected coins as tracked keywords.
- Generates an AI-powered market summary for those selected coins.
- Fetches real-time market data (price and 24h change).
- Returns both the AI-generated summary and market data via a clean REST API.

### 📊 Market Digest Agent

- Accepts a `recipient` (optional for targeting or email-based digests) and `tracked_keywords`.
- Generates a digest-style AI summary covering selected cryptocurrencies.
- Returns a markdown-formatted digest summary.
- Supports integration into email services or frontend notifications.

### 🔍 Fact-Checker Agent for Crypto News

- Accepts a news article URL.
- Fetches the article content.
- Uses an LLM to verify the credibility of the content.
- Returns:
  - Verdict (e.g. Legitimate, Misleading, Fake)
  - Reasoning points behind the verdict
  - Legitimacy percentage score.

---

## 🔧 Tech Stack

- **Python 3.11+**
- **FastAPI** for REST API routing and serving.
- **Pydantic** for data validation.
- **httpx / requests** for external market data fetching and news scraping.
- **BeautifulSoup4** for HTML parsing (fact-checker).
- **LLM API integration** (like OpenAI or Gemini — configurable via environment)
- **Markdown** for AI-generated content rendering

---

## 📡 API Endpoints

| Method | Endpoint               | Description                                                     |
|:--------|:--------------------------|:----------------------------------------------------------------|
| `GET`   | `/available-coins`         | Fetch list of available cryptocurrency coins                    |
| `POST`  | `/market-summary`          | Generate a market summary for selected tracked coins            |
| `POST`  | `/digest`                  | Generate a digest summary for selected tracked coins            |
| `POST`  | `/fact-check`              | Fact-check a crypto news article and provide verdict + reasoning|

---

## 🤝 Contribution

If you'd like to contribute, feel free to fork the repo and submit a pull request. Suggestions and improvements are always welcome.

---

## 📃 License

Open-source project — feel free to use and modify for your own crypto intelligence dashboards.

---

## 💚 Built With Love by Yohanes Mesfin 🚀
