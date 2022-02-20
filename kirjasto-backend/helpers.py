"""
helpers.py:
File that contains tester functions
that are needed for the project's functions.
"""

from pymongo.mongo_client import MongoClient
from passlib.hash import pbkdf2_sha256
import db_secret

client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":"
    + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?" +
    "retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
book_collection = db['books']
user_collection = db['users']
rating_collection = db['ratings']
comment_collection = db['comments']


def is_object_number(object):
    """Function that checks whether object is a number."""

    numbers = "0123456789"
    for letter in str(object):
        if letter not in numbers:
            return False
    return True


def is_object_decimal(object):
    """Function that checks whether object is a number."""

    count = 0
    numbers = "0123456789"
    for letter in str(object):
        if letter not in numbers and count != 1:
            return False
        count += 1
    return True


def is_book_already_added(name, isbn):
    """Function that checks whether book is already inside the database."""

    retrieved_book_collection = list(book_collection.find({}, {'_id': False}))

    for book in retrieved_book_collection:
        if book["Name"] == name or book["ISBN"] == isbn:
            return True
    return False


#Editing this
def is_book_already_loaned(book_id):
    """Function that checks whether book is already inside the database."""

    retrieved_book_collection = list(book_collection.find({}, {'_id': False}))

    for book in retrieved_book_collection:
        if book["Book_ID"] == book_id:
            if book["Loan_Status"] == "false" or book["Loan_Status"] is False:
                return False
    return True


def is_book_id_inside_book_collection(book_id):
    """
    Function that checks whether book id can be found
    from the books collection.
    """

    retrieved_book_collection = list(book_collection.find({}, {'_id': False}))

    for book in retrieved_book_collection:
        if book["Book_ID"] == book_id:
            return True
    return False


def is_book_id_inside_comment_collection(book_id):
    """
    Function that checks whether book id can be found
    from the comments collection.
    """

    retrieved_comment_collection = \
        list(comment_collection.find({}, {'_id': False}))

    for comment in retrieved_comment_collection:
        if comment["Book_ID"] == book_id:
            return True
    return False


def is_book_id_inside_rating_collection(book_id):
    """
    Function that checks whether book id can be found from
    the ratings collection.
    """

    retrieved_rating_collection = \
        list(rating_collection.find({}, {'_id': False}))

    for rating in retrieved_rating_collection:
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

    retrieved_comment_collection = \
        list(comment_collection.find({}, {'_id': False}))

    for comment in retrieved_comment_collection:
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

    retrieved_rating_collection = \
        list(rating_collection.find({}, {'_id': False}))

    for rating in retrieved_rating_collection:
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

    retrieved_user_collection = list(user_collection.find({}, {'_id': False}))

    for user in retrieved_user_collection:
        if user["Username"] == user_name:
            return True
    return False


def is_email_inside_user_collection(email):
    """
    Function that checks
    whether email can be found inside the users collection.
    """

    retrieved_user_collection = list(user_collection.find({}, {'_id': False}))

    for user in retrieved_user_collection:
        if user["Email"] == email:
            return True
    return False


def is_password_inside_user_collection(password):
    """
    Function that checks
    whether password can be found inside the users collection.
    """

    retrieved_user_collection = list(user_collection.find({}, {'_id': False}))

    for user in retrieved_user_collection:
        if pbkdf2_sha256.verify(
                password,
                user['Password']):
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
