#!/bin/bash

#docker run --name db_flask_app -e POSTGRES_PASSWORD=test -e POSTGRES_USER=test -e POSTGRES_DB=test -p 5432:5432 -d postgres

python {{cookiecutter.app_name}}/manage.py init

