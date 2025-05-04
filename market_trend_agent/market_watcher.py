import os
import json
from dotenv import load_dotenv
from pathlib import Path
import requests

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Load config
config_path = Path(__file__).parent / "config.json"
with open(config_path) as f:
    config = json.load(f)

# Example print to confirm config load
print("🔍 Tracked Keywords:", config["tracked_keywords"])
print("📦 Output will be saved to:", config["output_file"])

# Placeholder function for AI request (we'll plug in Gemini API later)
def analyze_market_trends(keywords):
    print(f"📈 Analyzing trends for: {', '.join(keywords)}")
    # TODO: Call Gemini API here


def fetch_crypto_data(keywords):
    print(f"📊 Fetching market data for: {', '.join(keywords)}")
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(keywords),
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        result = {}
        for coin in keywords:
            if coin in data:
                price = data[coin]['usd']
                change = data[coin]['usd_24h_change']
                result[coin] = {
                    "price_usd": price,
                    "change_24h": f"{change:.2f}%"
                }
            else:
                result[coin] = "No data available"
        return result
    else:
        print("❌ Error fetching data:", response.status_code)
        return {}
    

def get_available_coins():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)

    if response.status_code == 200:
        coins = response.json()
        return [coin['id'] for coin in coins]
    else:
        print("❌ Error fetching coin list:", response.status_code)
        return []


if __name__ == "__main__":
    available_coins = get_available_coins()
    crypto_keywords = [k for k in config["tracked_keywords"] if k in available_coins]
    insights = fetch_crypto_data(crypto_keywords)

    output_path = Path(__file__).parent.parent / config["output_file"]
    with open(output_path, "w") as outfile:
        json.dump(insights, outfile, indent=2)

    print(f"✅ Market data saved to {output_path}")
