from .constants import ALLOWED_EXTENSIONS


def get_referral_data(referral_data):
    """
    Calculates total earning through referral.
    Referral earning can happen in different coins like WRX, USDT, INR

    Args:
        referral_data: mongo db find iterable

    Returns:
        earning in each type coin eg {WRX:10, USDT:10}
    """
    referral_earnings = dict()
    for record in referral_data:
        if record["Currency"] in referral_earnings:
            referral_earnings[record["Currency"]] += record["Amount"]
        else:
            referral_earnings[record["Currency"]] = record["Amount"]

    return referral_earnings


def get_total_deposits_and_withdrawals(deposits_and_withdrawals_data):
    """
    Calculates total deposits and withdrawals

    Args:
        deposits_and_withdrawals_data : mongo db find iterable

    Returns:
        total_deposits_and_withdrawals : dict of dict eg {INR:{deposit:10, withdrawal:40}}
    """
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


def allowed_file(filename):
    "Returns file type is allowed or not"
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_files(request):
    """
    Checks multiple files allowed or not with different conditions.
    """
    if "file" not in request.files:
        return "Please try again"
    for file in request.files.getlist('file'):
        if file.filename == '':
            return 'No selected file'
        if file and not allowed_file(file.filename):
            return f"{file.filename} is not allowed"

    return None
