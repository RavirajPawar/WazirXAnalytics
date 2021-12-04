from flask import Flask, render_template
from flask_pymongo import PyMongo

from utility import total_portfolio, coin_analyzer

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/wazirx_analytics"
mongo = PyMongo(app)


@app.route("/portfolio/")
@app.route("/portfolio/<string:market>/")
def portfolio(market=None):
    print("Passed market ", market)
    if market:
        coin_specific_trades = mongo.db.exchange_trades.find({"Market": market}, {'_id': False})
        specific_trades = total_portfolio(coin_specific_trades)[market]
        specific_trades = coin_analyzer(specific_trades)
        return render_template("specific_market.html", specific_trades=specific_trades, market=market)
    else:
        all_trades = mongo.db.exchange_trades.find({}, {'_id': False})
        my_trades = total_portfolio(all_trades)
        return render_template("portfolio.html", my_trades=my_trades)


@app.route("/")
def index():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
