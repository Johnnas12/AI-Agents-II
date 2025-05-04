from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from market_trend_agent.market_watcher import fetch_crypto_data, get_available_coins
from market_trend_agent.market_summary_agent import generate_market_summary
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("❌ GEMINI_API_KEY not found in environment variables.")

# Gemini config
genai.configure(api_key=api_key)

# FastAPI app instance
app = FastAPI(
    title="AI Agents Service",
    description="A microservice for market trend analysis and AI-generated summaries",
    version="1.0.0"
)

# Request model
class MarketRequest(BaseModel):
    tracked_keywords: list[str]

# Endpoint — get available crypto coin IDs
@app.get("/available-coins")
def available_coins():
    coins = get_available_coins()
    return {"available_coins": coins}

# Endpoint — fetch market data and summary on demand
@app.post("/market-summary")
def market_summary(request: MarketRequest):
    available_coins_list = get_available_coins()
    crypto_keywords = [k for k in request.tracked_keywords if k in available_coins_list]
    if not crypto_keywords:
        raise HTTPException(status_code=400, detail="No valid crypto keywords found.")

    market_data = fetch_crypto_data(crypto_keywords)
    summary = generate_market_summary(market_data)

    return {
        "tracked_keywords": crypto_keywords,
        "market_data": market_data,
        "summary": summary
    }

# Test route
@app.get("/")
def root():
    return {"message": "🚀 AI Agents API is running!"}
