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


if __name__ == '__main__':
        app.run(debug=True)
