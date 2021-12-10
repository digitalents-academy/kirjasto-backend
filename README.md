# kirjasto-backend 📚

## Description
This is the backend repo for the Digitalents Academy Library Application 📚 Kirjasto is a Digitalents Academy project made by the workshop interns in collaboration. The main repositiory for the project is at [digitalents-academy/kirjasto](https://github.com/digitalents-academy/kirjasto)

## Authors
Boris Hiltunen ([BorisHiltunen](https://github.com/BorisHiltunen))

Siim Laineste ([shiimu](https://github.com/shiimu))

Sakhi Hashmat ([Sakhi97](https://github.com/Sakhi97))

## Tools and Libraries
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [MongoDB](https://www.mongodb.com/)
- [flask-restful](https://flask-restful.readthedocs.io/en/latest/)
- You can find required packets from Requirements.txt
- Python 3.9

## Setup
- pip install -r Requirements.txt

## Api endpoints:

```html 
localhost:8000/api/
```

<b>GET</b>
  - **/status**
    ```python 
    Returns every book's status
    ```
  - **/status/id**
    ```python 
    Returns book information by book id
    ```
  - **/books**
    ```python 
    Returns every book's information
    ```
  - **/comments**
    ```python 
    Returns all comments
    ```
  - **/comments/id**
    ```python 
    Returns Comments by book id
    ```
    
<b>POST</b>
  - **/loan**
    ```python 
    Updates book's loan status (True or False)
    ```
  - **/comment**
    ```python 
    Posts one comment
    ```
<b>Delete</b>
  - **/comments/d/id**
    ```python 
    Delete comment by comment id
    ```
    
<b>To do</b>
- Authentication/Login/Userid + password
- Authentication/Logout/Userid + password
- Rating </br>
-> Posts one rating

## Items

Stories, comments, jobs, Ask HNs and even polls are just items. They're identified by their ids, which are unique integers, and live under `/v0/item/<id>`.

All items have some of the following properties, with required properties in bold:

### Books

Field | Description
------|------------
**id** | The item's unique id.
book_ID | The item's unique id.
name | Name of the book.
writer | Name of the author.
year | Publication date.
isbn | International Standard Book Number.
rating | Books rating.
about | What the book is about.
tags | Descriptive keywords you can add to help users find similar books.
description | Description of the book.
loan_status | True or False value of the loan_status.
loaner | User which has loaned the book.
rating_count | How many times people have rated the book.
rating_score | Sum of all the ratings.

For example: https://hacker-news.firebaseio.com/v0/item/8863.json?print=pretty

```javascript
    {
        "Book ID": "7",
        "Name": "Web security for developers",
        "Writer": "Malcolm MCDonald",
        "Year": "2020",
        "ISBN": "978-1-59327-994-3",
        "Rating": 4,
        "About": "Networking & Cloud Computing",
        "Tags": "tags",
        "Description": "ksl",
        "Loan Status": "False",
        "Loaner": "None",
        "Rating Count": "3",
        "Rating Score": "11"
    }
```

### Comments

Field | Description
------|------------
**id** | The item's unique id.
book_ID | The item's unique id.
comment | body of user message.
comment_ID | The item's unique id.
user_ID | The item's unique id.

For example: https://hacker-news.firebaseio.com/v0/item/8863.json?print=pretty

```javascript
{
    "Book ID": "7",
    "Comment": "I really love books",
    "Comment ID": "1",
    "User ID": "3000"
}
```

### Users

Field | Description
------|------------
**id** | The item's unique id.
user_ID | The item's unique id.
user_name | The item's unique name.


For example: https://hacker-news.firebaseio.com/v0/item/8863.json?print=pretty

```javascript
{
  "by" : "dhouston",
  "descendants" : 71,
  "id" : 8863,
  "kids" : [ 8952, 9224, 8917, 8884, 8887, 8943, 8869, 8958, 9005, 9671, 8940, 9067, 8908, 9055, 8865, 8881, 8872, 8873, 8955, 10403, 8903, 8928, 9125, 8998, 8901, 8902, 8907, 8894, 8878, 8870, 8980, 8934, 8876 ],
  "score" : 111,
  "time" : 1175714200,
  "title" : "My YC app: Dropbox - Throw away your USB drive",
  "type" : "story",
  "url" : "http://www.getdropbox.com/u/2/screencast.html"
}
```
