from flask import Flask, render_template, redirect, url_for, flash, session
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user

#Testing
from flask_restful import Resource, Api, reqparse
from pymongo import ALL, MongoClient
import db_secret

app = Flask(__name__)
api = Api(app)

# Initiate connection to mongoDB
client = MongoClient("mongodb+srv://"+ db_secret.secret_id +":"+ db_secret.secret_key +"@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['kirjasto-backend']
collection = db['backendAPI']

#Used to "connect" to mysql
#app.config['SECRET_KEY'] = 'a really really really really long secret key'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/flask_app_db' # enter //<mysql:username>:<mysql:password>@
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

#Testing
#Pretty sure this isn't important
def user_profile(user_id):
    return "Profile page of user #{}".format(user_id), 200

#Testing
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = collection.session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('admin')), 200

        flash("Invalid username/password", 'error')
        return redirect(url_for('login')), 401
    #return render_template('login.html', form=form), 200
    return "logged in", 200

#Testing
@app.route('/logout/')
@login_required
def logout():
    logout_user()    
    flash("You have been logged out.")
    #return redirect(url_for('login')), 200
    return "logged out", 200

#Testing
@app.route('/admin/')
@login_required
def admin():
    #return render_template('admin.html'), 200
    return "admin", 200

#Testing
@login_manager.user_loader
def load_user(user_id):
    return collection.session.query(User).get(user_id), 200

#Testing
class User(collection.Model, UserMixin):
    __tablename__ = 'users'
    id = collection.Column(collection.Integer(), primary_key=True)
    name = collection.Column(collection.String(100))
    username = collection.Column(collection.String(50), nullable=False, unique=True)
    email = collection.Column(collection.String(100), nullable=False, unique=True)
    password_hash = collection.Column(collection.String(100), nullable=False)
    created_on = collection.Column(collection.DateTime(), default=datetime.utcnow)
    updated_on = collection.Column(collection.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

if __name__ == "__main__":
    app.run()