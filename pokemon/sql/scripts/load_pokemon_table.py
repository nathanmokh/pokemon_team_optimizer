import requests
import logging
from pokemon.util.db_utils import execute_sql, get_db_connection, load_sql
from pokemon.util.common_utils import get_config

def load_pokemon_table():

    
    def get_types(pokemon_data):
        if len(pokemon_data['types']) == 2:
            return [pokemon_data['types'][0]['type']['name'], 
                     pokemon_data['types'][1]['type']['name']]
        else:
            return [pokemon_data['types'][0]['type']['name'], 'NULL']
        
    # TODO: assign a role mapping to each pokemon
    def get_role(pokemon_id):
        return 'NULL'
    
    def get_official_artwork(pokemon_data):
        return pokemon_data['sprites']['other']['official-artwork']['front_default'], \
        pokemon_data['sprites']['other']['official-artwork']['front_shiny']
        
    def get_name(pokemon_data):
        return pokemon_data['name']
    
    def create_rows():
        rows = []
        for pokemon_id in range(1, config['num_pokemon'] + 1):
            if pokemon_id in currently_loaded_pokemon_ids:
                continue
            rows.append(get_pokemon(pokemon_id))
            print(f"Row created for pokemon {pokemon_id}")
    
        return ', '.join(str(row) for row in rows)
        
        
    # TODO: Once pokemon object is finalized, load ID into constructor and retrieve the data via the object
    # the above methods can be recycled for this
    def get_pokemon(pokemon_id: int) -> dict:
        URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        pokemon_data = requests.get(URL).json()
        official_artwork_default, official_artwork_shiny = get_official_artwork(pokemon_data)
        type1, type2 = get_types(pokemon_data)
        role = get_role(pokemon_id)
        official_artwork_default, official_artwork_shiny = get_official_artwork(pokemon_data)
        name = get_name(pokemon_data)
        return (
            pokemon_id,
            name,
            type1,
            type2,
            role,
            official_artwork_default,
            official_artwork_shiny
        )
        
    
    config = get_config()
    
    # Query to prevent duplicates
    execute_sql('create_pokemon_table.sql', is_ddl_statement=True)
    currently_loaded_pokemon_ids = execute_sql("get_pokemon_ids_from_pokemon_table.sql")
    currently_loaded_pokemon_ids = {record[0]: None for record in currently_loaded_pokemon_ids}
    execute_sql('populate_pokemon_table.sql', substitutions={'values': create_rows()}, is_ddl_statement=True)
    
 
        
if __name__ == '__main__':
    load_pokemon_table()