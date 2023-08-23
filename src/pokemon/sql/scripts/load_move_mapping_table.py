import requests
from src.pokemon.util.common_utils import parse_id_from_end_of_url
from src.pokemon.util.db_utils import execute_sql


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
    load_moves_junction_table()
