import pokebase as pb
import os
import sys
import psycopg2

from pokemon.util.db_utils import get_db_connection
from pokemon.util.common_utils import get_config

def load_stats_table():
    
    stats_data_to_insert = []
    config = get_config()
    for pokemon_id in range(1, config.get('num_pokemon', 1)):
        pokemon_stats = pb.pokemon(pokemon_id).stats
        # need ID as PK, hp, attack, defense, sp_attack, sp_defense, speed, generation
        stats_data_to_insert.append(tuple(
            [pokemon_id, * [stat.base_stat for stat in pokemon_stats]]
            )
        )
        
    connection = get_db_connection()
    cursor = connection.cursor
    x = 3
    
    
    
    
    

        
if __name__ == '__main__':
    load_stats_table()