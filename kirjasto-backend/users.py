"""
users.py: File that contains necessary funktions
for updating, editing and deleting user data from the database.
"""

from pymongo import MongoClient
from flask_restful import reqparse
from passlib.hash import pbkdf2_sha256
import db_secret
from helpers import (
    is_email_inside_user_collection,
    is_object_id_inside_user_collection,
    is_password_inside_user_collection,
    is_user_name_inside_user_collection
    )

# Initiate connection to mongoDB
client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":" + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
user_collection = db['users']
retrieved_user_collection = list(user_collection.find({}, {'_id': False}))
parser = reqparse.RequestParser()


def get_users():
    """Function that returns all users."""

    return retrieved_user_collection


def get_user_by_id(object_id):
    """Function that returns user data depending on the id."""

    retrieved = list(user_collection.find({'_id': object_id}))
    return retrieved


def get_user_by_username(user_name):
    """
    Function that returns user data from the database
    depending on the username.
    """

    retrieved = list(
        user_collection.find({'Username': user_name}, {'_id': False})
        )
    return retrieved


#The error handling for checking whether update was succesful
#needs to be edited.
def update_user():
    """Function that posts updated user_data to the database."""

    old_user_name = ""
    old_email = ""
    old_password = ""

    parser.add_argument('object_id', required=True, type=str)
    parser.add_argument('user_name', required=True, type=str)
    parser.add_argument('email', required=True, type=str)
    parser.add_argument('password', required=True, type=str)

    args = parser.parse_args()

    if is_object_id_inside_user_collection(args["object_id"]) is False or \
            is_user_name_inside_user_collection(args["user_name"]) \
            is False or is_email_inside_user_collection(args["email"]) \
            is False or is_password_inside_user_collection(args["password"]) \
            is False:
        return "error: Not a valid book_id, name, isbn or rating! " \
                "book_id, name and isbn must be inside the database!"

    for user in retrieved_user_collection:
        if user["_id"] == args["object_id"]:
            old_user_name = user["Username"]
            old_email = user["Email"]
            old_password = user["Password"]

    user_collection.update(
        {'_id': args["object_id"]},
        {
            "$set": {
                'Username': args['user_name'],
                'Email': args['email'],
                'Password': pbkdf2_sha256.encrypt(args['password'])
                }
            }
        )

    if old_user_name != "" or old_user_name != args["user_name"] or \
            old_email != "" or old_email != args["email"] or \
            old_password != "" or old_password != args["password"]:
        return
    return "Something went wrong!"


def delete_user_by_id():
    """Function that deletes a user from the database."""

    parser.add_argument('object_id', required=True, type=str)

    args = parser.parse_args()

    if is_object_id_inside_user_collection(args["object_id"]) is False:
        return "error: Not a valid object_id! " \
                "object_id must be inside the database!"

    user_collection.delete_one({"_id": args["object_id"]})

    if is_object_id_inside_user_collection(args["object_id"]) is False:
        return "Something went wrong!"
