import pandas as pd
from flask import Blueprint, render_template, request, session, redirect, url_for
from database import mongo
from .constants import REQUIRED_SHEETS, COLLECTION_NAMES
from .utility import get_referral_data, get_total_deposits_and_withdrawals, check_files

general_blueprint = Blueprint('general', __name__,
                              template_folder='templates',
                              static_folder='static')


def login_status(base):
    def check_login(*args, **kwargs):
        if not session.get("email"):
            return redirect("/login")
        else:
            return base()

    return check_login


@general_blueprint.route("/user")
def user():
    if not session.get("email"):
        return redirect("/login")

    referral_data = mongo.db.additional_transfers.find({"user": session.get("email")}, {'_id': False})
    file_upload_msg = request.args.get("msg")  # if user uploads file it's status will come through upload-file view
    file_upload_error = request.args.get("error")
    referral_earnings = get_referral_data(referral_data)
    deposits_and_withdrawals_data = mongo.db.deposits_and_withdrawals.find({"user": session.get("email")},
                                                                           {'_id': False})
    total_deposits_and_withdrawals = get_total_deposits_and_withdrawals(deposits_and_withdrawals_data)
    return render_template("general/general.html", referral_earnings=referral_earnings,
                           total_deposits_and_withdrawals=total_deposits_and_withdrawals,
                           msg=file_upload_msg, error=file_upload_error)


@general_blueprint.route("/upload-file", methods=["GET", "POST"])
def upload_file():
    if not session.get("email"):
        return redirect("/login")
    try:
        file_status = check_files(request)
        if file_status:
            return redirect(url_for(".user", error=file_status))
        import time
        start_time = time.time()
        # for file in request.files.getlist('file'):
        #     for sheet, collection in zip(REQUIRED_SHEETS, COLLECTION_NAMES):
        #         sheet_start_time = time.time()
        #         df = pd.read_excel(file, sheet_name=sheet)
        #         for _, row in df.iterrows():
        #             row = dict(row)
        #             row["user"] = session["email"]
        #             mongo.db[collection].update(dict(row), dict(row), upsert=True)
        #         sheet_end_time = time.time()
        #         print(f"Time taken form file {sheet} = {sheet_end_time-sheet_start_time}")

        for file in request.files.getlist('file'):
            for sheet, collection in zip(REQUIRED_SHEETS, COLLECTION_NAMES):
                sheet_start_time = time.time()
                df = pd.read_excel(file, sheet_name=sheet)
                df["user"] = session["email"]  # added new column user with constant value users email
                records = df.to_dict(orient='records')  # converted each row to dict
                mongo.db[collection].insertMany(records, {"ordered": False})
                sheet_end_time = time.time()
                print(f"Time taken form file {sheet} = {sheet_end_time-sheet_start_time}")
        end_time = time.time()
        return redirect(url_for(".user", msg=f"File Uploaded Successfully Time taken {end_time-start_time}"))

    except Exception as e:
        return redirect(url_for(".user", error=str(e)))
