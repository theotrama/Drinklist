FROM python:3.7

RUN apt-get update && \
    apt-get install -y && \
    pip3 install uwsgi

COPY . /opt/drinklist

RUN pip3 install -r /opt/drinklist/requirements.txt

# Create new group and user
RUN groupadd app
RUN useradd app -g app -m

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# chown all the files to the app user
RUN chown -R app:app /opt/drinklist

# change to the app user
USER app

ENV DJANGO_ENV=prod
ENV DOCKER_CONTAINER=1

EXPOSE 8000

CMD ["uwsgi", "--ini", "/opt/drinklist/uwsgi.ini"]
