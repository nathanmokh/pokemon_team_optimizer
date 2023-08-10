CREATE TABLE IF NOT EXISTS stats (
    pokemon_id INTEGER PRIMARY KEY,
    hp INTEGER,
    attack INTEGER,
    defense INTEGER,
    sp_attack INTEGER,
    sp_defense INTEGER,
    speed INTEGER,
    generation INTEGER
);

INSERT INTO stats 
    (pokemon_id, hp, attack, defense, sp_attack, sp_defense, speed) 
VALUES {values};