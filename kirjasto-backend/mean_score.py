# Add the scores of all the people who took the test.
# Divide that total by the number of people.
# mean= (rating + rating1 + rating 2 + ...) / rating_count
# post rating -> count +=1 score += score -> get count, score -
# mean = score / count -> post mean
# Initiate connection to mongoDB
from pymongo import MongoClient
import db_secret
from flask_restful import reqparse

client = MongoClient("mongodb+srv://" + db_secret.secret_id + ":"
                     + db_secret.secret_key +
                     "@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['kirjasto-backend']
collection = db['backendAPI']
retrieved = list(collection.find({}, {'_id': False}))


def get_rating_count():
    pass


def add_rating_count_score():

    parser = reqparse.RequestParser()
    parser.add_argument('book_id', required=True)

    args = parser.parse_args()
    retrieved = list(collection.find({}, {'_id': False}))
    for booknumbers in retrieved:
        if args['book_id'] in booknumbers['Book ID']:
            new_book = collection.find_one_and_update(booknumbers,
                                                      {"$set": parse()})
        elif args['book_id'] != booknumbers['Book ID']:
            retrieved = list(collection.find({}, {'_id': False}))

    return retrieved


def calc_mean_score():
    pass


def post_mean():
    pass


def parse():
    parser = reqparse.RequestParser()
    parser.add_argument('book_id', required=True)
    parser.add_argument('rating_count', required=True)
    parser.add_argument('user_id', required=True)
    parser.add_argument('rating_score', required=True)
    args = parser.parse_args()
    values = {
        'Book ID': args['book_id'],
        'Rating Count': args['rating_count'],
        'Rating Score': args['rating_score']
    }

    return values
