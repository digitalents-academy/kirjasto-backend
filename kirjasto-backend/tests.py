from app import (
    TesterData, Books, BooksAddNewBook, BooksDeleteByID,
    BooksLoanByUsernameAndID, BooksUpdateBook, Comments,
    CommentsAddNewComment, CommentsDelete, Ratings,
    RatingsAddNewRating, RatingsDeleteByUsernameAndBookID,
    Users, UsersDeleteByID, UsersUpdateUser
    )

from pymongo.mongo_client import MongoClient
import db_secret
#Library needs to be downloaded
#Maybe not needed?
#from parameterized import parameterized
import unittest

client = MongoClient(
    "mongodb+srv://" + db_secret.secret_id + ":"
    + db_secret.secret_key +
    "@cluster0.6se1s.mongodb.net/myFirstDatabase?" +
    "retryWrites=true&w=majority"
    )
db = client['kirjasto-backend']
book_collection = db['books']
user_collection = db['users']
rating_collection = db['ratings']
comment_collection = db['comments']
retrieved_book_collection = list(book_collection.find({}, {'_id': False}))
retrieved_user_collection = list(user_collection.find({}, {'_id': False}))
retrieved_rating_collection = \
    list(rating_collection.find({}, {'_id': False}))
retrieved_comment_collection = \
    list(comment_collection.find({}, {'_id': False}))


#Trying testerdata out
#class TestTesterData(unittest.TestCase):
#    def test_None(self):
#        result = TesterData.get("object_id")
#        assert result == None
#        self.assertEqual(result, None)


#Gives assertion error even though it should pass?
class TestBooks(unittest.TestCase):
    def test_books_get_wrong_object_id(self):
        result = Books.get("Book_ID_thats_not_inside_the_database")
        assert result == "Book is not inside the database!"
        self.assertEqual(result, "Book is not inside the database!")


if __name__ == "__main__":
    unittest.main()
    #TestBooks.test_books_get_wrong_object_id()
