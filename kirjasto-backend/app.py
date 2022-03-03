"""app.py: The project's main file. The app will be run from here."""

from functools import wraps
from flask_cors import CORS
from flask import Flask, render_template, session, redirect, request
from flask_restful import Resource, Api, reqparse
from pymongo.mongo_client import MongoClient
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
    get_comments_by_book_id,
    post_comment,
    update_comment
    )
from rating_system import (
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
CORS(app)

client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":" + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
collection = db['users']
testcollection = db["testerdata"]
retrieved_testcollection = list(testcollection.find({}, {'_id': False}))


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

    def get(self, book_id):
        """Function that returns comment data depending on the url."""

        return get_comments_by_book_id(book_id)


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

    def get(self, user_name, book_id=None):
        """Function that returns rating data depending on the url."""

        if book_id is not None:
            return get_ratings_by_username_and_book_id(
                user_name,
                book_id
                )
        else:
            return get_ratings_by_username(
                user_name)


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


class UsersGetAll(Resource):
    """Class for returning all user data from the database."""

    @token_required
    def get(self):
        """Function that returns all user data."""

        return get_users()


class UsersGet(Resource):
    """Class for returning user data from the database."""

    def get(self, user_name, object_id=None):
        """Function that returns user data depending on the url."""

        if object_id is not None:
            return get_user_by_object_id(object_id)
        else:
            return get_user_by_username(user_name)


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


api.add_resource(
    BooksGet,
    '/api/books',
    '/api/books/<book_id>'
    )
api.add_resource(
    BooksAddNewBook,
    '/api/books/add')
api.add_resource(
    BooksUpdateBook, '/api/books/update'
    )
api.add_resource(BooksDeleteByBookID, '/api/books/d')
api.add_resource(
    BooksLoanByUsernameAndBookID,
    '/api/books/loan'
    )
api.add_resource(
    BooksReturnByUsernameAndBookID,
    '/api/books/return'
    )
api.add_resource(
    CommentsGet,
    '/api/comments/<book_id>'
    )
api.add_resource(
    CommentsAddNewComment,
    '/api/comments/add'
    )
api.add_resource(
    CommentsUpdateComment,
    '/api/comments/update'
    )
api.add_resource(
    CommentsDelete,
    '/api/comments/d'
    )
api.add_resource(
    RatingsGet,
    '/api/ratings/<user_name>',
    '/api/ratings/<user_name>/<book_id>'
    )
api.add_resource(
    RatingsAddNewRating,
    '/api/ratings/add'
    )
api.add_resource(
    RatingsUpdateRating,
    '/api/ratings/update'
    )
api.add_resource(
    RatingsDeleteByUsernameAndBookID,
    '/api/ratings/d'
    )
api.add_resource(UsersGetAll, '/api/users')
api.add_resource(
    UsersGet,
    '/api/users/<user_name>',
    '/api/users/<user_name>/<object_id>'
    )
api.add_resource(
    UsersUpdateUser,
    '/api/users/update'
    )
api.add_resource(
    UsersPromoteUser,
    '/api/users/promote'
    )
api.add_resource(
    UsersDeleteByObjectID,
    '/api/users/d'
    )


# Runs on port 5000!!
if __name__ == "__main__":
    # api urls work with this
    app.run(debug=True)
    # api urls work with this without authentication
    # app.run(debug=True, host='127.0.0.1', port=5000)
