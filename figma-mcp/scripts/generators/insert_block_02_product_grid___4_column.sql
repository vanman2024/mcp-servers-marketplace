-- Block 2: Product Grid - 4 Column
-- Description: Responsive 4-column product grid for larger displays
-- Generated: 2025-07-17T03:46:56.379203

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'c6d946bc-a5cf-4018-975b-7cf89c0f51f5',
    'Product Grid - 4 Column',
    'Responsive 4-column product grid for larger displays',
    'product-grid',
    'e-commerce',
    'import React from ''react'';
import { Card, CardContent, CardFooter, CardHeader } from ''@/components/ui/card'';
import { Button } from ''@/components/ui/button'';
import { Badge } from ''@/components/ui/badge'';
import { Heart, ShoppingCart } from ''lucide-react'';

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
}',
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge"]}',
    '{"type": "object", "properties": {"products": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "image": {"type": "string"}, "category": {"type": "string"}, "isNew": {"type": "boolean"}, "discount": {"type": "number"}}, "required": ["id", "name", "price", "image", "category"]}}, "onAddToCart": {"type": "function"}, "onToggleWishlist": {"type": "function"}}, "required": ["products"]}',
    '{"products": [{"id": "1", "name": "Premium Wireless Mouse", "price": 39.99, "originalPrice": 59.99, "image": "/api/placeholder/300/300", "category": "Accessories", "discount": 33}, {"id": "2", "name": "USB-C Hub 7-in-1", "price": 49.99, "image": "/api/placeholder/300/300", "category": "Adapters", "isNew": true}]}',
    ARRAY['responsive', 'accessible', 'e-commerce', 'products', 'grid', 'wishlist']::text[],
    '2025-07-17T03:46:56.375362',
    '2025-07-17T03:46:56.375366'
);
