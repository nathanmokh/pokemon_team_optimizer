FROM python:3.10

ARG POSTGRESQL_DATABASE_URI
ARG FLASK_SECRET_KEY

ENV POSTGRESQL_DATABASE_URI=${POSTGRESQL_DATABASE_URI}
ENV FLASK_SECRET_KEY=${FLASK_SECRET_KEY}

RUN apt-get update && apt-get install -y \
    postgresql \
    libpq-dev

RUN pip install -r requirements.txt

CMD flask --app pokebuilder/app run