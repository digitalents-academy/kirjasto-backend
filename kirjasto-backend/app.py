"""app.py: The project's main file. The app will be run from here."""

from functools import wraps
import json
from json import JSONEncoder
from flask import Flask, Response, render_template, session, redirect, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
import jwt
from books import (
    get_books,
    get_book_by_book_id,
    add_new_book,
    delete_book_by_book_id,
    update_book,
    loan_book_by_username_and_book_id,
    return_book_by_username_and_book_id
    )
from comments import (
    delete_comments_by_comment_id,
    get_comments,
    get_comments_by_book_id,
    post_comment,
    update_comment
    )
from rating_system import (
    get_ratings,
    get_ratings_by_username,
    get_ratings_by_username_and_book_id,
    update_rating,
    give_rating,
    delete_rating
    )
import db_secret
from users import (
    get_user_by_username,
    get_users,
    get_user_by_object_id,
    promote_user_to_admin,
    update_user,
    delete_user_by_object_id
    )

parser = reqparse.RequestParser()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
api = Api(app)

client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":" + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
collection = db['users']
testcollection = db["testerdata"]
retrieved_testcollection = list(testcollection.find({}, {'_id': False}))


#testing the use of object id
class MongoEncoder(JSONEncoder):
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return JSONEncoder.default(obj, **kwargs)


#testing the use of object id
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return 'Error: Token is missing!'
        try:
            jwt.decode(token, app.config['SECRET_KEY'],  algorithms=["HS256"])
        except:
            return "Error: Token is invalid!"
        return f(*args, **kwargs)
    return decorated


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap


from user import routes


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')


#Not used atm
class TesterData(Resource):
    """Class for testing sending and returning data."""
    # def get(self):
    #     return list(testcollection.find())

    def get(self, _id):
        """Function that returns data with object id."""

        retrieved = testcollection.find_one({"_id": ObjectId(_id)})

        #return JSONEncoder().encode(retrieved)
        return json.dumps(retrieved, cls=MongoEncoder)

    def post(self):
        """
        Function that posts data depending on
        what is writed on the frontend form.
        """

        parser.add_argument("name", type=str)
        parser.add_argument("writer", type=str)
        parser.add_argument("year", type=int)
        args = parser.parse_args()

        item = {
            "name": args["name"],
            "writer": args["writer"],
            "year": args["year"]
            }
        testcollection.insert_one(item)
        return "Nice!"


class BooksGet(Resource):
    """Class for returning book data from the database."""

    def get(self, book_id=None):
        """Function that returns book data depending on the url."""

        if book_id is not None:
            return get_book_by_book_id(book_id)
        return get_books()


class BooksAddNewBook(Resource):
    """Class for posting book data to the database."""

    @token_required
    def post(self):
        """Function that posts book data to the database."""

        return add_new_book()


class BooksUpdateBook(Resource):
    """Class for updating book data to the database."""

    @token_required
    def put(self):
        """Function that updates book data to the database."""

        return update_book()


class BooksDeleteByBookID(Resource):
    """Class for deleting book data from the database."""

    @token_required
    def delete(self):
        """Function that deletes book data from the database."""

        return delete_book_by_book_id()


class BooksLoanByUsernameAndBookID(Resource):
    """Class for changing book's loan state."""

    def put(self):
        """Function that changes book's loan state."""

        return loan_book_by_username_and_book_id()


class BooksReturnByUsernameAndBookID(Resource):
    """Class for changing book's loan state."""

    def put(self):
        """Function that changes book's loan state."""

        return return_book_by_username_and_book_id()


class CommentsGet(Resource):
    """Class for returning comment data from the database."""

    def get(self, book_id=None):
        """Function that returns comment data depending on the url."""

        if book_id is not None:
            return get_comments_by_book_id(book_id)
        return get_comments()


class CommentsAddNewComment(Resource):
    """Class for posting comment data to the database."""

    def post(self):
        """Function that posts comment data to the database."""

        return post_comment()


class CommentsUpdateComment(Resource):
    """Class for updating comment data to the database."""

    def put(self):
        """Function that updates comment data to the database."""

        return update_comment()


class CommentsDelete(Resource):
    """Class for deleting comment data from the database."""

    def delete(self):
        """Function that deletes comment data from the database."""

        return delete_comments_by_comment_id()


class RatingsGet(Resource):
    """Class for returning rating data from the database."""

    def get(self, user_name=None, book_id=None):
        """Function that returns rating data depending on the url."""

        if book_id is not None:
            return get_ratings_by_username_and_book_id(
                user_name,
                book_id
                )
        elif user_name is not None:
            return get_ratings_by_username(
                user_name)
        return get_ratings()


class RatingsAddNewRating(Resource):
    """Class for posting rating data to the database."""

    def post(self):
        """Function that posts rating data to the database."""

        return give_rating()


class RatingsUpdateRating(Resource):
    """Class for updating rating data to the database."""

    def put(self):
        """Function that updates rating data to the database."""

        return update_rating()


class RatingsDeleteByUsernameAndBookID(Resource):
    """Class for deleting rating data from the database."""

    def delete(self):
        """Function that deletes rating data from the database."""

        return delete_rating()


class UsersGet(Resource):
    """Class for returning user data from the database."""

    def get(self, user_name=None, object_id=None):
        """Function that returns user data depending on the url."""

        if object_id is not None:
            return get_user_by_object_id(object_id)
        elif user_name is not None:
            return get_user_by_username(user_name)
        return get_users()


class UsersUpdateUser(Resource):
    """Class for updating user data to the database."""

    def put(self):
        """Function that updates user data to the database."""

        return update_user()


class UsersPromoteUser(Resource):
    """Class for promoting user to admin."""

    @token_required
    def put(self):
        """Function that promotes user to admin."""

        return promote_user_to_admin()


class UsersDeleteByObjectID(Resource):
    """Class for deleting user data from the database."""

    def delete(self):
        """Function that deletes user data from the database."""

        return delete_user_by_object_id()


# Not used atm
class HomePage(Resource):
    def get(self):
        return Response(response=render_template("index.html"))


api.add_resource(TesterData, "/api/testerdata/<_id>")
# Not used atm
#api.add_resource(HomePage, '/')
# Works
api.add_resource(
    BooksGet,
    '/api/books',
    '/api/books/<book_id>'
    )
# Works
api.add_resource(
    BooksAddNewBook,
    '/api/books/add')
# Works
api.add_resource(
    BooksUpdateBook, '/api/books/update'
    )
# Works
api.add_resource(BooksDeleteByBookID, '/api/books/d')
# Works
api.add_resource(
    BooksLoanByUsernameAndBookID,
    '/api/books/loan'
    )
# Works
api.add_resource(
    BooksReturnByUsernameAndBookID,
    '/api/books/return'
    )
# Works
api.add_resource(
    CommentsGet,
    '/api/comments',
    '/api/comments/<book_id>'
    )
# Works
api.add_resource(
    CommentsAddNewComment,
    '/api/comments/add'
    )
# Works
api.add_resource(
    CommentsUpdateComment,
    '/api/comments/update'
    )
# Works
api.add_resource(
    CommentsDelete,
    '/api/comments/d'
    )
# Works but when book is added doesn't work before reboot?
api.add_resource(
    RatingsGet,
    '/api/ratings',
    '/api/ratings/<user_name>',
    '/api/ratings/<user_name>/<book_id>'
    )
# Works
api.add_resource(
    RatingsAddNewRating,
    '/api/ratings/add'
    )
# Works
api.add_resource(
    RatingsUpdateRating,
    '/api/ratings/update'
    )
# Works
api.add_resource(
    RatingsDeleteByUsernameAndBookID,
    '/api/ratings/d'
    )
# Works
api.add_resource(
    UsersGet,
    '/api/users',
    '/api/users/<user_name>',
    '/api/users/<user_name>/<object_id>'
    )
# Works
api.add_resource(
    UsersUpdateUser,
    '/api/users/update'
    )
# Works
api.add_resource(
    UsersPromoteUser,
    '/api/users/promote'
    )
# Works
api.add_resource(
    UsersDeleteByObjectID,
    '/api/users/d'
    )


# Runs on port 5000!!
if __name__ == "__main__":
    #api urls work with this
    app.run(debug=True)
    #api urls work with this without authentication
    #app.run(debug=True, host='127.0.0.1', port=5000)
