# CS50W Finance Tracker
#### Video Demo: https://youtu.be/Y7p4wvrOxyo

This is my capstone project for CS50W. Finance Tracker is a simple web application built for users to document their financial activity as well as further understand their own spending habits and financial activity. 

This web application is implemented with Django as a backend framework while programming and markup languages such as HTML, CSS and Javascript were used to implement the front end. Furthermore, a SQLite database consisting of 3 Django models (User, Record, Planned) was used to keep track of users, financial records and planned payments respectively. Lastly, this web application was designed to be mobile responsive using Bootstrap. 

## Distinctiveness and Complexity
The idea for this project stemmed from receiving red envelopes from my relatives during the Lunar New Year because I thought it would be much easier to document my earnings on a computer :money_mouth_face:. From there, the idea spiralled into documenting not only my red envelope earnings, but my expenses as well as to get an insight on my own spending habits. 

During the development of this web application, not only had I used all the programming and markup languages as well as skills learned during this course (Python, Django, CSS, Javascript), I had also done plenty of research and explored  with new technical fields from implementing data charts with Chart.js to implementing the smallest user interface details and mobile responsiveness with bootstrap. As a result, I am proud to have been able to improve on my previously learned skills from this course as well as pick up some new ones along the way.

Furthermore, I also believe that my project is unique compared to other projects done in this course (Google search, Wikipedia, Auction, Mail, Network) because it provides a personalised solution for me to manage my finances. Also, this web application both retrieves and analyses financial data for users, which is something highly relevant and useful for people of all ages, making it unique from previous projects and also untapped with potential for future feature additions.

## Files Contents and Directories
- `finance` - Application Directory
    - `static/finance` - Contains static content
        - `dashboard.PNG` - "Dashboard" image for the "welcome" template
        - `finance.svg` - "Finance" image for the "welcome" template
        - `records.js` - Javascript for "records" template
        - `records.PNG` - "Records" image for the "welcome" template
        - `style.css` - Custom CSS for all the Djano templates
    - `templates/finance` - Contains Django templates
        - `dashboard.html` - Dashboard page for logged in users
        - `layout.html` - Layout template for other templates
        - `login.html` - Login page 
        - `records.html` - Records page displays all of a users financial records 
        - `register.html` - Registration page
        - `welcome.html` - Landing page for unregistered users
    - `admin.py` - Django models registration for superuser 
    - `models.py` - Contains 3 Django models for this Project - User, Record and Planned
    - `urls.py` - Handles all the URLs of the application
    - `views.py` - Handles all the Django application views 
- `final` - Project Directory
- `README.md` - Project Description about implementation and other aspects
- `requiremenents.txt` - Required Packages for this project 

## Installation and Running the Application
Step 1: Install the project requirements. 
```
pip install -r requirements.txt
```
Step 2: Create and Apply database migrations.
```
python manage.py makemigrations
python manage.py migrate
``` 
Step 3: Create a Superuser to be able to access the Django admin webpage (Optional).
```
python manage.py createsuperuser
```
Step 4: Launch the Django server.
```
python manage.py runserver
```

## Additional Information
Overall, I would like to thank CS50W lecturer Brian Yu and all the staff involved in this cs50w course for making this entire course available to students all over the world as I genuinely learned alot about web application coding skills after taking this course.