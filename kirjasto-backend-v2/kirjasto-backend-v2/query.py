from pymongo import ALL, MongoClient
from flask_restful import reqparse

# Initiate connection to mongoDB
client = MongoClient("mongodb+srv://kirjastoAdmin:s3yS2zcXETkqCM@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['kirjasto-backend']
collection = db['backendAPI']

def db_query():

        # had to make id not show, because it threw a not json serializable error.
        retrievedStatus = list(collection.find({}, {
            'Book ID' : True, 'Name' : True, 'Loan Status' : True, '_id': False 
        }))

        return retrievedStatus, 200 
def db_full_query():
        retrievedFull = list(collection.find({}, {'_id' : False}))
        return retrievedFull, 200       
def parse():
# Required values for the api requests. False would be optional
    parser = reqparse.RequestParser()
    parser.add_argument('book_id', required = True)     
#    parser.add_argument('name', required = True)
#    parser.add_argument('writer', required = True)
#    parser.add_argument('year', required = True)
#    parser.add_argument('isbn', required = True)
#    parser.add_argument('rating', required = True)
#    parser.add_argument('about', required = True)
#    parser.add_argument('tags', required = True)
#    parser.add_argument('description', required = True)
    parser.add_argument('loaner', required = True)
    parser.add_argument('loan_status', required = True)
    
    args = parser.parse_args()

    values = {
            'Book ID' : args['book_id'],
#            'Name' : args['name'],
#            'Writer' : args['writer'],
#            'Year' : args['year'],
#            'ISBN' : args['isbn'],
#            'Rating' : args['rating'],
#            'About' : args['about'],
#            'Tags' : args['tags'],            
#            'Description' : args['description'],
            'Loaner' : args['loaner'],
            'Loan Status' : args['loan_status']        
        
            }
    return values
