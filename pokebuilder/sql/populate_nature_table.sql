INSERT INTO nature(id, name, increased_stat, decreased_stat)
VALUES {values}
ON CONFLICT (id)
DO NOTHING;
