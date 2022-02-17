"""rating_system.py: Contains Rating class."""
import uuid
from pymongo.mongo_client import MongoClient
from flask_restful import reqparse
import db_secret
from helpers import (
    is_book_id_inside_book_collection,
    is_rating_id_inside_rating_collection,
    is_user_name_inside_user_collection
    )

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
retrieved_book_collection = list(book_collection.find({}, {'_id': False}))
retrieved_user_collection = list(user_collection.find({}, {'_id': False}))
retrieved_rating_collection = list(rating_collection.find({}, {'_id': False}))
parser = reqparse.RequestParser()


def get_retrieved_rating_collection():
    """
    Function that returns a dictionary called retrieved_rating_collection
    that contains retrieved rating collection.
    """

    if len(retrieved_rating_collection) > 0:
        return retrieved_rating_collection
    return "Something went wrong!"


def get_retrieved_ratings_by_username(user_name):
    """Function that returns all of user's ratings."""

    if is_user_name_inside_user_collection(user_name) is False:
        return "Incorrect username!"

    retrieved = list(
        rating_collection.find(
            {'Username': user_name}, {'_id': False}
            )
        )
    if len(retrieved) > 0:
        return retrieved
    return "Something went wrong!"


def get_retrieved_rating_by_username_and_id(user_name, book_id):
    """Function that returns user's ratings on a book."""

    if is_book_id_inside_book_collection(book_id) is False or \
            is_user_name_inside_user_collection(user_name) is False:
        return "Incorrect username or book id!"

    retrieved = list(
        rating_collection.find(
            {
                'Username': user_name,
                'Book_ID': book_id
                }, {'_id': False}
            )
        )
    if len(retrieved) > 0:
        return retrieved
    return "Something went wrong!"


def has_the_user_already_rated_this_book(user_name, book_id):
    """Function that checks whether a user has already rated the book."""

    if len(
        list(
            rating_collection.find(
                {
                    'Username': user_name,
                    'Book_ID': book_id
                    }, {'_id': False}
                )
            )) > 0:
        return True
    return False


def give_rating():
    """
    Function that posts user's rating data the database.
    If the user has already given a rating,
    the old one will be updated.
    """

    parser.add_argument('user_name', required=True, type=str)
    parser.add_argument('book_id', required=True, type=str)
    parser.add_argument('rating', required=True, type=int)

    args = parser.parse_args()

    rating_id = uuid.uuid4().hex

    new_rating = {
        "Rating_ID": rating_id,
        "Username": args["user_name"],
        "Book_ID": args["book_id"],
        "Rating": int(args["rating"])
        }

    if is_user_name_inside_user_collection(new_rating["Username"]) \
            is False or is_book_id_inside_book_collection(
                new_rating["Book_ID"]) is False:
        return "error: Not a valid username or book id. " \
            "Book id and username must exist"

#Update_one?
    if has_the_user_already_rated_this_book(
            args["user_name"],
            args["book_id"]):
        for retrieved in retrieved_rating_collection:
            if retrieved["Username"] == args["user_name"] and \
                    retrieved["Book_ID"] == args["book_id"]:
                rating_id = retrieved["Rating_ID"]
            rating_collection.update(
                {'Rating_ID': rating_id},
                {
                    "$set": {
                        "Rating": int(args["rating"]),
                        }
                    }
                )
    else:
        rating_collection.insert_one(new_rating)

    update_books_rating_data(args["book_id"])
    update_users_mean_score_data(args["user_name"])

    if is_rating_id_inside_rating_collection(rating_id):
        return "Rating was posted succesfully!"
    return "Something went wrong!"


def update_rating():
    """Function that posts updated rating data to the database."""

    parser.add_argument('rating_id', required=True, type=str)
    parser.add_argument('user_name', required=True, type=str)
    parser.add_argument('book_id', required=True, type=str)
    parser.add_argument('new_rating', required=True, type=int)

    args = parser.parse_args()

    old_rating = ""

    if is_rating_id_inside_rating_collection(args["rating_id"]) is False or \
            is_user_name_inside_user_collection(args["user_name"]) \
            is False or is_book_id_inside_book_collection(args["book_id"])\
            is False:
        return "error: Not a valid rating id, username or book id." \
            "Book id, rating id and username must exist!"

    rating_collection.update(
        {'Rating_ID': args["rating_id"]},
        {
            "$set": {
                "Rating": int(args["new_rating"])
                }
            }
        )

    update_books_rating_data(args["book_id"])
    update_users_mean_score_data(args["user_name"])

    if old_rating != args["new_rating"] or old_rating != "":
        return "Rating was updated succesfully!"
    return "Something went wrong!"


def delete_rating():
    """Function that deletes a rating and updates data after."""

    parser.add_argument('rating_id', required=True, type=str)
    parser.add_argument('user_name', required=True, type=str)
    parser.add_argument('book_id', required=True, type=str)

    args = parser.parse_args()

    if is_rating_id_inside_rating_collection(args["rating_id"]) is False or \
            is_book_id_inside_book_collection(args["book_id"]) is False or \
            is_user_name_inside_user_collection(args["user_name"]) is False:
        return "error: Not a valid rating id, username or book id." \
            "Book id, rating id and username must exist!"

    rating_collection.delete_one({"Rating_ID": args["rating_id"]})

    update_books_rating_data(args["book_id"])
    update_users_mean_score_data(args["user_name"])

    if is_rating_id_inside_rating_collection(args["rating_id"]):
        return "Something went wrong!"
    return "Rating was deleted succesfully!"


def get_books_rating_data(book_id):
    """
    Function that returns single books rating
    and the amount that the book has been rated.
    """

    count = 0
    rating_sum = 0
    for rating in retrieved_rating_collection:
        if rating["Book_ID"] == book_id:
            count += 1
            rating_sum += int(rating["Rating"])
    if rating_sum == 0:
        return (0, 0)
    else:
        return (rating_sum / count, count)


def get_users_mean_score(user_name):
    """
    Function that returns single user's mean score
    and the amount that the user has rated books.
    """

    count = 0
    rating_sum = 0

    for rating in retrieved_rating_collection:
        if rating["Username"] == user_name:
            if rating["Username"]:
                count += 1
                rating_sum += int(rating["Rating"])
    if rating_sum == 0:
        return (0, 0)
    else:
        return (rating_sum / count, count)


def update_books_rating_data(book_id):
    """Function that updates ratings in the dictionary called books."""

    old_rating = ""
    new_rating = ""

    for rating in retrieved_book_collection:
        if rating['Book_ID'] == book_id:
            old_rating = rating["Rating"]

    book_collection.update(
        {'Book_ID': book_id},
        {
            "$set": {
                "Rating": float(get_books_rating_data(book_id)[0]),
                "Rating_count": get_books_rating_data(book_id)[1]
                }
            }
        )

    for rating in retrieved_book_collection:
        if rating['Book_ID'] == book_id:
            new_rating = rating["Rating"]

    if old_rating != new_rating or old_rating != "" or new_rating != "":
        return
    return "Something went wrong!"


def update_users_mean_score_data(user_name):
    """Function that updates mean score in the dictionary called users."""

    old_mean_score = ""
    old_mean_count = ""
    new_mean_score = ""
    new_mean_count = ""

    for score in retrieved_user_collection:
        if score["Username"] == user_name:
            old_mean_score = score["Mean_score"]
            old_mean_count = score["Mean_count"]

    user_collection.update(
        {'Username': user_name},
        {
            "$set": {
                "Mean_score": float(get_users_mean_score(user_name)[0]),
                "Mean_count": get_users_mean_score(user_name)[1]
                }
            }
        )

    for score in retrieved_user_collection:
        if score['Username'] == user_name:
            new_mean_score = score['Mean_score']
            new_mean_count = score['Mean_count']

    if old_mean_score != new_mean_score or old_mean_score != "" or \
            old_mean_count != new_mean_count or \
            new_mean_score != "" or new_mean_count != "":
        return
    return "Something went wrong!"
