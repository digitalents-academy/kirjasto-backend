"""new_rating_system.py: Contains RatingSystem class."""

import json


class RatingSystem:
    """
    Class that contain functions
    that are necessary to make rating system work as intended.
    """

    def __init__(self):
        self.books = []
        self.users = []
        self.user_ratings = []

    def update_books_dictionary(self):
        """Function that updates dictionary called books."""

        self.books = self.get_data_from_file("book_data.json")

    def update_users_dictionary(self):
        """Function that updates dictionary called users."""

        self.users = self.get_data_from_file("users.json")

    def update_user_ratings_dictionary(self):
        """Function that updates dictionary called user_ratings."""

        self.user_ratings = self.get_data_from_file("user_ratings.json")

    def get_books_rating_data(self, book_id):
        """
        Function that returns single books rating
        and the amount that the book has been rated.
        """

        count = 0
        rating_sum = 0
        for rating in self.user_ratings:
            if rating["Book ID"] == book_id:
                if rating["Book ID"]:
                    count += 1
                    rating_sum += int(rating["Rating"])
        if rating_sum == 0:
            return (0, 0)
        else:
            return (rating_sum / count, count)

    def get_users_mean_score(self, user_id):
        """
        Function that returns single user's mean score
        and the amount that the user has rated books.
        """

        count = 0
        rating_sum = 0
        for rating in self.user_ratings:
            if rating["User ID"] == user_id:
                if rating["User ID"]:
                    count += 1
                    rating_sum += int(rating["Rating"])
        if rating_sum == 0:
            return (0, 0)
        else:
            return (rating_sum / count, count)

    def update_books_dictionary_ratings(self):
        """Function that updates ratings in the dictionary called books."""

        for rating in self.books:
            book_id = rating["Book ID"]
            rating["Rating"] = (
                f"{self.get_books_rating_data(book_id)[0]} "
                f"out of 5 ({self.get_books_rating_data(book_id)[1]} "
                f"ratings)"
                )

    def update_users_dictionary_rating(self):
        """Function that updates mean score in the dictionary called users."""

        for score in self.books:
            user_id = score["User ID"]
            score["Mean_score"] = (
                f"{self.get_users_mean_score(user_id)[0]} "
                f"out of 5 ({self.get_users_mean_score(user_id)[1]} "
                f"ratings)"
                )

    def set_data(self, file, data):
        """Function that sends data to a file."""

        with open(file, "w", encoding="utf8") as datafile:
            json.dump(data, datafile, sort_keys=False, indent=4)

    def get_data_from_file(self, file):
        """Function that gets data from a file."""

        with open(file, encoding="utf8") as datafile:
            data = datafile.read()
        information = json.loads(data)

        return information

    def give_rating(self, oid: str, user_id: str, book_id: str, rating: str):
        """
        Function that saves user's rating,
        oid, user id, rated book's id and rating
        to a list called self.user_ratings.
        """

        new_rating = {
            "_id": {
                "$oid": oid
                },
            "User ID": user_id,
            "Book ID": book_id,
            "Rating": rating
            }

        self.user_ratings.append(new_rating)


if __name__ == "__main__":

    rating_system = RatingSystem()

    user_ratings_dictionary = rating_system.get_data_from_file(
        "user_ratings.json"
        )

    # Updating application's dictionarys
    rating_system.update_books_dictionary()
    rating_system.update_users_dictionary()
    rating_system.update_user_ratings_dictionary()
    rating_system.update_books_dictionary_ratings()

    # Giving ratings
    rating_system.give_rating(
        user_ratings_dictionary[0]["_id"]["$oid"],
        user_ratings_dictionary[0]["User ID"],
        user_ratings_dictionary[0]["Book ID"],
        user_ratings_dictionary[0]["Rating"]
        )
    rating_system.give_rating(
        user_ratings_dictionary[0]["_id"]["$oid"],
        user_ratings_dictionary[0]["User ID"],
        user_ratings_dictionary[0]["Book ID"],
        user_ratings_dictionary[0]["Rating"]
        )
    rating_system.give_rating(
        user_ratings_dictionary[0]["_id"]["$oid"],
        user_ratings_dictionary[0]["User ID"],
        user_ratings_dictionary[0]["Book ID"],
        user_ratings_dictionary[0]["Rating"]
        )
    rating_system.give_rating(
        user_ratings_dictionary[0]["_id"]["$oid"],
        user_ratings_dictionary[0]["User ID"],
        user_ratings_dictionary[0]["Book ID"],
        user_ratings_dictionary[0]["Rating"]
        )

    # Updating files
    rating_system.set_data("user_ratings.json", rating_system.user_ratings)
    rating_system.set_data("book_data.json", rating_system.books)
