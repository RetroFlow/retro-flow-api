#!/usr/bin/env bash

python manage.py migrate authentication
python manage.py migrate board 0001_initial
python manage.py create_defaults
python manage.py migrate
