import requests
from flask import Flask, render_template
from flask_pymongo import PyMongo

from constants import BUY_KEYS, SELL_KEYS, URL
from utility import total_portfolio, coin_analyzer, get_referral_data, get_total_deposits_and_withdrawals

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/wazirx_analytics"
mongo = PyMongo(app)


@app.route("/portfolio/")
@app.route("/portfolio/<string:market>/")
def portfolio(market=None):
    print("Passed market ", market)
    if market:
        coin_specific_trades = mongo.db.exchange_trades.find({"Market": market}, {'_id': False})
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

        return render_template("specific_market.html", coin_data=coin_data, market=market,
                               BUY_KEYS=BUY_KEYS, SELL_KEYS=SELL_KEYS,
                               buy_trades=buy_trades, sell_trades=sell_trades,
                               wazirx_coin_data=wazirx_coin_data
                               )
    else:
        all_trades = mongo.db.exchange_trades.find({}, {'_id': False})
        my_trades, _, _ = total_portfolio(all_trades)
        return render_template("portfolio.html", my_trades=my_trades)


@app.route("/")
def index():
    referral_data = mongo.db.additional_transfers.find({}, {'_id': False})
    referral_earnings = get_referral_data(referral_data)
    deposits_and_withdrawals_data = mongo.db.deposits_and_withdrawals.find({}, {'_id': False})
    total_deposits_and_withdrawals = get_total_deposits_and_withdrawals(deposits_and_withdrawals_data)
    return render_template("home.html", referral_earnings=referral_earnings,
                           total_deposits_and_withdrawals=total_deposits_and_withdrawals)


if __name__ == "__main__":
    app.run(debug=True)
