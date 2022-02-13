from .constants import USDT_REGEX, BTC_REGEX


def total_portfolio(all_trades):
    """
    calculate total fees, total investment , total profit for each coin from total portfolio.

    Args:
        all_trades :- iterable mongo db find result [{market:BTCINR, volume:0.5}, {market:SCINR, volume:12}]

    Returns:
        my_trades - dictionary key as market and details as value which is again dict.
        {BTCINR:{total_buy_fees:1, total_investment_on_buy:12}, SCINR:{total_buy_fees:2, total_investment_on_buy:234}}
        buy_trades - list of buy trades
        sell_trades - list of sell trades
    """
    my_trades = dict()
    buy_trades = list()
    sell_trades = list()
    for trade in all_trades:
        market = trade["Market"]
        volume = trade["Volume"]
        fee = trade["Fee"]
        amount = trade["Total"]
        order_type = trade["Trade"].strip()
        # REMINDER buy fees added to investment and sell fees subtracted from sell earnings
        if market in my_trades:
            if order_type == "Buy":
                my_trades[market]["total_coin_bought"] += volume
                my_trades[market]["total_buy_fees"] += fee
                my_trades[market]["total_investment_on_buy"] += amount
                buy_trades.append(trade)

            elif order_type == "Sell":
                my_trades[market]["total_coin_sold"] += volume
                my_trades[market]["total_sell_fees"] += fee
                my_trades[market]["total_sell_earning"] += amount
                sell_trades.append(trade)
        else:
            my_trades[market] = dict()
            if order_type == "Buy":
                my_trades[market]["total_coin_bought"] = volume
                my_trades[market]["total_buy_fees"] = fee
                my_trades[market]["total_investment_on_buy"] = amount
                my_trades[market]["total_coin_sold"] = 0
                my_trades[market]["total_sell_fees"] = 0
                my_trades[market]["total_sell_earning"] = 0
                buy_trades.append(trade)

            elif order_type == "Sell":
                my_trades[market]["total_coin_bought"] = 0
                my_trades[market]["total_buy_fees"] = 0
                my_trades[market]["total_investment_on_buy"] = 0
                my_trades[market]["total_coin_sold"] = volume
                my_trades[market]["total_sell_fees"] = fee
                my_trades[market]["total_sell_earning"] = amount
                sell_trades.append(trade)

    return my_trades, buy_trades, sell_trades


"""
TODO 
key_neutralizer = lambda original_key: " ".join(original_key.split("_"))
# original db keys are renamed for UI purpose
original_key_map = {original_key: key_neutralizer(original_key).capitalize() for original_key in specific_trades.keys()}
print(original_key_map)
"""


def coin_analyzer(specific_trade):
    """
        calculates average buy and sell price, total investment and booked profit aka  final_sell_earning

        Args:
              specific_trade :- dict of keys total_coin_bought, total_coin_sold, total_sell_earning

        Returns:
            specific_trade :- same dict with additional keys final_investment_on_buy, avg_buy_price
    """

    specific_trade["coin_balance"] = specific_trade["total_coin_bought"] \
                                     - specific_trade["total_coin_sold"]

    specific_trade["final_investment_on_buy"] = specific_trade["total_buy_fees"] \
                                                + specific_trade["total_investment_on_buy"]

    specific_trade["final_sell_earning"] = specific_trade["total_sell_earning"] \
                                           - specific_trade["total_sell_fees"]

    specific_trade["avg_buy_price"] = specific_trade["final_investment_on_buy"] / specific_trade["total_coin_bought"]

    try:
        specific_trade["avg_sell_price"] = specific_trade["final_sell_earning"] / specific_trade["total_coin_sold"]
    except ZeroDivisionError:
        specific_trade["avg_sell_price"] = "You haven't done any sell yet"

    return specific_trade


def rate_converter(my_trades, usdt_rate, btc_rate):
    """
        Some trades are done in USDT and BTC pair. To get correct analysis rate needs to convert in INR

        Args:
              my_trades : dict of all trades details key as coin with pair
              usdt_rate : dict which tells current price of USDT
              btc_rate : dict which tells current price of BTC

        Returns:
              my_trades : where each key is multiplied by matching pair coins current rate

    """

    for coin_pair in my_trades:
        if USDT_REGEX.search(coin_pair):
            my_trades[coin_pair]["total_investment_on_buy"] *= float(usdt_rate["sell"])
            my_trades[coin_pair]["total_sell_earning"] *= float(usdt_rate["sell"])
        elif BTC_REGEX.search(coin_pair):
            my_trades[coin_pair]["total_investment_on_buy"] *= float(btc_rate["sell"])
            my_trades[coin_pair]["total_sell_earning"] *= float(btc_rate["sell"])

        my_trades[coin_pair]["profit_booking"] = (my_trades[coin_pair]["total_sell_earning"] +
                                                  my_trades[coin_pair]["total_sell_fees"] -
                                                  my_trades[coin_pair]["total_investment_on_buy"] +
                                                  my_trades[coin_pair]["total_buy_fees"]
                                                  )
    return my_trades


def round_fig(my_trades):
    """
        Converts trade detail numbers to 3 digits.
    """
    for coin_pair in my_trades:
        for parameter in my_trades[coin_pair]:
            my_trades[coin_pair][parameter] = round(my_trades[coin_pair][parameter], 3)

    return my_trades
