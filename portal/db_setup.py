from pymongo import MongoClient
from portal import APP
import pandas as pd
import time
import random


MONGO_URI = APP.config['MONGO_URI']
client = MongoClient(MONGO_URI)

db = client.get_database('SpookyFinanceHubDb')
bankdb = client.get_database('BankPortal')
# records = db.fraudcollection
# records.count_documents({})
#
# read_excel_ = pd.read_excel(
#     "/Users/sandeepkumarrudhravaram/HACKUNT2024/SpookyFinanceHub/Final_Transaction_Data_30K.xlsx")
# data_to_insert = read_excel_.to_dict(orient='records')
#
# user_ids = [f'User{i}' for i in range(9)] + ['SandeepR']
# random.shuffle(user_ids)
#
# for i in data_to_insert:
#     if i['isFraud']==1:
#         try:
#             i['user_id'] = random.choice(user_ids)
#             records.insert_one(i)
#             print("Data inserted successfully!")
#         except:
#             time.sleep(2)
#             records.insert_one(i)
#             print("Data inserted successfully!")

# # Insert data into MongoDB
# if data_to_insert:
#     records.insert_many(data_to_insert)
#     print("Data inserted successfully!")
# else:
#     print("No data to insert.")

# records.insert_many(read_excel_)

#C2127862399