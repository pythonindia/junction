#!/bin/bash

echo "-> Remove database:"
rm db.sqlite3

echo "-> Run migration:"
python manage.py migrate --noinput

echo "-> Generate sample data:"
python manage.py sample_data

echo "-> Some frontend changes"

echo "-> Node install:"
cd junction/static/
npm install

echo "-> Bower install:"
bower install

echo "-> Grunt:"
grunt less

cd -
echo "You can keep running grunt for compiling less files, by running grunt inside static directory"
