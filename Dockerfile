FROM python:3.10

COPY requirements.txt .
COPY pokebuilder ./pokebuilder

RUN apt-get update && apt-get install -y \
    postgresql \
    libpq-dev
RUN pip install -r requirements.txt

EXPOSE 5000

CMD flask --app pokebuilder/app run --host 0.0.0.0 --port 5000