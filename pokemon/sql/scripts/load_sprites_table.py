import requests
import logging
from pokemon.util.db_utils import execute_sql
from pokemon.util.common_utils import get_config

def load_sprites_table():
            
    def get_official_artwork(pokemon_data):
        return pokemon_data['sprites']['other']['official-artwork']['front_default'], \
        pokemon_data['sprites']['other']['official-artwork']['front_shiny']
            
    def create_rows():
        rows = [
            get_sprites(pokemon_id) 
            for pokemon_id in range(1, config['num_pokemon'] + 1) 
            if pokemon_id not in currently_loaded_pokemon_ids
            ]
        return ', '.join(str(row) for row in rows)
        
        
    # TODO: Finish
    def get_sprites(pokemon_id: int) -> dict:
        URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        pokemon_data = requests.get(URL).json()
        official_artwork_default, official_artwork_shiny = get_official_artwork(pokemon_data)
        return (
            pokemon_id
        )
        
    
    config = get_config()
    
    # Query to prevent duplicates
    execute_sql('create_sprites_table.sql', is_ddl_statement=True)
    currently_loaded_pokemon_ids = execute_sql("get_pokemon_ids_from_sprites_table.sql")
    currently_loaded_pokemon_ids = {record[0]: None for record in currently_loaded_pokemon_ids}
    execute_sql('populate_sprites_table.sql', substitutions={'values': create_rows()}, is_ddl_statement=True)
    
 
        
if __name__ == '__main__':
    load_sprites_table()