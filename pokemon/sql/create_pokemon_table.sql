CREATE TABLE IF NOT EXISTS pokemon (
    id INTEGER PRIMARY KEY,
    pokemon_name VARCHAR(50),
    type_1 VARCHAR(10),
    type_2 VARCHAR(10),
    team_role VARCHAR(10),
    official_artwork VARCHAR(120),
    official_artwork_shiny VARCHAR(120)
);