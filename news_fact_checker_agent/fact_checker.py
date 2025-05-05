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
    


def run_fact_check_with_gemini(article):
    prompt = f"""
You are a fact-checking AI assistant. Given the following news article content, evaluate its legitimacy by cross-referencing known information. 
Provide:
- Verdict: Legitimate, Likely Legitimate, Unverified, or Fake
- Legitimacy Percentage (0-100)
- 3-5 bullet point reasoning statements.

Article Content:
"{article}"

Respond clearly in readable text. No JSON formatting needed.
"""

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    return response.text.strip()

# Main logic
def main():
    news_items = load_news_from_config()

    for news in news_items:
        print(f"\n📖 Title: {news['title']}")
        result = run_fact_check_with_gemini(news['content'])
        print(f"📝 Fact Check Result:\n{result}")
if __name__ == "__main__":
    main()
