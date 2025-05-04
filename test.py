from market_trend_agent.market_watcher import fetch_crypto_data, get_available_coins


# get available coins
available_coins = get_available_coins()
print(f"Available coins: {available_coins}")