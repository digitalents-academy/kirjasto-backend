from flask import Flask
from flask_restful import Resource, Api, reqparse
from pymongo import ALL, MongoClient
from query import db_query, db_full_query, parse, status_query
from comments import delete_comments_by_id, get_comments, get_comments_by_book_id, post_comments
from rating_system import RatingSystem
from user import routes
import db_secret

app = Flask(__name__)
api = Api(app)
rating_system = RatingSystem()

# Initiate connection to mongoDB
client = MongoClient("mongodb+srv://" + db_secret.secret_id + ":" + db_secret.secret_key +
                     "@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['kirjasto-backend']
collection = db['backendAPI']


class Status(Resource):
    # Get the status for all of the books in the books collection
    def get(self):
        # Query books with book name id and loan status
        return db_query()


class StatusID(Resource):
    def get(self, book_id):
        return status_query(), 200


class Books(Resource):
    # Get the details of all of the books in the books collection
    def get(self):
        # Query with full info
        return db_full_query()


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
        # iterate through retrieved and find if POST value "book_id" is the same as database value Book ID.
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

# Class for interacting with comments collection


class Comments(Resource):
    def get(self):
        return get_comments(), 200

    def post(self):
        return post_comments(), 200


class CommentsID(Resource):
    def get(self, book_id):
        return get_comments_by_book_id(book_id), 200


class CommentsDeleteByID(Resource):
    def delete(self, comment_id):
        return delete_comments_by_id(comment_id),  {"Deleted comment!"}, 200


class RatingsBooks(Resource):

    def get(self):
        rating_system.get_retrieved_book_collection()

    def post(self):
        rating_system.post_updated_book_collection()


class RatingsUsers(Resource):

    def get(self):
        rating_system.get_retrieved_user_collection()

    def post(self):
        rating_system.post_updated_user_collection()


class Ratings(Resource):

    def get(self):
        rating_system.get_retrieved_rating_collection()

    def post(self, rating_data):
        rating_system.give_rating(rating_data)

    def delete(self, user_id, book_id):
        rating_system.delete_rating(user_id, book_id)


class AuthenticationSignup(Resource):
    def post(self):
        return routes.signup()


class AuthenticationSignout(Resource):
    def get(self):
        return routes.signout()


class AuthenticationLogin(Resource):
    def post(self):
        return routes.login()


# works
api.add_resource(Status, '/api/status')
# works
api.add_resource(StatusID, '/api/status/<book_id>')
# works
api.add_resource(Books, '/api/books')
# not complete
api.add_resource(Loan, '/api/loan')
# works
api.add_resource(Comments, '/api/comments')
# works
api.add_resource(CommentsID, '/api/comments/<book_id>')
# post comment api path not made yet
# not complete
api.add_resource(CommentsDeleteByID, '/api/comments/d/<comment_id>')
#dunno
api.add_resource(RatingsBooks, '/api/ratings/books/')
api.add_resource(RatingsUsers, '/api/ratings/users/')
api.add_resource(Ratings, '/api/ratings/')
api.add_resource(AuthenticationSignup,
                 '/api/authentication/signup', methods=['POST'])
api.add_resource(AuthenticationSignout, '/api/authentication/signout')
api.add_resource(AuthenticationLogin,
                 '/api/authentication/login', methods=['POST'])

# Runs on port 8000!!
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8000)
