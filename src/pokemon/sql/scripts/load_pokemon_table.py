import requests
from src.pokemon.util.db_utils import execute_sql, get_db_connection, load_sql
from src.pokemon.util.common_utils import get_current_number_of_pokemon_pokeapi


class PokemonTableLoader:
    def __init__(self) -> None:
        self.num_pokemon = get_current_number_of_pokemon_pokeapi()
        self.table_creation_script = "create_pokemon_table.sql"
        self.table_population_script = "populate_pokemon_table.sql"

    def _get_pokemon(self, pokemon_id: int) -> dict:
        URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        pokemon_data = requests.get(URL).json()
        type1, type2 = self._get_types(pokemon_data)
        role = self._get_role(pokemon_id)
        name = self._get_name(pokemon_data)
        return (
            pokemon_id,
            name,
            type1,
            type2,
            role,
        )

    def _create_rows(self, currently_loaded_pokemon_ids: dict):
        rows = []
        for pokemon_id in range(1, self.num_pokemon + 1):
            if pokemon_id in currently_loaded_pokemon_ids:
                continue
            rows.append(self._get_pokemon(pokemon_id))
            print(f"Row created for pokemon {pokemon_id}")

        return ", ".join(str(row) for row in rows)

    def _get_name(self, pokemon_data: dict) -> str:
        return pokemon_data["name"]

    def _get_currently_loaded_pokemon_ids(self) -> dict:
        currently_loaded_pokemon_ids = execute_sql(raw_sql="SELECT id FROM pokemon;")
        return {record[0]: None for record in currently_loaded_pokemon_ids}

    # TODO: assign a role mapping to each pokemon
    def _get_role(self, pokemon_id: int) -> str:
        return "NULL"

    def _get_types(self, pokemon_data):
        if len(pokemon_data["types"]) == 2:
            return [
                pokemon_data["types"][0]["type"]["name"],
                pokemon_data["types"][1]["type"]["name"],
            ]
        else:
            return [pokemon_data["types"][0]["type"]["name"], "NULL"]

    def run(self) -> None:
        execute_sql(self.table_creation_script)
        currently_loaded_pokemon_ids = self._get_currently_loaded_pokemon_ids()

        rows = self._create_rows(currently_loaded_pokemon_ids)

        if rows:
            execute_sql(
                self.table_population_script,
                substitutions={"values": rows},
            )
        else:
            print(f"No rows created.")


if __name__ == "__main__":
    PokemonTableLoader().run()
