import requests
from src.pokemon.util.common_utils import parse_id_from_end_of_url
from src.pokemon.util.db_utils import execute_sql


class MoveMappingTableLoader:
    def __init__(self) -> None:
        self.moves_mapping_table_creation_query = "create_moves_mapping.sql"
        self.populate_rows_mapping_table_query = "populate_move_mapping_table.sql"

    def get_move_data(self, pokemon_id: int) -> dict:
        URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        response = requests.get(URL)

        if response.status_code != 200:
            print(f"Data for pokemon id {pokemon_id} not found, skipping.")
            return {}

        return response.json()["moves"]

    def create_mapping_rows(self):
        # iterate over all pokemon in pokemon table
        pokemon_ids = execute_sql(raw_sql="SELECT id FROM pokemon")
        pokemon_ids = [data[0] for data in pokemon_ids]

        rows = []
        for pokemon_id in pokemon_ids:
            # move_data = response.json()["moves"]
            move_data = self.get_move_data(pokemon_id)

            if not move_data:
                continue

            for move in move_data:
                rows.extend(self.create_rows_set_from_move(move, pokemon_id))
            print(f"Done loading moves for pokemon {pokemon_id}")
        return self.format_rows(rows)

    def create_rows_set_from_move(self, move: dict, pokemon_id: int):
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

    def format_rows(self, rows):
        # convert to string represented tuples with only the values
        list_of_tuples = [str(tuple(row.values())) for row in rows]
        return ", ".join(list_of_tuples)

    def run(self):
        execute_sql(self.moves_mapping_table_creation_query)
        rows = self.create_mapping_rows()
        if rows:
            execute_sql(
                self.populate_rows_mapping_table_query, substitutions={"rows": rows}
            )


if __name__ == "__main__":
    MoveMappingTableLoader().run()
