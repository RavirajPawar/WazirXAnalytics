import pandas as pd
import requests
from flask import Blueprint, render_template, session, redirect, send_file

from database import mongo
from .constants import BUY_KEYS, SELL_KEYS, URL, USDT_RATE, BTC_RATE
from .utility import total_portfolio, coin_analyzer, rate_converter, round_fig

portfolio_blueprint = Blueprint('portfolio', __name__,
                                template_folder='templates',
                                static_folder='static')


@portfolio_blueprint.route("/portfolio/")
@portfolio_blueprint.route("/portfolio/<string:market>/")
def portfolio(market=None):
    """
    Works in 2 direction
    Part 1 : If Market is passed like BTCINR then it will show all trade data of that coin with additional information.
    Goes to Wazirx API for getting market details of coin
    eg. BALANCE , Overall ROI %, Profit Booked, Current Buy Sell rate, consolidated buy sell trades.
    Part 2 : Market not passed then will fetch all coin trades and show basic information.
    Goes to Wazirx API for getting BTC, USDT details
    eg. total investment, sold earning. bought & sold coin amount

    Args:
        market : it is pair of coin and (stable coin or INR)
        eg. If BTC crypto bought using INR  then market will be BTCINR

    Returns:
        HTML page rendered with the help of Jinja Template.
    """
    if not session.get("email"):
        return redirect("/login")

    print("Passed market ", market)
    if market:
        coin_specific_trades = mongo.db.exchange_trades.find({"Market": market, "user": session.get("email")},
                                                             {'_id': False})
        coin_data, buy_trades, sell_trades = total_portfolio(coin_specific_trades)
        coin_data = coin_analyzer(coin_data[market])
        wazirx_coin_data = requests.get(URL.format(market.lower())).json()["ticker"]
        wazirx_coin_data["coin_roi"] = ((float(wazirx_coin_data["sell"]) * 100) / coin_data["avg_buy_price"]) - 100
        wazirx_coin_data["coin_roi"] = round(wazirx_coin_data["coin_roi"], 2)

        if (coin_data["final_investment_on_buy"] - coin_data["final_sell_earning"]) > 0:
            wazirx_coin_data["overall_roi"] = (float(wazirx_coin_data["sell"]) * coin_data["coin_balance"] * 100) / \
                                              (coin_data["final_investment_on_buy"] - coin_data[
                                                  "final_sell_earning"]) - 100
        else:
            wazirx_coin_data["overall_roi"] = (((float(wazirx_coin_data["sell"]) * coin_data["coin_balance"]) + \
                                                coin_data["final_sell_earning"]) * 100) / \
                                              coin_data["final_investment_on_buy"]
        wazirx_coin_data["overall_roi"] = round(wazirx_coin_data["overall_roi"], 2)

        return render_template("portfoliodetails/specific_market.html", coin_data=coin_data, market=market,
                               BUY_KEYS=BUY_KEYS, SELL_KEYS=SELL_KEYS,
                               buy_trades=buy_trades, sell_trades=sell_trades,
                               wazirx_coin_data=wazirx_coin_data
                               )
    else:
        all_trades = mongo.db.exchange_trades.find({"user": session.get("email")}, {'_id': False})
        usdt_rate = requests.get(USDT_RATE).json()["ticker"]
        btc_rate = requests.get(BTC_RATE).json()["ticker"]
        my_trades, _, _ = total_portfolio(all_trades)
        my_trades = rate_converter(my_trades, usdt_rate, btc_rate)
        my_trades = round_fig(my_trades)
        return render_template("portfoliodetails/portfolio.html", my_trades=my_trades)


@portfolio_blueprint.route("/export-report/")
def export_excel():
    """
    Send consolidated excel report file with all trades taken by users.
    """
    if not session.get("email"):
        return redirect("/login")
    all_trades = mongo.db.exchange_trades.find({"user": session.get("email")}, {'_id': False, 'user': False})
    excel_report = pd.DataFrame([trade for trade in all_trades])
    excel_report.to_excel(f"reports/{session.get('email')}-Trade-Report.xls",
                          sheet_name="trades", index=False)
    return send_file(f"reports/{session.get('email')}-Trade-Report.xls",
                     mimetype="application/vnd.ms-excel",
                     download_name=f"{session.get('email')}-Trade-Report.xls",
                     as_attachment=True)
