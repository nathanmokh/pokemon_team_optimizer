SELECT
    p.pokemon_name,
    m.move_name,
    m.move_type,
    pmm.learn_method,
    p.type_1 AS "pokemon type",
    p.type_2 AS "pokemon_type_2",
    pmm.level_learned,
    m.power,
    m.pp,
    m.accuracy,
    m.category,
    m.crit_rate,
    m.damage_class
FROM
    pokemon p
    JOIN pokemonmovesmapping pmm ON p.id = pmm.pokemon_id
    JOIN moves m ON m.move_id = pmm.move_id
WHERE
    p.id = {pokemon_id}
    AND pmm.game_version = {game_version}
ORDER BY
    pmm.level_learned;