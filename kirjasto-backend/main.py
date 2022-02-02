from flask import Flask, Response, render_template
from flask_restful import Resource, Api, reqparse
#from pymongo import ALL
from pymongo import MongoClient
from query import (
    db_query,
    parse,
    status_query,
    add_new_book,
    delete_book_by_id,
    update_book
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


app = Flask(__name__)
api = Api(app)
rating_system = RatingSystem()

client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":" + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
collection = db['backendAPI']


class StatusGetBooks(Resource):
    # Get the status for all of the books in the books collection
    def get(self):
        # Query books with book name id and loan status
        return db_query()


class StatusAddNewBook(Resource):
    def post(
            self, book_id, name, writer, year, isbn, rating, about, tags,
            description, loaner, loan_status):
        add_new_book(
            book_id, name, writer, year, isbn, rating, about, tags,
            description, loaner, loan_status
            )


class StatusUpdateBook(Resource):
    def post(
            self, book_id, name, writer, year, isbn, rating, about, tags,
            description, loaner, loan_status):
        update_book(
            book_id, name, writer, year, isbn, rating, about, tags,
            description, loaner, loan_status
            )


class StatusDeleteBookByID(Resource):
    def delete(self, book_id):
        return delete_book_by_id(book_id),  {"Deleted comment!"}, 200


class StatusID(Resource):
    def get(self, book_id):
        return status_query(book_id), 200


class Loan (Resource):
    # Manipulate the loaning system for the books in the books collection
    def post(self):
        # Require these args for the POST request.
        parser = reqparse.RequestParser()
        parser.add_argument('book_id', required=True)
        parser.add_argument('loaner', required=True)
        parser.add_argument('loan_status', required=True)

        args = parser.parse_args()
        # Checking if the book name already exists.
        retrieved = list(collection.find({}, {'_id': False}))
        # iterate through retrieved and find if POST value "book_id"
        # is the same as database value Book ID.
        # if true -> update. else throw errors.
        for booknumbers in retrieved:
            if args['book_id'] in booknumbers['Book ID']:
                new_book = collection.find_one_and_update(
                    booknumbers, {"$set": parse()})
            elif args['book_id'] != booknumbers['Book ID']:
                return {'message': f"'{args['book_id']}' doesnt exist."
                        }, 401
            else:
                return {
                    'message': f" Unknown error."
                }, 401

        retrieved = list(collection.find({}, {'_id': False}))
        return retrieved, 200


class CommentsGet(Resource):
    def get(self):
        return get_comments(), 200


class CommentsPost(Resource):
    def post(self, user_id, comment, book_id, comment_id):
        return post_comment(user_id, comment, book_id, comment_id), 200


class CommentsGetByID(Resource):
    def get(self, book_id):
        return get_comments_by_book_id(book_id), 200


class CommentsDeleteByID(Resource):
    def delete(self, comment_id):
        return delete_comments_by_id(comment_id),  {"Deleted comment!"}, 200


class RatingsGetBooks(Resource):

    def get(self):
        return rating_system.get_retrieved_book_collection(), 200


class RatingsGetBookByID(Resource):

    def get(self, book_id):
        return rating_system.get_retrieved_book_by_id(book_id), 200


class RatingsPostBooks(Resource):

    def post(self):
        rating_system.post_updated_book_collection(), 200


class RatingsGetUsers(Resource):

    def get(self):
        return rating_system.get_retrieved_user_collection(), 200


class RatingsGetUserByUsername(Resource):

    def get(self, user_name):
        return rating_system.get_retrieved_user_by_id(user_name), 200


class RatingsPostUsers(Resource):

    def post(self):
        rating_system.post_updated_user_collection(), 200


class RatingsGetRatings(Resource):

    def get(self):
        return rating_system.get_retrieved_rating_collection(), 200


class RatingsGetRatingsByUsername(Resource):

    def get(self, user_name):
        return rating_system.get_retrieved_ratings_by_username(
            user_name
            ), 200


class RatingsGetRatingByID(Resource):

    def get(self, user_id, book_id):
        return rating_system.get_retrieved_rating_by_id(
            user_id,
            book_id
            ), 200


class RatingsPostRating(Resource):

    def post(self, user_name: int, book_id: int, rating: int):
        rating_system.give_rating(user_name, book_id, rating), 200


class RatingsDeleteRating(Resource):

    def delete(self, user_name, book_id):
        rating_system.delete_rating(user_name, book_id), 200


class AuthenticationSignup(Resource):
    def post(self):
        return routes.signup(), 200


class AuthenticationSignout(Resource):
    def get(self):
        return routes.signout(), 200


class AuthenticationLogin(Resource):
    def post(self):
        return routes.login(), 200


class HomePage(Resource):
    def get(self):
        return Response(response=render_template("index.html"))

# works
api.add_resource(HomePage, '/')
# works 
api.add_resource(StatusGetBooks, '/api/status')
# not complete
api.add_resource(StatusAddNewBook, '/api/status/add/<book_id>/<name>/<writer>/<year>/<isbn>/<rating>/<about>/<tags>/<description>/<loaner>/<loan_status>')
# not complete
api.add_resource(StatusUpdateBook, '/api/status/update/<book_id>/<name>/<writer>/<year>/<isbn>/<rating>/<about>/<tags>/<description>/<loaner>/<loan_status>')
# not complete
api.add_resource(StatusDeleteBookByID, '/api/status/d/<book_id>/')
# works
api.add_resource(StatusID, '/api/status/<book_id>')
# not complete
api.add_resource(Loan, '/api/loan')
# works
api.add_resource(CommentsGet, '/api/comments/get')
# works
api.add_resource(CommentsGetByID, '/api/comments/get/<book_id>')
# not complete
api.add_resource(CommentsPost, '/api/comments/<user_id>/<comment>/<book_id>/<comment_id>')
# not complete
api.add_resource(CommentsDeleteByID, '/api/comments/d/<comment_id>')
# dunno
api.add_resource(RatingsGetBooks, '/api/ratings/get/books/')
api.add_resource(RatingsGetBookByID, '/api/ratings/get/books/<book_id>/')
api.add_resource(RatingsPostBooks, '/api/ratings/post/books/')
api.add_resource(RatingsGetUsers, '/api/ratings/get/users/')
api.add_resource(
    RatingsGetUserByUsername,
    '/api/ratings/get/users/<user_name>/'
    )
api.add_resource(RatingsPostUsers, '/api/ratings/post/users/')
api.add_resource(RatingsGetRatings, '/api/ratings/get/ratings/')
# not complete
api.add_resource(
    RatingsGetRatingsByUsername,
    '/api/ratings/get/ratings/<user_name>'
    )
# not complete
api.add_resource(
    RatingsGetRatingByID,
    '/api/ratings/get/ratings/user_name/book_id/'
    )
# not complete
api.add_resource(
    RatingsPostRating,
    '/api/ratings/post/<user_name>/<book_id>/<rating>/'
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
