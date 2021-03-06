"""models.py: File that contains user class."""

import uuid
import datetime
from flask import session, redirect
from passlib.hash import pbkdf2_sha256
import jwt
from flask_restful import reqparse
from app import collection, app

parser = reqparse.RequestParser()


class User:
    """Class that contains necessary user functions."""

    def start_session(self, user):
        """Function that starts session."""

        del user["Password"]
        session['logged_in'] = True
        session['user'] = user
        session['user']['token'] = "No token"

        if user["Admin"]:
            token = jwt.encode(
                {
                    "Username": user["Username"],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(
                        minutes=30)
                    },
                app.config['SECRET_KEY']
                )
            session['user']['token'] = token

        return session['user'], 200

    def signup(self):
        """Function that creates a new user and starts the session."""

        parser.add_argument('name', required=True, type=str)
        parser.add_argument('email', required=True, type=str)
        parser.add_argument('password', required=True, type=str)

        args = parser.parse_args()

        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "Username": args['name'],
            "Email": args['email'],
            "Password": args['password'],
            "Mean_score": 0,
            "Mean_count": 0,
            "Admin": False
            }

        # Encrypt the password
        user["Password"] = pbkdf2_sha256.encrypt(user["Password"])

        # Check for existing email address
        if collection.find_one({
            "Email": user["Email"]
            }) or collection.find_one({
                "Username": user["Username"]
                }):
            return {"error": "Email address or username already in use"}, 400

        if collection.insert_one(user):
            return self.start_session(user)

        return {"error": "Signup failed"}, 400

    def signout(self):
        """
        Function that clears the session
        and redirects the user to the home page.
        """

        session.clear()
        return redirect('/')

    def login(self):
        """Function that starts a new session for a old user."""

        parser.add_argument('email', required=True, type=str)
        parser.add_argument('password', required=True, type=str)

        args = parser.parse_args()

        user = collection.find_one({
            "Email": args['email']
        })

        if user and pbkdf2_sha256.verify(
                args['password'],
                user["Password"]):
            return self.start_session(user)

        return {"error": "Invalid login credentials"}, 401
