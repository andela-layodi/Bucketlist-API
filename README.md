# Bucket-y! - Online Bucketlist System
This application provides API endpoints that enable managemant of user data in the Bucketlist system.
The building blocks used to come up with this system include:
* Python 3
* Flask
* PostgreSQl

## Setting Up/ Installation
The following set of steps are necessary to facilitate running the application locally:
* Create a directory for the project code
      ```$ mkdir -p ~/buckety
        $ cd ~/buckety```

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

  and to delete tables running:
        $ python manage.py drop_db

* Start the application by running:
        $ python manage.py runserver

## API
The endpoints include:
EndPoint | Functionality
------------ | -------------
POST /auth/login | Logs a user in and generates a unique token
POST /auth/register | Register a user
POST /bucketlists/  | Create a new bucket list
GET /bucketlists/ | List all the created bucket lists that belongs to the logged in user
GET /bucketlists/<id> | Get single bucket list
PUT /bucketlists/<id> | Updates the specified bucket list
DELETE /bucketlists/<id> | Delete the specified bucket list
POST /bucketlists/<id>/items/ | Create a new item in bucket list
PUT /bucketlists/<id>/items/<item_id> | Update a bucket list item
DELETE /bucketlists/<id>/items/<item_id> | Delete an item in a bucket list
