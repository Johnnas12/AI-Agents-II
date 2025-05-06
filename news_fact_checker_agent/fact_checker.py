import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load news articles from config.json
def load_news_from_config():
    with open('news_fact_checker_agent/config.json', 'r') as f:
        return json.load(f)
    

def scrape_article_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Simple scrape: get all paragraph text
        paragraphs = soup.find_all('p')
        article_text = "\n".join([para.get_text() for para in paragraphs])
        return article_text if article_text else "No full content available."
    except Exception as e:
        print(f"Scraping failed: {e}")
        return "Unable to scrape full article content."
    


def run_fact_check_with_gemini_full(article):
    scraped_content = scrape_article_content(article["url"])

    prompt = f"""
You are a fact-checking AI assistant. Evaluate the following news article for factual legitimacy by considering:

- Source: {article['source']}
- Source URL: {article['url']}
- Title: {article['title']}
- Description: {article['description']}
- Provided Content: {article['content']}
- Scraped Full Article Content: {scraped_content}

Fact Check Instructions:
- Provide a Verdict: Legitimate, Likely Legitimate, Unverified, or Fake.
- Legitimacy Score: 0-100%
- 3-5 bullet-point reasoning points explaining your decision.

Respond in clear readable text — no JSON formatting. also use emojis to make it more engaging.
"""

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    return response.text.strip()
