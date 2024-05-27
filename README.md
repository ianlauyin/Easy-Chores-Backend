### Introduction

This is the backend part for project Easy Chores
For the ios app for Easy Chores, please visit [https://github.com/ianlauyin/easy-chores-ios](https://github.com/ianlauyin/easy-chores-ios)

### What does this backend server do

This backend server is mulitple API Endpoints for client to access the easy-chores database.

##ERD
[Easy-Chores-ERD](https://drawsql.app/teams/ianlau/diagrams/easy-chores)


### Requirement

Pyhton and pip

All the required package is in requirement.txt

Use this command to install all the required package

```
pip install -r requirements. txt
```

### How to run

First you need to have a postgreSQL Database

Include your database config in your .env

Then use this command to migrate the database

```
python3 manage.py migrate
```

Use this command to start the server

```
python manage.py runserver
```

### Enviroment variable

You need these in your .env for django setting.py
SECRET_KEY
DEBUG
ALLOWED_HOSTS

You need these in your .env for postgreSQL database
DB_NAME
DB_USER
DB_HOST
DB_PORT

You need this in your .env for authentication token generation
TOKEN_SECRET
