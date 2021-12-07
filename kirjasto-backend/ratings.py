from flask_restful import reqparse
from pymongo.mongo_client import MongoClient
import db_secret

# Initiate connection to mongoDB
client = MongoClient("mongodb+srv://"+ db_secret.secret_id +":"+ db_secret.secret_key +"@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['kirjasto-backend']
def get_ratings():
    collection = db['ratings']
    retrieved = list(collection.find({}, {'_id' : False}))
    return retrieved, 200

# Get mean score from the books collection
def get_mean_ratings():
    collection = db['backendAPI']
    retrieved = list(collection.find({}, {'_id' : False}))
    return retrieved, 200

def post_ratings():
    pass

def post_mean_ratings():
    pass

# make a function that converts the ratings into mean score.
# so ratings can be posted as a mean score already.
# user posts ratings -> add to ratings database -> get mean rating from the db. get user rating from the db ->
#add user rating into mean rating and post to book db as rating. 

# Convert posted ratings to mean score.

def convert_to_mean():
    pass