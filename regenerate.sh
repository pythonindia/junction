#!/bin/bash

echo "-> Remove database"
rm db.sqlite3

echo "-> Run migration"
python manage.py migrate --noinput

echo "-> Generate sample data"
python manage.py sample_data
