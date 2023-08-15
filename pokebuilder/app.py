from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pokemon.pokemon import Pokemon

from pokemon.util.config import get_config

db = SQLAlchemy()
app = Flask(__name__)

config = get_config()
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{config['db']['user']}:{config['db']['password']}@{config['db']['host']}:{config['db']['port']}/{config['db']['dbname']}"

db.init_app(app)

pokemon_data = session.query(Pokemon).all()

for pokemon in pokemon_data:
    print(
        f"ID: {pokemon.id}, Name: {pokemon.pokemon_name}, Type 1: {pokemon.type_1}, Type 2: {pokemon.type_2}, Team Role: {pokemon.team_role}"
    )
    print(
        f"Stats: HP: {pokemon.stats.hp}, Attack: {pokemon.stats.attack}, Defense: {pokemon.stats.defense}, Speed: {pokemon.stats.speed}"
    )
