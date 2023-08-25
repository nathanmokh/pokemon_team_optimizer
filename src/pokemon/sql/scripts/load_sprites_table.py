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
        else:
            return []

    def _get_official_artwork(self, sprites_data):
        return (
            sprites_data["other"]["official-artwork"]["front_default"],
            sprites_data["other"]["official-artwork"]["front_shiny"],
        )

    def _get_default_sprites(self, sprites_data):
        return (
            sprites_data["back_default"],
            sprites_data["back_female"],
            sprites_data["front_default"],
            sprites_data["front_female"],
        )

    def _get_shiny_sprites(self, sprites_data):
        return (
            sprites_data["back_shiny"],
            sprites_data["back_shiny_female"],
            sprites_data["front_shiny"],
            sprites_data["front_shiny_female"],
        )

    def _create_rows(self, currently_loaded_pokemon_ids: dict):
        num_pokemon = get_current_number_of_pokemon_pokeapi()
        rows = [
            self._get_sprites(pokemon_id)
            for pokemon_id in range(1, num_pokemon + 1)
            if pokemon_id not in currently_loaded_pokemon_ids
        ]

        return ", ".join(str(tuple(row.values())) for row in rows)

    def _get_sprites(self, pokemon_id: int) -> dict:
        print(f"Creating sprites table row for pokemon {pokemon_id}.")
        URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        pokemon_data = requests.get(URL)
        if pokemon_data.status_code == 200:
            sprites_data = pokemon_data.json()["sprites"]
        else:
            print(f"Could not retrieve data for pokemon {pokemon_id}, skipping")
            raise Exception("Pokemon could not be found")

        official_artwork_default, official_artwork_shiny = self._get_official_artwork(
            sprites_data
        )
        (
            back_default,
            back_female,
            front_default,
            front_female,
        ) = self._get_default_sprites(sprites_data)
        (
            back_shiny,
            back_shiny_female,
            front_shiny,
            front_shiny_female,
        ) = self._get_shiny_sprites(sprites_data)

        return {
            "pokemon_id": pokemon_id,
            "official_artwork": official_artwork_default,
            "official_artwork_shiny": official_artwork_shiny,
            "back_default": back_default,
            "back_female": back_female if back_female else "NULL",
            "front_default": front_default,
            "front_female": front_female if front_female else "NULL",
            "back_shiny": back_shiny,
            "back_shiny_female": back_shiny_female if back_shiny_female else "NULL",
            "front_shiny": front_shiny,
            "front_shiny_female": front_shiny_female if front_shiny_female else "NULL",
        }

    # TODO potentially in the future, could get sprites for each generation and display them accordingly,
    # not priority right now, but something to consider. - Nathan
    def run(self):
        execute_sql(self.create_table_script)
        currently_loaded_pokemon_ids = self._get_currently_loaded_pokemon_ids()

        rows = self._create_rows(currently_loaded_pokemon_ids)

        if rows:
            execute_sql(
                self.populate_table_script,
                substitutions={"rows": rows},
            )


if __name__ == "__main__":
    SpritesTableLoader().run()
