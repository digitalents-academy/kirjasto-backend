"""rating_system.py: Contains Rating class."""
import uuid
from pymongo.mongo_client import MongoClient
import db_secret

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
retrieved_book_collection = list(book_collection.find({}, {'_id': False}))
retrieved_user_collection = list(user_collection.find({}, {'_id': False}))
retrieved_rating_collection = list(rating_collection.find({}, {'_id': False}))


def get_retrieved_rating_collection():
    """
    Function that returns a dictionary called retrieved_rating_collection
    that contains retrieved rating collection.
    """

    return retrieved_rating_collection


def get_retrieved_ratings_by_username(user_name):
    """Function that returns all of user's ratings."""

    retrieved = list(
        rating_collection.find(
            {'Username': str(user_name)}, {'_id': False}
            )
        )
    if len(retrieved) > 0:
        return retrieved


def get_retrieved_rating_by_username_and_id(user_name, book_id):
    """Function that returns user's ratings on a book."""

    retrieved = list(
        rating_collection.find(
            {
                'Username': user_name,
                'Book_ID': book_id
                }, {'_id': False}
            )
        )
    return retrieved


def has_the_user_already_rated_this_book(user_name, book_id):
    """Function that checks whether a user has already rated the book."""

    #if len(
    #    list(
    #        rating_collection.find(
    #            {
    #                'Username': user_name,
    #                'Book_ID': book_id
    #                }, {'_id': False}
    #            )
    #        )):
    #    return True
    #return False

    for rating in retrieved_rating_collection:
        if rating["Username"] == user_name and \
                rating["Book_ID"] == book_id:
            return True
    return False


#When the link is still open (same)
#the book or user data isn't updated.
def update_rating(rating_id, user_name, book_id, new_rating):
    """Function that posts updated rating data to the database."""

    rating_collection.update(
        {'Rating_ID': rating_id},
        {
            "$set": {
                "Rating_ID": rating_id,
                "Username": user_name,
                "Book_ID": book_id,
                "Rating": int(new_rating)
                }
            }
        )

    update_books_rating_data(book_id)
    update_users_mean_score_data(user_name)


#Needs to be edited
#User's mean score should change after gicing a rating
#Also Books rating score and rating count should change
def give_rating(user_name, book_id, rating):
    """
    Function that posts user's rating data the database.
    If the user has already given a rating,
    the old one will be updated.
    """

    rating_id = uuid.uuid4().hex

    new_rating = {
        "Rating_ID": rating_id,
        "Rating": int(rating),
        "Username": user_name,
        "Book_ID": book_id,
        }

#Update_one?
    if has_the_user_already_rated_this_book(user_name, book_id):
        for retrieved in retrieved_rating_collection:
            if retrieved["Username"] == user_name and \
                    retrieved["Book_ID"] == book_id:
                rating_id = retrieved["Rating_ID"]
            rating_collection.update(
                {'Rating_ID': rating_id},
                {
                    "$set": {
                        "Rating": rating,
                        }
                    }
                )
    else:
        rating_collection.insert_one(new_rating)

    update_books_rating_data(book_id)
    update_users_mean_score_data(user_name)


#rating id could work better here
def delete_rating(user_name, book_id):
    """Function that deletes a rating and updates data after."""

    for rating in retrieved_rating_collection:
        if rating["Username"] == user_name and \
                rating["Book_ID"] == book_id:
            rating_collection.remove(rating)

    for rating in retrieved_rating_collection:
        if rating["Username"] == user_name and \
                rating["Book_ID"] == book_id:
            return "Something went wrong!"

    update_books_rating_data(book_id)
    update_users_mean_score_data(user_name)


def get_books_rating_data(book_id):
    """
    Function that returns single books rating
    and the amount that the book has been rated.
    """

    count = 0
    rating_sum = 0
    for rating in retrieved_rating_collection:
        if rating["Book_ID"] == book_id:
            count += 1
            rating_sum += int(rating["Rating"])
    if rating_sum == 0:
        return (0, 0)
    else:
        return (rating_sum / count, count)


def get_users_mean_score(user_name):
    """
    Function that returns single user's mean score
    and the amount that the user has rated books.
    """

    count = 0
    rating_sum = 0

    for rating in retrieved_rating_collection:
        if rating["Username"] == user_name:
            if rating["Username"]:
                count += 1
                rating_sum += int(rating["Rating"])
    if rating_sum == 0:
        return (0, 0)
    else:
        return (rating_sum / count, count)


def update_books_rating_data(book_id):
    """Function that updates ratings in the dictionary called books."""

    book_collection.update(
        {'Book_ID': book_id},
        {
            "$set": {
                "Rating": float(get_books_rating_data(book_id)[0]),
                "Rating_count": get_books_rating_data(book_id)[1]
                }
            }
        )


#Test this when users are in the right form!
#Thus having Mean count
def update_users_mean_score_data(user_name):
    """Function that updates mean score in the dictionary called users."""

    user_collection.update(
        {'Username': user_name},
        {
            "$set": {
                "Mean_score": float(get_users_mean_score(user_name)[0]),
                "Mean_count": get_users_mean_score(user_name)[1]
                }
            }
        )
