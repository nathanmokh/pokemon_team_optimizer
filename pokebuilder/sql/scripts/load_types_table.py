import requests
import logging
from src.pokemon.util.db_utils import execute_sql, get_db_connection, load_sql
from src.pokemon.util.common_utils import get_config


class TypeTableLoader:
    def get_type_name(self, type_data):
        return type_data.get("name")

    def get_type_data(self, type_id: int) -> dict:
        URL = f"https://pokeapi.co/api/v2/type/{type_id}/"
        pokemon_data = requests.get(URL)

        if pokemon_data.status_code != 200:
            print(
                f"Failed to retrieve type with ID {type_id}. HTTP Status Code: {pokemon_data.status_code}"
            )
            return None

        pokemon_data = pokemon_data.json()

        type_name = self.get_type_name(pokemon_data)

        return (
            type_id,
            type_name,
        )

    def get_types(self):
        URL = f"https://pokeapi.co/api/v2/type/"
        response = requests.get(URL)
        if response.status_code != 200:
            print("Failed to retrieve the total count of types.")
            return 0
        temp_data = response.json()

        return temp_data.get("results")  # Returns the names of types from URLs

    def create_rows(self):
        type_ids = []
        data = self.get_types()

        for item in data:
            # Splitting the URL by '/' and picking up the second last element after removing trailing slash (if it exists)
            type_id = int(item["url"].rstrip("/").split("/")[-1])
            type_ids.append(self.get_type_data(type_id))
            print(f"Row created for ID: {type_id}")

        return ", ".join(str(row) for row in type_ids)

    def run(self) -> None:
        execute_sql("create_type_table.sql")
        currently_loaded_type_ids = execute_sql("get_type_id_from_type_table.sql")
        currently_loaded_type_ids = {
            record[0]: None for record in currently_loaded_type_ids
        }

        rows = self.create_rows()

        if rows:
            execute_sql(
                "populate_type_table.sql",
                substitutions={"values": rows},
            )
        else:
            print(f"No rows created.")


if __name__ == "__main__":
    TypeTableLoader().run()
