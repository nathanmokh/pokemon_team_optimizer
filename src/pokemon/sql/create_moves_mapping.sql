CREATE TABLE IF NOT EXISTS pokemonMovesMapping (
    move_id INTEGER,
    pokemon_id INTEGER,
    level_learned INTEGER,
    learn_method VARCHAR(32),
    game_version VARCHAR(32)
);