from flask_restful import Resource, reqparse
from pymongo.mongo_client import MongoClient

# Initiate connection to the comments db
client = MongoClient("mongodb+srv://kirjastoAdmin:s3yS2zcXETkqCM@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['kirjasto-backend']
collection = db['comments']


def get_comments():
    retrieved = list(collection.find({}, {'_id' : False}))
    return retrieved, 200
    
def get_comments_by_book_id(book_id):

    retrievedID = list(collection.find({'Book ID' : book_id,}, {
     '_id': False
    }))
    # Check if input is an int, otherwise throw an error
    for booknumbers in retrievedID:
        if int(book_id):
            return retrievedID
    #else:
    #    return 'error: Not a valid BookID! Book ID must be an int and the book must exist!', 400
        
def post_comments():
    # Require these args for the POST request.
    parser = reqparse.RequestParser()
    parser.add_argument('comment_id', required = True)
    parser.add_argument('comment', required = True)
    parser.add_argument('book_id', required = True)
    parser.add_argument('user_id', required = True)
    
    args = parser.parse_args()

    new_book = collection.insert_one({
        'User ID' : args['user_id'],
        'Comment' : args['comment'],
        'Book ID' : args['book_id'],
        'Comment ID' : args['comment_id']     
    })    
    retrieved = list(collection.find({}, {'_id' : False}))
    return retrieved, 200


def delete_comments_by_id(comment_id):
# Require these args for the DELETE request.

    parser = reqparse.RequestParser()
    parser.add_argument('comment_id', required = False)
    parser.add_argument('comment', required = False)
    parser.add_argument('book_id', required = False)
    parser.add_argument('user_id', required = False)
    
    args = parser.parse_args()
    if int(comment_id):
        removeBook = collection.find_one_and_delete({
            'User ID' : args['user_id'],
            'Comment' : args['comment'],
            'Book ID' : args['book_id'],
            'Comment ID' : args['comment_id']
                      
        }),    
        return {"Deleted comment!"}, 200
    
