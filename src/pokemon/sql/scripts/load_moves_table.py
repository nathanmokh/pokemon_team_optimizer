import requests
import logging
from src.pokemon.util.common_utils import (
    parse_id_from_end_of_url,
)
from src.pokemon.util.db_utils import execute_sql
from time import time


def load_moves_table():
    def create_rows_moves_tbl(currently_loaded_moves, num_moves):
        rows = []
        for move_id in range(num_moves):
            if move_id in currently_loaded_moves:
                continue
            move = get_move(move_id)
            if move:
                rows.append((move))
                print(f"Row created for move {move['move_name']}, id: {move_id}")
        return rows

    def get_crit_rate(move_data):
        if move_data["meta"]:
            return move_data["meta"]["crit_rate"]

    def get_stat_chance(move_data):
        if move_data["meta"]:
            return move_data["meta"]["stat_chance"]

    def get_move_effect_description(move_data):
        if move_data["effect_entries"]:
            return move_data["effect_entries"][0]["effect"].replace("'", "")

    def get_effect_chance(move_data):
        if move_data["effect_chance"]:
            return move_data["effect_chance"]
        else:
            return "NULL"

    def get_drain(move_data):
        if move_data["meta"]:
            return move_data["meta"]["drain"]
        else:
            return "NULL"

    def get_move(move_id):
        URL = f"https://pokeapi.co/api/v2/move/{move_id}"
        request = requests.get(URL)
        if request.status_code == 200:
            move_data = requests.get(URL).json()
        else:
            print(f"Could not retrieve row for move id {move_id}, skipping")
            return
        return {
            "move_id": move_id,
            "move_name": move_data["name"],
            "move_type": move_data["type"]["name"],
            "power": move_data["power"],
            "accuracy": move_data["accuracy"],
            "pp": move_data["pp"],
            "priority": move_data["priority"],
            "description": get_move_effect_description(move_data),
            "effect_chance": get_effect_chance(move_data),
            "healing_percentage": "NULL",  # TODO: fill in
            "damage_class": move_data["damage_class"]["name"],
            "category": "NULL",  # TODO: fill in, see if necessary
            "crit_rate": get_crit_rate(move_data),
            "stat_chance": get_stat_chance(move_data),
            "drain": get_drain(move_data),
        }

    # get total number of moves in pokeapi
    total_moves_request = "https://pokeapi.co/api/v2/move/"
    num_moves = requests.get(total_moves_request).json()["count"]

    # create moves table if none exists
    execute_sql("create_moves_table.sql")
    # get currently loaded IDs to prevent creating duplicate rows
    currently_loaded_pokemon_move_ids = [
        record[0] for record in execute_sql(raw_sql="SELECT move_id FROM moves;")
    ]
    # create rows
    rows = create_rows_moves_tbl(currently_loaded_pokemon_move_ids, num_moves)

    logging.info(f"Loading pokemon moves to table, {len(rows)} rows.")
    print(f"Loading pokemon moves to table, {len(rows)} rows.")
    formatted_insert_rows = ", ".join(str(tuple(row.values())) for row in rows)

    if rows:
        execute_sql("populate_moves_table.sql", {"rows": formatted_insert_rows})

    execute_sql("create_moves_mapping.sql")


def load_moves_junction_table():
    def create_all_rows():
        # iterate over all pokemon in pokemon table
        pokemon_ids = execute_sql(raw_sql="SELECT id FROM pokemon")
        pokemon_ids = [data[0] for data in pokemon_ids]

        rows = []
        for pokemon_id in pokemon_ids:
            URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
            response = requests.get(URL)

            if response.status_code != 200:
                print(f"Data for pokemon id {pokemon_id} not found, skipping.")
                continue

            move_data = response.json()["moves"]

            for move in move_data:
                rows.extend(create_rows_set_from_move(move, pokemon_id))
            print(f"Done loading moves for pokemon {pokemon_id}")
        return rows

    def format_rows(rows):
        # convert to string represented tuples with only the values
        list_of_tuples = [str(tuple(row.values())) for row in rows]
        return ", ".join(list_of_tuples)

    start = time()

    def create_rows_set_from_move(move, pokemon_id):
        rows_set = []
        move_id = parse_id_from_end_of_url(move["move"]["url"])
        version_group_details = move["version_group_details"]
        for details in version_group_details:
            row = {
                "move_id": int(move_id),
                "pokemon_id": pokemon_id,
                "level_learned": int(details["level_learned_at"]),
                "learn_method": details["move_learn_method"]["name"],
                "game_version": details["version_group"]["name"],
            }
            rows_set.append(row)
        return rows_set

    # create PokemonMovesMapping table
    execute_sql("create_moves_mapping.sql")
    rows = create_all_rows()
    rows = format_rows(rows)
    execute_sql("populate_move_mapping_table.sql", substitutions={"rows": rows})


if __name__ == "__main__":
    load_moves_table()
    load_moves_junction_table()
