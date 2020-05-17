# Drinklist
This project is a drinklist to track the drink consumption of e.g. residents in a dormitory. I started to code this project to replace our dormitory's paper tally sheet. But it was more of a project to learn Django and I did not yet deploy it to a production server.

## Tech Stack
The project is mainly build with the powerful Django web framework for Python. To have nice looking and responsive templates, Bootstrap was utilized. The project does use only very limited JavaScript, this could be improved in the future (e.g. decouple the backend from the frontend by refactoring the app into a REST API with Angular, Vue or React as the frontend). Currently the database in use is a simple sqlite database for testing. If you want to deploy the app to production you should use PostgreSQL, MySQL, etc.

## Setup
To get the project up and running just clone it to your local work environment. Go to the root directory of the project and run `conda env create -f environment.yml` to create the conda environment. Then you should make the necessary database initializations with Django's built in manage.py file. Therefore run 
```bash
python manage.py makemigrations
python manage.py migrate
```
These commands should create the database. Verify that everything worked by running the server locally with `python manage.py runserver`. Create an admin user with `python manage.py createsuperuser` and go to [http://localhost:8000/admin/](http://localhost:8000/admin/). On this page login with the previously created admin user. Make sure that the database tables were added successfully. Subsequently go to the webapp's interface at [http://localhost:8000/drinkcounter/overview/](http://localhost:8000/drinkcounter/overview/).

## Deploy to production
* With database to PostgreSQL, MySQL or similar
* Use nginx (web server) and gunicorn or uwsgi (application server) to deploy the app

## Todo
* Add database to make it possible to switch between development and production
* Deploy with a docker container