"""
books.py:
Contains necessary functions for making book function work as intended.
"""

import uuid
from pymongo import MongoClient
from flask_restful import reqparse
import db_secret
from helpers import is_book_already_added

client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":" + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
book_collection = db['books']
retrieved_book_collection = list(book_collection.find({}, {'_id': False}))
parser = reqparse.RequestParser()


def get_books():
    """Function that returns all books."""

    if len(retrieved_book_collection) > 0:
        return retrieved_book_collection
    return "Something went wrong!"


# cannot see books that have string book_id
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

    for book in retrieved_book_collection:
        if book["Book_ID"] == book_id:
            return
        return "Something went wrong!"


def update_book():
    """Function that posts updated book data to the database."""

    #Necessary tests
    #if is_book_id_inside_book_collection(book_id) and \
    #            is_book_already_added(name, isbn) and \
    #            is_object_int(year) and is_object_int(rating) and \
    #            is_object_int(rating_count):
    #return "error: Not a valid book_id, name, isbn or rating! " \
    #        "book_id, name and isbn must be inside the database!"

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

    values = {
        'Book_ID': args['book_id'],
        'Name': args['name'],
        'Writer': args['writer'],
        'Year': int(args['year']),
        'ISBN': args['isbn'],
        'Rating': args['rating'],
        "Rating_count": args['rating_count'],
        'About': args['about'],
        'Tags': args['tags'],
        'Description': args['description'],
        'Loaner': args['loaner'],
        'Loan_Status': args['loan_status']
        }

    if values["Loaner"] == "null":
        values["Loaner"] = None
    if values["Loan_Status"] == "false":
        values["Loan_Status"] = False
    elif values["Loan_Status"] == "true":
        values["Loan_Status"] = True

    old_isbn = ""
    old_about = ""
    old_description = ""

    for book in retrieved_book_collection:
        if book["Book_ID"] == values["Book_ID"]:
            old_isbn == book["ISBN"]
            old_about == book["About"]
            old_description == book["Description"]
    
    book_collection.update(
        {'Book_ID': values["Book_ID"]},
        {
            "$set": {
                "Name": values["Name"],
                "Writer": values["Writer"],
                "Year": int(values["Year"]),
                "ISBN": values["ISBN"],
                "Rating": int(values["Rating"]),
                "Rating_count": int(values["Rating_count"]),
                "About": values["About"],
                "Tags": values["Tags"],
                "Description": values["Description"],
                "Loaner": values["Loaner"],
                "Loan_Status": values["Loan_Status"]
                }
            }
        )

    if old_description != values["Description"] or old_description != "" or old_isbn != values["ISBN"] or old_isbn != "" or old_about != values["About"] or old_about != "":
        return "Book updated!"
    return "Something went Wrong!"


def delete_book_by_id(book_id):
    """Function that deletes a book from the database."""

    book_collection.delete_one({"Book_ID": book_id})

    for book in retrieved_book_collection:
        if book["Book_ID"] == book_id:
            return "Something went wrong!"

    #When a book is deleted
    #also the comments and ratings
    #for that book should be deleted.


#Not Done Yet!
def loan_book_by_username_and_id(user_name, book_id):
    """Function that changes book's loan state."""

    #parser.add_argument('user_name', required=True, type=str)
    #parser.add_argument('book_id', required=True, type=str)

    #args = parser.parse_args()

    # values = {
    #     'Book_ID': args['book_id'],
    #     'Name': args['name'],
    #     'Writer': args['writer'],
    #     'Year': int(args['year']),
    #     'ISBN': args['isbn'],
    #     'Rating': args['rating'],
    #     "Rating_count": args['rating_count'],
    #     'About': args['about'],
    #     'Tags': args['tags'],
    #     'Description': args['description'],
    #     'Loaner': args['loaner'],
    #     'Loan_Status': args['loan_status']
    #     }

    #book = get_book_by_id(values["book_ID"])
    book = get_book_by_id(book_id)
    if book[0]['Loan_Status'] is False:
        new_book = {
            'Book_ID': book[0]['Book_ID'],
            'Name': book[0]['Name'],
            'Writer': book[0]['Writer'],
            'Year': book[0]['Year'],
            'ISBN': book[0]['ISBN'],
            'Rating': book[0]['Rating'],
            'About': book[0]['About'],
            'Tags': book[0]['Tags'],
            'Description': book[0]['Description'],
            'Loaner': user_name,
            'Loan_Status': True
        }
        book_collection.replace_one(book[0], new_book)

    for book in retrieved_book_collection:
        if book["Book_ID"] == book_id:
            if book["Loan_Status"] == True:
                return
    return "Something went wrong!"
