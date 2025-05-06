import google.generativeai as genai
import os
from email_utils import send_email
from market_watcher import fetch_crypto_data, get_available_coins
from dotenv import load_dotenv



load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro')


def generate_digest_email_content(prices):
    """
    Generates a digest email message from crypto prices using Gemini LLM.
    """
    price_summary = "\n".join([f"{coin.capitalize()}: ${data['price_usd']} (24h Change: {data['change_24h']})" for coin, data in prices.items()])


    prompt = f"""
    You are a financial market analyst AI assistant. Write a friendly, clear, and engaging daily email digest summarizing today's cryptocurrency prices for the following coins:

    {price_summary}

    Include:
    - A warm introduction
    - A list or bullet points of the coin prices
    - A brief closing remark about market trends or reminders about market volatility.

    Keep it human-like, professional but casual.
    """

    try:
        response = model.generate_content(prompt)

        if response and response.text:
            return response.text.strip()
        else:
            return "No content generated."
    except Exception as e:
        print("❌ Error generating email content:", e)
        return "Failed to generate digest message."
    

# User-selected coins for digest
coins_of_interest = ["bitcoin", "ethereum", "dogecoin"]

# 1️⃣ Fetch Prices
prices = fetch_crypto_data(coins_of_interest)
if not prices:
    print("No prices fetched. Exiting.")
    exit()

# 2️⃣ Generate Digest via LLM
email_content = generate_digest_email_content(prices)

# 3️⃣ Send Email
recipient_email = "yohanesmesfin3@gmail.com"
subject = "📈 Your Daily Crypto Market Digest"
send_email(subject, email_content, recipient_email)