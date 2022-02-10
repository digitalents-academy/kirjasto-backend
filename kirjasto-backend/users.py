"""
users.py: File that contains necessary funktions
for updating, editing and deleting user data from the database.
"""

from pymongo import MongoClient
from flask_restful import reqparse
import db_secret

# Initiate connection to mongoDB
client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":" + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
collection = db['users']
retrieved_user_collection = list(collection.find({}, {'_id': False}))


def get_users():
    """Function that returns all users."""

    return retrieved_user_collection


def get_user_by_id(object_id):
    """Function that returns user data depending on the id."""

    retrieved = list(collection.find({'_id': object_id}))
    return retrieved


def get_user_by_username(user_name):
    """
    Function that returns user data from the database
    depending on the username.
    """

    retrieved = list(
        collection.find({'Username': user_name}, {'_id': False})
        )
    return retrieved


#Id is a dictionary so isn't operable atm
def update_user(object_id, user_name, email, password):
    """Function that posts updated user_data to the database."""

    collection.update(
        {'_id': object_id},
        {
            "$set": {
                "Username": user_name,
                "Email": email,
                "Password": password
                }
            }
        )


#Is user, email and password needed?
def delete_user_by_id(object_id):
    """Function that deletes a user from the database."""

    collection.delete_one({"_id": object_id})
