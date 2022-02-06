# from pymongo import ALL
from pymongo import MongoClient
from flask_restful import reqparse
import db_secret
import user

# Initiate connection to mongoDB
client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":" + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
collection = db['books']
retrieved_book_collection = list(collection.find({}, {'_id': False}))


def get_books():
    """Function that returns all books."""

    retrieved_status = list(collection.find({}, {
        '_id': False
    }))

    return retrieved_status


# cannot see books that have string book_id
def get_book_by_id(book_id):
    """Function that returns book data depending on the book_id."""

    correct_book_id = True
    numbers = "0123456789"

    for letter in book_id:
        if letter not in numbers:
            correct_book_id = False
    if correct_book_id:
        retrieved = list(
            collection.find(
                {'Book_ID': int(book_id)},
                {'_id': False}
                )
            )
        return retrieved
    return (
        'error: Not a valid Book ID! ' +
        'Book ID must be an int and the book must exist!'
        )


#Not complete
#Unique Book_id needed
def add_new_book(
        book_id, name, writer, year, isbn, about, tags, description):
    """Function that posts new book to the database."""

    for book in retrieved_book_collection:
        if book["Book_ID"] == int(book_id):
            collection.update(
                {'Book_ID': int(book_id)},
                {
                    "$set": {
                        "Name": name,
                        "Writer": writer,
                        "Year": year,
                        "ISBN": isbn,
                        "Rating": book["Rating"],
                        "About": about,
                        "Tags": tags,
                        "Description": description,
                        "Loaner": book["Loaner"],
                        "Loan_Status": book["Loan_Status"]
                        }
                    }
                )
            return
        else:
            collection.insert_one({
                #"Book_ID": len(retrieved_book_collection) + 1,
                "Book_ID": book_id,
                "Name": name,
                "Writer": writer,
                "Year": int(year),
                "ISBN": isbn,
                "Rating": 0,
                "About": about,
                "Tags": tags,
                "Description": description,
                "Loaner": None,
                "Loan_Status": False

            })
        return


#Needed?
def update_book(
        book_id, name, writer, year, isbn, rating, about, tags, description,
        loaner, loan_status):
    """Function that posts updated book_data to the database."""

    collection.update(
        {'Book_ID': book_id},
        {
            "$set": {
                "Name": name,
                "Writer": writer,
                "Year": year,
                "ISBN": isbn,
                "Rating": rating,
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

    correct_book_id = True
    numbers = "0123456789"

    for letter in book_id:
        if letter not in numbers:
            correct_book_id = False
    if correct_book_id:
        collection.delete_one({"Book_ID": int(book_id)})


#Need to be checked out
#Doesn't work
def loan_book_by_username_and_id(user_name, book_id):
    """Function that changes book's loan state."""

    correct_book_id = True
    numbers = "0123456789"

    for letter in book_id:
        if letter not in numbers:
            correct_book_id = False
    if correct_book_id:
        for book in retrieved_book_collection:
            if book["Book_ID"] == int(book_id):
                if book['Loan_Status'] is False:
                    new_book = {
                        'Book_ID': book['Book_ID'],
                        'Name': book['Name'],
                        'Writer': book['Writer'],
                        'Year': book['Year'],
                        'ISBN': book['ISBN'],
                        'Rating': book['Rating'],
                        'About': book['About'],
                        'Tags': book['Tags'],
                        'Description': book['Description'],
                        'Loaner': None,
                        'Loan_Status': True
                    }
                    collection.replace_one(book, new_book)

    # retrieved = list(collection.find({'Book_ID': book_id}, {'_id': False}))
    # for data in retrieved:
    #     if data['Book_ID'] == book_id:
    #         return collection.find_one_and_update(
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
