from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from pokebuilder.extensions import db
from pokebuilder.sql.models.stats import Stats
from pokebuilder.sql.models.pokemon import Pokemon
from pokebuilder.sql.models.moves import Moves
from pokebuilder.sql.models.moves_mapping import PokemonMovesMapping
from pokebuilder.sql.models.types import Types


class Natures(db.Model):
    __tablename__ = "nature"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    increased_stat = Column(String, nullable=False)
    decreased_stat = Column(String, nullable=False)
