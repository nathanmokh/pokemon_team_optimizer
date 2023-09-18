INSERT INTO 
    type_relations (
        source_type_id, 
        target_type_id, 
        effectiveness
    )
VALUES 
{values}
ON CONFLICT(source_type_id, target_type_id) DO NOTHING;