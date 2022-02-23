"""
users.py: File that contains necessary funktions
for updating, editing and deleting user data from the database.
"""

from pymongo import MongoClient
from flask_restful import reqparse
#from flask import session
from passlib.hash import pbkdf2_sha256
import db_secret
from helpers import (
    checking_if_user_is_authenticated_with_object_id,
    is_object_id_inside_user_collection,
    is_user_name_inside_comment_collection,
    is_user_name_inside_rating_collection,
    is_user_name_inside_user_collection,
    checking_if_user_is_authenticated_with_user_name
    )

client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":" + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
user_collection = db['users']
rating_collection = db['ratings']
comment_collection = db['comments']
retrieved_user_collection = list(user_collection.find({}))
retrieved_rating_collection = list(rating_collection.find({}))
retrieved_comment_collection = list(comment_collection.find({}))
parser = reqparse.RequestParser()


#Not needed?
def get_users():
    """Function that returns all users."""

    if len(retrieved_user_collection) > 0:
        return retrieved_user_collection
    return "Error: There doesn't seem to be any users inside the database!"


def get_user_by_username(user_name):
    """
    Function that returns user data from the database
    depending on the username.
    """

    if is_user_name_inside_user_collection(user_name) is False:
        return 'Error: Not a valid username! Username must exist!'

    if checking_if_user_is_authenticated_with_user_name(user_name) is False:
        return "Error: Access denied!"

    retrieved = list(
        user_collection.find({'Username': user_name}, {'_id': False})
        )

    if len(retrieved) > 0:
        return retrieved
    return "Error: There doesn't seem to be any users inside the database!"


def get_user_by_object_id(object_id):
    """Function that returns user data depending on the object id."""

    if is_object_id_inside_user_collection(object_id) is False:
        return 'Error: Not a valid object id! Object id must exist!'

    if checking_if_user_is_authenticated_with_object_id(object_id) is False:
        return "Error: Access denied!"

    retrieved = list(user_collection.find({'_id': object_id}))

    if len(retrieved) > 0:
        return retrieved
    return "Error: There doesn't seem to be any users inside the database!"


#Not needed atm
# def get_token(object_id):
#     """Function that returns token depending on the object_id"""
#     user = user_collection.find_one({
#         "_id": object_id
#     })
#     if session['user']['_id'] == user['_id'] and user['Admin']:
#         return session['token']
#     else:
#         return "Error: You're not authorized!"


#Needs token_required
def promote_user_to_admin():
    """Function that updates user's admin state."""

    old_admin_state = ""

    parser.add_argument('object_id', required=True, type=str)

    args = parser.parse_args()

    if is_object_id_inside_user_collection(args["object_id"]) is False:
        return "Error: Not a valid object id! " \
            "Object id must be inside the database!"

    for user in retrieved_user_collection:
        if user["_id"] == args["object_id"]:
            old_admin_state = user["Admin"]

    user_collection.update(
        {'_id': args["object_id"]},
        {
            "$set": {
                'Admin': True
                }
            }
        )

    if old_admin_state != "" or old_admin_state != args["admin"]:
        return "User was promoted succesfully!"
    return "Error: Something went wrong!"


#The error handling for checking whether update was succesfull
#needs to be edited.
def update_user():
    """Function that posts updated user data to the database."""

    old_user_name = ""
    old_email = ""
    old_password = ""

    parser.add_argument('object_id', required=True, type=str)
    parser.add_argument('user_name', required=True, type=str)
    parser.add_argument('email', required=True, type=str)
    parser.add_argument('password', required=True, type=str)

    args = parser.parse_args()

    if checking_if_user_is_authenticated_with_object_id(
            args["object_id"]) is False:
        return "Error: Access denied!"

    if is_object_id_inside_user_collection(args["object_id"]) is False:
        return "Error: Not a valid object id! " \
            "Object id must be inside the database!"

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
        return "User was updated succesfully!"
    return "Error: Something went wrong!"


def delete_user_by_object_id():
    """Function that deletes a user from the database."""

    parser.add_argument('object_id', required=True, type=str)

    args = parser.parse_args()

    if checking_if_user_is_authenticated_with_object_id(
            args["object_id"]) is False:
        return "Error: Access denied!"

    if is_object_id_inside_user_collection(args["object_id"]) is False:
        return "Error: Not a valid object id! " \
            "Object id must be inside the database!"

    user_collection.delete_one({"_id": args["object_id"]})

    if is_object_id_inside_user_collection(args["object_id"]) is False:
        if is_user_name_inside_comment_collection(args["user_name"]):
            comment_collection.delete_many({"Username": args["user_name"]})
        if is_user_name_inside_rating_collection(args["user_name"]):
            rating_collection.delete_many({"Username": args["user_name"]})
    else:
        return "Error: Something went wrong!"
    return "User was deleted succesfully!"
