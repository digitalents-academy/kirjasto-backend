# from flask import Flask, jsonify
import uuid
from flask import request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import collection


class User:

    def start_session(self, user):
        del user['Password']
        session['logged_in'] = True
        session['user'] = user
        # return jsonify(user), 200
        return user, 200

    def signup(self):

        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "Username": request.form.get('name'),
            "Email": request.form.get('email'),
            "Password": request.form.get('password'),
            "Mean_score": 0,
            "Mean_count": 0
        }

        # Encrypt the password
        user['Password'] = pbkdf2_sha256.encrypt(user['Password'])

        # Check for existing email address
        if collection.find_one({"Email": user['Email']}):
            return {"error": "Email address already in use"}, 400

        if collection.insert_one(user):
            return self.start_session(user)

        return {"error": "Signup failed"}, 400

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):

        user = collection.find_one({
            "Email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(
                request.form.get('password'),
                user['Password']):
            return self.start_session(user)

        return {"error": "Invalid login credentials"}, 401
