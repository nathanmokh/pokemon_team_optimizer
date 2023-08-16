CREATE TYPE category_enum AS ENUM ('damage', 'ailment');
CREATE TYPE dmg_class_enum AS ENUM ('physical', 'special');

CREATE TABLE IF NOT EXISTS moves (
    move_id INTEGER PRIMARY KEY,
    move_name VARCHAR(32),
    move_type VARCHAR(16),
    power INTEGER,
    accuracy INTEGER,
    is_hm BOOLEAN,
    is_tm BOOLEAN,
    pp INTEGER,
    priority INTEGER,
    description VARCHAR(512),
    effect_chance INTEGER,
    effect VARCHAR(16),
    ailment VARCHAR(16),
    healing_percentage INTEGER,
    damage_class dmg_class_enum,
    category category_enum,
    crit_rate INTEGER,
    stat_chance INTEGER,
    -- percent chance a stat change is caused to the target pokemon
    drain INTEGER,
    -- HP drain (if positive) or Recoil damage (if negative), in percent of damage done.
    past_values JSON -- A move resource value changes across version groups of the game.
);