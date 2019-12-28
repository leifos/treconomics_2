#!/bin/bash

if [ "$1" != "keepdata" ]; then
    rm treconomics.db
    rm experiment.log
fi

rm survey/migrations/*
rm survey/migrations/__pycache__/*
rm treconomics/migrations/*
rm treconomics/migrations/__pycache__/*

if [ "$1" != "keepdata" ]; then
    python manage.py makemigrations
    python manage.py makemigrations treconomics
    python manage.py makemigrations survey
    python manage.py migrate
    python manage.py migrate treconomics
    python manage.py migrate survey
    python manage.py createsuperuser
    python populate_treconomics_db.py
    python populate_ads.py
    python populate_users.py
fi