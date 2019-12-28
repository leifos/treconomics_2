#!/bin/bash

if [ "$1" != "keepdata" ]; then
    echo "Just a sanity check."
    echo "This script will delete the log and database."
    read -p "ARE YOU ABSOLUTELY SURE YOU WANT TO DO THIS? [Y/N]" -n 1 -r
    echo

    if [[ $REPLY =~ ^[Nn]$ ]]; then
        exit 1
    fi
fi

if [ "$1" != "keepdata" ]; then
    rm treconomics.db
    rm experiment.log

    rm survey/migrations/*
    rm survey/migrations/__pycache__/*
    rm treconomics/migrations/*
    rm treconomics/migrations/__pycache__/*

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