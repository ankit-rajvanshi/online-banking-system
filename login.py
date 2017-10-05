#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys

from flask import Flask, redirect, url_for, request, render_template, session
from pymongo import MongoClient
from validate_email import validate_email

import os
#import http.server
#import socketserver

PORT = int(os.getenv('VCAP_APP_PORT', '8000'))

#Handler = http.server.SimpleHTTPRequestHandler

#httpd = socketserver.TCPServer(("", PORT), Handler)

#print("serving at port", PORT)
#httpd.serve_forever()

global name, flag1, flag2
app = Flask(__name__)
app.secret_key = "123213"
@app.route('/')
def welcome():
	return render_template('login.html')



@app.route('/login', methods = ['POST', 'GET'])
def login():
	
	client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
	db = client.onlinebank

	flag1=0
	flag2=0
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
			#session['name'] = name

	if flag1 and flag2==1:
		session['username'] = user
		session['name'] = name
		return render_template('admin.html')
	elif flag1 and flag2==2:
		session['username'] = user
		session['name'] = name
		return render_template('manager.html')
	elif flag1 and flag2==3:
		session['username'] = user
		session['name'] = name
		return render_template('employee.html')
	elif flag1 and flag2==4:
		session['username'] = user
		session['name'] = name
		return render_template('customer.html')
	elif not(flag1) or flag2==5:
		return render_template('login_again.html')
			
	return render_template('login_again.html')

@app.route('/adde', methods = ['POST', 'GET'])
def adde():
	return render_template('add.html')

@app.route('/add', methods = ['POST', 'GET'])
def add():

	client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
	db = client.onlinebank
	

	#if request.method == 'POST':
	user = request.form['user_id']
	password = request.form['password']
	name = request.form['name']
	age = request.form['age']
	gender = request.form['gender']
	mobile = request.form['mobile']
	email = request.form['email']
	address = request.form['address']
	joindate = request.form['joindate']
	#post = request.form['post']

	is_valid = validate_email(email)
	length = len(mobile)

	

	if post == "employee" and is_valid and length==10:
		db.employee.insert_one(
			{
				"id": user,
				"name": name,
				"age": age,
				"gender": gender,
				"mobile" : mobile,
				"email" : email,
				"address" : address,
				"join_date" : joindate
			}
		)
		error = 0

	else:
		error = 1
		return render_template('add.html',error=error)

	if not(error):
		db.users.insert_one(
			{
				"id": user,
				"type": post,
				"password" : password
			}
		)
	
	return render_template('added.html')

@app.route('/create1', methods = ['POST', 'GET'])
def create1():
	return render_template('create.html')

@app.route('/create', methods = ['POST', 'GET'])
def create_account():
	
	client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
	db = client.onlinebank

	#if request.method == 'POST':
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

	if is_valid and (verify == "yes" or "YES" or "Yes") and length==10 and initial_amount>=5000:
		
		db.users.insert_one(
			{
				"id": user,
				"type": "customer",
				"name" : name,
				"password" : password
			}
		)

		db.customer.insert_one(
			{
				"id": user,
				"name": name,
				"age": age,
				"gender": gender,
				"mobile" : mobile,
				"email" : email,
				"address" : address,
				"opening_date" : opening_date,
				"account_number" : account_number,
				"pancard" : pancard,
				"aadhaar" : aadhaar,
				"balance" : initial_amount

			}
		)
		return render_template('created.html')
	else:
		error=1
		return render_template('create.html',error=error)



@app.route('/viewAdmin', methods = ['POST', 'GET'])
def viewAdmin():
	client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
	db = client.onlinebank
	val=[]
	obj=[]
	cursor = db.admin.find({"id": session['username']})
	for document in cursor:
		for key in document:
			val.append(document[key])
			obj.append(key)

	return render_template('adminView.html',result=val,result2=obj)


@app.route('/viewEmployee', methods = ['POST', 'GET'])
def viewEmployee():
	client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
	db = client.onlinebank
	val=[]
	obj=[]
	cursor = db.employee.find({"id": session['username']})
	for document in cursor:
		for key in document:
			val.append(document[key])

	return render_template('eployeeView.html',result=val,result2=obj)



@app.route('/viewCustomer', methods = ['POST', 'GET'])
def viewCustomer():
	client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
	db = client.onlinebank
	val=[]
	obj=[]
	cursor = db.customer.find({"id": session['username']})
	for document in cursor:
		for key in document:
			val.append(document[key])

	return render_template('customerView.html',result=val,result2=obj)


if __name__ == '__main__':
	
	app.run(host='0.0.0.0', port=int(PORT), debug=True)
