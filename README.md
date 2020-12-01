# Cookiecutter Flask All-In-One

A Flask template that uses cookiecutter. (Supports Python ≥ 3.6)

![Python](https://img.shields.io/badge/Python-v^3.7-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![Flask](https://img.shields.io/badge/Flask-v1.1.2-blue.svg?longCache=true&logo=flask&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Flask-SQLAlchemy](https://img.shields.io/badge/Flask--SQLAlchemy-2.4.1-red.svg?longCache=true&style=flat-square&logo=flask&logoColor=white&colorA=4c566a&colorB=5e81ac)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&colorB=a3be8c)

<p>
  <img src="{{cookiecutter.project_name}}/{{cookiecutter.app_name}}/static/img/cookiecutter.png" alt="Sublime's custom image"/>
</p>

## Introduction

Cookiecutter-Flask-All-In-One is an easy tool that allows you to quickly create a flask project.
It allows you to easily launch a REST API using JWT authentication tokens, to use GragphQl or just the user interface with the possibility to authenticate with Google, Facebook etc.

## Use it now

First of all you need to install [cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/) 
Launch `pip install cookiecutter`

Once cookiecutter installed, run this command to create the project
```
cookiecutter https://github.com/gregadc/cookiecutter-flask-all-in-one.git
```

You have the possibility to change the values of the cookiecutter.json file in order to change the name of the project, the name of the application, or whatever you want want and relaunch the command
```json
{
    "project_name": "cookiecutter-flask-all-in-one",
    "app_name": "myapp",
    "python_version": ["3.8", "3.6", "3.7"],
    "full_name": "admin",
    "email": "admin@gmail.com",
    "password": "admin",
    "debug": [0, 1],
    "_copy_without_render": [
        "{{cookiecutter.project_name}}/app/templates/*.html",
        "*.html"
    ]
}
```

Once the project is created
```bash

cd cookiecutter-flask-all-in-one
pip install -r requirements.txt
pip install -e .

```
The database to use is postgres but you can change the DATABASE_URI of the .env if you want to use another one
If you don't have postgres and you are comfortable with docker run this command it will create a docker postgres container for you

```bash
docker run --name db_flask_app -e POSTGRES_PASSWORD=test -e POSTGRES_USER=test -e POSTGRES_DB=test -p 5432:5432 -d postgres
```

Run this command to create the database and create a user
`myapp init`

You can if you wish to change the `myapp/.env` which contains the default configuration of the project.

```
SECRET_KEY="secret" 
FLASK_APP="wsgi.py"
APP_NAME=myapp
EMAIL="admin@gmail.com"
PASSWORD_EMAIL="password"
FLASK_ENV="development"
DATABASE_URI="postgres://test:test@localhost/test"

# Facebook credentials
FACEBOOK_OAUTH_CLIENT_ID="id"
FACEBOOK_OAUTH_CLIENT_SECRET="secret-id"

# Twitter credentials
TWITTER_OAUTH_API_KEY="id"
TWITTER_OAUTH_API_SECRET="secret-id"

# Google credentials
GOOGLE_OAUTH_CLIENT_ID="id"
GOOGLE_OAUTH_CLIENT_SECRET="secret-id"
```

## Run project

```bash
(venv-kaCAdD68-py3.8) test@test:~/cookiecutter-flask-all-in-one-test$ myapp run
 * Serving Flask app "wsgi.py"
 * Environment: development
 * Debug mode: off
[2020-11-26 20:18:34,913: INFO | werkzeug]  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

We have multiple ways to use this project.

### User interface

Open a browser, and enter the url which provides a graphical interface and a basic authentication service, but also the possibility of using the google, facebook services if you have entered the necessary credentials

<p align="center">
  <img src="{{cookiecutter.project_name}}/{{cookiecutter.app_name}}/static/img/auth.png" alt=""/>
</p>

If you use Google, Facebook, or Twitter not forget to create a development application with these providers.
Here are the redirect urls you need to provide to your applications
```bash
http://localhost:5000/login/google/authorized
http://localhost:5000/login/twitter/authorized
etc ...
```
If you want to use other providers like github or linkedin look at [flask-dance](https://flask-dance.readthedocs.io/en/latest/) which allowed to implement these services.

### REST api

You can use the rest api, and his authentication using Flask-JWT-Extended including access token and refresh token management
A first call to the API will return the tokens to you
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}' http://localhost:5000/api/login

{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDY0MjQzOTAsIm5iZiI6MTYwNjQyNDM5MCwianRpIjoiYWU3ZjdiZjctMjkzYS00OTcwLThlNGYtNjMwNGY4MGExYjZhIiwiZXhwIjoxNjA2NDI1MjkwLCJpZGVudGl0eSI6InRvdG8iLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.Dbly2Mln9cD6olEMnoCxvoJ1rUGdjQgP6ekGJY5sOXw"
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDY0MjQ0NTgsIm5iZiI6MTYwNjQyNDQ1OCwianRpIjoiN2MyZGY2ZjAtZDZhZC00ZTI4LTk0NTktMDMyYzkwMDFkODI3IiwiZXhwIjoxNjA5MDE2NDU4LCJpZGVudGl0eSI6InRvdG8iLCJ0eXBlIjoicmVmcmVzaCJ9.IkQ93fdjH-w3veiVOZf92fTPbkrLXwXp37I5uBCgIYU"
}
```
Once the tokens have been recovered you can now use the API to consult the resources

```bash
export ACCESS="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDY0MjQzOTAsIm5iZiI6MTYwNjQyNDM5MCwianRpIjoiYWU3ZjdiZjctMjkzYS00OTcwLThlNGYtNjMwNGY4MGExYjZhIiwiZXhwIjoxNjA2NDI1MjkwLCJpZGVudGl0eSI6InRvdG8iLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.Dbly2Mln9cD6olEMnoCxvoJ1rUGdjQgP6ekGJY5sOXw"
curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer $ACCESS http://localhost:5000/api/users
```

You can also refresh the token
```bash
export REFRESH="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDY0MjQ0NTgsIm5iZiI6MTYwNjQyNDQ1OCwianRpIjoiN2MyZGY2ZjAtZDZhZC00ZTI4LTk0NTktMDMyYzkwMDFkODI3IiwiZXhwIjoxNjA5MDE2NDU4LCJpZGVudGl0eSI6InRvdG8iLCJ0eXBlIjoicmVmcmVzaCJ9.IkQ93fdjH-w3veiVOZf92fTPbkrLXwXp37I5uBCgIYU"
curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer $REFRESH http://localhost:5000/api/refresh

{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDY0MjUzNjUsIm5iZiI6MTYwNjQyNTM2NSwianRpIjoiZmQ3Y2RiMmYtZTZlZC00NDdmLTg3ZWItNzg2ZTc1ZGY0NzYzIiwiZXhwIjoxNjA2NDI2MjY1LCJpZGVudGl0eSI6InRvdG8iLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.hLrksk8nKrqY4wED1QYOGjIXhR-Rq7Zf_TalhPsJ-sI"
}
```

You can list your tokens and revoke them if you want
```bash
curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer $NEW_ACCESS http://localhost:5000/api/tokens
```
This endpoint will return the tokens with their id so that you can revoke them
```bash
curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer $NEW_ACCESS http://localhost:5000/api/revoke_token/<token_id>

{
    "message": "token revoked"
}
```

### GraphQl

You also have the possibility of viewing GraphQl resources if you are connected, launch `http://0.0.0.0:5000/graphql` in your browser

Used packages :

* [Graphene](https://docs.graphene-python.org/en/latest/)
* [Flask-GraphQL](https://github.com/graphql-python/flask-graphql)
* [graphene-sqlalchemy](https://readthedocs.org/projects/graphene-sqlalchemy/)

<p align="center">
  <img src="{{cookiecutter.project_name}}/{{cookiecutter.app_name}}/static/img/graph.png" alt=""/>
</p>

## Docker deploy

In progress
