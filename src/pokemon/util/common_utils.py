from jinja2 import Template
import yaml
import os
import requests
from urllib.parse import urlparse


def get_config():
    with open(f"src/config/{os.environ.get('ENV')}.yaml", "r") as f:
        template = Template(f.read())
        rendered_yaml = template.render(DB_PASSWORD=os.environ.get("DB_PASSWORD"))
    return yaml.safe_load(rendered_yaml)


def get_current_number_of_pokemon_pokeapi() -> int:
    """Gets the current number of pokemon from pokeapi"""
    return int(
        requests.get("https://pokeapi.co/api/v2/pokemon-species/").json()["count"]
    )


def parse_id_from_end_of_url(url):
    url = url.rstrip("/")  # Remove any trailing slashes
    parsed_url = urlparse(url)
    path = parsed_url.path
    return path.split("/")[-1]


def make_request():
    pass
