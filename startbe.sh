#!/bin/bash
# My first script

echo "Hello World!"
echo `source /bizopsbe/bizops_be/env/bin/activate`
echo `cd /bizopsbe/bizops_be/web/bizops_backend/`
echo `python manage.py runserver 0.0.0.0:8000`