FROM python:3.8-slim-buster

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        apt-utils \
        build-essential \
        libgdal-dev \
        libgeos-dev \
        libpq-dev \
        libproj-dev \
        musl-dev \
        postgresql-client-11 \
        tini


ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.dev.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

COPY ./docker/django/entrypoint /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/django/start /start
RUN chmod +x /start


WORKDIR /app

ENTRYPOINT ["tini", "--" ,"/entrypoint"]
