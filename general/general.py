import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from flask import Blueprint, render_template, request, session, redirect, url_for

from database import mongo
from .constants import REQUIRED_SHEETS, COLLECTION_NAMES
from .utility import get_referral_data, get_total_deposits_and_withdrawals, check_files

general_blueprint = Blueprint('general', __name__,
                              template_folder='templates',
                              static_folder='static')


@general_blueprint.route("/user")
def user():
    """
    login dashboard for user where they can see upload section, fear & greed index and referral earnings.
    """
    if not session.get("email"):
        return redirect("/login")
    # referral data section
    referral_data = mongo.db.additional_transfers.find({"user": session.get("email")}, {'_id': False})
    referral_earnings = get_referral_data(referral_data)
    # deposit withdrawals section
    deposits_and_withdrawals_data = mongo.db.deposits_and_withdrawals.find({"user": session.get("email")},
                                                                        {'_id': False})
    total_deposits_and_withdrawals = get_total_deposits_and_withdrawals(deposits_and_withdrawals_data)
    # File upload status will come through upload-file view
    file_upload_msg = request.args.get("msg")
    file_upload_error = request.args.get("error")
    return render_template("general/general.html", referral_earnings=referral_earnings,
                           total_deposits_and_withdrawals=total_deposits_and_withdrawals,
                           msg=file_upload_msg, error=file_upload_error)


def update_document(collection, document):
    """
    For insertion we are using update document cause we want to avoid duplicates in db
    """
    return mongo.db[collection].update(dict(document), dict(document), upsert=True)


async def threaded_upload(collection_row_container):
    """
    Uses ThreadPoolExecutor for Threading. each collection and its record is created as task
    """
    with ThreadPoolExecutor(max_workers=None) as executor:  # max_workers None creates cpu * 5 number of threads
        loop = asyncio.get_event_loop()
        tasks = list()
        for collection, documents in collection_row_container.items():
            for document in documents:
                tasks.append(
                    loop.run_in_executor(
                        executor,
                        update_document,
                        *(collection, document)
                    )
                )
        return await asyncio.gather(*tasks)


@general_blueprint.route("/upload-file", methods=["GET", "POST"])
def upload_file():
    """
    Verifies and uploads WazirX report to db.
    """
    start_time = time.time()
    if not session.get("email"):
        return redirect("/login")
    try:
        file_status = check_files(request)
        if file_status:
            return redirect(url_for(".user", error=file_status))
        collection_row_container = {collection: [] for collection in COLLECTION_NAMES}
        # below section segregate file sheets and each row in sheet
        for file in request.files.getlist('file'):
            for sheet, collection in zip(REQUIRED_SHEETS, COLLECTION_NAMES):
                df = pd.read_excel(file, sheet_name=sheet)
                df["user"] = session["email"]  # added new column user with constant value users email
                documents = df.to_dict(orient='records')  # converted each row to dict
                collection_row_container[collection].extend(documents)
        # multi threading section begins
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(threaded_upload(collection_row_container))
        loop.run_until_complete(future)
        end_time = time.time()
        return redirect(url_for(".user", msg=f"File Uploaded Successfully Time taken {end_time - start_time}"))

    except Exception as e:
        print(e)
        return redirect(url_for(".user", error=str(e)))
