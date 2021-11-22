from flask_restful import Resource, reqparse
from pymongo.mongo_client import MongoClient

# Initiate connection to the comments db
client = MongoClient("mongodb+srv://kirjastoAdmin:s3yS2zcXETkqCM@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['kirjasto-backend']
collection = db['comments']


def get_comments():
    # had to make id not show, because it threw a not json serializable error.
    retrieved = list(collection.find({}, {'_id' : False}))
    return retrieved, 200

def post_comments():
    # Require these args for the POST request.
    parser = reqparse.RequestParser()
    parser.add_argument('commenter', required = True)
    parser.add_argument('message', required = True)

    args = parser.parse_args()

    new_book = collection.insert_one({
        'Commenter' : args['commenter'],
        'Message' : args['message'],     
    })    
    retrieved = list(collection.find({}, {'_id' : False}))
    return retrieved, 200

def put_comments(self):
    parser = reqparse.RequestParser()
    parser.add_argument('commenter', required = True)
    parser.add_argument('message', required = True)

    args = parser.parse_args()

    if args['name'] in list(collection['Name']):
        client = MongoClient('localhost', 27017)
        db = client['Laiberi']
        collection = db['booksAvail']
        updateBook = collection.find_one_and_replace({
            'Commenter' : args['commenter'],
            'Message' : args['message'],     
    })    

    retrieved = list(collection.find({}, {'_id' : False}))


    return retrieved, 200

def delete_comments_by_id(self):
# Require these args for the DELETE request.

    parser = reqparse.RequestParser()
    parser.add_argument('commenter', required = True)
    parser.add_argument('message', required = True)
    args = parser.parse_args()

    client = MongoClient('localhost', 27017)
    db = client['Laiberi']
    collection = db['booksAvail']
    removeBook = collection.find_one_and_delete({
        'Commenter' : args['commenter'],
        'Message' : args['message'],          
    })    
    retrieved = list(collection.find({}, {'_id' : False}))
    return retrieved, 200
    
    