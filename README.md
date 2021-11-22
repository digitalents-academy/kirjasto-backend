# kirjasto-backend 📚

# Description
This is the backend repo for the Digitalents Academy Library Application 📚 Kirjasto is a Digitalents Academy project made by the workshop interns in collaboration. The main repositiory for the project is at [digitalents-academy/kirjasto](https://github.com/digitalents-academy/kirjasto)

# Authors
Boris ([BorisHiltunen](https://github.com/BorisHiltunen))

Siim ([shiimu](https://github.com/shiimu))

# Tools and Libraries
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [MongoDB](https://www.mongodb.com/)
- [flask-restful](https://flask-restful.readthedocs.io/en/latest/)

# Setup

<b>Requirements</b>
- Flask
- Mongodp
- Git clone
- 

# Api endpoints:

Localhost:8000/

In use

<b>GET</b>
- Status </br>
Returns every book's status
- Status/id </br>
Returns book information by book id
- Books </br>
Returns every book's information

<b>POST</b>
- Loan </br>
Updates book's loan status (True or False)

To do

<b>GET</b>
- Comments </br>
Returns all comments
- Comments/id </br>
Returns Comment by book id
- Status/id </br>
Returns book information by book id

<b>POST</b>
- Comment </br>
Posts one comment

<b>Delete</b>
- Comments </br>
Delete comment by comment id
