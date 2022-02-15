"""
books.py:
Contains necessary functions for making book function work as intended.
"""

import uuid
from pymongo import MongoClient
from flask_restful import reqparse
import db_secret
from helpers import (
    is_book_already_added,
    is_book_id_inside_book_collection,
    is_object_int,
    is_user_name_inside_user_collection,
    is_book_id_inside_comment_collection,
    is_book_id_inside_rating_collection
    )

client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":" + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
book_collection = db['books']
comment_collection = db['comments']
rating_collection = db['ratings']
retrieved_book_collection = list(book_collection.find({}, {'_id': False}))
parser = reqparse.RequestParser()


def get_books():
    """Function that returns all books."""

    if len(retrieved_book_collection) > 0:
        return retrieved_book_collection
    return "Something went wrong!"


def get_book_by_id(book_id):
    """Function that returns book data depending on the book_id."""

    retrieved = list(
        book_collection.find(
            {'Book_ID': book_id},
            {'_id': False}
            )
        )
    return retrieved


def add_new_book():
    """Function that posts new book to the database."""

    book_id = uuid.uuid4().hex

    parser.add_argument('name', required=True, type=str)
    parser.add_argument('writer', required=True, type=str)
    parser.add_argument('year', required=True, type=int)
    parser.add_argument('isbn', required=True, type=str)
    parser.add_argument('about', required=True, type=str)
    parser.add_argument('tags', required=True, type=str)
    parser.add_argument('description', required=True, type=str)

    args = parser.parse_args()

    values = {
        'Book_ID': book_id,
        'Name': args['name'],
        'Writer': args['writer'],
        'Year': int(args['year']),
        'ISBN': args['isbn'],
        'Rating': 0,
        "Rating_count": 0,
        'About': args['about'],
        'Tags': args['tags'],
        'Description': args['description'],
        'Loaner': None,
        'Loan_Status': False
        }

    if is_book_already_added(values["Name"], values["ISBN"]):
        return "Book has already been added!"

    book_collection.insert_one(values)

    if is_book_id_inside_book_collection(book_id) is False:
        return "Something went wrong!"


#The error handling for checking whether update was succesful
#needs to be edited.
def update_book():
    """Function that posts updated book data to the database."""

    parser.add_argument('book_id', required=True, type=str)
    parser.add_argument('name', required=True, type=str)
    parser.add_argument('writer', required=True, type=str)
    parser.add_argument('year', required=True, type=int)
    parser.add_argument('isbn', required=True, type=str)
    parser.add_argument('rating', required=True, type=int)
    parser.add_argument('rating_count', required=True, type=int)
    parser.add_argument('about', required=True, type=str)
    parser.add_argument('tags', required=True, type=str)
    parser.add_argument('description', required=True, type=str)
    parser.add_argument('loaner', required=True, type=str)
    parser.add_argument('loan_status', required=True, type=bool)

    args = parser.parse_args()

    if args["loaner"] == "null":
        args["loaner"] = None
    elif args["loan_status"] == "false":
        args["loan_status"] = False
    elif args["loan_status"] == "true":
        args["loan_status"] = True

    elif is_book_id_inside_book_collection(args["book_id"]) is False or \
            is_book_already_added(args["name"], args["isbn"]) \
            is False or is_object_int(args["year"]) is False or \
            is_object_int(args["rating"]) is False or \
            is_object_int(args["rating_count"]) is False:
        return "error: Not a valid book_id, name, isbn or rating! " \
                "book_id, name and isbn must be inside the database!"

    #Better way for checking if the update worked is needed!

    old_name = ""
    old_writer = ""
    old_year = ""
    old_isbn = ""
    old_rating = ""
    old_rating_count = ""
    old_about = ""
    old_tags = ""
    old_description = ""
    old_loaner = ""
    old_loan_status = ""

    for book in retrieved_book_collection:
        if book["Book_ID"] == args["book_id"]:
            old_name = book["Name"]
            old_writer = book["Writer"]
            old_year = book["Year"]
            old_isbn = book["ISBN"]
            old_rating = book["Rating"]
            old_rating_count = book["Rating_count"]
            old_about = book["About"]
            old_tags = book["Tags"]
            old_description = book["Description"]
            old_loaner = book["Loaner"]
            old_loan_status = book["Loan_Status"]

    book_collection.update(
        {'Book_ID': args["book_id"]},
        {
            "$set": {
                "Name": args["name"],
                "Writer": args["writer"],
                "Year": int(args["year"]),
                "ISBN": args["isbn"],
                "Rating": int(args["rating"]),
                "Rating_count": int(args["rating_count"]),
                "About": args["about"],
                "Tags": args["tags"],
                "Description": args["description"],
                "Loaner": args["loaner"],
                "Loan_Status": args["loan_status"]
                }
            }
        )

    if old_name != "" or old_name != args["name"] or old_writer != "" or \
            old_writer != args["writer"] or old_year != "" or \
            old_year != args["year"] or old_isbn != "" or \
            old_isbn != args["isbn"] or old_rating != "" or \
            old_rating != args["rating"] or old_rating_count != "" or \
            old_rating_count != args["rating_count"] or old_about != "" or \
            old_about != args["about"] or old_tags != "" or \
            old_tags != args["tags"] or old_description != "" or \
            old_description != args["description"] or old_loaner != "" or \
            old_loaner != args["loaner"] or old_loan_status != "" or \
            old_loan_status != args["loan_status"]:
        return
    return "Something went wrong!"


def delete_book_by_id():
    """Function that deletes a book from the database."""

    parser.add_argument('book_id', required=True, type=str)

    args = parser.parse_args()

    if is_book_id_inside_book_collection(args["book_id"]) is False:
        return "error: Not a valid book_id! " \
                "Book_id must be inside the database!"

    book_collection.delete_one({"Book_ID": args["book_id"]})

    if is_book_id_inside_book_collection(args["book_id"]) is False:
        if is_book_id_inside_comment_collection(args["book_id"]):
            comment_collection.delete_one({"Book_ID": args["book_id"]})
        if is_book_id_inside_rating_collection(args["book_id"]):
            rating_collection.delete_one({"Book_ID": args["book_id"]})
    else:
        return "Something went wrong!"

    if is_book_id_inside_comment_collection(args["book_id"]) or \
            is_book_id_inside_rating_collection(args["book_id"]):
        return "Something went wrong!"


def loan_book_by_username_and_id():
    """Function that changes book's loan state."""

    parser.add_argument('user_name', required=True, type=str)
    parser.add_argument('book_id', required=True, type=str)

    args = parser.parse_args()

    if is_user_name_inside_user_collection(args["user_name"]) is False or \
            is_book_id_inside_book_collection(args["book_id"]) is False:
        return "error: Not a valid username or book_id." \
            "Book_id and username must exist"

    old_loaner = ""
    old_loan_status = ""

    for book in retrieved_book_collection:
        if book["Book_ID"] == args["book_id"]:
            old_loaner = book["Loaner"]
            old_loan_status = book["Loan_status"]

    book_collection.update(
        {'Book_ID': args["book_id"]},
        {
            "$set": {
                "Loaner": args["user_name"],
                "Loan_Status": True
                }
            }
        )

    if old_loaner != args["user_name"] or \
            old_loaner != "" or old_loan_status is not False \
            or old_loan_status != "":
        return
    return "Something went wrong!"
