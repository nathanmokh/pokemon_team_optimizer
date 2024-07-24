# Poke-Builder
*By: Nathan Mokhtarzadeh, Jonah Mokhtarzadeh, Zachary Mokhtarzadeh, David Golshirazian, Austin Boling*

## Pokemon Team Builder Project!
The purpose of this project is to create a team builder/optimizer for pokemon. 
Feature suggestions are welcome, the goal is to build a system that will auto update with the newest pokemon from the PokeAPI, and be able to create the "optimal" team given certain parameters and constraints. 
We are using a wrapper for the Pokemon API called [Pokebase](https://github.com/PokeAPI/pokebase/) which comes with auto caching which will be a significant performance boost over using the PokeAPI directly.

## Install Dependencies
TODO:
- Add [init script](https://stackoverflow.com/questions/33309121/using-docker-compose-to-create-tables-in-postgresql-database) to Compose to create `pokemon` database
- Designate Python Version, 3.10?
- Create virtual environment using [venv](https://docs.python.org/3/library/venv.html) or [conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment)
- setup environemnt using `pip install` or `conda create`   

## Local Environment Setup
- Create `.dbenv` which will hold environment variables for PostgreSQL
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=pokemon
```
- Create `.flaskenv` which will hold the necessary environment variables for flask. Example:
```bash
FLASK_SECRET_KEY=123456789
SQLALCHEMY_DATABASE_URI=postgresql://postgres:password@localhost:5432/pokemon
```
- Start up the database first and then the flask app

## [Trello Board 🥇](https://trello.com/b/u5sFBvQs/poke-builder)

