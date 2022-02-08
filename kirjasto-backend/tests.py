"""
tests.py:
File that contains tester functions
that are needed for the Kirjasto functions.
"""

from pymongo.mongo_client import MongoClient
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
retrieved_book_collection = list(book_collection.find({}, {'_id': False}))
retrieved_user_collection = list(user_collection.find({}, {'_id': False}))
retrieved_rating_collection = \
    list(rating_collection.find({}, {'_id': False}))
retrieved_comment_collection = \
    list(comment_collection.find({}, {'_id': False}))


def is_book_already_added(name, isbn):
    """Function that checks whether book is already inside the database."""

    for book in retrieved_book_collection:
        if book["Name"] == name or book["ISBN"] == isbn:
            return True
    return False


def is_book_id_inside_book_collection(book_id):
    """Function that checks whether book_id can be found from the database."""

    for book in retrieved_book_collection:
        if book["Book_ID"] == book_id:
            return True
    return False


def is_comment_data_inside_comment_collection(user_name, book_id):
    """
    Function that checks
    whether comment data can be found inside the database.
    """

    for comment in retrieved_comment_collection:
        if comment["Username"] == user_name and \
                comment["Book_ID"] == book_id:
            return True
    return False


def is_rating_acceptable(rating):
    """
    Function that checks
    whether rating is acceptable.
    """

    if rating <= 5 and rating >= 0:
        return True
    return False


def is_user_name_inside_user_collection(user_name):
    """
    Function that checks
    whether user_name can be found inside the database.
    """

    for user in retrieved_user_collection:
        if user["Username"] == user_name:
            return True
    return False


# Needed if the object_id is changed
def is_object_int(object_id):
    """Function that checks whether object is integer."""

    numbers = "0123456789"
    for letter in object_id:
        if letter not in numbers:
            return False
    return True
