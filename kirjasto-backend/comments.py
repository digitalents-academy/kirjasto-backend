import uuid
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

    retrieved = list(
        collection.find({'Book_ID': book_id}, {'_id': False})
        )
    return retrieved


#Works but the comment_id could be same with the help of delete
#so some new way to make ids is needed
#Error handling is done correctly here, but nowhere else!
def post_comment(user_name, comment, book_id):
    """Function that posts new comment to the database."""

    collection.insert_one({
        'Username': user_name,
        'Comment': comment,
        'Book_ID': book_id,
        'Comment_ID': uuid.uuid4().hex
    })

    current_comment_id = retrieved_comment_collection['Comment_ID']

    for comment in retrieved_comment_collection:
        if comment["Comment_ID"] == current_comment_id:
            return "Something went wrong!"


def update_comment(comment_id, user_name, comment, book_id):
    """Function that posts updated comment data to the database."""
    
    old_user_name = ""
    old_comment = ""
    old_book_id = ""

    for comment in retrieved_comment_collection:
        if comment["_id"] == comment_id:
            old_user_name = comment["Username"]
            old_comment = comment["Comment"]
            old_book_id = comment["Book_ID"]

    collection.update(
        {'Comment_ID': comment_id},
        {
            "$set": {
                "Username": user_name,
                "Comment": comment,
                "Book_ID": book_id,
                "Comment_ID": comment_id
                }
            }
        )

    if old_user_name != user_name or old_user_name != "" or old_comment != comment or old_comment != "" or old_book_id != book_id or old_book_id != "":
        return "Comment updated!"



def delete_comments_by_id(user_name, book_id, comment_id):
    """Function that deletes comment by comment id."""

    collection.delete_one(
        {
            "Comment_ID": comment_id,
            "Username": user_name,
            "Book_ID": book_id
            }
        )

    for comment in retrieved_comment_collection:
        if comment["Comment_ID"] == comment_id:
            return "Something went wrong!"


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
