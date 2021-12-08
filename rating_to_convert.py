#Importing necessary modules
import json

class Rating:

    #Initializing necessary attributes
    def __init__(self):
        self.Mean_score = {}
        self.Book_score = {}

    #Function that is responsible for the correct way of giving books and mean_score's ratings
    def give_rating(self, book_name, user_name: str, number: int):
        if self.is_book_in_file(book_name) == True:
            if book_name not in self.Book_score:
                self.Book_score[book_name] = []
            if user_name not in self.Mean_score:
                self.Mean_score[user_name] = []

            self.Book_score[book_name].append({user_name : number})
            self.Mean_score[user_name].append({book_name : number})
        else:
            print("Book is not in the file or the username is not correct")

    #Function responsible in assessing overall book rating
    def assess_overall_book_ratings(self):
        average = 0
        sum = 0
        for i in self.Book_score:
            for e in self.Book_score[i]:
                if len(self.Book_score[i]) > 0:
                    for key in e:
                        sum += e[key]

        if len(self.Book_score) > 0:
            average = sum / len(self.Book_score)
            return f"Overall book rating: {average}"
        else:
            return 0

    #Function responsible in assessing chosen books rating
    def assess_book_rating(self, book_name):
        average = 0
        sum = 0
        count = 0
        for i in self.Book_score:
            if i == book_name:
                count += 1
                for e in self.Book_score[i]:
                    if len(self.Book_score[i]) > 0:
                        for key in e:
                            sum += e[key]
        if count > 0:
            average = sum / count
            return f"{book_name}: {average}"
        else:
            return 0

    #Function responsible in assessing overall mean_score rating
    def assess_overall_mean_score(self):
        average = 0
        sum = 0
        for i in self.Mean_score:
            for e in self.Mean_score[i]:
                if len(self.Mean_score[i]) > 0:
                    for key in e:
                        sum += e[key]
        if len(self.Mean_score) > 0:
            average = sum / len(self.Mean_score)
            return f"Overall meanscore: {average}"
        else:
            return 0
    
    #Function responsible in assessing chosen persons mean_score rating
    def assess_mean_rating(self, user_name):
        average = 0
        sum = 0
        count = 0
        for i in self.Mean_score:
            if i == user_name:
                count += 1
                for e in self.Mean_score[i]:
                    if len(self.Mean_score[i]) > 0:
                        for key in e:
                            sum += e[key]
        if count > 0:
            average = sum / count
            return f"{user_name}: {average}"
        else:
            return 0

    #Function that checks whether a book is in a file called test2.json
    def is_book_in_file(self, book):
        list = []
        with open("test2.json") as datafile:
            data = datafile.read()
        Information = json.loads(data)
        for i in Information:
            list.append(i["Name"])
        if book in list:
            return True
        else:
            return False

    #Function that sends data to a file
    def set_data(self, file, data):
        with open(file, "w") as datafile:
            json.dump(data, datafile, sort_keys=True, indent=4)

    #Function that gets data from a file
    def get_data_from_file(self, file):
        with open(file) as datafile:
            data = datafile.read()
        Information = json.loads(data)
        return Information

    #Function that updates book and mean -score dictionarys situated in the class
    def update_scores_with_file(self, file):
        with open(file) as datafile:
            data = datafile.read()
        Information = json.loads(data)
        for i in Information:
            self.give_rating(i["Book_name"], i["Name"], i["Rating"])
    
    #Function that returns a dictionary called self.Mean_score
    def get_mean_info(self):
        return self.Mean_score

    #Function that returns a dictionary called self.Book_score
    def get_book_info(self):
        return self.Book_score
