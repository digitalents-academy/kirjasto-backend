"""
comments.py:
File that contains necessary functions
for making comment system work as intended.
"""

import uuid
from flask import session
from flask_restful import reqparse
from pymongo.mongo_client import MongoClient
import db_secret
from helpers import (
    get_retrieved_comment_collection,
    checking_if_user_is_authenticated_with_user_name,
    is_book_id_inside_book_collection,
    is_comment_id_inside_comment_collection,
    is_user_name_inside_user_collection,
    is_user_logged_in
    )

client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":"
    + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?" +
    "retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
user_collection = db['users']
comment_collection = db['comments']
parser = reqparse.RequestParser()


def get_comments():
    """Function that returns all comments."""

    retrieved = list(comment_collection.find({}, {'_id': False}))
    if len(retrieved) > 0:
        return retrieved
    return "Error: There doesn't seem to be any comments inside the database!"


def get_comments_by_book_id(book_id):
    """Function that returns comment's data by book id."""

    if is_book_id_inside_book_collection is False:
        return "Error: Not a valid book id!"

    retrieved = list(
        comment_collection.find({'Book_ID': book_id}, {'_id': False})
        )
    if len(retrieved) > 0:
        return retrieved
    return "Error: There doesn't seem to be any comments inside the database!"


def post_comment():
    """Function that posts new comment to the database."""

    if is_user_logged_in() is False:
        return "Error: You have to be logged in!"

    comment_id = uuid.uuid4().hex

    parser.add_argument('book_id', required=True, type=str)
    parser.add_argument('user_name', required=True, type=str)
    parser.add_argument('comment', required=True, type=str)

    args = parser.parse_args()

    if checking_if_user_is_authenticated_with_user_name(
            args["user_name"]) is False:
        return "Error: Access denied!"

    values = {
        "Book_ID": args["book_id"],
        "Username": args["user_name"],
        "Comment_ID": comment_id,
        "Comment": args["comment"]
        }

    if is_book_id_inside_book_collection(values["Book_ID"]) and \
            is_user_name_inside_user_collection(values["Username"]):
        comment_collection.insert_one(values)
    else:
        return "Error: Not a valid book id, username! " \
            "book id and username must be inside the database!"

    if is_comment_id_inside_comment_collection(comment_id) is False:
        return "Error: Something went wrong!"
    return "Comment was posted succesfully!"


def update_comment():
    """Function that updates comment data in the database."""

    if is_user_logged_in() is False:
        return "Error: You have to be logged in!"

    old_book_id = ""
    old_user_name = ""
    old_comment = ""

    parser.add_argument('book_id', required=True, type=str)
    parser.add_argument('user_name', required=True, type=str)
    parser.add_argument('comment_id', required=True, type=str)
    parser.add_argument('comment', required=True, type=str)

    args = parser.parse_args()

    if checking_if_user_is_authenticated_with_user_name(
            args["user_name"]) is False:
        return "Error: Access denied!"

    if is_comment_id_inside_comment_collection(args["comment_id"]) is False \
            or is_book_id_inside_book_collection(args["book_id"]) is False \
            or is_user_name_inside_user_collection(args["user_name"]) is False:
        return "Error: Not a valid book id, username or comment id! " \
            "book id, username and comment id must be inside the database!"

    for comment in get_retrieved_comment_collection():
        if comment["Comment_ID"] == args["comment_id"]:
            old_book_id = comment["Book_ID"]
            old_user_name = comment["Username"]
            old_comment = comment["Comment"]

    comment_collection.update(
        {'Comment_ID': args["comment_id"]},
        {
            "$set": {
                "Book_ID": args["book_id"],
                "Username": args["user_name"],
                "Comment": args["comment"]
                }
            }
        )

    if old_book_id != "" or old_book_id != args["book_id"] or \
            old_user_name != "" or old_user_name != args["user_name"] or \
            old_comment != "" or old_comment != args["comment"]:
        return "Comment was updated succesfully!"
    return "Error: Something went wrong!"


def update_comment_username(new_username, old_username):
    """Function that updates comment data in the database."""

    if is_user_logged_in() is False:
        return "Error: You have to be logged in!"

    if checking_if_user_is_authenticated_with_user_name(
            old_username) is False:
        return "Error: Access denied!"
    
    print(old_username)
    print(new_username)


    comment_collection.update(
        {'Username': old_username},
        {
            "$set": {
                "Username": new_username    
                }
            }
        )
    

def delete_comments_by_comment_id():
    """Function that deletes comment by comment id."""

    if is_user_logged_in() is False:
        return "Error: You have to be logged in!"

    parser.add_argument('comment_id', required=True, type=str)

    args = parser.parse_args()

    if is_comment_id_inside_comment_collection(args["comment_id"]) is False:
        return "Error: Not a valid comment id! " \
            "Comment id must be inside the database!"

    # Checking if user is authenticated
    # by first getting a users comment from comment_collection
    # And then checking whether that user's username matches
    # with the one that is logged in.
    comment = comment_collection.find_one({
                "Comment_ID": args['comment_id']
                })
    if session['user']['Username'] != comment["Username"]:
        return "Error: Access denied!"

    comment_collection.delete_one({"Comment_ID": args["comment_id"]})

    if is_comment_id_inside_comment_collection(args["comment_id"]):
        return "Error: Something went wrong!"
    return "Comment was deleted succesfully!"
