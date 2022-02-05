from flask import Flask, Response, render_template
from flask_restful import Resource, Api, reqparse
#from flask_restful import reqparse
#from pymongo import ALL
from pymongo import MongoClient
from query import (
    db_query,
    status_query,
    add_new_book,
    delete_book_by_id,
    update_book,
    loan_book_by_id
    )
from comments import (
    delete_comments_by_id,
    get_comments,
    get_comments_by_book_id,
    post_comment
    )
from rating_system import RatingSystem
from user import routes
import db_secret
from bson.objectid import ObjectId
from app import login_required, home, dashboard

parser = reqparse.RequestParser()

app = Flask(__name__)
api = Api(app)
rating_system = RatingSystem()

client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":" + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
collection = db['backendAPI']
testcollection = db["testerdata"]


class TesterData(Resource):
    # def get(self):
    #     return list(testcollection.find())

    def get(self, _id):
        return testcollection.find_one({"_id": ObjectId(_id)})

    def post(self):
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


class StatusGetBooks(Resource):
    # Get the status for all of the books in the books collection
    def get(self):
        # Query books with book name id and loan status
        return db_query()


class StatusAddNewBook(Resource):
    def post(
            self, book_id, name, writer, year, isbn, about, tags,
            description):
        add_new_book(
            book_id, name, writer, year, isbn, about, tags,
            description
            )
        return " Book was added succesfully!"


class StatusUpdateBook(Resource):
    def put(
            self, book_id, name, writer, year, isbn, rating, about, tags,
            description, loaner, loan_status):
        update_book(
            book_id, name, writer, year, isbn, rating, about, tags,
            description, loaner, loan_status
            )
        return "Book was added succesfully!"


class StatusDeleteBookByID(Resource):
    def delete(self, book_id):
        delete_book_by_id(book_id)
        return "Book was deleted succesfully!"


class StatusID(Resource):
    def get(self, book_id):
        return status_query(book_id)


class StatusLoan (Resource):
    def post(self, user_name, book_id):
        loan_book_by_id(user_name, book_id)
        return "Book was loaned succesfully!"


class CommentsGet(Resource):
    def get(self):
        return get_comments()


class CommentsPost(Resource):
    def post(self, user_name, comment, book_id, comment_id):
        post_comment(user_name, comment, book_id, comment_id)
        return "Comment was posted succesfully!"


class CommentsGetByID(Resource):
    def get(self, book_id):
        return get_comments_by_book_id(book_id)


class CommentsDeleteByID(Resource):
    def delete(self, comment_id):
        delete_comments_by_id(comment_id)
        return "Comment was deleted succesfully!"


#Not needed in rating system?
#-----------------------------------------------------------------------------
#Needed in user file
class RatingsGetUsers(Resource):

    def get(self):
        return rating_system.get_retrieved_user_collection()


class RatingsGetUserByUsername(Resource):

    def get(self, user_name):
        return rating_system.get_retrieved_user_by_id(user_name)


class RatingsPostUsers(Resource):

    def post(self):
        rating_system.post_updated_user_collection()
        return ""
#-----------------------------------------------------------------------------


class RatingsGetRatings(Resource):

    def get(self):
        return rating_system.get_retrieved_rating_collection()


#every users ratings
class RatingsGetRatingsByUsername(Resource):

    def get(self, user_name):
        return rating_system.get_retrieved_ratings_by_username(
            user_name
            )


#users rating for single book
class RatingsGetRatingByID(Resource):

    def get(self, user_name, book_id):
        return rating_system.get_retrieved_rating_by_id(
            user_name,
            book_id
            )


class RatingsAddRating(Resource):

    def post(self, user_name: int, book_id: int, rating: int):
        rating_system.give_rating(user_name, book_id, rating)
        return "Rating was posted succesfully!"


class RatingsDeleteRating(Resource):

    def delete(self, user_name, book_id):
        rating_system.delete_rating(user_name, book_id)
        return "Rating was deleted succesfully!"


#Not working
#-----------------------------------------------------------------------------
class AuthenticationSignup(Resource):
    def post(self):
        routes.signup()
        return "User was added succesfully!"


class AuthenticationSignout(Resource):
    def get(self):
        return routes.signout()


class AuthenticationLogin(Resource):
    def post(self):
        return routes.login()


class AuthenticationLoginRequired(Resource):
    def get(self, f):
        return login_required(f)


class AuthenticationHome(Resource):
    def get(self):
        return home()


class AuthenticationDashBoard(Resource):
    def get(self):
        return dashboard()


class HomePage(Resource):
    def get(self):
        return Response(response=render_template("index.html"))
#-----------------------------------------------------------------------------


api.add_resource(TesterData, "/api/testerdata/<_id>")
# works
#api.add_resource(HomePage, '/')
# testing
#api.add_resource(AuthenticationLoginRequired, )
# testing
api.add_resource(AuthenticationHome, '/')
# testing
api.add_resource(AuthenticationDashBoard, '/dashboard/')
# works
api.add_resource(StatusGetBooks, '/api/status')
# works
api.add_resource(
    StatusAddNewBook,
    '/api/status/add/<book_id>/<name>/<writer>/<year>/<isbn>/' +
    '<about>/<tags>/<description>'
    )
# works but is this needed?
api.add_resource(
    StatusUpdateBook, '/api/status/update/<book_id>/<name>/<writer>/' +
    '<year>/<isbn>/<about>/<tags>/<description>/'
    )
# works
api.add_resource(StatusDeleteBookByID, '/api/status/d/<book_id>/')
# works
api.add_resource(StatusID, '/api/status/<book_id>')
# not complete
api.add_resource(StatusLoan, '/api/loan/<user_name>/<book_id>')
# works
api.add_resource(CommentsGet, '/api/comments/get')
# works
api.add_resource(CommentsGetByID, '/api/comments/get/<book_id>')
# works
api.add_resource(
    CommentsPost,
    '/api/comments/<user_name>/<comment>/<book_id>/<comment_id>'
    )
# Works
api.add_resource(CommentsDeleteByID, '/api/comments/d/<comment_id>')
# Works
api.add_resource(RatingsGetUsers, '/api/ratings/get/users/')
# Works
api.add_resource(
    RatingsGetUserByUsername,
    '/api/ratings/get/users/<user_name>/'
    )
# Not sure
api.add_resource(RatingsPostUsers, '/api/ratings/post/users/')
# Works but when book is added doesn't work after reboot?
api.add_resource(RatingsGetRatings, '/api/ratings/get/ratings/')
# Works
api.add_resource(
    RatingsGetRatingsByUsername,
    '/api/ratings/get/ratings/<user_name>'
    )
# not complete
api.add_resource(
    RatingsGetRatingByID,
    '/api/ratings/get/ratings/user_name/book_id/'
    )
# Works
api.add_resource(
    RatingsAddRating,
    '/api/ratings/add/<user_name>/<book_id>/<rating>/'
    )
# not complete
api.add_resource(RatingsDeleteRating, '/api/ratings/d/<book_id>/user_name/')
api.add_resource(AuthenticationSignup,
                 '/api/authentication/signup', methods=['POST'])
api.add_resource(AuthenticationSignout, '/api/authentication/signout')
api.add_resource(AuthenticationLogin,
                 '/api/authentication/login', methods=['POST'])

# Runs on port 8000!!
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8000)
