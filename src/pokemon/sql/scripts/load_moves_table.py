import requests
import logging
from src.pokemon.util.db_utils import execute_sql
from src.pokemon.util.common_utils import get_config


def load_moves_table():
    def create_insert_rows_moves_tbl(config, currently_loaded_moves):
        
        # get total number of moves in pokeapi
        total_moves_request = "https://pokeapi.co/api/v2/move/"
        response = requests.get(total_moves_request).json()
        x = 3
        
        fetched_data = []
        for pokemon_id in range(1, config["num_pokemon"] + 1):
            if pokemon_id in currently_loaded_moves:
                continue
            stats = get_moves(pokemon_id)
            fetched_data.append((pokemon_id, *stats))
            print(f"Row created for pokemon {pokemon_id}")
        return fetched_data

    def create_insert_rows_junction_tbl(config, currently_loaded_moves):
        pass

    def get_moves(pokemon_id):
        URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        stats = requests.get(URL).json()["stats"]
        return [stat["base_stat"] for stat in stats]

    config = get_config()

    # create moves table if none exists
    execute_sql("create_moves_table.sql")
    # get currently loaded IDs to prevent creating duplicate rows
    currently_loaded_pokemon_move_ids = [
        record[0] for record in execute_sql(raw_sql="SELECT id FROM moves;")
    ]
    # create rows
    rows = create_insert_rows_moves_tbl(config, currently_loaded_pokemon_move_ids)

    logging.info(f"Loading pokemon moves to table, {len(rows)} rows.")
    print(f"Loading pokemon moves to table, {len(rows)} rows.")
    formatted_insert_rows = ", ".join(str(tuple(row)) for row in rows)

    if rows:
        execute_sql(
            "populate_moves_table.sql",
            {"rows": formatted_insert_rows}
        )

        # TODO: name junction table PokemonMoveMapping
        execute_sql("populate_pokemon_move_mapping.sql")


if __name__ == "__main__":
    load_moves_table()
