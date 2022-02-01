from flask_restful import reqparse
from pymongo.mongo_client import MongoClient
import db_secret

client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":"
    + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?" +
    "retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
collection = db['comments']


def get_comments():
    retrieved = list(collection.find({}, {'_id': False}))
    return retrieved, 200


def get_comments_by_book_id(book_id):

    retrievedID = list(
        collection.find({'Book_ID': book_id}, {'_id': False})
        )

    # Check if input is an int, otherwise throw an error
    if book_id.is_integer():
        return retrievedID, 200
    return (
        'error: Not a valid BookID!' +
        'Book ID must be an int and the book must exist!',
        400
        )


def post_comments(user_id, comment, book_id, comment_id):

    collection.insert_one({
        'User_ID': user_id,
        'Comment': comment,
        'Book_ID': book_id,
        'Comment_ID': comment_id
    })
    #Needed?
    retrieved = list(collection.find({}, {'_id': False}))
    return retrieved, 200


def delete_comments_by_id(comment_id):
    """Function that deletes comment by comment id."""

    if comment_id.is_integer():
        parser = reqparse.RequestParser()
        parser.add_argument('comment_id', required=False)
        parser.add_argument('comment', required=False)
        parser.add_argument('book_id', required=False)
        parser.add_argument('user_id', required=False)

        args = parser.parse_args()
        retrievedID = list(
            collection.find(
                {'Comment_ID': comment_id},
                {'_id': False}
                )
            )

        for data in retrievedID:
            if data["Comment_ID"] == comment_id:
                collection.find_one_and_delete(
                    {"Comment_ID": comment_id},
                    {
                        'User_ID': args['user_id'],
                        'Comment': args['comment'],
                        'Book_ID': args['book_id'],
                        'Comment_ID': args['comment_id']
                        }
                        )
