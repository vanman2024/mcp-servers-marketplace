BEGIN;

Product Grid - 3 Column
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'a7149163-135c-4ab2-ab01-bf0bc7240780',
    'Product Grid - 3 Column',
    'Responsive 3-column product grid with hover effects',
    'product-grid',
    'e-commerce',
    $$1$$import React from 'react';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Star, ShoppingCart } from 'lucide-react';

interface Product {
  id: string;
  name: string;
  price: number;
  image: string;
  rating: number;
  reviews: number;
  badge?: string;
}

interface ProductGrid3ColumnProps {
  products: Product[];
  onAddToCart?: (productId: string) => void;
  onProductClick?: (productId: string) => void;
}

export function ProductGrid3Column({ 
  products, 
  onAddToCart, 
  onProductClick 
}: ProductGrid3ColumnProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {products.map((product) => (
        <Card key={product.id} className="group cursor-pointer">
          <CardHeader className="p-0 relative overflow-hidden">
            {product.badge && (
              <span className="absolute top-4 left-4 z-10 bg-accent text-accent-foreground px-2 py-1 text-xs font-semibold rounded">
                {product.badge}
              </span>
            )}
            <img
              src={product.image}
              alt={product.name}
              className="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-300"
              onClick={() => onProductClick?.(product.id)}
            />
          </CardHeader>
          <CardContent className="p-4">
            <h3 className="font-semibold text-lg mb-2" onClick={() => onProductClick?.(product.id)}>
              {product.name}
            </h3>
            <div className="flex items-center gap-2 mb-2">
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    className={`w-4 h-4 ${
                      i < Math.floor(product.rating)
                        ? 'fill-primary text-primary'
                        : 'text-muted'
                    }`}
                  />
                ))}
              </div>
              <span className="text-sm text-muted-foreground">
                ({product.reviews})
              </span>
            </div>
            <p className="text-lg font-semibold">${product.price.toFixed(2)}</p>
          </CardContent>
          <CardFooter className="p-4 pt-0">
            <Button
              className="w-full"
              onClick={(e) => {
                e.stopPropagation();
                onAddToCart?.(product.id);
              }}
            >
              <ShoppingCart className="w-4 h-4 mr-2" />
              Add to Cart
            </Button>
          </CardFooter>
        </Card>
      ))}
    </div>
  );
}$$1$$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button"]}',
    '{"type": "object", "properties": {"products": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "image": {"type": "string"}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "badge": {"type": "string"}}, "required": ["id", "name", "price", "image", "rating", "reviews"]}}, "onAddToCart": {"type": "function"}, "onProductClick": {"type": "function"}}, "required": ["products"]}',
    '{"products": [{"id": "1", "name": "Wireless Headphones", "price": 79.99, "image": "/api/placeholder/300/300", "rating": 4.5, "reviews": 234, "badge": "New"}, {"id": "2", "name": "Smart Watch", "price": 299.99, "image": "/api/placeholder/300/300", "rating": 4.8, "reviews": 512}, {"id": "3", "name": "Laptop Stand", "price": 49.99, "image": "/api/placeholder/300/300", "rating": 4.2, "reviews": 89, "badge": "Sale"}]}',
    ARRAY['responsive', 'accessible', 'e-commerce', 'products', 'grid']::text[],
    '2025-07-17T03:50:42.150313',
    '2025-07-17T03:50:42.150422'
);

Product Grid - 4 Column
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '6ec8906a-c0e4-4af2-9d65-a3f2c65ed47b',
    'Product Grid - 4 Column',
    'Responsive 4-column product grid for larger displays',
    'product-grid',
    'e-commerce',
    $$2$$import React from 'react';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Heart, ShoppingCart } from 'lucide-react';

interface Product {
  id: string;
  name: string;
  price: number;
  originalPrice?: number;
  image: string;
  category: string;
  isNew?: boolean;
  discount?: number;
}

interface ProductGrid4ColumnProps {
  products: Product[];
  onAddToCart?: (productId: string) => void;
  onToggleWishlist?: (productId: string) => void;
}

export function ProductGrid4Column({ 
  products, 
  onAddToCart,
  onToggleWishlist 
}: ProductGrid4ColumnProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {products.map((product) => (
        <Card key={product.id} className="group relative">
          <button
            onClick={() => onToggleWishlist?.(product.id)}
            className="absolute top-4 right-4 z-10 p-2 bg-background/80 backdrop-blur rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <Heart className="w-4 h-4" />
          </button>
          
          {(product.isNew || product.discount) && (
            <div className="absolute top-4 left-4 z-10 flex flex-col gap-2">
              {product.isNew && <Badge>New</Badge>}
              {product.discount && (
                <Badge variant="destructive">-{product.discount}%</Badge>
              )}
            </div>
          )}
          
          <CardHeader className="p-0">
            <img
              src={product.image}
              alt={product.name}
              className="w-full h-48 object-cover"
            />
          </CardHeader>
          
          <CardContent className="p-4">
            <p className="text-sm text-muted-foreground mb-1">{product.category}</p>
            <h3 className="font-semibold text-base mb-2 line-clamp-2">{product.name}</h3>
            <div className="flex items-center gap-2">
              <p className="text-lg font-semibold">${product.price.toFixed(2)}</p>
              {product.originalPrice && (
                <p className="text-sm text-muted-foreground line-through">
                  ${product.originalPrice.toFixed(2)}
                </p>
              )}
            </div>
          </CardContent>
          
          <CardFooter className="p-4 pt-0">
            <Button
              size="sm"
              className="w-full"
              onClick={() => onAddToCart?.(product.id)}
            >
              <ShoppingCart className="w-4 h-4 mr-2" />
              Add to Cart
            </Button>
          </CardFooter>
        </Card>
      ))}
    </div>
  );
}$$2$$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge"]}',
    '{"type": "object", "properties": {"products": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "image": {"type": "string"}, "category": {"type": "string"}, "isNew": {"type": "boolean"}, "discount": {"type": "number"}}, "required": ["id", "name", "price", "image", "category"]}}, "onAddToCart": {"type": "function"}, "onToggleWishlist": {"type": "function"}}, "required": ["products"]}',
    '{"products": [{"id": "1", "name": "Premium Wireless Mouse", "price": 39.99, "originalPrice": 59.99, "image": "/api/placeholder/300/300", "category": "Accessories", "discount": 33}, {"id": "2", "name": "USB-C Hub 7-in-1", "price": 49.99, "image": "/api/placeholder/300/300", "category": "Adapters", "isNew": true}]}',
    ARRAY['responsive', 'accessible', 'e-commerce', 'products', 'grid', 'wishlist']::text[],
    '2025-07-17T03:50:42.150440',
    '2025-07-17T03:50:42.150442'
);

Product Card - Simple
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'db7c5b8e-470b-4f98-b254-2c4957b92697',
    'Product Card - Simple',
    'Simple product card with minimal information',
    'product-card',
    'e-commerce',
    $$3$$import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface SimpleProductCardProps {
  id: string;
  name: string;
  price: number;
  image: string;
  onSelect?: () => void;
}

export function SimpleProductCard({ 
  id, 
  name, 
  price, 
  image, 
  onSelect 
}: SimpleProductCardProps) {
  return (
    <Card className="overflow-hidden cursor-pointer hover:shadow-lg transition-shadow" onClick={onSelect}>
      <div className="aspect-square relative">
        <img
          src={image}
          alt={name}
          className="w-full h-full object-cover"
        />
      </div>
      <CardContent className="p-4">
        <h3 className="font-semibold text-base mb-2 line-clamp-1">{name}</h3>
        <div className="flex items-center justify-between">
          <p className="text-lg font-semibold">${price.toFixed(2)}</p>
          <Button size="sm" variant="ghost">
            View
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}$$3$$,
    '{"npm": [], "components": ["Card", "Button"]}',
    '{"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "image": {"type": "string"}, "onSelect": {"type": "function"}}, "required": ["id", "name", "price", "image"]}',
    '{"id": "1", "name": "Minimalist Desk Lamp", "price": 89.99, "image": "/api/placeholder/300/300"}',
    ARRAY['simple', 'product', 'card', 'e-commerce']::text[],
    '2025-07-17T03:50:42.150452',
    '2025-07-17T03:50:42.150454'
);

COMMIT;