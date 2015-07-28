#!/bin/bash

echo "-> Install requirements:"
pip install -r requirements-dev.txt

echo "-> Remove database:"
rm db.sqlite3

echo "-> Run migration:"
python manage.py migrate --noinput

echo "-> Generate sample data:"
python manage.py sample_data

echo "-> Build frontend assets:"

echo "--> Node install:"
cd junction/static/
npm install

echo "-_> Bower install:"
bower install

echo "--> Run Grunt:"
grunt less

cd -
echo "You can keep running grunt for compiling less files, by running 'grunt' inside 'junction/static' directory"
