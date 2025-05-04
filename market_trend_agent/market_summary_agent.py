import os
import json
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from market_watcher import fetch_crypto_data, get_available_coins

# Load env vars
load_dotenv()

config_path = Path(__file__).parent / "config.json"
with open(config_path) as f:
    config = json.load(f)


api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not found in environment variables.")
    exit(1)

# Gemini config
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro')

def load_market_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def generate_market_summary(data):
    market_insights = json.dumps(data, indent=2)
    prompt = f"""
You are a financial market analyst AI. Based on the following real-time crypto market data, provide a concise, human-readable summary of the market trends. Highlight which coins are gaining, which are losing, and overall sentiment.

Market Data:
{market_insights}

Summary:
"""

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":

    available_coins = get_available_coins()
    crypto_keywords = [k for k in config["tracked_keywords"] if k in available_coins]
    insights = fetch_crypto_data(crypto_keywords)

    output_path = Path(__file__).parent.parent / config["output_file"]
    with open(output_path, "w") as outfile:
        json.dump(insights, outfile, indent=2)

    print(f"✅ Market data saved to {output_path}")
    summary = generate_market_summary(insights)

    summary_output_file = Path(__file__).parent.parent / "shared/results/market_summary.txt"
    with open(summary_output_file, "w") as f:
        f.write(summary)

    print(f"✅ Market summary generated and saved to {summary_output_file}")
