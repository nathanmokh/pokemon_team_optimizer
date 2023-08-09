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