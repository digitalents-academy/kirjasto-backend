import unittest
from pymongo.mongo_client import MongoClient
from books import (
    get_books,
    get_book_by_book_id,
    add_new_book,
    update_book,
    loan_book_by_username_and_book_id,
    delete_book_by_book_id
    )
from comments import (
    get_comments,
    get_comments_by_book_id,
    post_comment,
    update_comment,
    delete_comments_by_comment_id
    )
from rating_system import (
    get_ratings,
    get_ratings_by_username,
    get_ratings_by_username_and_book_id,
    has_the_user_already_rated_this_book, give_rating,
    update_rating,
    delete_rating,
    get_books_rating_data,
    get_users_mean_score_data,
    update_books_rating_data,
    update_users_mean_score_data
    )
from users import (
    get_users,
    get_user_by_username,
    get_user_by_object_id,
    update_user,
    delete_user_by_object_id
    )
from app import (
    TesterData, BooksGet, BooksAddNewBook, BooksDeleteByBookID,
    BooksLoanByUsernameAndBookID, BooksUpdateBook, CommentsGet,
    CommentsAddNewComment, CommentsDelete, RatingsGet,
    RatingsAddNewRating, RatingsDeleteByUsernameAndBookID,
    UsersGet, UsersDeleteByObjectID, UsersUpdateUser
    )

import db_secret
#Library needs to be downloaded
#Maybe not needed?
#from parameterized import parameterized

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


class TestApp(unittest.TestCase):
    def test_Books(self):
        pass


# Maybe not needed
class TestBooks(unittest.TestCase):
    def test_get_books(self):
        result = get_books()
        if result == "Something went wrong!":
            raise AssertionError(
                "There doesn't seem to be any books inside the database!"
                )

    def test_get_books_by_id(self):
        result = get_book_by_book_id("Book_ID_thats_not_inside_the_database")
        self.assertEqual(result, "Book is not inside the database!")

    def test_add_new_book(self):
        pass
        #self.assertEqual(
        #    result,
        #    "Book is not inside the database!",
        #    "Book is not inside the database!"
        #    )
        #self.assertEqual(result, expected, error)


class TestComments(unittest.TestCase):
    def test_get_comments(self):
        result = get_comments()
        if result == "Something went wrong!":
            raise AssertionError(
                "There doesn't seem to be any comments inside the database!"
                )

    def test_get_comments_by_book_id(self):
        result = get_comments_by_book_id(
            "Book_ID_thats_not_inside_the_database"
            )
        self.assertEqual(result, "error: Not a valid book id!")


#Editing this
class TestRatingSystem(unittest.TestCase):
    def test_get_ratings(self):
        result = get_ratings()
        if result == "Something went wrong!":
            raise AssertionError(
                "There doesn't seem to be any comments inside the database!"
                )

    def test_get_comments_by_book_id(self):
        result = get_comments_by_book_id(
            "Book_ID_thats_not_inside_the_database"
            )
        self.assertEqual(result, "error: Not a valid book id!")


if __name__ == "__main__":
    unittest.main()
    #TestBooks.test_books_get_wrong_object_id()
