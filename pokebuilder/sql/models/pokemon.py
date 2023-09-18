from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from pokebuilder.extensions import db
from pokebuilder.sql.models.stats import Stats


class Pokemon(db.Model):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True)
    pokemon_name = Column(String)
    type_1 = Column(String)
    type_2 = Column(String)
    team_role = Column(String)

    type_id = Column(Integer, ForeignKey('types.id'))

    stats = relationship("Stats", back_populates="pokemon")
    moves = relationship("PokemonMovesMapping", back_populates="pokemon")
    
