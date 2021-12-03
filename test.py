import pandas as pd
import os
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


connection = MongoClient()
# deposites_and_withdrawals | exchange_trades | additional_transfers
db = connection["wazirx_analytics"]
counter = 0


"""
prototype 1 for inserting data in dbs
"""

for file in os.listdir(EXCEL_FILE_PATH)[:-3]:
    file_path = os.path.join(EXCEL_FILE_PATH, file)
    df = pd.read_excel(file_path, sheet_name=REQUIRED_SHEETS[0])
    print(file)
    for _, row in df.iterrows():
        counter += 1
        db["additional_transfers"].update(
            dict(row), dict(row), upsert=True)

    print("-"*80)

print("counter ", counter)
