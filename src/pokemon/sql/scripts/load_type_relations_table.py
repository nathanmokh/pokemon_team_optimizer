import requests
import logging
from src.pokemon.util.db_utils import execute_sql, get_db_connection, load_sql
from src.pokemon.util.common_utils import get_config


def load_type_relations_table():
    def get_type_id_by_name(type_name, all_types_map):
        return all_types_map[type_name]

    def populate_relations(
        source_type_id, target_type_names, effectiveness, all_types_map
    ):
        relations = []
        for type_name in target_type_names:
            target_type_id = get_type_id_by_name(type_name, all_types_map)
            relations.append((source_type_id, target_type_id, effectiveness))
        return relations

    def get_all_type_ids():
        results = execute_sql("get_all_type_ids_and_names.sql")
        return {record[1]: record[0] for record in results}

    def create_rows():
        rows = []
        for relation in total_relations:
            source_type_id, target_type_id, effectiveness = relation
            rows.append(f"({source_type_id}, {target_type_id}, {effectiveness})")
        return ", ".join(rows)

    all_types_map = get_all_type_ids()

    total_relations = []
    for type_name, type_id in all_types_map.items():
        URL = f"https://pokeapi.co/api/v2/type/{type_name}/"
        response = requests.get(URL)

        if response.status_code != 200:
            print(f"Failed to retrieve type details for {type_name}.")
            continue

        type_data = response.json()

        damage_relations = type_data["damage_relations"]
        total_relations.extend(
            populate_relations(
                type_id,
                [
                    type_info["name"]
                    for type_info in damage_relations["double_damage_to"]
                ],
                2.0,
                all_types_map,
            )
        )
        total_relations.extend(
            populate_relations(
                type_id,
                [type_info["name"] for type_info in damage_relations["half_damage_to"]],
                0.5,
                all_types_map,
            )
        )
        total_relations.extend(
            populate_relations(
                type_id,
                [type_info["name"] for type_info in damage_relations["no_damage_to"]],
                0.0,
                all_types_map,
            )
        )

    execute_sql("create_type_relations_table.sql", is_ddl_statement=True)

    rows = create_rows()

    if rows:
        execute_sql(
            "populate_type_relations_table.sql",
            substitutions={"values": rows},
            is_ddl_statement=True,
        )


if __name__ == "__main__":
    load_type_relations_table()
