CREATE TABLE IF NOT EXISTS moves (
    move_id INTEGER PRIMARY KEY,
    move_name VARCHAR(32),
    move_type VARCHAR(32),
    power INTEGER,
    accuracy INTEGER,
    pp INTEGER,
    priority INTEGER,
    description VARCHAR(512),
    effect_chance INTEGER,
    effect_description VARCHAR(512),
    healing_percentage INTEGER,
    damage_class VARCHAR(32),
    -- replace with enum in future
    category VARCHAR(32),
    -- replace with enum in future 
    crit_rate INTEGER,
    stat_chance INTEGER,
    -- percent chance a stat change is caused to the target pokemon
    drain INTEGER
    -- HP drain (if positive) or Recoil damage (if negative), in percent of damage done.
);