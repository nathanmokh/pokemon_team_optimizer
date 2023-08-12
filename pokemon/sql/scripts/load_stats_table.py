import requests
import logging
from pokemon.util.db_utils import execute_sql
from pokemon.util.common_utils import get_config

def load_stats_table():

    def create_insert_rows(config, currently_loaded_pokemon):
        fetched_data = []
        for pokemon_id in range(1, config['num_pokemon'] + 1):
            if pokemon_id in currently_loaded_pokemon:
                continue
            stats = get_pokemon_stats(pokemon_id)
            fetched_data.append((pokemon_id, *stats))
            print(f"Row created for pokemon {pokemon_id}")
        return fetched_data
    
    def get_pokemon_stats(pokemon_id):
        URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        stats = requests.get(URL).json()['stats']
        return [stat['base_stat'] for stat in stats]
    
    config = get_config()
    
    # create stats table if none exists
    execute_sql("create_stats_table.sql", is_ddl_statement=True)
    # get currently loaded IDs to prevent creating duplicate rows
    currently_loaded_pokemon_stats_ids = [record[0] for record in execute_sql("get_pokemon_ids_from_stats_tbl.sql")] 
    # create rows
    rows = create_insert_rows(config, currently_loaded_pokemon_stats_ids)

    logging.info(f"Loading pokemon base stats to table, {len(rows)} rows.")
    print(f"Loading pokemon base stats to table, {len(rows)} rows.")
    formatted_insert_rows = ', '.join(str(tuple(row)) for row in rows)
    
    execute_sql('populate_stats_table.sql', {'rows': formatted_insert_rows}, is_ddl_statement=True)
    
 
        
if __name__ == '__main__':
    load_stats_table()