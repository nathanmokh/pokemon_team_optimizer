import psycopg2
import os
import yaml
from jinja2 import Template
from psycopg2.extras import execute_values



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
    
def load_sql(filename: str, values: dict={}) -> str:
    
    with open(f"pokemon/sql/{filename}", "r") as sql_file:
        sql = sql_file.read()
        if values:
            sql = sql.format(**values)
        sql = sql.replace("'NULL'", 'NULL')
        sql = sql.replace('"NULL"', 'NULL')
    return sql
    
def execute_sql(filename: str, substitutions: dict={}, is_ddl_statement: bool=False):
    """Main method for executing sql scripts in the sql directory, DDL statements are statements that 
    don't return rows like a CREATE TABLE statement"""
    
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = load_sql(filename, substitutions)
    try:
        cursor.execute(sql)
        connection.commit()

    except Exception as e:
        print()
        print(e.args[0])
    
    if is_ddl_statement: return
    
    results = cursor.fetchall()
    connection.close()
    return results
    