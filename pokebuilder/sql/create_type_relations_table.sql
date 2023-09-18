CREATE TABLE type_relations (
    source_type_id INTEGER REFERENCES types(type_id),
    target_type_id INTEGER REFERENCES types(type_id),
    effectiveness VARCHAR(255),
    PRIMARY KEY (source_type_id, target_type_id)
);
