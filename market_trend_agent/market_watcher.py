import requests

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
    


def top_10_coins():
    keywords = ["bitcoin", "ethereum", "solana", "dogecoin", "ripple", "litecoin", "polkadot", "chainlink", "cardano", "stellar", "avalanche-2"]
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
    
