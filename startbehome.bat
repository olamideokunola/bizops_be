@ECHO OFF
:: This file runs the backend server for Burecs
workon sales_backend & cd web\bizops_backend\ & py manage.py runserver 192.168.1.105:8000