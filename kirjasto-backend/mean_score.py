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
    retrieved = list(collection.find({}, {'id_': False}))


def get_rating_count_score(book_id):
    retrieved = list(collection.find({'Book ID': book_id}, {'Rating': True, 'Rating Count': True, 'Rating Score': True, '_id': False}))
    return retrieved


def add_rating_count_score():
    has_rated = False
    parser = reqparse.RequestParser()
    parser.add_argument('book_id', required=True)
    parser.add_argument('rating', required=True)

    args = parser.parse_args()
    retrieved = list(collection.find({}, {'_id': False}))
    for booknumbers in retrieved:
        if args['book_id'] in booknumbers['Book ID']:
            has_rated = True
            new_book = collection.find_one_and_update(booknumbers,
                                                      {"$set": parse()})
    if has_rated is True:
        rated_counter = 0
        score_counter = 0
        rated_counter += 1
        score_counter += int(args['rating'])
        get_rating_count_score(args['book_id'])
        has_rated = False
        print(rated_counter, score_counter)
    retrieved = list(collection.find({}, {'_id': False}))
    return retrieved


def post_counters():
    parser = reqparse.RequestParser()
    parser.add_argument('book_id', required=True)
    parser.add_argument('rating', required=True)
    args = parser.parse_args()
    values = {
        'Book ID': args['book_id'],
        'Rating': int(args['rating']),
    }


def calc_mean_score():
    pass


def post_mean():
    pass


def parse():
    parser = reqparse.RequestParser()
    parser.add_argument('book_id', required=True)
    parser.add_argument('rating', required=True)
    args = parser.parse_args()
    values = {
        'Book ID': args['book_id'],
        'Rating': int(args['rating']),
    }

    return values
