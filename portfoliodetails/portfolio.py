from flask import Blueprint, render_template, session, redirect
from .constants import BUY_KEYS, SELL_KEYS, URL, USDT_RATE, BTC_RATE
from .utility import total_portfolio, coin_analyzer, rate_converter
from database import mongo
import requests

portfolio_blueprint = Blueprint('portfolio', __name__,
                                template_folder='templates',
                                static_folder='static')


@portfolio_blueprint.route("/portfolio/")
@portfolio_blueprint.route("/portfolio/<string:market>/")
def portfolio(market=None):
    if not session.get("email"):
        return redirect("/login")

    print("Passed market ", market)
    if market:
        coin_specific_trades = mongo.db.exchange_trades.find({"Market": market,"user":session.get("email")}, {'_id': False})
        coin_data, buy_trades, sell_trades = total_portfolio(coin_specific_trades)
        coin_data = coin_analyzer(coin_data[market])
        wazirx_coin_data = requests.get(URL.format(market.lower())).json()["ticker"]
        wazirx_coin_data["coin_roi"] = ((float(wazirx_coin_data["sell"]) * 100) / coin_data["avg_buy_price"]) - 100

        if (coin_data["final_investment_on_buy"] - coin_data["final_sell_earning"]) > 0:
            wazirx_coin_data["overall_roi"] = (float(wazirx_coin_data["sell"]) * coin_data["coin_balance"] * 100) / \
                                              (coin_data["final_investment_on_buy"] - coin_data[
                                                  "final_sell_earning"]) - 100
        else:
            wazirx_coin_data["overall_roi"] = (((float(wazirx_coin_data["sell"]) * coin_data["coin_balance"]) + \
                                                coin_data["final_sell_earning"]) * 100) / \
                                              coin_data["final_investment_on_buy"]

        return render_template("portfoliodetails/specific_market.html", coin_data=coin_data, market=market,
                               BUY_KEYS=BUY_KEYS, SELL_KEYS=SELL_KEYS,
                               buy_trades=buy_trades, sell_trades=sell_trades,
                               wazirx_coin_data=wazirx_coin_data
                               )
    else:
        all_trades = mongo.db.exchange_trades.find({"user":session.get("email")}, {'_id': False})
        usdt_rate = requests.get(USDT_RATE).json()["ticker"]
        btc_rate = requests.get(BTC_RATE).json()["ticker"]
        my_trades, _, _ = total_portfolio(all_trades)
        my_trades = rate_converter(my_trades, usdt_rate, btc_rate)
        return render_template("portfoliodetails/portfolio.html", my_trades=my_trades)
