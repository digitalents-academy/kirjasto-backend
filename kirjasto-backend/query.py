from pymongo import ALL, MongoClient
from flask_restful import reqparse
import db_secret

# Initiate connection to mongoDB
client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":" + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
collection = db['backendAPI']


def db_query():

    # had to make id not show, because it threw a not json serializable error.
    retrievedStatus = list(collection.find({}, {
        '_id': False
    }))

    return retrievedStatus, 200


def db_full_query():
    retrievedFull = list(collection.find({}, {'_id': False}))

    return retrievedFull, 200


def status_query(book_id):

    correct_book_id = True
    numbers = "0123456789"

    for letter in book_id:
        if letter not in numbers:
            correct_book_id = False
    if correct_book_id == True:
        retrievedID = list(
            collection.find({'Book_ID': int(book_id)},
            {'_id': False})
            )
        return retrievedID
    return (
        'error: Not a valid BookID!' +
        'Book ID must be an int and the book must exist!',
        400
        )

def add_new_book(book_id, name, writer, year, isbn, rating, about, tags, description, loaner, loan_status):

    collection.insert_one({
        "Book_ID": book_id,
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

    })


def update_book(book_id, name, writer, year, isbn, rating, about, tags, description, loaner, loan_status):
    collection.update({'Book_ID': book_id},
    {"$set":
        {
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


def delete_book(book_id):
    collection.delete_one({"Book_ID": book_id})
        
def parse():
# Required values for the api requests. False would be optional
    parser = reqparse.RequestParser()
    parser.add_argument('book_id', required=True)
#    parser.add_argument('name', required=True)
#    parser.add_argument('writer', required=True)
#    parser.add_argument('year', required=True)
#    parser.add_argument('isbn', required=True)
#    parser.add_argument('rating', required=True)
#    parser.add_argument('about', required=True)
#    parser.add_argument('tags', required=True)
#    parser.add_argument('description', required=True)
    parser.add_argument('loaner', required=True)
    parser.add_argument('loan_status', required=True)

    args = parser.parse_args()

    values = {
            'Book_ID': args['book_id'],
#            'Name': args['name'],
#            'Writer': args['writer'],
#            'Year': args['year'],
#            'ISBN': args['isbn'],
#            'Rating': args['rating'],
#            'About': args['about'],
#            'Tags': args['tags'],
#            'Description': args['description'],
            'Loaner': args['loaner'],
            'Loan_Status': args['loan_status']

            }
    return values
