import requests
import logging
from src.pokemon.util.common_utils import get_currently_loaded_pokemon_move_ids
from src.pokemon.util.db_utils import execute_sql


class MoveTableLoader:
    def __init__(self) -> None:
        self.moves_table_creation_query = "create_moves_table.sql"
        self.populate_rows_table_query = "populate_moves_table.sql"
        self.all_moves_request_url = "https://pokeapi.co/api/v2/move/"

    def _create_rows(self, currently_loaded_move_ids, num_moves):
        rows = []
        for move_id in range(1, num_moves):
            if move_id in currently_loaded_move_ids:
                continue
            move = self._get_move(move_id)
            if move:
                rows.append((move))
                print(f"Row created for move {move['move_name']}, id: {move_id}")
        return rows

    def _get_crit_rate(self, move_data):
        if move_data["meta"]:
            return move_data["meta"]["crit_rate"]

    def _get_stat_chance(self, move_data):
        if move_data["meta"]:
            return move_data["meta"]["stat_chance"]

    def _get_move_effect_description(self, move_data):
        if move_data["effect_entries"]:
            return move_data["effect_entries"][0]["effect"].replace("'", "")

    def _get_effect_chance(self, move_data):
        if move_data["effect_chance"]:
            return move_data["effect_chance"]
        else:
            return "NULL"

    def _get_drain(self, move_data):
        if move_data["meta"]:
            return move_data["meta"]["drain"]
        else:
            return "NULL"

    def _get_category(self, move_data):
        if move_data["meta"]:
            return move_data["meta"]["category"]["name"]
        else:
            return "NULL"

    def _get_move(self, move_id):
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
            "power": move_data.get("power", "NULL"),
            "accuracy": move_data["accuracy"],
            "pp": move_data["pp"],
            "priority": move_data["priority"],
            "description": self._get_move_effect_description(move_data),
            "effect_chance": self._get_effect_chance(move_data),
            "healing_percentage": "NULL",  # TODO: fill in
            "damage_class": move_data["damage_class"]["name"],
            "category": self._get_category(move_data),
            "crit_rate": self._get_crit_rate(move_data),
            "stat_chance": self._get_stat_chance(move_data),
            "drain": self._get_drain(move_data),
        }

    def run(self):
        # get total number of moves in pokeapi
        num_moves = requests.get(self.all_moves_request_url).json()["count"]

        # create moves table if none exists
        execute_sql(self.moves_table_creation_query)
        # get currently loaded IDs to prevent creating duplicate rows
        currently_loaded_pokemon_move_ids = get_currently_loaded_pokemon_move_ids()
        # create rows
        rows = self._create_rows(currently_loaded_pokemon_move_ids, num_moves)

        logging.info(f"Loading pokemon moves to table, {len(rows)} rows.")
        print(f"Loading pokemon moves to table, {len(rows)} rows.")
        formatted_insert_rows = ", ".join(str(tuple(row.values())) for row in rows)

        if rows:
            execute_sql(self.populate_rows_table_query, {"rows": formatted_insert_rows})
        else:
            print(f"No rows created.")


if __name__ == "__main__":
    MoveTableLoader().run()
