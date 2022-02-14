"""
books.py:
Contains necessary functions for making book function work as intended.
"""

import uuid
from pymongo import MongoClient
from flask_restful import reqparse
import db_secret

client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":" + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
book_collection = db['books']
retrieved_book_collection = list(book_collection.find({}, {'_id': False}))


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


def add_new_book(
        name, writer, year, isbn, about, tags, description):
    """Function that posts new book to the database."""

    book_collection.insert_one({
        "Book_ID": uuid.uuid4().hex,
        "Name": name,
        "Writer": writer,
        "Year": int(year),
        "ISBN": isbn,
        "Rating": 0,
        "Rating_count": 0,
        "About": about,
        "Tags": tags,
        "Description": description,
        "Loaner": None,
        "Loan_Status": False
    })


def update_book(
        book_id, name, writer, year, isbn, rating, rating_count, about, tags,
        description, loaner, loan_status):
    """Function that posts updated book data to the database."""

    if loaner == "null":
        loaner = None
    if loan_status == "false":
        loan_status = False
    elif loan_status == "true":
        loan_status = True

    book_collection.update(
        {'Book_ID': book_id},
        {
            "$set": {
                "Name": name,
                "Writer": writer,
                "Year": int(year),
                "ISBN": isbn,
                "Rating": int(rating),
                "Rating_count": int(rating_count),
                "About": about,
                "Tags": tags,
                "Description": description,
                "Loaner": loaner,
                "Loan_Status": loan_status
                }
            }
        )


def delete_book_by_id(book_id):
    """Function that deletes a book from the database."""

    book_collection.delete_one({"Book_ID": book_id})

    for book in retrieved_book_collection:
        if book["Book_ID"] == book_id:
            return "Something went wrong!"

    #When a book is deleted
    #also the comments and ratings
    #for that book should be deleted.


def loan_book_by_username_and_id(user_name, book_id):
    """Function that changes book's loan state."""

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

    #retrieved = list(book_collection.find(
    #    {'Book_ID': book_id},
    #    {'_id': False}
    #    ))
    # for data in retrieved:
    #     if data['Book_ID'] == book_id:
    #         return book_collection.find_one_and_update(
    #             data, {"$set": parse()})
    #     elif data['Book_ID'] != book_id:
    #         return {'message': f"{book_id} doesn't exist."
    #                 }, 401
    #     else:
    #         return {
    #             'message': " Unknown error."
    #         }, 401


def parse():
    # Required values for the api requests. False would be optional
    parser = reqparse.RequestParser()
    parser.add_argument('book_id', required=True)
    parser.add_argument('name', required=True)
    parser.add_argument('writer', required=True)
    parser.add_argument('year', required=True)
    parser.add_argument('isbn', required=True)
    parser.add_argument('rating', required=True)
    parser.add_argument('about', required=True)
    parser.add_argument('tags', required=True)
    parser.add_argument('description', required=True)
    parser.add_argument('loaner', required=True)
    parser.add_argument('loan_status', required=True)

    args = parser.parse_args()

    values = {
        'Book_ID': args['book_id'],
        'Name': args['name'],
        'Writer': args['writer'],
        'Year': args['year'],
        'ISBN': args['isbn'],
        'Rating': args['rating'],
        'About': args['about'],
        'Tags': args['tags'],
        'Description': args['description'],
        'Loaner': args['loaner'],
        'Loan_Status': args['loan_status']
        }
    return values
