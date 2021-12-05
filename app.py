from flask import Flask, render_template
from flask_pymongo import PyMongo
import requests

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
        return_on_investment = (float(wazirx_coin_data["sell"])*100)/ coin_data["avg_buy_price"]
        return_on_investment = return_on_investment - 100
        return render_template("specific_market.html", coin_data=coin_data, market=market,
                               BUY_KEYS=BUY_KEYS, SELL_KEYS=SELL_KEYS,
                               buy_trades=buy_trades, sell_trades=sell_trades,
                               wazirx_coin_data = wazirx_coin_data,
                               return_on_investment= return_on_investment)
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
    return render_template("home.html", referral_earnings= referral_earnings,
                           total_deposits_and_withdrawals = total_deposits_and_withdrawals)


if __name__ == "__main__":
    app.run(debug=True)
