from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from extensions import db


class Stats(db.Model):
    __tablename__ = "stats"

    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), primary_key=True)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    sp_attack = Column(Integer)
    sp_defense = Column(Integer)
    speed = Column(Integer)

    pokemon = relationship("Pokemon", back_populates="stats")
