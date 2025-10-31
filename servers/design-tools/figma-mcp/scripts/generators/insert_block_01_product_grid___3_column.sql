-- Block 1: Product Grid - 3 Column
-- Description: Responsive 3-column product grid with hover effects
-- Generated: 2025-07-17T03:46:56.378791

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '09599586-33a3-46f8-a3fa-c1af37cb86c9',
    'Product Grid - 3 Column',
    'Responsive 3-column product grid with hover effects',
    'product-grid',
    'e-commerce',
    'import React from ''react'';
import { Card, CardContent, CardFooter, CardHeader } from ''@/components/ui/card'';
import { Button } from ''@/components/ui/button'';
import { Star, ShoppingCart } from ''lucide-react'';

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
                        ? ''fill-primary text-primary''
                        : ''text-muted''
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
}',
    '{"npm": ["lucide-react"], "components": ["Card", "Button"]}',
    '{"type": "object", "properties": {"products": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "image": {"type": "string"}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "badge": {"type": "string"}}, "required": ["id", "name", "price", "image", "rating", "reviews"]}}, "onAddToCart": {"type": "function"}, "onProductClick": {"type": "function"}}, "required": ["products"]}',
    '{"products": [{"id": "1", "name": "Wireless Headphones", "price": 79.99, "image": "/api/placeholder/300/300", "rating": 4.5, "reviews": 234, "badge": "New"}, {"id": "2", "name": "Smart Watch", "price": 299.99, "image": "/api/placeholder/300/300", "rating": 4.8, "reviews": 512}, {"id": "3", "name": "Laptop Stand", "price": 49.99, "image": "/api/placeholder/300/300", "rating": 4.2, "reviews": 89, "badge": "Sale"}]}',
    ARRAY['responsive', 'accessible', 'e-commerce', 'products', 'grid']::text[],
    '2025-07-17T03:46:56.375309',
    '2025-07-17T03:46:56.375324'
);
