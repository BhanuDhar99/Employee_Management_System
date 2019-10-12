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
@app.route('/store_signup_info', methods=['GET', 'POST'])
def store_func():
        return render_template('signup_conf.html')

if __name__ == '__main__':
        app.run(debug=True)
