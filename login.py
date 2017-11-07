#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys, time

from flask import Flask, redirect, url_for, request, render_template, session
from pymongo import MongoClient
from validate_email import validate_email

import os

PORT = int(os.getenv('VCAP_APP_PORT', '8000'))

global name, flag1, flag2, user, password, account_number, balance, amount, account_number2, balance2, error, typo

app = Flask(__name__)
app.secret_key = "123213"


@app.route('/')
def welcome():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
    db = client.onlinebank

    flag1 = 0
    flag2 = 0
    user = 0
    password = 0

    if request.method == 'POST':
        user = request.form['user_id']
        password = request.form['password']
    cursor = db.users.find({"id": user}, {"password": 1, "_id": 0})

    for document in cursor:
        for key in document:
            value = document[key]
            if value == password:
                flag1 = 1

    cursor = db.users.find({"id": user}, {"type": 1, "_id": 0})

    for document in cursor:
        for key in document:
            value = document[key]
            if value == "admin":
                flag2 = 1
            elif value == "manager":
                flag2 = 2
            elif value == "employee":
                flag2 = 3
            elif value == "customer":
                flag2 = 4
            else:
                flag2 = 5
    cursor = db.users.find({"id": user}, {"name": 1, "_id": 0})
    for document in cursor:
        for key in document:
            name = document[key]
            session['name'] = name

    if flag1 and flag2 == 1:
        session['username'] = user
        # session['name'] = name
        return render_template('admin.html')
    elif flag1 and flag2 == 2:
        session['username'] = user
        # session['name'] = name
        return render_template('manager.html')
    elif flag1 and flag2 == 3:
        session['username'] = user
        # session['name'] = name
        return render_template('employee.html')
    elif flag1 and flag2 == 4:
        session['username'] = user
        # session['name'] = name
        return render_template('customer.html')
    elif not (flag1) or flag2 == 5 or flag2 == 0:
        return render_template('login_again.html')

    return render_template('login_again.html')


@app.route('/adde', methods=['POST', 'GET'])
def adde():
    return render_template('add.html')


@app.route('/add', methods=['POST', 'GET'])
def add():
    client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
    db = client.onlinebank

    # if request.method == 'POST':
    user = request.form['user_id']
    password = request.form['password']
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    mobile = request.form['mobile']
    email = request.form['email']
    address = request.form['address']
    joindate = request.form['joindate']
    # post = request.form['post']

    is_valid = validate_email(email)
    length = len(mobile)

    if is_valid and length == 10:
        db.employee.insert_one(
            {
                "id": user,
                "name": name,
                "age": age,
                "gender": gender,
                "mobile": mobile,
                "email": email,
                "address": address,
                "join_date": joindate
            }
        )
        error = 0

    else:
        error = 1
        return render_template('add.html', error=error)

    if not (error):
        db.users.insert_one(
            {
                "id": user,
                "name": name,
                "type": "employee",
                "password": password
            }
        )

    return render_template('added.html')


@app.route('/create1', methods=['POST', 'GET'])
def create1():
    return render_template('create.html')


@app.route('/create', methods=['POST', 'GET'])
def create_account():
    client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
    db = client.onlinebank

    # if request.method == 'POST':
    user = request.form['user_id']
    password = request.form['password']
    account_number = request.form['account_number']
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    mobile = request.form['mobile']
    email = request.form['email']
    address = request.form['address']
    pancard = request.form['pancard']
    aadhaar = request.form['aadhaar']
    opening_date = request.form['opening_date']
    initial_amount = request.form['initial_amount']
    verify = request.form['verify']

    is_valid = validate_email(email)
    length = len(mobile)

    if is_valid and (verify == "yes" or "YES" or "Yes") and length == 10 and initial_amount >= 5000:

        db.users.insert_one(
            {
                "id": user,
                "type": "customer",
                "name": name,
                "password": password
            }
        )

        db.customer.insert_one(
            {
                "id": user,
                "name": name,
                "age": age,
                "gender": gender,
                "mobile": mobile,
                "email": email,
                "address": address,
                "opening_date": opening_date,
                "account_number": account_number,
                "pancard": pancard,
                "aadhaar": aadhaar,
                "balance": initial_amount

            }
        )
        return render_template('created.html')
    else:
        error = 1
        return render_template('create.html', error=error)


@app.route('/viewAdmin', methods=['POST', 'GET'])
def viewAdmin():
    client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
    db = client.onlinebank
    val = []
    obj = []
    cursor = db.admin.find({"id": session['username']})
    for document in cursor:
        for key in document:
            val.append(document[key])
            obj.append(key)

    return render_template('adminView.html', result=zip(val, obj))


@app.route('/viewEmployee', methods=['POST', 'GET'])
def viewEmployee():
    client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
    db = client.onlinebank
    val = []
    obj = []
    cursor = db.employee.find({"id": session['username']})
    for document in cursor:
        for key in document:
            val.append(document[key])
            obj.append(key)

    return render_template('employeeView.html', result=zip(val, obj))


@app.route('/viewCustomer', methods=['POST', 'GET'])
def viewCustomer():
    client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
    db = client.onlinebank
    val = []
    obj = []
    cursor = db.customer.find({"id": session['username']})
    for document in cursor:
        for key in document:
            val.append(document[key])
            obj.append(key)

    return render_template('customerView.html', result=zip(val, obj))


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('username', None)
    session.pop('name', None)
    session.pop('password', None)

    return render_template('login.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == "GET":
        typo = request.args.get('type')

    return render_template('search.html', result=typo)


@app.route('/searchResult', methods=['POST', 'GET'])
def searchResult():
    if request.method == 'POST':
        account_number = request.form['account_number']
        typo = request.form['type']

    # session['account_number'] = account_number
    client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
    db = client.onlinebank
    cursor = db.customer.find({"account_number": account_number}, {"name": 1, "_id": 0})

    print cursor.count

    if cursor.count()==0:
        error = 1
        return render_template('searchResult.html', result=error)

    for document in cursor:
        name = document['name']

        
    if cursor.count()!=0:
        error = 0
        session['account_number'] = account_number
        session['cust_name'] = name
        return render_template('searchResult.html', result=error, result3=typo)
    # elif cursor.count!=0 and typo=="deposit":
    # 	error=0
    # 	session['account_number'] = account_number
    # 	session['cust_name'] = name
    # 	return render_template('searchResult.html',result2=name,result=error,result3=typo)

    return render_template('search.html')


# @app.route('/withdrawalp', methods = ['POST', 'GET'])
# def withdrawalp():
# 	return render_template('withdrawal.html')

@app.route('/withdrawal', methods=['POST', 'GET'])
def withdrawal():
    if request.method == 'POST':
        amount = request.form['amount']

    account_number = session['account_number']
    client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
    db = client.onlinebank

    cursor = db.customer.find({"account_number": account_number}, {"balance": 1, "name": 1, "_id": 0})

    for document in cursor:
        balance = document['balance']
        name = document['name']

    if (int(amount)<=int(balance)):
        balance = int(balance) - int(amount)
        db.customer.update_one({"account_number": account_number}, {"$set": {"balance": balance}})
        db.withdrawal.insert_one(
            {
                "Transaction_id": session['account_number'][0:5] + time.strftime("%Y%m%d"),
                "Description": 'Cash Withdrawal',
                "Account_number": account_number,
                "Debit": amount,
                "Employee_id": session['username'],
                "Time": time.ctime(),
                "Status": 'Successfull'
            }
        )
        error = 0
        return render_template('withdrawal.html', result1=balance, result2=amount, result3=error)

    else:
        error = 1
        return render_template('withdrawal.html', result1=balance, result2=amount, result3=error)


    # return render_template('searchResult.html')


# @app.route('/depositp', methods = ['POST', 'GET'])
# def depositp():
# 	return render_template('deposit.html')

@app.route('/deposit', methods=['POST', 'GET'])
def deposit():
    if request.method == 'POST':
        amount = request.form['amount']

    account_number = session['account_number']
    client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
    db = client.onlinebank

    cursor = db.customer.find({"account_number": account_number}, {"balance": 1, "name": 1, "_id": 0})

    for document in cursor:
        balance = document['balance']
        name = document['name']

    if (int(amount)>=500):
        balance = int(balance) + int(amount)
        db.customer.update_one({"account_number": account_number}, {"$set": {"balance": balance}})
        db.deposit.insert_one(
            {
                "Transaction_id": session['account_number'][0:5] + time.strftime("%Y%m%d"),
                "Description": 'Cash Deposit',
                "Account_number": account_number,
                "Credit": amount,
                "Employee_id": session['username'],
                "Time": time.ctime(),
                "Status": 'Successfull'
            }
        )
        error = 0
        return render_template('deposit.html', result1=balance, result2=amount, result3=error)

    else:
        error = 1
        return render_template('deposit.html', result1=balance, result2=amount, result3=error)


    # return render_template('searchResult.html')


@app.route('/transferp', methods=['POST', 'GET'])
def depositp():
    return render_template('transfer.html')


@app.route('/transfer', methods=['POST', 'GET'])
def transfer():
    client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
    db = client.onlinebank
    if request.method == 'POST':
        account_number = request.form['account_number']
        amount = request.form['amount']

    cursor2 = db.customer.find({"id": session['username']}, {"balance": 1, "account_number": 1, "_id": 0})
    cursor = db.customer.find({"account_number": account_number}, {"balance": 1, "_id": 0})

    if cursor.count() == 0:
        return render_template('transferResult.html', result=1)

    for document in cursor2:
        account_number2 = document['account_number']
        balance = document['balance']

    for document in cursor:
        balance2 = document['balance']

    if int(balance) < int(amount):
        print amount
        print balance
        return render_template("transferResult.html", result=2, result2=balance, result3=account_number2 )

    elif int(balance) >= int(amount):
        value1 = int(balance) - int(amount)
        value2 = int(balance2) + int(amount)
        db.customer.update_one({"account_number": account_number}, {"$set": {"balance": value2}})
        db.customer.update_one({"id": session['username']}, {"$set": {"balance": value1}})
        db.transfer.insert_one(
            {
                "Transaction_id": account_number2[0:5] + time.strftime("%Y%m%d"),
                "Description": 'Customer Transfer',
                "Sender": account_number2,
                "Receiver": account_number,
                "Amount": amount,
                "Time": time.ctime(),
                "Status": 'Successfull'
            }
        )
        return render_template('transferResult.html', result=3, result2=amount, result3=value1, result4=account_number)
    else:
        return render_template('transfer.html')

    # return render_template('transfer.html')


@app.route('/withdrawalSummary', methods=['POST', 'GET'])
def withdrawalSummary():
    client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
    db = client.onlinebank

    cursor = db.withdrawal.find({})

    return render_template('withdrawalReport.html',result=cursor)

@app.route('/depositSummary', methods=['POST', 'GET'])
def depositSummary():
    client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
    db = client.onlinebank

    cursor = db.deposit.find({})

    return render_template('depositReport.html',result=cursor)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(PORT), debug=True)
