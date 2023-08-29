CREATE TABLE
    IF NOT EXISTS stats (
        pokemon_id INTEGER PRIMARY KEY,
        hp INTEGER,
        attack INTEGER,
        defense INTEGER,
        special_attack INTEGER,
        special_defense INTEGER,
        speed INTEGER
    );