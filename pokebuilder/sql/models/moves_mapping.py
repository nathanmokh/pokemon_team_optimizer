from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from pokebuilder.extensions import db


class PokemonMovesMapping(db.Model):
    __tablename__ = "pokemonmovesmapping"

    id = Column(Integer, primary_key=True)
    move_id = Column(Integer, ForeignKey("moves.move_id"))
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"))
    level_learned = Column(Integer)
    learn_method = Column(String)
    game_version = Column(String)

    move = relationship("Moves", backref="pokemon_moves")
    pokemon = relationship("Pokemon", back_populates="moves")
