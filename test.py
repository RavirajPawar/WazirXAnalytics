import os
import pandas as pd
from pymongo import MongoClient

"""
WazirX_TradeReport_2021-01-01_2021-03-31.xlsx 9
['Account Balance', 'Account Ledger', 'Additional Transfers', 'Deposits and Withdrawals', 'Exchange Trades', 'P2P Trades', 'STF Trades', 'Third party transfers', 'WazirX']
--------------------------------------------------
WazirX_TradeReport_2021-04-01_2021-06-30.xlsx 9
['Account Balance', 'Account Ledger', 'Additional Transfers', 'Deposits and Withdrawals', 'Exchange Trades', 'P2P Trades', 'STF Trades', 'Third party transfers', 'WazirX']
--------------------------------------------------
WazirX_TradeReport_2021-07-01_2021-11-28.xlsx 10
['Account Balance', 'Account Ledger', 'Additional Transfers', 'Deposits and Withdrawals', 'Exchange Trades', 'OTC Trades', 'P2P Trades', 'STF Trades', 'Third party transfers', 'WazirX']
--------------------------------------------------
"""

EXCEL_FILE_PATH = "excel"
REQUIRED_SHEETS = ['Additional Transfers',
                   'Exchange Trades',
                   'Deposits and Withdrawals'
                   ]
COLLECTION_NAMES = ["additional_transfers",
                    "exchange_trades",
                    "deposits_and_withdrawals"]

connection = MongoClient()

db = connection["wazirx_analytics"]
counter = 0

"""
prototype 1 for inserting data in dbs
additional_transfers 874 additional_transfers
exchange_trades 80
deposits_and_withdrawals 8

"""

for file in os.listdir(EXCEL_FILE_PATH)[:]:
    file_path = os.path.join(EXCEL_FILE_PATH, file)
    for sheet, collection in zip(REQUIRED_SHEETS, COLLECTION_NAMES):
        df = pd.read_excel(file_path, sheet_name=sheet)
        print(file)
        for _, row in df.iterrows():
            counter += 1
            db[collection].update(
                dict(row), dict(row), upsert=True)

        print("-" * 80)

print("counter ", counter)
