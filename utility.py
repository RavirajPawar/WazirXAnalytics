def total_portfolio(all_trades):
    """
    calculate total fees, investment in your account
    Args:
        all_trades :- trades
    Returns:
        my_trades - dictionary key as market and details as value
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


def coin_analyzer(specific_trades):
    """
    {'total_coin_bought': 25.32, 'total_buy_fees': 10.994848000000001, 'total_investment_on_buy': 5497.424,
     'total_coin_sold': 6.5600000000000005, 'total_sell_fees': 4.358, 'total_sell_earning': 2179.0}
    """

    specific_trades["coin_balance"] = specific_trades["total_coin_bought"] \
                                      - specific_trades["total_coin_sold"]

    specific_trades["final_investment_on_buy"] = specific_trades["total_buy_fees"] \
                                                     + specific_trades["total_investment_on_buy"]

    specific_trades["final_sell_earning"] = specific_trades["total_sell_earning"] \
                                                - specific_trades["total_sell_fees"]

    specific_trades["avg_buy_price"] = specific_trades["final_investment_on_buy"]/specific_trades["total_coin_bought"]

    try:
        specific_trades["avg_sell_price"] = specific_trades["final_sell_earning"]/specific_trades["total_coin_sold"]
    except ZeroDivisionError:
        specific_trades["avg_sell_price"] = "You haven't done any sell yet"

    return specific_trades



