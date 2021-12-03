from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/wazirx_analytics"
mongo = PyMongo(app)


@app.route("/portfolio")
def portfolio():
    my_trades = dict()
    for index, trade in enumerate(mongo.db.exchange_trades.find({}, {'_id': False})):
        market = trade["Market"]
        volume = trade["Volume"]
        fee = trade["Fee"]
        amount = trade["Total"]
        order_type = trade["Trade"].strip()
        if market in my_trades:
            if order_type == "Buy":
                my_trades[market]["total_coin_bought"] += volume
                my_trades[market]["total_buy_fees"] += fee
                my_trades[market]["total_investment_on_buy"] += amount

            elif order_type == "Sell":
                my_trades[market]["total_coin_sold"] += volume
                my_trades[market]["total_sell_fees"] += fee
                my_trades[market]["total_sell_earning"] += amount
        else:
            my_trades[market] = dict()
            if order_type == "Buy":
                my_trades[market]["total_coin_bought"] = volume
                my_trades[market]["total_buy_fees"] = fee
                my_trades[market]["total_investment_on_buy"] = amount
                my_trades[market]["total_coin_sold"] = 0
                my_trades[market]["total_sell_fees"] = 0
                my_trades[market]["total_sell_earning"] = 0

            elif order_type == "Sell":
                my_trades[market]["total_coin_bought"] = 0
                my_trades[market]["total_buy_fees"] = 0
                my_trades[market]["total_investment_on_buy"] = 0
                my_trades[market]["total_coin_sold"] = volume
                my_trades[market]["total_sell_fees"] = fee
                my_trades[market]["total_sell_earning"] = amount

    return render_template("home.html", my_trades=my_trades, ravi={"name":"ravi"})


@app.route("/")
def index():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
