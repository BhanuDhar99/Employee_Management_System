from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import sqlite3
import pickle
import pandas as pd
import os
import numpy as np


app = Flask(__name__)

#HOME PAGE 
@app.route('/')
def index():
        return render_template('index.html')
@app.route('/about')
def about_fun():
        return render_template('about.html')

@app.route('/login')
def login_fun():
        return render_template('login.html')

@app.route('/signup')
def signup_fun():
        return render_template('signup.html')

@app.route('/admin_signup')
def admin_singup():
        return render_template('admin_signup.html')
@app.route('/admin_login')
def admin_login():
        return render_template('admin_login.html')

#now to store_signup info in database
@app.route('/store_signup_info', methods =['GET','POST'])
def store_func():

        fname = request.form['Fname']
        lname = request.form['Lname']
        email = request.form['Email']
        password = request.form['password']
        phno = request.form['PhoneNumber']
        org_name = request.form['Organization']

        #now to store in our database
        with sqlite3.connect('ems.db') as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO UserInfo VALUES(?,?,?,?,?,?)''',(fname,lname,email,password,phno,org_name))
                con.commit
        return render_template('signup_conf.html')

#this route is called after user enters login information
@app.route('/login_check', methods = ['GET', 'POST'])
def login_check_fun():
        email = request.form['Email']
        password = request.form['Password']
        with sqlite3.connect('ems.db') as con:
                cur = con.cursor()
                cur.execute('''SELECT Password from UserInfo where Email = ?''',(email,))
                correct_password = cur.fetchall()
        if(correct_password[0][0]==password):
                return render_template('successful_user_login.html')
        else:
                return render_template('unsuccessful_user_login.html')



if __name__ == '__main__':
        app.run(debug=True)
