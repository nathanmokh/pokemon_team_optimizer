import requests
import logging
from src.pokemon.util.db_utils import execute_sql, get_db_connection, load_sql
from src.pokemon.util.common_utils import (
    get_config,
    get_current_number_of_pokemon_pokeapi,
)


def load_pokemon_table():
    def get_types(pokemon_data):
        if len(pokemon_data["types"]) == 2:
            return [
                pokemon_data["types"][0]["type"]["name"],
                pokemon_data["types"][1]["type"]["name"],
            ]
        else:
            return [pokemon_data["types"][0]["type"]["name"], "NULL"]

    # TODO: assign a role mapping to each pokemon
    def get_role(pokemon_id):
        return "NULL"

    def get_name(pokemon_data):
        return pokemon_data["name"]

    def create_rows():
        num_pokemon = get_current_number_of_pokemon_pokeapi()
        rows = []
        for pokemon_id in range(1, num_pokemon + 1):
            if pokemon_id in currently_loaded_pokemon_ids:
                continue
            rows.append(get_pokemon(pokemon_id))
            print(f"Row created for pokemon {pokemon_id}")

        return ", ".join(str(row) for row in rows)

    # TODO: Once pokemon object is finalized, load ID into constructor and retrieve the data via the object
    # the above methods can be recycled for this
    def get_pokemon(pokemon_id: int) -> dict:
        URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        pokemon_data = requests.get(URL).json()
        type1, type2 = get_types(pokemon_data)
        role = get_role(pokemon_id)
        name = get_name(pokemon_data)
        return (
            pokemon_id,
            name,
            type1,
            type2,
            role,
        )

    # Query to prevent duplicates
    execute_sql("create_pokemon_table.sql")
    currently_loaded_pokemon_ids = execute_sql("get_pokemon_ids_from_pokemon_table.sql")
    currently_loaded_pokemon_ids = {
        record[0]: None for record in currently_loaded_pokemon_ids
    }

    rows = create_rows()

    if rows:
        execute_sql(
            "populate_pokemon_table.sql",
            substitutions={"values": rows},
        )


if __name__ == "__main__":
    load_pokemon_table()
