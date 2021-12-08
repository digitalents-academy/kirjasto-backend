# kirjasto-backend 📚

# Description
This is the backend repo for the Digitalents Academy Library Application 📚 Kirjasto is a Digitalents Academy project made by the workshop interns in collaboration. The main repositiory for the project is at [digitalents-academy/kirjasto](https://github.com/digitalents-academy/kirjasto)

# Authors
Boris Hiltunen ([BorisHiltunen](https://github.com/BorisHiltunen))

Siim Laineste ([shiimu](https://github.com/shiimu))

Sakhi Hashmat ([Sakhi97](https://github.com/Sakhi97))

# Tools and Libraries
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [MongoDB](https://www.mongodb.com/)
- [flask-restful](https://flask-restful.readthedocs.io/en/latest/)
- Requests.txt

# Setup

<b>Requirements</b>
- Flask
- Mongodp
- Git clone
- Requests.txt

# Api endpoints:

Localhost:8000/api/

<b>GET</b>
- Status </br>
Returns every book's status
- Status/id </br>
Returns book information by book id
- Books </br>
Returns every book's information
- Comments </br>
Returns all comments
- Comments/id </br>
Returns Comment by book id
- Authentication/Login/Userid + password
- Authentication/Logout/Userid + password

<b>POST</b>
- Loan </br>
Updates book's loan status (True or False)
- Comment </br>
Posts one comment
- Rating </br>
Posts one rating

<b>Delete</b>
- Comments </br>
Delete comment by comment id
