"""
tests.py:
File that contains tester functions
that are needed for the Kirjasto functions.
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


def is_object_int(object_id):
    """Function that checks whether object is integer."""

    numbers = "0123456789"
    for letter in str(object_id):
        if letter not in numbers:
            return False
    return True


def is_book_already_added(name, isbn):
    """Function that checks whether book is already inside the database."""

    retrieved_book_collection = list(book_collection.find({}, {'_id': False}))

    for book in retrieved_book_collection:
        if book["Name"] == name or book["ISBN"] == isbn:
            return True
    return False


def is_book_id_inside_book_collection(book_id):
    """Function that checks whether book_id can be found from the database."""

    # List containing the collection must be updated in the tests.
    # Otherwise
    # when a book is added succesfully the test tells it isn't.
    # Since it's looking at the old collection objects.
    retrieved_book_collection = list(book_collection.find({}, {'_id': False}))

    for book in retrieved_book_collection:
        if book["Book_ID"] == book_id:
            return True
    return False


def is_book_id_inside_comment_collection(book_id):
    """Function that checks whether book_id can be found from the database."""

    retrieved_comment_collection = \
        list(comment_collection.find({}, {'_id': False}))

    for comment in retrieved_comment_collection:
        if comment["Book_ID"] == book_id:
            return True
    return False


def is_book_id_inside_rating_collection(book_id):
    """Function that checks whether book_id can be found from the database."""

    retrieved_rating_collection = \
        list(rating_collection.find({}, {'_id': False}))

    for rating in retrieved_rating_collection:
        if rating["Book_ID"] == book_id:
            return True
    return False


def is_object_id_inside_book_collection(object_id):
    """
    Function that checks
    whether object_id can be found inside the user collection.
    """

    retrieved = list(book_collection.find({}))
    for book in retrieved:
        if book["_id"] == object_id:
            return True
    return False


def is_comment_id_inside_comment_collection(comment_id):
    """
    Function that checks
    whether comment id can be found inside the database.
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
    whether object_id can be found inside the user collection.
    """

    retrieved = list(comment_collection.find({}))
    for comment in retrieved:
        if comment["_id"] == object_id:
            return True
    return False


def is_user_name_inside_comment_collection(user_name):
    """
    Function that checks
    whether username can be found inside the comment collection.
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

    if int(rating) <= 5 and int(rating) >= 0:
        return True
    return False


def is_rating_id_inside_rating_collection(rating_id):
    """
    Function that checks
    whether rating id can be found inside rating collection.
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
    whether object_id can be found inside the user collection.
    """

    retrieved = list(rating_collection.find({}))
    for rating in retrieved:
        if rating["_id"] == object_id:
            return True
    return False


def is_user_name_inside_rating_collection(user_name):
    """
    Function that checks
    whether username can be found inside the rating collection.
    """

    retrieved = list(rating_collection.find({}))
    for rating in retrieved:
        if rating["Username"] == user_name:
            return True
    return False


def is_user_name_inside_user_collection(user_name):
    """
    Function that checks
    whether user_name can be found inside the database.
    """

    retrieved_user_collection = list(user_collection.find({}, {'_id': False}))

    for user in retrieved_user_collection:
        if user["Username"] == user_name:
            return True
    return False


def is_email_inside_user_collection(email):
    """
    Function that checks
    whether email can be found inside the database.
    """

    retrieved_user_collection = list(user_collection.find({}, {'_id': False}))

    for user in retrieved_user_collection:
        if user["Email"] == email:
            return True
    return False


def is_password_inside_user_collection(password):
    """
    Function that checks
    whether password can be found inside the database.
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
    whether object_id can be found inside the user collection.
    """

    retrieved = list(user_collection.find({}))
    for user in retrieved:
        if user["_id"] == object_id:
            return True
    return False
