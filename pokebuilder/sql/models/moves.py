from sqlalchemy import Column, Integer, String
from extensions import db


class Moves(db.Model):
    __tablename__ = "moves"

    move_id = Column(Integer, primary_key=True)
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

    # pokemon_moves_mapping_id = Column(
    #     Integer, ForeignKey("pokemonmovesmapping.move_id")
    # )
    # pokemon = relationship("PokemonMovesMapping", back_populates="moves")
