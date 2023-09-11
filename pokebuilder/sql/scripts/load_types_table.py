import requests
import logging
from src.pokemon.util.db_utils import execute_sql, get_db_connection, load_sql
from src.pokemon.util.common_utils import get_config

# TODO: fix auto-imports


def load_types_table():
    # Getter functions
    def get_type_name(type_data):
        return type_data.get("name")

    def get_damage_relations(type_data):
        return type_data.get("damage_relations")

    # Get Double Damage Functions
    def get_double_damage_from(type_relations):
        double_damage_from_types = type_relations["double_damage_from"]
        types = ""

        for index, type_info in enumerate(double_damage_from_types):
            types += type_info["name"]

            if index < len(double_damage_from_types) - 1:
                types += ", "

        return types

    def get_double_damage_to(type_relations):
        double_damage_to_types = type_relations["double_damage_to"]
        types = ""

        for index, type_info in enumerate(double_damage_to_types):
            types += type_info["name"]

            if index < len(double_damage_to_types) - 1:
                types += ", "

        return types

    # Get Half Damage Functions
    def get_half_damage_from(type_relations):
        half_damage_from_types = type_relations["half_damage_from"]
        types = ""

        for index, type_info in enumerate(half_damage_from_types):
            types += type_info["name"]

            if index < len(half_damage_from_types) - 1:
                types += ", "

        return types

    def get_half_damage_to(type_relations):
        half_damage_to_types = type_relations["half_damage_to"]
        types = ""

        for index, type_info in enumerate(half_damage_to_types):
            types += type_info["name"]

            if index < len(half_damage_to_types) - 1:
                types += ", "

        return types

    def get_type_data(type_id: int) -> dict:
        URL = f"https://pokeapi.co/api/v2/type/{type_id}/"
        pokemon_data = requests.get(URL)

        if pokemon_data.status_code != 200:
            print(
                f"Failed to retrieve type with ID {type_id}. HTTP Status Code: {pokemon_data.status_code}"
            )
            return None

        pokemon_data = pokemon_data.json()

        # TODO: Column ideas - id, name, pokemon, damage_relations

        type_name = get_type_name(pokemon_data)

        return (
            type_id,
            type_name,
        )

    def get_types():
        URL = f"https://pokeapi.co/api/v2/type/"
        response = requests.get(URL)
        if response.status_code != 200:
            print("Failed to retrieve the total count of types.")
            return 0
        temp_data = response.json()

        return temp_data.get("results")  # Returns the names of types from URLs

    def create_rows():
        type_ids = []
        data = get_types()

        for item in data:
            # Splitting the URL by '/' and picking up the second last element after removing trailing slash (if it exists)
            type_id = int(item["url"].rstrip("/").split("/")[-1])
            type_ids.append(get_type_data(type_id))
            print(f"Row created for ID: {type_id}")

        return ", ".join(str(row) for row in type_ids)

    config = get_config()

    execute_sql("create_type_table.sql", is_ddl_statement=True)
    currently_loaded_type_ids = execute_sql("get_type_id_from_type_table.sql")
    currently_loaded_type_ids = {
        record[0]: None for record in currently_loaded_type_ids
    }

    rows = create_rows()

    if rows:
        execute_sql(
            "populate_type_table.sql",
            substitutions={"values": rows},
            is_ddl_statement=True,
        )


# Printing before the URL change
if __name__ == "__main__":
    load_types_table()


# result = get_type(1)
# print(result)

# count_type_result = count_type_num()
# print(count_type_result)

# Get number of types
# def count_type_num() -> dict:
#     total_types = f"https://pokeapi.co/api/v2/type/"
#     type_data = requests.get(total_types).json()
#     return type_data['count']
