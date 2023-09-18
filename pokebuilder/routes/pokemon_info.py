from flask import abort
from flask import jsonify, Blueprint
from flask import request

from pokebuilder.services.pokemon_services import (
    get_pokemon_moveset_endpoint,
    get_pokemon_stats,
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


@pokemon_routes.route("/api/pokemon/getStats")
def get_pokemon_stats_endpoint():
    args = request.args
    pokemon_id = args.get("pokemon_id")
    pokemon_name = args.get("pokemon_name")
    base_stats = args.get("base_stats") == "true"
    hp_iv = int(args.get("hp_iv"))
    hp_ev = int(args.get("hp_ev"))
    attack_iv = int(args.get("attack_iv"))
    attack_ev = int(args.get("attack_ev"))
    defense_iv = int(args.get("defense_iv"))
    defense_ev = int(args.get("defense_ev"))
    special_attack_iv = int(args.get("special_attack_iv"))
    special_attack_ev = int(args.get("special_attack_ev"))
    special_defense_iv = int(args.get("special_defense_iv"))
    special_defense_ev = int(args.get("special_defense_ev"))
    speed_iv = int(args.get("speed_iv"))
    speed_ev = int(args.get("speed_ev"))
    level = int(args.get("level"))
    nature = args.get("nature")

    return create_api_response(
        get_pokemon_stats(
            pokemon_id=pokemon_id,
            pokemon_name=pokemon_name,
            base_stats=base_stats,
            hp_iv=hp_iv,
            hp_ev=hp_ev,
            attack_iv=attack_iv,
            attack_ev=attack_ev,
            defense_iv=defense_iv,
            defense_ev=defense_ev,
            special_attack_iv=special_attack_iv,
            special_attack_ev=special_attack_ev,
            special_defense_iv=special_defense_iv,
            special_defense_ev=special_defense_ev,
            speed_iv=speed_iv,
            speed_ev=speed_ev,
            level=level,
            nature=nature,
        )
    )
