from sqlalchemy.orm import aliased
from sqlalchemy import and_
from extensions import db

from pokebuilder.models import Moves, Pokemon, PokemonMovesMapping

# Define aliases for the table names
pokemon_alias = aliased(Pokemon)
pmm_alias = aliased(PokemonMovesMapping)
moves_alias = aliased(Moves)


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


# get_pokemon_moveset_query(150, 'yellow')
