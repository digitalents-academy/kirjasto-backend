"""
helpers.py:
File that contains tester functions
that are needed for the project's functions.
"""

from datetime import date
from pymongo.mongo_client import MongoClient
from passlib.hash import pbkdf2_sha256
from flask import session
import db_secret

client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":"
    + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?" +
    "retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
book_collection = db['books']
comment_collection = db['comments']
rating_collection = db['ratings']
user_collection = db['users']


def get_retrieved_book_collection():
    """Function that returns retrieved book collection."""

    return list(book_collection.find({}, {'_id': False}))


def get_retrieved_comment_collection():
    """Function that returns retrieved comment collection."""

    return list(comment_collection.find({}, {'_id': False}))


def get_retrieved_rating_collection():
    """Function that returns retrieved rating collection."""

    return list(rating_collection.find({}, {'_id': False}))


def get_retrieved_user_collection():
    """Function that returns retrieved user collection."""

    return list(user_collection.find({}))


def is_item_number(item):
    """Function that checks whether object is a number."""

    numbers = "0123456789"
    for letter in str(item):
        if letter not in numbers:
            return False
    return True


def is_item_decimal(item):
    """Function that checks whether object is a number."""

    count = 0
    numbers = "0123456789"
    for letter in str(item):
        if letter not in numbers and count != 1:
            return False
        count += 1
    return True


def is_book_already_added(name, isbn):
    """Function that checks whether book is already inside the database."""

    for book in get_retrieved_book_collection():
        if book["Name"] == name or book["ISBN"] == isbn:
            return True
    return False


def is_book_already_loaned(book_id):
    """Function that checks whether book is already inside the database."""

    for book in get_retrieved_book_collection():
        if book["Book_ID"] == book_id:
            if book["Loan_Status"] == "false" or book["Loan_Status"] is False:
                return False
    return True


def is_year_acceptable(year):
    """Function that checks whether book's year is acceptable."""

    now = date.today().year
    if float(year) <= float(now) and float(year) > 1990:
        return True
    return False


def is_book_id_inside_book_collection(book_id):
    """
    Function that checks whether book id can be found
    from the books collection.
    """

    for book in get_retrieved_book_collection():
        if book["Book_ID"] == book_id:
            return True
    return False


def is_book_id_inside_comment_collection(book_id):
    """
    Function that checks whether book id can be found
    from the comments collection.
    """

    for comment in get_retrieved_comment_collection():
        if comment["Book_ID"] == book_id:
            return True
    return False


def is_book_id_inside_rating_collection(book_id):
    """
    Function that checks whether book id can be found from
    the ratings collection.
    """

    for rating in get_retrieved_rating_collection():
        if rating["Book_ID"] == book_id:
            return True
    return False


def is_object_id_inside_book_collection(object_id):
    """
    Function that checks
    whether object id can be found inside the users collection.
    """

    retrieved = list(book_collection.find({}))
    for book in retrieved:
        if book["_id"] == object_id:
            return True
    return False


def is_comment_id_inside_comment_collection(comment_id):
    """
    Function that checks
    whether comment id can be found inside the comments collection.
    """

    for comment in get_retrieved_comment_collection():
        if comment["Comment_ID"] == comment_id:
            return True
    return False


def is_object_id_inside_comment_collection(object_id):
    """
    Function that checks
    whether object id can be found inside the users collection.
    """

    retrieved = list(comment_collection.find({}))
    for comment in retrieved:
        if comment["_id"] == object_id:
            return True
    return False


def is_user_name_inside_comment_collection(user_name):
    """
    Function that checks
    whether username can be found inside the comments collection.
    """

    retrieved = list(comment_collection.find({}))
    for comment in retrieved:
        if comment["Username"] == user_name:
            return True
    return False


def is_rating_acceptable(rating):
    """
    Function that checks
    whether rating is acceptable.
    """

    if float(rating) <= 5 and float(rating) >= 0:
        return True
    return False


def is_rating_id_inside_rating_collection(rating_id):
    """
    Function that checks
    whether rating id can be found inside ratings collection.
    """

    for rating in get_retrieved_rating_collection():
        if rating["Rating_ID"] == rating_id:
            return True
    return False


def is_object_id_inside_rating_collection(object_id):
    """
    Function that checks
    whether object id can be found inside the ratings collection.
    """

    retrieved = list(rating_collection.find({}))
    for rating in retrieved:
        if rating["_id"] == object_id:
            return True
    return False


def is_user_name_inside_rating_collection(user_name):
    """
    Function that checks
    whether username can be found inside the ratings collection.
    """

    retrieved = list(rating_collection.find({}))
    for rating in retrieved:
        if rating["Username"] == user_name:
            return True
    return False


def is_user_name_inside_user_collection(user_name):
    """
    Function that checks
    whether username can be found inside the users collection.
    """

    for user in get_retrieved_user_collection():
        if user["Username"] == user_name:
            return True
    return False


def is_email_inside_user_collection(email):
    """
    Function that checks
    whether email can be found inside the users collection.
    """

    for user in get_retrieved_user_collection():
        if user["Email"] == email:
            return True
    return False


def is_password_inside_user_collection(password):
    """
    Function that checks
    whether password can be found inside the users collection.
    """

    for user in get_retrieved_user_collection():
        if pbkdf2_sha256.verify(
                password,
                user["Password"]):
            return True
    return False


def is_object_id_inside_user_collection(object_id):
    """
    Function that checks
    whether object id can be found inside the users collection.
    """

    retrieved = list(user_collection.find({}))
    for user in retrieved:
        if user["_id"] == object_id:
            return True
    return False


def checking_if_user_is_authenticated_with_object_id(object_id):
    """
    Function that checks
    whether user is authenticated with the help of object id.
    """

    user = user_collection.find_one({
        "_id": object_id
        })
    if session['user']['_id'] == user['_id']:
        return True
    return False


def checking_if_user_is_authenticated_with_user_name(user_name):
    """
    Function that checks
    whether user is authenticated with the help of username.
    """

    user = user_collection.find_one({
        "Username": user_name
        })

    if user is None:
        return False

    if session['user']['_id'] == user['_id']:
        return True
    return False


def is_current_user_admin():
    """
    Function that checks
    whether current user is admin.
    """

    if session['user']['Admin']:
        return True
    return False


def is_user_logged_in():
    """
    Function that checks
    whether someone is logged in or not.
    """

    if 'logged_in' in session:
        return True
    return False
