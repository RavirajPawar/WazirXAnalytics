import re

SPECIAL_KEYS= ["coin_balance", "final_investment_on_buy","final_sell_earning","avg_sell_price","avg_buy_price"]
BUY_KEYS = ["total_coin_bought","total_investment_on_buy","total_buy_fees","final_investment_on_buy","avg_buy_price"]
SELL_KEYS = ["total_coin_sold","total_sell_earning","total_sell_fees","final_sell_earning","avg_sell_price"]
URL = "https://api.wazirx.com/api/v2/tickers/{}"
USDT_RATE = URL.format("usdtinr")
BTC_RATE = URL.format("btcinr")
USDT_REGEX = re.compile("usdt$", re.IGNORECASE)
BTC_REGEX = re.compile("btc$", re.IGNORECASE)