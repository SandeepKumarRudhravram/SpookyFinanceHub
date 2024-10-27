from pymongo import MongoClient
from datetime import datetime


# Step 1: Connect to MongoDB
MONGO_URI = "mongodb+srv://root:root12345@spookyfinancehubv2.ia1zt.mongodb.net/?retryWrites=true&w=majority&appName=SpookyFinanceHubV2"
client = MongoClient(MONGO_URI)

# Step 2: Select the database and collection
bankdb = client.get_database('BankPortal')
collection = bankdb['BankTransactions']  # Replace 'your_collection_name' with the correct collection name


# Get the current year and month
current_year = datetime.now().year
current_month = datetime.now().month

# Define the user to filter by (e.g., "C540962910")
user_name_orig = "C540962910"

# Aggregation pipeline to calculate the total amount spent in the current month for the specific user and approved transactions
pipeline = [
    # Filter for non-empty Date_of_transcation, specific user, and approved transactions
    {
        "$match": {
            "Date_of_transcation": {"$ne": ""},
            "nameOrig": user_name_orig,
            "status": "Approved"
        }
    },
    # Match transactions from the current month and year
    {
        "$match": {
            "$expr": {
                "$and": [
                    {"$eq": [{"$year": {"$dateFromString": {"dateString": "$Date_of_transcation", "onError": None, "onNull": None}}}, current_year]},
                    {"$eq": [{"$month": {"$dateFromString": {"dateString": "$Date_of_transcation", "onError": None, "onNull": None}}}, current_month]}
                ]
            }
        }
    },
    # Sum the total amount spent
    {
        "$group": {
            "_id": None,
            "total_spent": {"$sum": {"$toDouble": "$amount"}}
        }
    }
]

# Execute the aggregation pipeline
result = list(collection.aggregate(pipeline))

print(result)

# Print the total amount spent for the user
if result:
    total_spent = result[0]['total_spent']
    print(f"Total amount spent by user '{user_name_orig}' in the current month: {total_spent}")
else:
    print(f"No transactions found for user '{user_name_orig}' in the current month.")