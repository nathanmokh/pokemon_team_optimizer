import pokebase as pb
import time

class Pokemon:
    """Represents a pokemon
    Args:
        id (int, optional): pokemon ID..
    """
    def __init__(self, id: int=1):
        pokemon_data = pb.pokemon(id)
        
        
        self.id = id
        self.abilities = pokemon_data.abilities
        self.moves_list = pokemon_data.moves
        self.current_moves = []
        self.is_shiny = False
        self.level = 1
        self.type_1 = None
        self.type_2 = None
        self.damage_relations = None
        self.encounters = None        
        
    
    def _get_pokemon_moves(self):
        """returns a list of pokemon move objects available to the pokemon
        """
        return self.moves_list

