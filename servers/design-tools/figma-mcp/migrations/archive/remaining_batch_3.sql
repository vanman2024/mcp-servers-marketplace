BEGIN;

-- Block 8: Shopping Cart - Page

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '410f9959-fceb-4026-9b59-dc8ca7b4e21a',
    'Shopping Cart - Page',
    'Full page shopping cart with detailed item management',
    'shopping-cart',
    'e-commerce',
    \$\$\$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Input", "Separator", "Badge"]}'::jsonb,
    '{"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "description": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "quantity": {"type": "number"}, "image": {"type": "string"}, "variant": {"type": "string"}, "inStock": {"type": "boolean"}}, "required": ["id", "name", "description", "price", "quantity", "image", "inStock"]}}, "onUpdateQuantity": {"type": "function"}, "onRemoveItem": {"type": "function"}, "onApplyCoupon": {"type": "function"}, "onCheckout": {"type": "function"}, "appliedCoupon": {"type": "object", "properties": {"code": {"type": "string"}, "discount": {"type": "number"}}}}, "required": ["items", "onUpdateQuantity", "onRemoveItem", "onApplyCoupon", "onCheckout"]}'::jsonb,
    '{"items": [{"id": "1", "name": "Wireless Keyboard", "description": "Bluetooth mechanical keyboard with RGB backlighting", "price": 89.99, "originalPrice": 119.99, "quantity": 1, "image": "/api/placeholder/128/128", "variant": "Cherry MX Blue", "inStock": True}]}'::jsonb,
    ARRAY['shopping-cart', 'page', 'e-commerce', 'checkout', 'order-summary'],
    NOW(),
    NOW()
);

-- Block 9: Checkout - Single Page

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '998a9f37-69e3-47e6-8172-b766a196b4ac',
    'Checkout - Single Page',
    'Complete single-page checkout with all steps',
    'checkout',
    'e-commerce',
    \$\$\$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Input", "Label", "Checkbox", "RadioGroup", "Separator"]}'::jsonb,
    '{"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "quantity": {"type": "number"}, "image": {"type": "string"}}, "required": ["id", "name", "price", "quantity", "image"]}}, "onPlaceOrder": {"type": "function"}}, "required": ["items", "onPlaceOrder"]}'::jsonb,
    '{"items": [{"id": "1", "name": "Wireless Headphones", "price": 79.99, "quantity": 1, "image": "/api/placeholder/64/64"}, {"id": "2", "name": "Phone Case", "price": 24.99, "quantity": 2, "image": "/api/placeholder/64/64"}]}'::jsonb,
    ARRAY['checkout', 'single-page', 'e-commerce', 'payment', 'shipping'],
    NOW(),
    NOW()
);

-- Block 10: Order Summary - Card

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '6e35673b-5566-4b8d-86ed-61976085c8f7',
    'Order Summary - Card',
    'Compact order summary card for checkout and review',
    'order-summary',
    'e-commerce',
    \$\$\$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge", "Separator"]}'::jsonb,
    '{"type": "object", "properties": {"order": {"type": "object", "properties": {"id": {"type": "string"}, "status": {"type": "string", "enum": ["pending", "confirmed", "shipped", "delivered"]}, "date": {"type": "string"}, "total": {"type": "number"}, "subtotal": {"type": "number"}, "shipping": {"type": "number"}, "tax": {"type": "number"}, "items": {"type": "array"}, "shipping_address": {"type": "object"}, "estimated_delivery": {"type": "string"}}, "required": ["id", "status", "date", "total", "subtotal", "shipping", "tax", "items", "shipping_address"]}, "onTrackOrder": {"type": "function"}, "onViewDetails": {"type": "function"}}, "required": ["order"]}'::jsonb,
    '{"order": {"id": "ORD-2024-001", "status": "shipped", "date": "2024-01-15T10:30:00Z", "total": 124.97, "subtotal": 109.98, "shipping": 5.99, "tax": 8.8, "items": [{"id": "1", "name": "Wireless Mouse", "quantity": 2, "price": 29.99, "image": "/api/placeholder/48/48"}, {"id": "2", "name": "USB Cable", "quantity": 1, "price": 49.99, "image": "/api/placeholder/48/48"}], "shipping_address": {"name": "John Doe", "address": "123 Main St", "city": "Anytown", "postal_code": "12345"}, "estimated_delivery": "2024-01-20T00:00:00Z"}}'::jsonb,
    ARRAY['order-summary', 'card', 'e-commerce', 'tracking', 'delivery'],
    NOW(),
    NOW()
);

COMMIT;