import requests
import logging
from pokemon.util.db_utils import get_db_connection, load_sql, load_to_stats_table
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
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Query to prevent duplicates
    prevent_dupes_query = load_sql("get_pokemon_ids_from_stats_tbl.sql")
    cursor.execute(prevent_dupes_query)
    currently_loaded_pokemon_stats_ids = [record[0] for record in cursor.fetchall()]

    rows = create_insert_rows(config, currently_loaded_pokemon_stats_ids)

    # convert to list of tuples in string format for insert query
    logging.info(f"Loading pokemon base stats to table, {len(rows)} rows.")
    print(f"Loading pokemon base stats to table, {len(rows)} rows.")
    load_to_stats_table([str(row) for row in rows], connection, cursor)
    connection.close()
    
 
        
if __name__ == '__main__':
    load_stats_table()