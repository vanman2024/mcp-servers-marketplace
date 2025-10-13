BEGIN;

-- Block 11: Product Reviews - List

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '4c432e92-1368-43b6-97b8-96ab6870dd35',
    'Product Reviews - List',
    'Product reviews list with ratings and filtering',
    'product-reviews',
    'e-commerce',
    \$\$\$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge", "Progress", "Tabs"]}'::jsonb,
    '{"type": "object", "properties": {"productName": {"type": "string"}, "averageRating": {"type": "number"}, "totalReviews": {"type": "number"}, "ratingDistribution": {"type": "object", "properties": {"5": {"type": "number"}, "4": {"type": "number"}, "3": {"type": "number"}, "2": {"type": "number"}, "1": {"type": "number"}}, "required": ["5", "4", "3", "2", "1"]}, "reviews": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "author": {"type": "string"}, "rating": {"type": "number"}, "title": {"type": "string"}, "content": {"type": "string"}, "date": {"type": "string"}, "verified": {"type": "boolean"}, "helpful": {"type": "number"}, "images": {"type": "array", "items": {"type": "string"}}}, "required": ["id", "author", "rating", "title", "content", "date", "verified", "helpful"]}}, "onWriteReview": {"type": "function"}, "onHelpfulVote": {"type": "function"}}, "required": ["productName", "averageRating", "totalReviews", "ratingDistribution", "reviews"]}'::jsonb,
    '{"productName": "Wireless Headphones", "averageRating": 4.3, "totalReviews": 89, "ratingDistribution": {"5": 42, "4": 23, "3": 15, "2": 6, "1": 3}, "reviews": [{"id": "1", "author": "Sarah Johnson", "rating": 5, "title": "Excellent sound quality!", "content": "These headphones exceeded my expectations. The sound quality is crystal clear and the noise cancellation works perfectly.", "date": "2024-01-15T00:00:00Z", "verified": True, "helpful": 12, "images": ["/api/placeholder/64/64"]}, {"id": "2", "author": "Mike Chen", "rating": 4, "title": "Good value for money", "content": "Solid headphones for the price. Battery life is impressive and they"re comfortable for long listening sessions.", "date": "2024-01-10T00:00:00Z", "verified": True, "helpful": 8}]}'::jsonb,
    ARRAY['product-reviews', 'ratings', 'e-commerce', 'feedback', 'social-proof'],
    NOW(),
    NOW()
);

-- Block 12: Product Filter - Sidebar

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'e857d627-59e8-4a74-bf00-78f09bfff70d',
    'Product Filter - Sidebar',
    'Advanced product filtering sidebar with multiple filter types',
    'product-filter',
    'e-commerce',
    \$\$\$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Checkbox", "Label", "Slider", "Badge", "Collapsible"]}'::jsonb,
    '{"type": "object", "properties": {"filters": {"type": "object", "properties": {"categories": {"type": "array", "items": {"type": "string"}}, "brands": {"type": "array", "items": {"type": "string"}}, "priceRange": {"type": "array", "items": {"type": "number"}}, "ratings": {"type": "array", "items": {"type": "number"}}, "inStock": {"type": "boolean"}, "onSale": {"type": "boolean"}}}, "onFiltersChange": {"type": "function"}, "onClearFilters": {"type": "function"}, "availableFilters": {"type": "object"}, "resultCount": {"type": "number"}}, "required": ["filters", "onFiltersChange", "onClearFilters", "availableFilters", "resultCount"]}'::jsonb,
    '{"filters": {"categories": ["electronics"], "brands": [], "priceRange": [0, 1000], "ratings": [4, 5], "inStock": True, "onSale": False}, "resultCount": 42, "availableFilters": {"categories": [{"id": "electronics", "name": "Electronics", "count": 156}, {"id": "clothing", "name": "Clothing", "count": 89}, {"id": "books", "name": "Books", "count": 234}], "brands": [{"id": "apple", "name": "Apple", "count": 45}, {"id": "samsung", "name": "Samsung", "count": 67}], "priceRange": {"min": 0, "max": 2000}}}'::jsonb,
    ARRAY['product-filter', 'sidebar', 'e-commerce', 'search', 'categories'],
    NOW(),
    NOW()
);

-- Block 13: Category Banner

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '2ea0bac5-dd6a-42bf-a641-476166f82f2d',
    'Category Banner',
    'Hero banner for product category pages with navigation',
    'category-banner',
    'e-commerce',
    \$\$\$,
    '{"npm": ["lucide-react"], "components": ["Button", "Badge"]}'::jsonb,
    '{"type": "object", "properties": {"category": {"type": "object", "properties": {"name": {"type": "string"}, "description": {"type": "string"}, "image": {"type": "string"}, "productCount": {"type": "number"}, "featured": {"type": "boolean"}, "trending": {"type": "boolean"}}, "required": ["name", "description", "image", "productCount"]}, "subcategories": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "image": {"type": "string"}, "productCount": {"type": "number"}}, "required": ["id", "name", "image", "productCount"]}}, "onExploreCategory": {"type": "function"}, "onSelectSubcategory": {"type": "function"}}, "required": ["category"]}'::jsonb,
    '{"category": {"name": "Electronics", "description": "Discover the latest technology and gadgets from top brands. From smartphones to smart home devices, find everything you need to stay connected and productive.", "image": "/api/placeholder/800/400", "productCount": 1247, "featured": True, "trending": True}, "subcategories": [{"id": "smartphones", "name": "Smartphones", "image": "/api/placeholder/200/200", "productCount": 156}, {"id": "laptops", "name": "Laptops", "image": "/api/placeholder/200/200", "productCount": 89}, {"id": "headphones", "name": "Headphones", "image": "/api/placeholder/200/200", "productCount": 234}, {"id": "cameras", "name": "Cameras", "image": "/api/placeholder/200/200", "productCount": 67}, {"id": "gaming", "name": "Gaming", "image": "/api/placeholder/200/200", "productCount": 178}, {"id": "accessories", "name": "Accessories", "image": "/api/placeholder/200/200", "productCount": 523}]}'::jsonb,
    ARRAY['category-banner', 'hero', 'e-commerce', 'navigation', 'subcategories'],
    NOW(),
    NOW()
);

COMMIT;