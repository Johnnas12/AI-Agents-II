import os
from dotenv import load_dotenv
import google.generativeai as genai

from email_utils import send_email
from market_watcher import fetch_crypto_data

load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro')


def send_crypto_digest_email(coins_of_interest, recipient_email):
    """
    Fetch crypto prices, generate digest content via Gemini, and send email to recipient.
    """
    print(f"📊 Fetching market data for: {', '.join(coins_of_interest)}")
    prices = fetch_crypto_data(coins_of_interest)
    if not prices:
        return {"status": "Failed", "message": "No prices fetched. Exiting."}

    # Build price summary string
    price_summary = "\n".join(
        [f"{coin.capitalize()}: ${data['price_usd']} (24h Change: {data['change_24h']})"
         for coin, data in prices.items()]
    )

    # Build prompt for Gemini
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
        email_content = response.text.strip() if response and response.text else "No content generated."

    except Exception as e:
        print("❌ Error generating email content:", e)
        return {"status": "Failed", "message": str(e)}

    try:
        subject = "📈 Your Daily Crypto Market Digest"
        send_email(subject, email_content, recipient_email)
        return {
            "status": "Success",
            "coins_tracked": coins_of_interest,
            "email_sent_to": recipient_email
        }
    except Exception as e:
        print("❌ Error sending email:", e)
        return {"status": "Failed", "message": str(e)}

if __name__ == "__main__":
    coins = ["bitcoin", "ethereum", "dogecoin"]
    recipient = "yohanesmesfin3@gmail.com"
    result = send_crypto_digest_email(coins, recipient)
    print(result)
