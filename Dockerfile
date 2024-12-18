FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN apt-get install libpq-dev -y
RUN apt-get install python3-dev build-essential -y
RUN apt-get install postgresql-client -y

RUN pip install --upgrade pip
RUN pip install virtualenv && python -m venv venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /srv/app
COPY . /srv/app

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN python manage.py collectstatic --noinput