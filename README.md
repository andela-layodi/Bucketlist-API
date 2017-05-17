# Bucket-y! - Online Bucketlist System
This application provides API endpoints that enable managemant of user data in the Bucketlist system.
The building blocks used to come up with this system include:
* Python 3
* Flask
* PostgreSQl

## Setting Up/ Installation
The following set of steps are necessary to facilitate running the application locally:
* Create a directory for the project code

        $ mkdir -p ~/buckety

        $ cd ~/buckety

* Create a virtual environment for the dependencies

        $ virtualenv --python=python3 buckety_venv

        $ source buckety_venv/bin/activate

* Clone the project code from the remote repository

        $ git clone https://github.com/andela-layodi/Bucketlist-API.git

* Install the dependencies

        $ cd buckety

        $ pip install -r requirements.txt

* Run database migrations

        $ python manage.py db init

        $ python manage.py db migrate

* Manually create database tables by running:

        $ python manage.py create_db

* To delete tables running:

        $ python manage.py drop_db

* Start the application by running:

        $ python manage.py runserver

## API
The endpoints include:
* `POST /auth/login` - Log in
* `POST /auth/register` - Register
* `POST /bucketlists/` - Create bucketlist
* `GET /bucketlists/` - Retrieve bucketlists
* `GET /bucketlists/<id>` - Retrieve a specific bucketlist
* `PUT /bucketlists/<id>` - Edit a bucketlist
* `DELETE /bucketlists/<id>` - Delete a bucketlist
* `POST /bucketlists/<id>/items/` - Create items in a bucketlist
* `PUT /bucketlists/<id>/items/<item_id>` - Edit an item in a bucketlist
* `DELETE /bucketlists/<id>/items/<item_id>` - Delete an item in a bucketlist
