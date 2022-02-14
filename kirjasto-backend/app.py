from distutils.log import debug
from functools import wraps
from flask import Flask, Response, render_template, session, redirect
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from helpers import (
    is_book_already_added, is_book_id_inside_book_collection,
    is_comment_data_inside_comment_collection,
    is_rating_acceptable,
    is_user_name_inside_user_collection,
    is_object_int, is_id_inside_collection,
    is_email_inside_user_collection,
    is_password_inside_user_collection
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

    def post(
            self, name, writer, year, isbn, about, tags,
            description):
        """Function that posts book data to the database."""

        if is_book_already_added(name, isbn):
            return "Book has already been added!"

        add_new_book(
            name, writer, year, isbn, about, tags,
            description
            )
        return "Book was added succesfully!"


class BooksUpdateBook(Resource):
    """Class for updating book data to the database."""

    def put(
            self, book_id, name, writer, year, isbn, rating, rating_count,
            about, tags, description, loaner, loan_status):
        """Function that updates book data to the database."""

        if is_book_id_inside_book_collection(book_id) and \
                is_book_already_added(name, isbn) and \
                is_object_int(year) and is_object_int(rating) and \
                is_object_int(rating_count):
            update_book(
                book_id, name, writer, year, isbn,
                rating, rating_count, about, tags, description,
                loaner, loan_status)
            return "Book was updated succesfully!"
        return "error: Not a valid book_id, name, isbn or rating! " \
            "book_id, name and isbn must be inside the database!"


class BooksDeleteByID(Resource):
    """Class for deleting book data from the database."""

    def delete(self, book_id):
        """Function that deletes book data from the database."""

        if is_book_id_inside_book_collection(book_id):
            delete_book_by_id(book_id)
            return "Book was deleted succesfully!"
        return "error: Not a valid book_id! " \
            "Book_id must be inside the database!"


class BooksLoanByUsernameAndID(Resource):
    """Class for changing book datas loan state."""

    def post(self, user_name, book_id):
        """Function that changes book's loan state."""

        if is_user_name_inside_user_collection(user_name) and \
                is_book_id_inside_book_collection(book_id):
            loan_book_by_username_and_id(user_name, book_id)
            return "Book was loaned succesfully!"

        return "error: Not a valid username or book_id." \
            "Book_id and username must exist"


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

    def post(self, user_name, comment, book_id):
        """Function that posts comment data to the database."""

        if is_book_id_inside_book_collection(book_id) and \
                is_user_name_inside_user_collection(user_name):
            post_comment(user_name, comment, book_id)
            return "Comment was posted succesfully!"
        return "error: Not a valid username or book_id! " \
            "book_id and username must exist!"


class CommentsUpdateComment(Resource):
    """Class for updating comment data to the database."""

    def put(self, comment_id, user_name, comment, book_id):
        """Function that updates comment data to the database."""

        if is_comment_data_inside_comment_collection(
                comment_id, user_name, book_id) and \
                is_user_name_inside_user_collection(user_name) and \
                is_book_id_inside_book_collection(book_id):
            update_comment(comment_id, user_name, comment, book_id)
            return "Comment was updated succesfully!"
        return "error: Not a valid comment_id, username or book_id! " \
            "comment_id, username and book_id must be inside the database!"


class CommentsDelete(Resource):
    """Class for deleting comment data from the database."""

    def delete(self, user_name, book_id, comment_id):
        """Function that deletes comment data from the database."""
        if is_user_name_inside_user_collection(user_name) and \
                is_book_id_inside_book_collection(book_id) and \
                is_comment_data_inside_comment_collection(
                    comment_id, user_name, book_id):
            delete_comments_by_id(user_name, book_id, comment_id)
            return "Comment was deleted succesfully!"
        return "error: Not a valid username, book_id or comment_id!"


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

    def post(self, user_name, book_id, rating):
        """Function that posts comment data to the database."""

        if is_rating_acceptable(rating) is False \
                or is_user_name_inside_user_collection(user_name) \
                is False or is_book_id_inside_book_collection(book_id) \
                is False or is_object_int(rating) is False:
            return "error: Not a valid username, book_id or rating. " \
                "Username and book_id must exist inside the database!"

        give_rating(user_name, book_id, rating)
        return "Rating was posted succesfully!"


#Test is needed for the rating_id
class RatingsUpdateRating(Resource):
    """Class for updating rating data to the database."""

    def put(self, rating_id, user_name, book_id, rating):
        """Function that updates rating data to the database."""

        if is_user_name_inside_user_collection(user_name) and \
                is_book_id_inside_book_collection(book_id) and \
                is_object_int(rating):
            update_rating(rating_id, user_name, book_id, rating)
            return "Rating was updated succesfully!"
        return "error: Not a valid username, book_id or rating! " \
            "username and book_id must be inside the database " \
            "And Rating must be int!"


class RatingsDeleteByUsernameAndBookID(Resource):
    """Class for deleting rating data from the database."""

    def delete(self, user_name, book_id):
        """Function that deletes rating data from the database."""

        if is_user_name_inside_user_collection(user_name) and \
                is_book_id_inside_book_collection(book_id):
            delete_rating(user_name, book_id)
            return "Rating was deleted succesfully!"
        return "error: Not a valid username or book_id! " \
            "username and book_id must be inside the database!"


class Users(Resource):
    """Class for returning user data from the database."""

    def get(self, user_name=None, object_id=None):
        """Function that returns user data depending on the url."""

        if object_id is not None:
            if is_id_inside_collection(object_id):
                return get_user_by_id(object_id)
        elif user_name is not None:
            if is_user_name_inside_user_collection(user_name):
                return get_user_by_username(user_name)
            return 'error: Not a valid username! username must exist!'
        return get_users()


class UsersUpdateUser(Resource):
    """Class for updating user data to the database."""

    def put(self, object_id, user_name, email, password):
        """Function that updates user data to the database."""

        if is_id_inside_collection(object_id) and \
                is_user_name_inside_user_collection(user_name) and \
                is_email_inside_user_collection(email) and \
                is_password_inside_user_collection(password):
            update_user(object_id, user_name, email, password)
            return "User was updated succesfully!"
        return "error: Not a valid object_id! " \
            "object_id must be inside the database!"


class UsersDeleteByID(Resource):
    """Class for deleting user data from the database."""

    def delete(self, object_id):
        """Function that deletes user data from the database."""

        if is_id_inside_collection(object_id):
            delete_user_by_id(object_id)
            return "User was deleted succesfully!"
        return "error: Not a valid object_id! " \
            "object_id must be inside the database!"


class HomePage(Resource):
    def get(self):
        return Response(response=render_template("index.html"))


api.add_resource(TesterData, "/api/testerdata/<_id>")
# works
api.add_resource(HomePage, '/')
# works but needs to be edited
api.add_resource(
    Books,
    '/api/books',
    '/api/books/<book_id>'
    )
# works but needs to be edited
api.add_resource(
    BooksAddNewBook,
    '/api/books/add/<name>/<writer>/<year>/<isbn>/' +
    '<about>/<tags>/<description>'
    )
# Works
api.add_resource(
    BooksUpdateBook, '/api/books/update/<book_id>/<name>/<writer>/' +
    '<year>/<isbn>/<rating>/<rating_count>/<about>/<tags>/<description>/' +
    '<loaner>/<loan_status>'
    )
# works
api.add_resource(BooksDeleteByID, '/api/books/d/<book_id>')
# not complete
api.add_resource(
    BooksLoanByUsernameAndID,
    '/api/books/loan/<user_name>/<book_id>'
    )
# works
api.add_resource(
    Comments,
    '/api/comments',
    '/api/comments/<book_id>'
    )
# works
api.add_resource(
    CommentsAddNewComment,
    '/api/comments/add/<user_name>/<comment>/<book_id>'
    )
# Works
api.add_resource(
    CommentsUpdateComment,
    '/api/comments/update/<comment_id>/<user_name>/<comment>/<book_id>'
    )
# Works
api.add_resource(
    CommentsDelete,
    '/api/comments/d/<user_name>/<book_id>/<comment_id>'
    )
# Not complete
# Works but when book is added doesn't work after reboot?
api.add_resource(
    Ratings,
    '/api/ratings',
    '/api/ratings/<user_name>',
    '/api/ratings/<user_name>/<book_id>'
    )
# Works
api.add_resource(
    RatingsAddNewRating,
    '/api/ratings/add/<user_name>/<book_id>/<rating>'
    )
# Not complete
api.add_resource(
    RatingsUpdateRating,
    '/api/ratings/update/<rating_id>/<user_name>/<book_id>/<rating>'
    )
# not complete
api.add_resource(
    RatingsDeleteByUsernameAndBookID,
    '/api/ratings/d/<book_id>/<user_name>'
    )
api.add_resource(
    Users,
    '/api/users',
    '/api/users/<user_name>',
    '/api/users/<user_name>/<object_id>'
    )
api.add_resource(
    UsersUpdateUser,
    '/api/users/update/<object_id>/<user_name>/<email>/<password>'
    )
api.add_resource(
    UsersDeleteByID,
    '/api/users/d/<object_id>'
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
