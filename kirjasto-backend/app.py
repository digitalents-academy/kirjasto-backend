from functools import wraps
from flask import Flask, Response, render_template, session, redirect
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from helpers import (
    is_book_id_inside_book_collection,
    is_user_name_inside_user_collection,
    is_object_id_inside_user_collection
    )
from books import (
    get_books,
    get_book_by_id,
    add_new_book,
    delete_book_by_id,
    update_book,
    loan_book_by_username_and_id
    )
from comments import (
    delete_comments_by_id,
    get_comments,
    get_comments_by_book_id,
    post_comment,
    update_comment
    )
from rating_system import (
    get_retrieved_rating_collection,
    get_retrieved_ratings_by_username,
    get_retrieved_rating_by_username_and_id,
    update_rating,
    give_rating,
    delete_rating
    )
import db_secret
from users import (
    get_user_by_username,
    get_users,
    get_user_by_id,
    update_user,
    delete_user_by_id
    )

parser = reqparse.RequestParser()

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'
api = Api(app)

client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":" + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
collection = db['users']
testcollection = db["testerdata"]
retrieved_testcollection = list(testcollection.find({}, {'_id': False}))


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


class TesterData(Resource):
    """Class for testing sending and returning data."""
    # def get(self):
    #     return list(testcollection.find())

    def get(self, _id):
        """Function that returns data with object id."""

        return testcollection.find_one({"_id": ObjectId(_id)})

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


class Books(Resource):
    """Class for returning book data from the database."""

    def get(self, book_id=None):
        """Function that returns book data depending on the url."""

        if book_id is not None:
            if is_book_id_inside_book_collection(book_id):
                return get_book_by_id(book_id)
            return "Book is not inside the database!"
        return get_books()


class BooksAddNewBook(Resource):
    """Class for posting book data to the database."""

    def post(self):
        """Function that posts book data to the database."""

        return add_new_book()


class BooksUpdateBook(Resource):
    """Class for updating book data to the database."""

    def put(self):
        """Function that updates book data to the database."""

        return update_book()


class BooksDeleteByID(Resource):
    """Class for deleting book data from the database."""

    def delete(self):
        """Function that deletes book data from the database."""

        return delete_book_by_id()


class BooksLoanByUsernameAndID(Resource):
    """Class for changing book datas loan state."""

    def put(self):
        """Function that changes book's loan state."""

        return loan_book_by_username_and_id()


class Comments(Resource):
    """Class for returning comment data from the database."""

    def get(self, book_id=None):
        """Function that returns comment data depending on the url."""
        if book_id is not None:
            if is_book_id_inside_book_collection(book_id):
                return get_comments_by_book_id(book_id)
            return "error: Not a valid book_id!"
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

        return delete_comments_by_id()


class Ratings(Resource):
    """Class for returning rating data from the database."""

    def get(self, user_name=None, book_id=None):
        """Function that returns rating data depending on the url."""

        if book_id is not None:
            if is_book_id_inside_book_collection(book_id) and \
                    is_user_name_inside_user_collection(user_name):
                return get_retrieved_rating_by_username_and_id(
                    user_name,
                    book_id
                    )
            return "Incorrect username or book id!"
        elif user_name is not None:
            if is_user_name_inside_user_collection(user_name):
                return get_retrieved_ratings_by_username(
                    user_name)
            return "Incorrect username"
        return get_retrieved_rating_collection()


class RatingsAddNewRating(Resource):
    """Class for posting rating data to the database."""

    def post(self):
        """Function that posts comment data to the database."""

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


class Users(Resource):
    """Class for returning user data from the database."""

    def get(self, user_name=None, object_id=None):
        """Function that returns user data depending on the url."""

        if object_id is not None:
            if is_object_id_inside_user_collection(object_id):
                return get_user_by_id(object_id)
        elif user_name is not None:
            if is_user_name_inside_user_collection(user_name):
                return get_user_by_username(user_name)
            return 'error: Not a valid username! username must exist!'
        return get_users()


class UsersUpdateUser(Resource):
    """Class for updating user data to the database."""

    def put(self):
        """Function that updates user data to the database."""

        return update_user()


class UsersDeleteByID(Resource):
    """Class for deleting user data from the database."""

    def delete(self):
        """Function that deletes user data from the database."""

        return delete_user_by_id()


class HomePage(Resource):
    def get(self):
        return Response(response=render_template("index.html"))


api.add_resource(TesterData, "/api/testerdata/<_id>")
# Works
api.add_resource(HomePage, '/')
# Works
api.add_resource(
    Books,
    '/api/books',
    '/api/books/<book_id>'
    )
# Works but the error handling needs to be updated.
api.add_resource(
    BooksAddNewBook,
    '/api/books/add')
# Works but the error handling needs to be updated.
api.add_resource(
    BooksUpdateBook, '/api/books/update'
    )
# Works but the error handling needs to be updated.
api.add_resource(BooksDeleteByID, '/api/books/d')
# Works but the error handling needs to be updated.
api.add_resource(
    BooksLoanByUsernameAndID,
    '/api/books/loan'
    )
# Works
api.add_resource(
    Comments,
    '/api/comments',
    '/api/comments/<book_id>'
    )
# Works but the error handling needs to be updated.
api.add_resource(
    CommentsAddNewComment,
    '/api/comments/add'
    )
# Works but the error handling needs to be updated.
api.add_resource(
    CommentsUpdateComment,
    '/api/comments/update'
    )
# Works but the error handling needs to be updated.
api.add_resource(
    CommentsDelete,
    '/api/comments/d'
    )
# Works but when book is added doesn't work before reboot?
api.add_resource(
    Ratings,
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
    Users,
    '/api/users',
    '/api/users/<user_name>',
    '/api/users/<user_name>/<object_id>'
    )
# Works
api.add_resource(
    UsersUpdateUser,
    '/api/users/update'
    )
# Works but ratings and comments made by the user should be deleted too
api.add_resource(
    UsersDeleteByID,
    '/api/users/d'
    )


# Runs on port 8000!!
if __name__ == "__main__":
    #api urls work with this
    app.run(debug=True)
    #api urls work with this without authentication
    #app.run(debug=True, host='127.0.0.1', port=8000)
    #for testing
    #app.run(
    #    debug=True,
    #    use_debugger=False,
    #    use_reloader=False,
    #    host='127.0.0.1',
    #    port=8000
    #    )
