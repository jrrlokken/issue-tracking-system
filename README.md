Issue Tracking System (ITS) 

https://flask-its.herokuapp.com

ITS is intended to be used to track technical issues, customer complaints and product requests for a retail operation.

The issue list is an HTML table sortable by all columns and searchable by issue title or description.  Table rows are color coded to indicate issue priority.  

Users of the application have the ability to register with an email address, login, create new issues, add comments to those issues and logout.

Role-based authorization allows assignee users to edit issues while admin users have access to CRUD functionality for all users, issues and comments.

ITS is written in Python, JavaScript, HTML and CSS. It is a Flask application, utilizing WTForms and SQLAlchemy, backed by a PostgreSQL database and provides a custom REST API.

Demo credentials:

Admin user:  user1@example.com / password1
Normal user:  user2@example.com / password2
Assignee user: user3@example.com / password3



