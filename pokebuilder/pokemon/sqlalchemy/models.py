from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pokemon.util.config import get_config


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


# Repeat the same pattern for other related classes...
