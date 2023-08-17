import requests
import logging
from src.pokemon.util.db_utils import execute_sql, get_db_connection, load_sql
from src.pokemon.util.common_utils import get_config

def load_natures_table():

    def get_increased_stat(nature_data):
        return nature_data.get("increased_stat", "NULL")
        
    def get_decreased_stat(nature_data):
        return nature_data.get("decreased_stat", "NULL")

    def get_name(nature_data):
        return nature_data.get("name", "NULL")
    
    def create_rows():
        rows = []
        for nature_id in range(1, config["num_natures"] + 1):
            if nature_id in currently_loaded_nature_ids:
                continue
            rows.append(get_nature(nature_id))
            print(f"Row created for nature {nature_id}")

        return ", ".join(str(row) for row in rows)