import psycopg2
import os
import yaml
from jinja2 import Template



def get_db_connection():
    """returns a psycopg2 connection object to the database in config
    """
    
    with open(f"config/{os.environ.get('ENV')}.yaml", "r") as f:
        template = Template(f.read())
        rendered_yaml = template.render(DB_PASSWORD=os.environ.get('DB_PASSWORD'))
    config = yaml.safe_load(rendered_yaml)

    return psycopg2.connect(
        dbname=config['db']['dbname'],
        user=config['db']['user'],
        password=config['db']['password'],
        host=config['db']['host']
    )
    
def load_sql(filename: str) -> str:
    
    with open(f"pokemon/sql/{filename}", "r") as sql_file:
        return sql_file.read()

def load_to_stats_table(values, connection, cursor):
    if not values:
        return
    values = ", ".join(values)
    cursor = connection.cursor()
    # TODO: substitute with file in sql directory
    query_template = f"""INSERT INTO stats 
    (pokemon_id, hp, attack, defense, sp_attack, sp_defense, speed) 
    VALUES {values};"""
    cursor.execute(query_template)
    connection.commit()
    