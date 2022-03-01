# kirjasto-backend 📚

## Description
This is the backend repo for the Digitalents Academy Library Application 📚 Kirjasto is a Digitalents Academy project made by the workshop interns in collaboration. The main repository for the project is at [digitalents-academy/kirjasto](https://github.com/digitalents-academy/kirjasto).

## Authors
Boris Hiltunen ([BorisHiltunen](https://github.com/BorisHiltunen))

Siim Laineste ([shiimu](https://github.com/shiimu))

Sakhi Hashmat ([Sakhi97](https://github.com/Sakhi97))

Roman Klemiato ([SweetCinnamonBun](https://github.com/SweetCinnamonBun))

## Tools and Libraries
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [MongoDB](https://www.mongodb.com/)
- [flask-restful](https://flask-restful.readthedocs.io/en/latest/)
- You can find required packets from requirements.txt
- Python 3.9

## Setup
- pip install -r requirements.txt

## Api endpoints:

```html 
localhost:5000/api/
```

<b>GET</b>
  - **/books**
    ```python 
    Returns every book's data
    ```
  - **/books/book_id**
    ```python 
    Returns book data by book id
    ```
  - **/comments**
    ```python 
    Returns all comments
    ```
  - **/comments/book_id**
    ```python 
    Returns comments by book id
    ```
  - **/ratings**
    ```python 
    Returns every rating's data
    ```
  - **/ratings/user_name**
    ```python 
    Returns rating data by username
    ```
  - **/ratings/user_name/book_id**
    ```python 
    Returns rating data by username and book id
    ```
  - **/users**
    ```python 
    Returns every users's data
    ```
  - **/users/user_name**
    ```python 
    Returns user data by username
    ```
  - **/users/user_name/object_id**
    ```python 
    Returns user data by object id
    ```
    
<b>POST</b>
  - **/books/add**
    ```python 
    Posts new book to the books collection inside the database
    ```
  - **/comments/add**
    ```python 
    Posts new comment to the comments collection inside the database
    ```
  - **/ratings/add**
    ```python 
    Posts new rating to the ratings collection inside the database
    ```
  - **/user/signup**
    ```python 
    Posts new user to the users collection inside the database
    ```
  - **/authentication/login**
    ```python 
    Posts user data 
    ```
    
<b>PUT</b>
  - **/books/update**
    ```python 
    Updates book data inside the database with book id
    ```
  - **/comments/update**
    ```python 
    Updates comment data inside the database with comment id
    ```
  - **/ratings/update**
    ```python 
    Updates rating data inside the database with rating id
    ```
  - **/users/update**
    ```python 
    Updates user data inside the database with object id
    ```
    
<b>Delete</b>
  - **/books/d**
    ```python 
    Deletes a book from the database with book id
    ```
  - **/comments/d**
    ```python 
    Deletes a comment from the database with comment id
    ```
  - **/ratings/d**
    ```python 
    Deletes a rating from the database with rating id
    ```
  - **/users/d**
    ```python 
    Deletes a user from the database with object id
    ```

## Items

Stories, comments, jobs, Ask HNs and even polls are just items. They're identified by their ids, which are unique integers, and live under `/v0/item/<id>`.

All items have some of the following properties, with required properties in bold:

### Books

Field | Description
------|------------
**id** | The item's unique id.
Book_ID | The item's unique id.
Name | Name of the book.
Writer | Name of the author.
Year | Publication date.
ISBN | International Standard Book Number.
Rating | Books rating.
Rating_count | Books rating count.
About | What the book is about.
Tags | Descriptive keywords you can add to help users find similar books.
Description | Description of the book.
Loan_Status | True or False value of the loan_status.
Loaner | User which has loaned the book.

For example: localhost:5000/api/books/5b5b085cb60c48e28d304f3794ee9c15

```javascript
[
    {
        "Book_ID": "5b5b085cb60c48e28d304f3794ee9c15",
        "Name": "Eloquent JavaScript",
        "Writer": "Marjin Haverbeke",
        "Year": 2018,
        "ISBN": "978-1-59327-950-9",
        "Rating": 0,
        "Rating_count": 0,
        "About": "Programming(JavaScript)",
        "Tags": "tags",
        "Description": "ksl",
        "Loaner": null,
        "Loan_Status": false
    }
]
```

### Comments

Field | Description
------|------------
**id** | The item's unique id.
Book_ID | The item's unique id.
Username | The item's unique username.
Comment_ID | The item's unique id.
Comment | body of user message.

For example: localhost:5000/api/comments/8e1d8750ca0a472c81ed09cfe73c76bd

```javascript
[
    {
        "Book_ID": "8e1d8750ca0a472c81ed09cfe73c76bd",
        "Username": "test",
        "Comment_ID": "5b62d22a40db4cdaa650fafb1c7d6542",
        "Comment": "hello"
    }
]
```

### Ratings

Field | Description
------|------------
**id** | The item's unique id.
Rating_ID | The item's unique id.
Username | The item's unique username.
Book_ID | The item's unique id.
Rating | The item's rating.

For example: localhost:5000/api/ratings/test5

```javascript
[
    {
        "Rating_ID": "2996a284656b4ad7b9b9afb3d5e1436a",
        "Username": "test5",
        "Book_ID": "4ddf7b708df14cdd9d3df5193e839722",
        "Rating": 3.0
    }
]
```

### Users

Field | Description
------|------------
**id** | The item's unique id.
Username | The item's unique name.
Email | The item's unique email.
Password | The item's unique hashed password.
Mean_score | The item's mean score.
Mean_count | The item's mean count.
Token | The item's token.


For example: localhost:5000/api/users/test5

```javascript
[
    {
        "_id": "2701a485794542069dfbd31272f1a7ba",
        "Username": "test",
        "Email": "test@gmail.com",
        "Mean_count": 0,
        "Mean_score": 0,
        "token": "No token"
    }
]
