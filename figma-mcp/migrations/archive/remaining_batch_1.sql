BEGIN;

-- Block 2: Product Grid - 4 Column

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '206563cb-1843-4d5d-8865-e8362a9f682f',
    'Product Grid - 4 Column',
    'Responsive 4-column product grid for larger displays',
    'product-grid',
    'e-commerce',
    \$\$\$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge"]}'::jsonb,
    '{"type": "object", "properties": {"products": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "image": {"type": "string"}, "category": {"type": "string"}, "isNew": {"type": "boolean"}, "discount": {"type": "number"}}, "required": ["id", "name", "price", "image", "category"]}}, "onAddToCart": {"type": "function"}, "onToggleWishlist": {"type": "function"}}, "required": ["products"]}'::jsonb,
    '{"products": [{"id": "1", "name": "Premium Wireless Mouse", "price": 39.99, "originalPrice": 59.99, "image": "/api/placeholder/300/300", "category": "Accessories", "discount": 33}, {"id": "2", "name": "USB-C Hub 7-in-1", "price": 49.99, "image": "/api/placeholder/300/300", "category": "Adapters", "isNew": True}]}'::jsonb,
    ARRAY['responsive', 'accessible', 'e-commerce', 'products', 'grid', 'wishlist'],
    NOW(),
    NOW()
);

-- Block 3: Product Card - Simple

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'ae1e2cdd-d9b9-4274-9c91-230b3d15e751',
    'Product Card - Simple',
    'Simple product card with minimal information',
    'product-card',
    'e-commerce',
    \$\$\$,
    '{"npm": [], "components": ["Card", "Button"]}'::jsonb,
    '{"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "image": {"type": "string"}, "onSelect": {"type": "function"}}, "required": ["id", "name", "price", "image"]}'::jsonb,
    '{"id": "1", "name": "Minimalist Desk Lamp", "price": 89.99, "image": "/api/placeholder/300/300"}'::jsonb,
    ARRAY['simple', 'product', 'card', 'e-commerce'],
    NOW(),
    NOW()
);

-- Block 4: Product Card - Detailed

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'c67eedd6-9721-4d40-a731-74bdd90ba01e',
    'Product Card - Detailed',
    'Detailed product card with full information and actions',
    'product-card',
    'e-commerce',
    \$\$\$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge"]}'::jsonb,
    '{"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "description": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "image": {"type": "string"}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "inStock": {"type": "boolean"}, "tags": {"type": "array", "items": {"type": "string"}}, "onAddToCart": {"type": "function"}, "onToggleWishlist": {"type": "function"}, "onQuickView": {"type": "function"}}, "required": ["id", "name", "description", "price", "image", "rating", "reviews", "inStock"]}'::jsonb,
    '{"id": "1", "name": "Professional Camera Lens", "description": "High-quality 50mm f/1.8 prime lens perfect for portrait photography", "price": 399.99, "originalPrice": 499.99, "image": "/api/placeholder/300/300", "rating": 4.7, "reviews": 156, "inStock": True, "tags": ["Photography", "Prime Lens", "Professional"]}'::jsonb,
    ARRAY['detailed', 'product', 'card', 'e-commerce', 'ratings'],
    NOW(),
    NOW()
);

COMMIT;