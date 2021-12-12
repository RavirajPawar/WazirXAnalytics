def get_referral_data(referral_data):
    referral_earnings = dict()
    for record in referral_data:
        if record["Currency"] in referral_earnings:
            referral_earnings[record["Currency"]] += record["Amount"]
        else:
            referral_earnings[record["Currency"]] = record["Amount"]

    return referral_earnings


def get_total_deposits_and_withdrawals(deposits_and_withdrawals_data):
    total_deposits_and_withdrawals = dict()
    for record in deposits_and_withdrawals_data:
        if record["Currency"] in total_deposits_and_withdrawals:
            if record["Transaction"] == "Deposit":
                total_deposits_and_withdrawals[record["Currency"]]["Deposit"] += record["Volume"]
            else:
                total_deposits_and_withdrawals[record["Currency"]]["Withdrawal"] += record["Volume"]
        else:
            total_deposits_and_withdrawals[record["Currency"]] = dict()
            if record["Transaction"] == "Deposit":
                total_deposits_and_withdrawals[record["Currency"]]["Deposit"] = record["Volume"]
                total_deposits_and_withdrawals[record["Currency"]]["Withdrawal"] = 0
            else:
                total_deposits_and_withdrawals[record["Currency"]]["Deposit"] = 0
                total_deposits_and_withdrawals[record["Currency"]]["Withdrawal"] = record["Volume"]

    return total_deposits_and_withdrawals
