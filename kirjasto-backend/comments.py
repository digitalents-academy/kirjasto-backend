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
user_collection = db['users']
retrieved_comment_collection = list(collection.find({}, {'_id': False}))
retrieved_user_collection = list(user_collection.find({}, {'_id': False}))


def get_comments():
    """Function that returns all comments."""

    retrieved = list(collection.find({}, {'_id': False}))
    return retrieved


def get_comments_by_book_id(book_id):
    """Function that returns comment by book_id."""

    correct_book_id = True
    numbers = "0123456789"

    for letter in book_id:
        if letter not in numbers:
            correct_book_id = False
    if correct_book_id:
        retrieved = list(
            collection.find({'Book_ID': int(book_id)}, {'_id': False})
            )
        return retrieved
    return

#Works but the comment_id could be same with the help of delete
#so some new way to make ids is needed
#Error handling is done correctly here, but nowhere else!
def post_comment(user_name, comment, book_id, comment_id):
    """Function that posts new comment to the database."""

    correct_user_name = False
    correct_book_id = True
    numbers = "0123456789"

    for letter in book_id:
        if letter not in numbers:
            correct_book_id = False
    for user in retrieved_user_collection:
        if user["Username"] == user_name:
            correct_user_name = True
    if correct_book_id and correct_user_name:
        collection.insert_one({
            'Username': user_name,
            'Comment': comment,
            'Book_ID': int(book_id),
            'Comment_ID': int(comment_id)
        })
    else:
        return "Doesn't work"


def delete_comments_by_id(user_name, book_id, comment_id):
    """Function that deletes comment by comment id."""

    correct_user_name = False
    correct_book_id = True
    correct_comment_id = True
    numbers = "0123456789"

    for letter in book_id:
        if letter not in numbers:
            correct_book_id = False
    for letter in comment_id:
        if letter not in numbers:
            correct_comment_id = False
    for comment in retrieved_comment_collection:
        if comment["Username"] == user_name:
            correct_user_name = True
    if correct_user_name and correct_book_id and correct_comment_id:
        collection.delete_one({"Comment_ID": int(comment_id)})
    else:
         return "something went wrong"

#Maybe needed when the front is ready?
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('comment_id', required=False)
    #     parser.add_argument('comment', required=False)
    #     parser.add_argument('book_id', required=False)
    #     parser.add_argument('user_name', required=False)

    #     args = parser.parse_args()
    #     retrieved_ID = list(
    #         collection.find(
    #             {'Comment_ID': comment_id},
    #             {'_id': False}
    #             )
    #         )

    #     for data in retrieved_ID:
    #         if data["Comment_ID"] == comment_id:
    #             collection.find_one_and_delete(
    #                 {"Comment_ID": comment_id},
    #                 {
    #                     'Username': args['user_name'],
    #                     'Comment': args['comment'],
    #                     'Book_ID': args['book_id'],
    #                     'Comment_ID': args['comment_id']
    #                     }
    #                     )
