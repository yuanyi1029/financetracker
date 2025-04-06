# CS50W Finance Tracker

![Project Image](https://imgur.com/TmvFxJo.png)
#### Video Demo: https://youtu.be/Y7p4wvrOxyo

## 💬 Description
My capstone project for the CS50W course, which was my first ever web application in my computer science journey. The Finance Tracker application was made using Django as a backend framework with a simple SQLite database, along with vanilla HTML, CSS and JavaScript for the frontend. 

## 🚀 Setting Up Locally 
Step 1: Install project dependencies. 
```
pip install -r requirements.txt
```
Step 2: Create and apply database migrations.
```
python manage.py makemigrations
python manage.py migrate
``` 
Step 3: Create a superuser (Optional).
```
python manage.py createsuperuser
```
Step 4: Launch the Django server.
```
python manage.py runserver
```