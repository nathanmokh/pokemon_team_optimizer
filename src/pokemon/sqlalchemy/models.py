from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from src.pokemon.util.common_utils import get_config


Base = declarative_base()
config = get_config()


class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True)
    pokemon_name = Column(String)
    type_1 = Column(String)
    type_2 = Column(String)
    team_role = Column(String)

    stats = relationship("Stats", back_populates="pokemon")


class Stats(Base):
    __tablename__ = "stats"

    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), primary_key=True)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    sp_attack = Column(Integer)
    sp_defense = Column(Integer)
    speed = Column(Integer)

    pokemon = relationship("Pokemon", back_populates="stats")


class Moves(Base):
    __tablename__ = "moves"

    move_id = Column(Integer)
    move_name = Column(String)
    move_type = Column(String)
    power = Column(Integer)
    accuracy = Column(Integer)
    pp = Column(Integer)
    priority = Column(Integer)
    description = Column(String)
    effect_chance = Column(Integer)
    healing_percentage = Column(Integer)
    damage_class = Column(String)
    category = Column(String)
    crit_rate = Column(Integer)
    stat_chance = Column(Integer)
    drain = Column(Integer)

    pokemon = relationship("Pokemon", back_populates="moves")


class PokemonMovesMapping(Base):
    __tablename__ = "pokemonmovesmapping"

    move_id = Column(
        Integer, ForeignKey("pokemonmovesmapping.move_id"), primary_key=True
    )
    pokemon_id = Column(Integer)
    level_learned = Column(Integer)
    learn_method = Column(String)
    game_version = Column(String)

    pokemon = relationship("Pokemon", back_populates="pokemonmovesmapping")
    
class Sprites(Base):
    __tablename__ = "sprites"
    
    pokemon_id = Column(Integer)
    official_artwork = Column(String)
    official_artwork_shiny = Column(String)
    back_default = Column(String)
    back_female = Column(String)
    front_default = Column(String)
    front_female = Column(String)
    back_shiny = Column(String)
    back_shiny_female = Column(String)
    front_shiny = Column(String)
    front_shiny_female = Column(String)
    
    pokemon = relationship("Pokemon", back_populates="sprites")
