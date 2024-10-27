import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file, make_response, \
    Response, jsonify
import threading
from . import APP, LOG
import requests
from urllib.request import urlopen
import certifi
import json
from portal.db_setup import db
from portal.db_setup import bankdb
import random
from datetime import datetime

bp = Blueprint('view', __name__, url_prefix='/', template_folder="./templates", static_folder="./static")


#

# def real_time_price():



@bp.route('/real_time_price', methods=["GET", "POST"])
def real_time_price():
    url = "https://financialmodelingprep.com/api/v3/stock/full/real-time-price?apikey=wGFHzWmVJq5Tm8KLFou68nkMp2LbL4fB"
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


@bp.route('/detect_fraud', methods=["GET", "POST"])
def detect_fraud():
    data = request.json
    nameDest = data["nameDest"]
    # user_id = data["user_id"]
    # transaction_id=data["transaction_id"]
    fraudcollection_db = db.fraudcollection
    user = fraudcollection_db.find_one({'nameDest': nameDest})
    if user:
        return jsonify({"isFraud": 1, "status": "Declined","flag_":"Fraud"})

    else:
        return jsonify({"isFraud": '', "status": "Pending Review", "flag_": "wait"})


@bp.route('/verification/<string:transaction_id>')
def verification_transaction(transaction_id):
    data = request.json
    user_id = data['user_id']
    isFraud = data['isFraud']
    transactiovisert = bankdb.BankTransactions
    transactions = transactiovisert.find({'transaction_id': transaction_id})
    records2 = bankdb.AccountDetails
    account_details = records2.find_one({'user_id': user_id})
    amount = transactions["amount"]
    nameDest = account_details["Account_Number"]
    if isFraud == 0:
        categories = [
            "Business",
            "Convenience",
            "Entertainment",
            "Food",
            "Grocery",
            "Sport",
            "Subscription"
        ]
        Expense_Income = [
            "Expense",
            "Income"
        ]

        type = [
            "CASH_OUT",
            "TRANSFER",
            "PAYMENT"
        ]
        Category = random.choice(categories)

        oldbalanceOrg = round(account_details["Avl_balance"], 2)
        newbalanceOrig = round(account_details["Avl_balance"] - amount, 2)
        type = random.choice(type)
        Expense_Income = random.choice(Expense_Income),

        user_check_for_transation = records2.find_one({'nameDest': nameDest})
        oldbalanceDest = user_check_for_transation["newbalanceDest"]
        newbalanceDest = user_check_for_transation["newbalanceDest"] + amount

        isFraud = 0
        status = "approved"
        transactio_isert = bankdb.BankTransactions
        transactio_isert.update_one({"transaction_id": transaction_id},{"Category":Category,"Expense_Income":Expense_Income,"oldbalanceOrg": oldbalanceOrg,
                       "newbalanceOrig": newbalanceOrig, "nameDest": nameDest,
                       "oldbalanceDest": oldbalanceDest, "newbalanceDest": newbalanceDest,
                       "isFraud": isFraud, "isFlaggedFraud": 0, "status": status,"type":type})
    else:
        categories = [
            "Business",
            "Convenience",
            "Entertainment",
            "Food",
            "Grocery",
            "Sport",
            "Subscription"
        ]
        Expense_Income = [
            "Expense"
        ]

        type = [
            "CASH_OUT",
            "TRANSFER",
            "PAYMENT"
        ]
        Category = random.choice(categories)
        nameOrig = nameDest

        oldbalanceOrg = round(account_details["Avl_balance"], 2)
        newbalanceOrig = round(account_details["newbalanceOrig"], 2)
        type = random.choice(type)
        Expense_Income = random.choice(Expense_Income),

        user_check_for_transation = records2.find_one({'nameDest': nameDest})
        oldbalanceDest = user_check_for_transation["oldbalanceDest"]
        newbalanceDest = user_check_for_transation["newbalanceDest"]
        status = "Declined"
        new_record_ = {"type": type, "amount": amount, "transaction_id": transaction_id,
                       "nameOrig": nameOrig, "oldbalanceOrg": oldbalanceOrg,
                       "newbalanceOrig": newbalanceOrig, "nameDest": nameDest,
                       "oldbalanceDest": oldbalanceDest, "newbalanceDest": newbalanceDest, "isFlaggedFraud": 0,
                       "Category": Category,
                       "Expense/Income": Expense_Income, "user_id": user_id, "status": status}
        transactio_isert = bankdb.BankTransactions
        transactio_isert.insert_one(new_record_)
        transactio_isert2 = db.fraudcollection
        transactio_isert2.insert_one(new_record_)
    return redirect(url_for('login'))



@bp.route('/LMDBC/<string:userid>')
def LastMonthDataByCat(userid):
    collection = bankdb.BankTransactions


    # Get the current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Define the user to filter by (e.g., "C540962910")

    # Aggregation pipeline to filter by current month, user, and handle empty/invalid date strings
    pipeline = [
        # Filter out documents with empty or null Date_of_transcation and match the specific user
        {
            "$match": {
                "Date_of_transcation": {"$ne": ""},
                "nameOrig": userid
            }
        },
        # Match transactions from the current month and year
        {
            "$match": {
                "$expr": {
                    "$and": [
                        {"$eq": [{"$year": {"$dateFromString": {"dateString": "$Date_of_transcation", "onError": None,
                                                                "onNull": None}}}, current_year]},
                        {"$eq": [{"$month": {"$dateFromString": {"dateString": "$Date_of_transcation", "onError": None,
                                                                 "onNull": None}}}, current_month]}
                    ]
                }
            }
        },
        # Group by Category and count occurrences
        {
            "$group": {
                "_id": "$Category",
                "count": {"$sum": 1}
            }
        },
        # Sort by count in descending order
        {
            "$sort": {
                "count": -1
            }
        }
    ]

    # Execute the aggregation pipeline
    result = list(collection.aggregate(pipeline))

    # Print the results
    for record in result:
        print(f"Category: {record['_id']}, Count: {record['count']}")

    return jsonify(result)


@bp.route('/LMDBC/<string:userid>')
def MonthDataExp(userid):
    collection = bankdb.BankTransactions

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
                        {"$eq": [{"$year": {"$dateFromString": {"dateString": "$Date_of_transcation", "onError": None,
                                                                "onNull": None}}}, current_year]},
                        {"$eq": [{"$month": {"$dateFromString": {"dateString": "$Date_of_transcation", "onError": None,
                                                                 "onNull": None}}}, current_month]}
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

    return jsonify(result)



