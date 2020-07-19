# Drinklist
This project is a drinklist to track the drink consumption of e.g. residents in a dormitory.
I started to code this project to replace our dormitory's paper tally sheet.
But it was more of a project to learn Django and to learn how to deploy a Django app to production with docker containers.

## Tech Stack
The project is mainly build with the powerful Django web framework for Python. The templates are styled with Bootstrap 4.
The project does use only very limited JavaScript, this could be improved in the future
(e.g. decouple the backend from the frontend by refactoring the app into a REST API with Angular, Vue or React as the frontend).

## Development environment
To get the project up and running clone it to your local work environment.
### Conda
Go to the root directory of the project. There create and activate the conda environment.
```bash
conda env create -f environment.yml
conda activate djangoenv
```
### Pip
If you want to use pip instead of conda you can use the `requirements.txt` file to create a virtual environment.
```bash
pip install venv
source venv/bin/activate
pip install -r requirements.txt
```

### Initial setup
Initialize the database with Django's built in manage.py file and start the app.
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

These commands should create the database and start up the server. Create an admin user with `python manage.py createsuperuser`
and go to [http://localhost:8000/admin/](http://localhost:8000/admin/).
On this page login with the previously created admin user. Make sure that the database tables were added successfully.
Subsequently, go to the web app's interface at [http://localhost:8000](http://localhost:8000).

## Production environment
The production environment uses uwsgi as the application server and nginx as the web server.
The Django web app and the PostgreSQL database are running in separate docker containers that are tied together with docker-compose.
To deploy the web app to production with docker containers Oliver Eidel's [tutorial](https://www.eidel.io/2017/07/10/dockerizing-django-uwsgi-postgres/)
and testdriven.io's [tutorial](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/) were pure gold.

### Initial setup
Start the docker containers and apply the initial database migrations. Add the necessary admin staticfiles to the staticfiles directory.
```bash
docker-compose up --build -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input --clear
```

Additionally, you can create an admin user inside the docker container.
```bash
docker-compose exec web python manage.py createsuperuser
```

After this preliminary setup the web app is available at [localhost:1337](http://localhost:1337) if you ran the above
commands on your local machine.

If you make changes in the project spin the docker containers down and start them up again.
```bash
docker-compose down -v
docker-compose up --build
```

### Logging
The logs of uwsgi, nginx and PostgreSQL are accessible via `docker-compose`.
```bash
docker-compose logs -f
```

# Todo
- [ ] Load passwords from env file
- [x] Add section about conda and pip to development environment
- [ ] Add SSL certificate
- [x] Redirect `drinklist.raspberrypi.me` to `drinklist.raspberrypi.me/drinkcounter/overview`