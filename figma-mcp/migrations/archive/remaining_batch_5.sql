BEGIN;

-- Block 14: Sale Banner - Countdown

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '61d2b980-9205-4f90-9ea7-0e36d6f3b250',
    'Sale Banner - Countdown',
    'Promotional sale banner with countdown timer',
    'sale-banner',
    'e-commerce',
    \$\$\$,
    '{"npm": ["lucide-react"], "components": ["Button", "Badge", "Card"]}'::jsonb,
    '{"type": "object", "properties": {"sale": {"type": "object", "properties": {"title": {"type": "string"}, "subtitle": {"type": "string"}, "description": {"type": "string"}, "discountPercentage": {"type": "number"}, "endDate": {"type": "string"}, "image": {"type": "string"}, "backgroundColor": {"type": "string"}, "textColor": {"type": "string"}}, "required": ["title", "description", "discountPercentage", "endDate"]}, "onShopNow": {"type": "function"}, "compact": {"type": "boolean"}}, "required": ["sale"]}'::jsonb,
    '{"sale": {"title": "Black Friday Sale", "subtitle": "Biggest Sale of the Year", "description": "Get incredible discounts on thousands of products across all categories. From electronics to fashion, home goods to beauty products.", "discountPercentage": 50, "endDate": "2024-11-30T23:59:59Z", "backgroundColor": "#dc2626", "textColor": "#ffffff"}, "compact": False}'::jsonb,
    ARRAY['sale-banner', 'countdown', 'e-commerce', 'promotion', 'urgency'],
    NOW(),
    NOW()
);

-- Block 15: Wishlist Grid

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '88c76892-59b8-4b24-96f9-4a8734fe5068',
    'Wishlist Grid',
    'User wishlist display with product management',
    'wishlist',
    'e-commerce',
    \$\$\$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge"]}'::jsonb,
    '{"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "image": {"type": "string"}, "inStock": {"type": "boolean"}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "addedDate": {"type": "string"}}, "required": ["id", "name", "price", "image", "inStock", "addedDate"]}}, "onRemoveFromWishlist": {"type": "function"}, "onAddToCart": {"type": "function"}, "onShare": {"type": "function"}, "onViewProduct": {"type": "function"}, "emptyMessage": {"type": "string"}}, "required": ["items", "onRemoveFromWishlist", "onAddToCart"]}'::jsonb,
    '{"items": [{"id": "1", "name": "Wireless Noise-Cancelling Headphones", "price": 199.99, "originalPrice": 249.99, "image": "/api/placeholder/300/300", "inStock": True, "rating": 4.5, "reviews": 128, "addedDate": "2024-01-15T10:30:00Z"}, {"id": "2", "name": "Smart Fitness Watch", "price": 299.99, "image": "/api/placeholder/300/300", "inStock": False, "rating": 4.2, "reviews": 89, "addedDate": "2024-01-10T14:20:00Z"}, {"id": "3", "name": "Portable Bluetooth Speaker", "price": 79.99, "originalPrice": 99.99, "image": "/api/placeholder/300/300", "inStock": True, "rating": 4.7, "reviews": 234, "addedDate": "2024-01-05T09:15:00Z"}]}'::jsonb,
    ARRAY['wishlist', 'e-commerce', 'favorites', 'user-account', 'product-management'],
    NOW(),
    NOW()
);

COMMIT;