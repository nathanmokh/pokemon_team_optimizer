from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Sprites(db.Model):
    __tablename__ = "sprites"

    pokemon_id = Column(Integer, primary_key=True)
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
