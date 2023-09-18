from flask import abort
from sqlalchemy.orm import aliased
from sqlalchemy import and_
from extensions import db
from pokebuilder.sql.models.moves import Moves
from pokebuilder.sql.models.moves_mapping import PokemonMovesMapping
from pokebuilder.sql.models.pokemon import Pokemon
from pokebuilder.sql.models.stats import Stats
from services.stats_services import StatsCalculator
from src.pokemon.util.common_utils import get_current_number_of_pokemon_pokeapi
import random


# Define aliases for the table names
pokemon_alias = aliased(Pokemon)
pmm_alias = aliased(PokemonMovesMapping)
moves_alias = aliased(Moves)
stats_alias = aliased(Stats)


def get_pokemon_moveset_endpoint(pokemon_id, game_version):
    query = (
        db.session.query(
            Pokemon.pokemon_name,
            moves_alias.move_name,
            moves_alias.move_type,
            pmm_alias.learn_method,
            Pokemon.type_1.label("pokemon type"),
            Pokemon.type_2.label("pokemon_type_2"),
            pmm_alias.level_learned,
            moves_alias.power,
            moves_alias.pp,
            moves_alias.accuracy,
            moves_alias.category,
            moves_alias.crit_rate,
            moves_alias.damage_class,
        )
        .join(pmm_alias, Pokemon.id == pmm_alias.pokemon_id)
        .join(moves_alias, moves_alias.move_id == pmm_alias.move_id)
        .filter(and_(Pokemon.id == pokemon_id, pmm_alias.game_version == game_version))
        .order_by(pmm_alias.level_learned)
    )

    result = query.all()
    # Convert the result tuples to dictionaries using _asdict(), each key corresponds to the col name
    result_dicts = [row._asdict() for row in result]
    return {"count": len(result), "data": result_dicts}


def get_random_pokemon():
    pokemon_id = random.randint(1, get_current_number_of_pokemon_pokeapi())

    query = (
        db.session.query(
            Pokemon.pokemon_name,
            Pokemon.type_1.label("pokemon type"),
            Pokemon.type_2.label("pokemon_type_2"),
            stats_alias.hp,
            stats_alias.attack,
            stats_alias.special_attack,
            stats_alias.defense,
            stats_alias.special_defense,
            stats_alias.speed,
        )
        .join(stats_alias, stats_alias.pokemon_id == Pokemon.id)
        .filter(Pokemon.id == pokemon_id)
    )

    result = query.all()

    if not result:
        abort(500, "No pokemon in database")

    result = result[0]
    return result._asdict()


def get_random_team():
    pokemon_names = []
    ret = []
    while len(ret) < 6:
        random_pokemon = get_random_pokemon()
        if random_pokemon["pokemon_name"] not in pokemon_names:
            ret.append(random_pokemon)
            pokemon_names.append(random_pokemon["pokemon_name"])
    return ret


def get_pokemon_stats(
    pokemon_id=None,
    pokemon_name=None,
    base_stats=False,
    hp_iv=0,
    hp_ev=0,
    attack_iv=0,
    attack_ev=0,
    defense_iv=0,
    defense_ev=0,
    special_attack_iv=0,
    special_attack_ev=0,
    special_defense_iv=0,
    special_defense_ev=0,
    speed_iv=0,
    speed_ev=0,
    level=100,
):
    
    # First get the base stats for the given pokemon
    if not pokemon_id and not pokemon_name:
        raise ValueError

    if pokemon_id:
        query = db.session.query(
            Stats.hp,
            Stats.attack,
            Stats.special_attack,
            Stats.defense,
            Stats.special_defense,
            Stats.speed,
        ).filter(Stats.pokemon_id == pokemon_id)

        results = query.all()

        if not results:
            abort(500, "No pokemon in database")

        results = results[0]
        results = results._asdict()

    elif pokemon_name and not pokemon_id:
        query = db.session.query(
            Stats.hp,
            Stats.attack,
            Stats.special_attack,
            Stats.defense,
            Stats.special_defense,
            Stats.speed,
        ).filter(Stats.pokemon_id == pokemon_id)

        results = query.all()

        if not results:
            abort(500, "No pokemon in database")

        results = results[0]
        results = results._asdict()

    # if only base stats are being requested, just return those
    if base_stats:
        return results

    # run calculations for EVs and IVs and level
    if pokemon_id:
        StatsCalculator().calculate_stats()
