from flask_restful import reqparse
from pymongo.mongo_client import MongoClient
import db_secret

# Initiate connection to mongoDB
client = MongoClient("mongodb+srv://"+ db_secret.secret_id +":"+ db_secret.secret_key +"@cluster0.6se1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['kirjasto-backend']
collection = db['ratings']

def get_ratings():
    retrieved = list(collection.find({}, {'_id' : False}))
    return retrieved, 200

def post_ratings():
    pass

