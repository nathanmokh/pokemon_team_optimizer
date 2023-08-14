from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pokemon.pokemon import Pokemon

from pokemon.util.common_utils import get_config

config = get_config()
engine = create_engine(f"postgresql://{config['db']['user']}:{config['db']['password']}@{config['db']['host']}:{config['db']['port']}/{config['db']['dbname']}")

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Example usage: query the existing data
pokemon_data = session.query(Pokemon).all()

for pokemon in pokemon_data:
    print(f"ID: {pokemon.id}, Name: {pokemon.pokemon_name}, Type 1: {pokemon.type_1}, Type 2: {pokemon.type_2}, Team Role: {pokemon.team_role}")
    print(f"Stats: HP: {pokemon.stats.hp}, Attack: {pokemon.stats.attack}, Defense: {pokemon.stats.defense}, Speed: {pokemon.stats.speed}")
