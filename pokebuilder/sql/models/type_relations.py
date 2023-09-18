from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from pokebuilder.extensions import db
from pokebuilder.sql.models.stats import Stats
from pokebuilder.sql.models.pokemon import Pokemon
from pokebuilder.sql.models.moves import Moves
from pokebuilder.sql.models.moves_mapping import PokemonMovesMapping
from pokebuilder.sql.models.types import Types


class Type_Relations(db.Model):
    __tablename__ = "types_relations"

    source_type_id = Column(Integer, primary_key=True)
    target_type_id = Column(Integer, primary_key=True)
    effectiveness = Column(Float, primary_key=True)
