import os
import openpyxl
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file, make_response, \
    Response, jsonify
from datetime import datetime
from portal.db_setup import bankdb
from portal.db_setup import db
import random
import requests
import json
from portal import APP

admin_bp = Blueprint('bankportal', __name__, url_prefix='/bank', template_folder="./templates",
                     static_folder="./static")


@admin_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        records = bankdb.Users
        user = records.find_one({'username': username, "password": password})
        # user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        # conn.close()
        # print(user)
        if user:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            print('mdmmd')
            return redirect(url_for('bankportal.transactions'))
        else:
            return "Invalid credentials, please try again."
    return render_template('login.html')


@admin_bp.route('/transactions')
def transactions():
    if 'username' in session:
        user_id = session['user_id']
        records = bankdb.BankTransactions
        transactions = records.find({'user_id': user_id})
        # transactions = conn.execute('SELECT * FROM transactions2 WHERE user_id = ?', (user_id,)).fetchall()
        # conn.close()
        return render_template('transactions.html', transactions=transactions)
    else:
        return redirect(url_for('login'))


def call_fraud_detection(nameDest, user_id, transaction_id):
    URL_MAIN = APP.config['URL_MAIN']

    url = URL_MAIN + "/detect_fraud"

    payload = json.dumps({
        "nameDest": nameDest,
        "user_id": user_id,
        'transaction_id': transaction_id
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return jsonify(response)


# Route for making payments
@admin_bp.route('/make_payment', methods=['GET', 'POST'])
def make_payment():
    if 'username' in session:
        user_id = session['username']
        amount = float(request.form['amount'])
        records = bankdb.Users
        user = records.find_one({'username': user_id})

        if 0 < amount <= user['balance']:

            records2 = bankdb.AccountDetails

            nameDest = request.form['nameDest']

            account_details = records2.find_one({'user_id': user_id})
            transaction_id = ''

            ret_response_ = call_fraud_detection(nameDest, user_id, transaction_id)

            isFraud = ret_response_["isFraud"]
            status = ret_response_["status"]
            flag_ = ret_response_["flag_"]

            if flag_ == "wait":
                nameOrig = user['nameOrig']
                oldbalanceOrg = round(account_details["Avl_balance"], 2)
                newbalanceOrig = round(account_details["newbalanceOrig"], 2)

                user_check_for_transation = records2.find_one({'Account_Number': nameDest})
                oldbalanceDest = user_check_for_transation["oldbalanceDest"]
                newbalanceDest = user_check_for_transation["newbalanceDest"]

                new_record_ = {"transaction_id": transaction_id, "amount": amount,
                               "nameOrig": nameOrig, "oldbalanceOrg": oldbalanceOrg,
                               "newbalanceOrig": newbalanceOrig, "nameDest": nameDest,
                               "oldbalanceDest": oldbalanceDest, "newbalanceDest": newbalanceDest,
                               "isFraud": isFraud, "isFlaggedFraud": 0, "user_id": user_id, "status": status,"Date_of_transcation":datetime.now()}
                transactio_isert = bankdb.BankTransactions
                transactio_isert.insert_one(new_record_)
                return redirect(url_for('home'))
            elif flag_ == "Fraud":
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
                nameOrig = user['nameOrig']

                oldbalanceOrg = round(account_details["Avl_balance"], 2)
                newbalanceOrig = round(account_details["newbalanceOrig"], 2)
                type = random.choice(type)
                Expense_Income = random.choice(Expense_Income),

                user_check_for_transation = records2.find_one({'nameDest': nameDest})
                oldbalanceDest = user_check_for_transation["oldbalanceDest"]
                newbalanceDest = user_check_for_transation["newbalanceDest"]
                status = status
            new_record_ = {"type": type, "amount": amount,"transaction_id":transaction_id,
                           "nameOrig": nameOrig, "oldbalanceOrg": oldbalanceOrg,
                           "newbalanceOrig": newbalanceOrig, "nameDest": nameDest,
                           "oldbalanceDest": oldbalanceDest, "newbalanceDest": newbalanceDest, "isFlaggedFraud": 0,
                           "Category": Category,
                           "Expense/Income": Expense_Income, "user_id": user_id, "status": status}
            transactio_isert = bankdb.BankTransactions
            transactio_isert.insert_one(new_record_)

            transactio_isert2 = db.fraudcollection
            transactio_isert2.insert_one(new_record_)

            return redirect(url_for('home'))
        else:
            return "Insufficient balance or invalid amount."
    else:
        return redirect(url_for('login'))
#
# # Route for logging out


# if __name__ == '__main__':
#     app.run(debug=True)
