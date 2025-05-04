import os
import json
from dotenv import load_dotenv
from pathlib import Path

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

if __name__ == "__main__":
    analyze_market_trends(config["tracked_keywords"])
