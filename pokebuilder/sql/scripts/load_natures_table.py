import requests
import logging
from src.pokemon.util.db_utils import execute_sql, get_db_connection, load_sql
from src.pokemon.util.common_utils import get_config


class NatureTableLoader:
    def get_increased_stat(self, nature_data):
        increased_stat = nature_data.get("increased_stat")
        return increased_stat["name"] if increased_stat else "NULL"

    def get_decreased_stat(self, nature_data):
        decreased_stat = nature_data.get("decreased_stat")
        return decreased_stat["name"] if decreased_stat else "NULL"

    def get_name(self, nature_data):
        return nature_data.get("name")

    def get_total_natures(self):
        URL = f"https://pokeapi.co/api/v2/nature/"
        response = requests.get(URL)
        if response.status_code != 200:
            print("Failed to retrieve the total count of natures.")
            return 0
        temp_data = response.json()

        return temp_data.get("count")

    def create_rows(self):
        rows = []
        for nature_id in range(1, self.get_total_natures() + 1):
            if nature_id in self.currently_loaded_nature_ids:
                continue
            rows.append(self.get_nature(nature_id))
            print(f"Row created for nature {nature_id}")

        return ", ".join(str(row) for row in rows)

    def get_nature(self, nature_id: int) -> dict:
        URL = f"https://pokeapi.co/api/v2/nature/{nature_id}/"
        response = requests.get(URL)

        if response.status_code != 200:
            print(
                f"Failed to retrieve nature with ID {nature_id}. HTTP Status Code: {response.status_code}"
            )
            return None

        nature_data = response.json()

        increased_stat = self.get_increased_stat(nature_data)
        decreased_stat = self.get_decreased_stat(nature_data)
        name = self.get_name(nature_data)

        return (nature_id, name, increased_stat, decreased_stat)

    def run(self):
        execute_sql("create_nature_table.sql")
        self.currently_loaded_nature_ids = execute_sql(
            "get_nature_ids_from_nature_table.sql"
        )
        self.currently_loaded_nature_ids = {
            record[0]: None for record in self.currently_loaded_nature_ids
        }

        rows = self.create_rows()

        if rows:
            execute_sql("populate_nature_table.sql", substitutions={"values": rows})


if __name__ == "__main__":
    NatureTableLoader().run()
