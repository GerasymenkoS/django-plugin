# Django Templarbit package

#Installation guide:
1) Create a typical Django app
2) Take all dependencies from the requirements.txt
3) Add folder with Templarbit package code to the folder with the file manage.py
4) In the Templarbit package's folder, set values and settings in templarbit_settings.py
5) Add python middleware package to Django's MIDDLEWARE list - 'Templarbit.middleware.TemplarbitMiddleware'

#Usage:
1) Add Templarbit middleware package to Django's MIDDLEWARE list
2) Set up settings in templarbit_settings.py