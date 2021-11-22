from flask import Flask
from flask_restful import Resource, Api, reqparse
from pymongo import ALL, MongoClient
from query import db_query, db_full_query, parse

app = Flask(__name__)
api = Api(app)



class Status(Resource):
# Get the status for all of the books in the books collection
    def get(self):
        # Query books with book name id and loan status
        return db_query()
        
class StatusID(Resource):            
    def get(self, book_id):    
        client = MongoClient("mongodb+srv://kirjastoAdmin:<PASSWORD>@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client['kirjasto-backend']
        collection = db['backendAPI']
        retrievedID = list(collection.find({'Book ID' : book_id,}, {
         '_id': False
        }))
        # Check if input is an int, otherwise throw an error
        for booknumbers in retrievedID:    
            if int(book_id):
                return retrievedID
        else:
            return 'error: Not a valid BookID! Book ID must be an int and the book must exist!', 400
            
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
        parser.add_argument('book_id', required = True)
        parser.add_argument('loaner', required = True)
        parser.add_argument('loan_status', required = True)
        
        args = parser.parse_args()
        # Checking if the book name already exists.        
        client = MongoClient("mongodb+srv://kirjastoAdmin:<PASSWORD>@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client['kirjasto-backend']
        collection = db['backendAPI']
        retrieved = list(collection.find({}, {'_id' : False}))
        #iterate through retrieved and find if POST value "book_id" is the same as database value Book ID.
        #if true -> update. else throw errors.
        for booknumbers in retrieved:
            if args['book_id'] in booknumbers['Book ID']:
                new_book = collection.find_one_and_update(booknumbers,{"$set": parse()})
            elif args['book_id'] != booknumbers['Book ID']:
                return {'message': f"'{args['book_id']}' doesnt exist."
                }, 401
            else:
                return {
                     'message': f" Unknown error."
                }, 401
            

        retrieved = list(collection.find({}, {'_id' : False}))
        return retrieved, 200
 

api.add_resource(Status, '/status')
api.add_resource(StatusID, '/status/<book_id>')
api.add_resource(Books, '/books')
api.add_resource(Loan, '/loan')


# Runs on port 8080!!
if __name__ == "__main__":
    app.run( debug = True, host='127.0.0.1', port=8000 )
