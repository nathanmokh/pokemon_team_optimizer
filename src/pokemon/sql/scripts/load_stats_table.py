import requests
import logging
from src.pokemon.util.db_utils import execute_sql
from src.pokemon.util.common_utils import get_current_number_of_pokemon_pokeapi


class StatsTableLoader:
    def __init__(self) -> None:
        self.stats_table_creation_script = "create_stats_table.sql"
        self.stats_table_population_script = "populate_stats_table.sql"

    def create_insert_rows(self):
        currently_loaded_pokemon_stats_ids = self.get_currently_loaded_ids()

        fetched_data = []
        for pokemon_id in range(1, get_current_number_of_pokemon_pokeapi()):
            if pokemon_id in currently_loaded_pokemon_stats_ids:
                continue
            stats = self.get_pokemon_stats(pokemon_id)
            fetched_data.append((pokemon_id, *stats))
            print(f"Row created for pokemon {pokemon_id}")
        return self.format_insert_rows(fetched_data)

    def get_pokemon_stats(self, pokemon_id):
        URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        stats = requests.get(URL).json()["stats"]
        return [stat["base_stat"] for stat in stats]

    def get_currently_loaded_ids(self):
        return [
            record[0] for record in execute_sql(raw_sql="SELECT pokemon_id FROM stats;")
        ]

    def format_insert_rows(self, rows):
        return ", ".join(str(tuple(row)) for row in rows)

    def run(self):
        execute_sql(self.stats_table_creation_script)
        # get currently loaded IDs to prevent creating duplicate rows
        # create rows
        rows = self.create_insert_rows()

        logging.info(f"Loading pokemon base stats to table, {len(rows)} rows.")
        print(f"Loading pokemon base stats to table, {len(rows)} rows.")

        if rows:
            execute_sql(self.stats_table_population_script, {"rows": rows})


if __name__ == "__main__":
    StatsTableLoader().run()
