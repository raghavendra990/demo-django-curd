
## Software and Version
Python 3.10<br />
Django 4.2.9<br />
MySQL 8<br />

# Project Structure:
<pre> 
.
├── README.md
├── backend
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── userauth				# module for authentication
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── authentication.py		# custom authetication
│   ├── jwt.py
│   ├── log.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_blacklistedtoken.py
│   │   ├── 0003_alter_usermodel_password.py
│   │   ├── 0004_alter_blacklistedtoken_token.py
│   │   ├── 0005_alter_usermodel_created_at_and_more.py
│   │   └── __init__.py
│   ├── models.py			# Auth models for storing users data
│   ├── serializers.py			# auth serializers
│   ├── tests.py
│   ├── urls.py				# Auth endpoints
│   └── views.py			# Auth Views
└── useritem				# to display the items for the users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   ├── 0001_initial.py
    │   └── __init__.py
    ├── models.py			# item models for the user
    ├── serializers.py			# serializers for the items
    ├── tests.py			
    ├── urls.py
    └── views.py
</pre>

## Installation
## clone the backend project
	git clone https://github.com/raghavendra990/demo-docker-backend.git
	cd demo-django-curd
 	
 ### make virtual env
	virtualenv .venv -p python3
 	source .venv/bin/activate
  
 ### install requirements
 	install Mysql client on your machine
 	pip install -r requirements.txt
### run Migration
	python manage.py migrate
### runserver
	python manage.py runserver
  	

## Backend structure: 
![Architecture](/loadbalancer-architecture.png)

Backend is built using django rest framework and Postgres as backend DB. 

It majorly contain two apps details below:
	
<b>userauth</b>: It is used for authentication for the user with apis like Login, Register, Logout. I have used JWT custom authentication, code present at demo-backend/userauth/authentication.py .

<b>For Logout</b>, the frontend application will just delete the jwt token from storage, but there is still a chance that token remains valid and the fraudster can miss use it. That is Why we have created a Table BlackListedToken where we will store the blacklisted tokens and we have created Custom Permission Class IsTokenValid present in authentication.py file in userauth app.

<b>userItem</b>: it contains all the logic related to Items Add, Edit, remove, Get Items for the User and Summary API.

Postman collection for the APIs: https://api.postman.com/collections/655988-66fc581b-64e4-4c8e-a2a3-4240702ca1a2?access_key=PMAT-01HNCPCJ5Y84FV86H9NJA8X7RX
