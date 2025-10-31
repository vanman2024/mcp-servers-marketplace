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