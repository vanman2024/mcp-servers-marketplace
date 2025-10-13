
INSERT INTO figma_components (
    figma_id, name, description, category_id, figma_url, component_type,
    tags, complexity_score, popularity_score, props, figma_node_type,
    width, height, status, last_synced
) VALUES 
(
    '4:5685',
    'icon/zap-off',
    '',
    'baf047c3-c1e5-4885-bab2-9c7e636f629b',
    'https://www.figma.com/file/JGMQqO02q6wLSyk29RDsgh?node-id=4%3A5685',
    'icon',
    ARRAY['icon'],
    1,
    0,
    '{"fills": [{"blendMode": "NORMAL", "visible": false, "type": "SOLID", "color": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0}}]}'::jsonb,
    'COMPONENT',
    24.0,
    24.0,
    'active',
    '2025-07-14T01:37:30.770787+00:00'::timestamptz
),(
    '4:5686',
    'icon/zap',
    '',
    'baf047c3-c1e5-4885-bab2-9c7e636f629b',
    'https://www.figma.com/file/JGMQqO02q6wLSyk29RDsgh?node-id=4%3A5686',
    'icon',
    ARRAY['icon'],
    1,
    0,
    '{"fills": [{"blendMode": "NORMAL", "visible": false, "type": "SOLID", "color": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0}}]}'::jsonb,
    'COMPONENT',
    24.0,
    24.0,
    'active',
    '2025-07-14T01:37:30.770842+00:00'::timestamptz
),(
    '4:5687',
    'icon/zoom-in',
    '',
    'baf047c3-c1e5-4885-bab2-9c7e636f629b',
    'https://www.figma.com/file/JGMQqO02q6wLSyk29RDsgh?node-id=4%3A5687',
    'icon',
    ARRAY['icon'],
    1,
    0,
    '{"fills": [{"blendMode": "NORMAL", "visible": false, "type": "SOLID", "color": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0}}]}'::jsonb,
    'COMPONENT',
    24.0,
    24.0,
    'active',
    '2025-07-14T01:37:30.770852+00:00'::timestamptz
),(
    '4:5688',
    'icon/zoom-out',
    '',
    'baf047c3-c1e5-4885-bab2-9c7e636f629b',
    'https://www.figma.com/file/JGMQqO02q6wLSyk29RDsgh?node-id=4%3A5688',
    'icon',
    ARRAY['icon'],
    1,
    0,
    '{"fills": [{"blendMode": "NORMAL", "visible": false, "type": "SOLID", "color": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0}}]}'::jsonb,
    'COMPONENT',
    24.0,
    24.0,
    'active',
    '2025-07-14T01:37:30.770865+00:00'::timestamptz
)
ON CONFLICT (figma_id) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    last_synced = EXCLUDED.last_synced;
