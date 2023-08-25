import requests
from src.pokemon.util.db_utils import execute_sql
from src.pokemon.util.common_utils import get_current_number_of_pokemon_pokeapi


class SpritesTableLoader:
    def __init__(self) -> None:
        self.create_table_script = "create_sprites_table.sql"
        self.populate_table_script = "populate_sprites_table.sql"
        self.get_pokemon_ids_from_sprites_table_script = (
            "get_currently_loaded_pokemon_sprite_ids.sql"
        )

    def _get_currently_loaded_pokemon_ids(self):
        currently_loaded_pokemon_ids = execute_sql(
            self.get_pokemon_ids_from_sprites_table_script
        )
        if currently_loaded_pokemon_ids:
            return {record[0]: None for record in currently_loaded_pokemon_ids}

    def _get_official_artwork(self, pokemon_data):
        return (
            pokemon_data["sprites"]["other"]["official-artwork"]["front_default"],
            pokemon_data["sprites"]["other"]["official-artwork"]["front_shiny"],
        )

    def _create_rows(self, currently_loaded_pokemon_ids: dict):
        num_pokemon = get_current_number_of_pokemon_pokeapi()
        rows = [
            self._get_sprites(pokemon_id)
            for pokemon_id in range(1, num_pokemon)
            if currently_loaded_pokemon_ids
            and pokemon_id not in currently_loaded_pokemon_ids
        ]
        return ", ".join(str(row) for row in rows)

    def _get_sprites(self, pokemon_id: int) -> dict:
        URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        pokemon_data = requests.get(URL).json()
        official_artwork_default, official_artwork_shiny = self._get_official_artwork(
            pokemon_data
        )

        return pokemon_id

    def run(self):
        execute_sql(self.create_table_script)
        currently_loaded_pokemon_ids = self._get_currently_loaded_pokemon_ids()

        rows = self._create_rows(currently_loaded_pokemon_ids)

        if rows:
            execute_sql(
                self.populate_table_script,
                substitutions={"values": rows},
            )


if __name__ == "__main__":
    SpritesTableLoader().run()
