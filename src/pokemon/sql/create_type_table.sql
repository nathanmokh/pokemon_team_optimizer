CREATE TABLE IF NOT EXISTS types (
    type_id INTEGER PRIMARY KEY,
    type_name VARCHAR(20),
    double_damage_from VARCHAR(70), 
    double_damage_to VARCHAR(70),
    half_damage_to VARCHAR(70),
    half_damage_from VARCHAR(70)
);