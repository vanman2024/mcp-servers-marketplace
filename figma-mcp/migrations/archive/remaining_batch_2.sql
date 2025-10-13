BEGIN;

-- Block 5: Product Detail - Gallery

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '629ed4dc-bd7c-402a-9fe5-d6dc38658ffc',
    'Product Detail - Gallery',
    'Product detail page with image gallery and full information',
    'product-detail',
    'e-commerce',
    \$\$\$,
    '{"npm": ["lucide-react"], "components": ["Button", "Badge", "Tabs"]}'::jsonb,
    '{"type": "object", "properties": {"product": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "description": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "images": {"type": "array", "items": {"type": "string"}}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "inStock": {"type": "boolean"}, "category": {"type": "string"}, "sku": {"type": "string"}, "features": {"type": "array", "items": {"type": "string"}}, "specifications": {"type": "object", "additionalProperties": {"type": "string"}}}, "required": ["id", "name", "description", "price", "images", "rating", "reviews", "inStock", "category", "sku", "features", "specifications"]}, "onAddToCart": {"type": "function"}, "onToggleWishlist": {"type": "function"}, "onShare": {"type": "function"}}, "required": ["product"]}'::jsonb,
    '{"product": {"id": "1", "name": "Professional DSLR Camera", "description": "Capture stunning photos and videos with this professional-grade DSLR camera featuring advanced autofocus and 4K video recording.", "price": 1299.99, "originalPrice": 1599.99, "images": ["/api/placeholder/600/600", "/api/placeholder/600/600", "/api/placeholder/600/600", "/api/placeholder/600/600"], "rating": 4.8, "reviews": 324, "inStock": True, "category": "Electronics", "sku": "CAM-PRO-001", "features": ["24.2MP Full-Frame Sensor", "4K Video Recording at 60fps", "Advanced 45-Point Autofocus", "5-Axis Image Stabilization", "Weather-Sealed Body", "Dual Memory Card Slots"], "specifications": {"Sensor": "Full-Frame CMOS", "Resolution": "24.2 Megapixels", "ISO Range": "100-51200", "Video": "4K 60fps", "Weight": "850g", "Battery Life": "970 shots"}}}'::jsonb,
    ARRAY['product-detail', 'gallery', 'e-commerce', 'specifications'],
    NOW(),
    NOW()
);

-- Block 6: Product Detail - Tabs

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '18fe3dba-e7d7-47e2-aaec-7d63f807743a',
    'Product Detail - Tabs',
    'Product detail with tabbed content sections',
    'product-detail',
    'e-commerce',
    \$\$\$,
    '{"npm": ["lucide-react"], "components": ["Tabs", "Card", "Badge"]}'::jsonb,
    '{"type": "object", "properties": {"product": {"type": "object", "required": ["description", "features", "specifications", "shipping", "warranty"]}, "reviews": {"type": "array", "items": {"type": "object"}}}, "required": ["product"]}'::jsonb,
    '{"product": {"description": "This premium product delivers exceptional performance and reliability for all your needs.", "features": ["Advanced technology integration", "Energy efficient design", "Durable construction", "User-friendly interface"], "specifications": {"Dimensions": "10 x 8 x 6 inches", "Weight": "2.5 lbs", "Material": "Aluminum alloy", "Power": "USB-C charging"}, "shipping": {"methods": [{"name": "Standard Shipping", "price": "$5.99", "duration": "5-7 business days"}, {"name": "Express Shipping", "price": "$12.99", "duration": "2-3 business days"}, {"name": "Next Day", "price": "$24.99", "duration": "1 business day"}], "returns": "30-day return policy. Items must be in original condition."}, "warranty": {"period": "2 Year Limited Warranty", "coverage": ["Manufacturing defects", "Component failures", "Free repairs or replacement"]}}}'::jsonb,
    ARRAY['product-detail', 'tabs', 'e-commerce', 'reviews', 'specifications'],
    NOW(),
    NOW()
);

-- Block 7: Shopping Cart - Sidebar

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'b7f50239-7202-4f9e-ab0b-c628b0be49b9',
    'Shopping Cart - Sidebar',
    'Slide-out shopping cart sidebar with items and checkout',
    'shopping-cart',
    'e-commerce',
    \$\$\$,
    '{"npm": ["lucide-react"], "components": ["Sheet", "Button", "Separator"]}'::jsonb,
    '{"type": "object", "properties": {"isOpen": {"type": "boolean"}, "onClose": {"type": "function"}, "items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "quantity": {"type": "number"}, "image": {"type": "string"}, "variant": {"type": "string"}}, "required": ["id", "name", "price", "quantity", "image"]}}, "onUpdateQuantity": {"type": "function"}, "onRemoveItem": {"type": "function"}, "onCheckout": {"type": "function"}}, "required": ["isOpen", "onClose", "items", "onUpdateQuantity", "onRemoveItem", "onCheckout"]}'::jsonb,
    '{"isOpen": True, "items": [{"id": "1", "name": "Wireless Mouse", "price": 29.99, "quantity": 2, "image": "/api/placeholder/80/80", "variant": "Black"}, {"id": "2", "name": "USB-C Cable", "price": 12.99, "quantity": 1, "image": "/api/placeholder/80/80"}]}'::jsonb,
    ARRAY['shopping-cart', 'sidebar', 'e-commerce', 'checkout'],
    NOW(),
    NOW()
);

COMMIT;