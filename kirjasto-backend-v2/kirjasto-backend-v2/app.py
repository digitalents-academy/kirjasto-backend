from flask import Flask, render_template, session, redirect
from functools import wraps
from pymongo.mongo_client import MongoClient
import pymongo
import db_secret
app = Flask(__name__)

app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Own Database (localhost or 127.0.0.1 or 0.0.0.0)
#client = pymongo.MongoClient('localhost', 27017)
#db = client.user_login_system

#Kirjasto Database
client = MongoClient("mongodb+srv://"+ db_secret.secret_id +":"+ db_secret.secret_key +"@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['kirjasto-backend']
collection = db['user_login_system']
#db = client.user_login_system

# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap

# Routes
from user import routes

@app.route('/')
def home():
    return render_template('home.html')
    #return "home"

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')
    #return "dashboard"

#if __name__ == "__main__":
    #app.run(debug=True)