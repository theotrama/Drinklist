FROM python:3.7

RUN apt-get update && \
    apt-get install -y && \
    pip3 install uwsgi

# Create new group and user
RUN groupadd app
RUN useradd app -g app -m

# create the appropriate directories
ENV HOME=/opt/drinklist
ENV APP_HOME=/opt/drinklist
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

COPY . $APP_HOME

RUN pip3 install -r /opt/drinklist/requirements.txt

ENV DJANGO_ENV=prod
ENV DOCKER_CONTAINER=1

EXPOSE 8000

CMD ["uwsgi", "--ini", "/opt/drinklist/uwsgi.ini"]
