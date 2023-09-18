from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from pokebuilder.extensions import db
from pokebuilder.sql.models.stats import Stats
from pokebuilder.sql.models.pokemon import Pokemon
from pokebuilder.sql.models.moves import Moves
from pokebuilder.sql.models.moves_mapping import PokemonMovesMapping

class Types(db.Model):
    __tablename__ = "types"

    id = Column(Integer, primary_key = True)
    type_name = Column(String)
    
    pokemon = relationship("Pokemon", backref="type")


x = 3