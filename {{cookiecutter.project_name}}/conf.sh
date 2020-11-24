#!/bin/bash

if [ -d ".venv" ]
then
    . venv/bin/activate
    pip install -r requirements.txt
    python3 run.py
else
    python3 -m venv .venv
    . venv/bin/activate
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    python3 run.py
fi

#docker run --name db_flask_app -e POSTGRES_PASSWORD=test -e POSTGRES_USER=test -e POSTGRES_DB=test -p 5432:5432 -d postgres
#flask db init
#flask db upgrade
#flask db migrate
#flask db upgrade
