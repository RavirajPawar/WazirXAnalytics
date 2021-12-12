from flask import Blueprint, render_template

from database import mongo
from .utility import get_referral_data, get_total_deposits_and_withdrawals

general_blueprint = Blueprint('general', __name__,
                              template_folder='templates',
                              static_folder='static')


@general_blueprint.route("/user")
def user():
    referral_data = mongo.db.additional_transfers.find({}, {'_id': False})
    referral_earnings = get_referral_data(referral_data)
    deposits_and_withdrawals_data = mongo.db.deposits_and_withdrawals.find({}, {'_id': False})
    total_deposits_and_withdrawals = get_total_deposits_and_withdrawals(deposits_and_withdrawals_data)
    return render_template("general/general.html", referral_earnings=referral_earnings,
                           total_deposits_and_withdrawals=total_deposits_and_withdrawals)
