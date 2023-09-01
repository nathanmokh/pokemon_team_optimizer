from flask import abort
from flask import jsonify, Blueprint
from flask import request

from pokebuilder.services.pokemon_services import (
    get_pokemon_moveset_endpoint,
    get_random_pokemon,
    get_random_team,
)
from src.pokemon.util.common_utils import create_api_response


pokemon_routes = Blueprint("pokemon_info", __name__)


# Routes


@pokemon_routes.route("/")
def default_endpoint():
    return jsonify(message="Pokebuilder")


@pokemon_routes.route("/api/pokemon/getMoveset")
def get_moves_for_pokemon_endpoint():
    args = request.args
    pokemon_id = args.get("pokemon_id")
    game_version = args.get("game_version")
    if not game_version:
        abort(400, "Missing game_version parameter")
    return get_pokemon_moveset_endpoint(pokemon_id, game_version)


@pokemon_routes.route("/api/pokemon/getRandom")
def get_random_pokemon_endpoint():
    return create_api_response(get_random_pokemon())


@pokemon_routes.route("/api/pokemon/getRandomTeam")
def get_random_pokemon_team_endpoint():
    return create_api_response(get_random_team())
