-- Block 4: Product Card - Detailed
-- Description: Detailed product card with full information and actions
-- Generated: 2025-07-17T03:46:56.379604

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '7f8b6cff-43a9-43a1-ae7e-ce466725e8af',
    'Product Card - Detailed',
    'Detailed product card with full information and actions',
    'product-card',
    'e-commerce',
    'import React from ''react'';
import { Card, CardContent, CardFooter, CardHeader } from ''@/components/ui/card'';
import { Button } from ''@/components/ui/button'';
import { Badge } from ''@/components/ui/badge'';
import { Star, ShoppingCart, Heart, Eye } from ''lucide-react'';

interface DetailedProductCardProps {
  id: string;
  name: string;
  description: string;
  price: number;
  originalPrice?: number;
  image: string;
  rating: number;
  reviews: number;
  inStock: boolean;
  tags?: string[];
  onAddToCart?: () => void;
  onToggleWishlist?: () => void;
  onQuickView?: () => void;
}

export function DetailedProductCard({ 
  id,
  name,
  description,
  price,
  originalPrice,
  image,
  rating,
  reviews,
  inStock,
  tags = [],
  onAddToCart,
  onToggleWishlist,
  onQuickView
}: DetailedProductCardProps) {
  const discount = originalPrice ? Math.round(((originalPrice - price) / originalPrice) * 100) : 0;
  
  return (
    <Card className="flex flex-col h-full">
      <CardHeader className="p-0 relative">
        {discount > 0 && (
          <Badge className="absolute top-4 left-4 z-10" variant="destructive">
            -{discount}%
          </Badge>
        )}
        <div className="absolute top-4 right-4 z-10 flex flex-col gap-2">
          <Button
            size="icon"
            variant="secondary"
            className="w-8 h-8"
            onClick={onToggleWishlist}
          >
            <Heart className="w-4 h-4" />
          </Button>
          <Button
            size="icon"
            variant="secondary"
            className="w-8 h-8"
            onClick={onQuickView}
          >
            <Eye className="w-4 h-4" />
          </Button>
        </div>
        <img
          src={image}
          alt={name}
          className="w-full h-64 object-cover"
        />
      </CardHeader>
      
      <CardContent className="flex-1 p-4">
        <h3 className="font-semibold text-lg mb-2">{name}</h3>
        <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
          {description}
        </p>
        
        <div className="flex items-center gap-2 mb-4">
          <div className="flex items-center">
            {[...Array(5)].map((_, i) => (
              <Star
                key={i}
                className={`w-4 h-4 ${
                  i < Math.floor(rating)
                    ? ''fill-primary text-primary''
                    : ''text-muted''
                }`}
              />
            ))}
          </div>
          <span className="text-sm text-muted-foreground">
            {rating} ({reviews} reviews)
          </span>
        </div>
        
        <div className="flex items-baseline gap-2 mb-4">
          <p className="text-lg font-semibold">${price.toFixed(2)}</p>
          {originalPrice && (
            <p className="text-sm text-muted-foreground line-through">
              ${originalPrice.toFixed(2)}
            </p>
          )}
        </div>
        
        {tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-4">
            {tags.map((tag) => (
              <Badge key={tag} variant="secondary" className="text-xs">
                {tag}
              </Badge>
            ))}
          </div>
        )}
        
        <p className={`text-sm font-semibold ${inStock ? ''text-success'' : ''text-destructive''}`}>
          {inStock ? ''In Stock'' : ''Out of Stock''}
        </p>
      </CardContent>
      
      <CardFooter className="p-4 pt-0">
        <Button
          className="w-full"
          disabled={!inStock}
          onClick={onAddToCart}
        >
          <ShoppingCart className="w-4 h-4 mr-2" />
          {inStock ? ''Add to Cart'' : ''Out of Stock''}
        </Button>
      </CardFooter>
    </Card>
  );
}',
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge"]}',
    '{"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "description": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "image": {"type": "string"}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "inStock": {"type": "boolean"}, "tags": {"type": "array", "items": {"type": "string"}}, "onAddToCart": {"type": "function"}, "onToggleWishlist": {"type": "function"}, "onQuickView": {"type": "function"}}, "required": ["id", "name", "description", "price", "image", "rating", "reviews", "inStock"]}',
    '{"id": "1", "name": "Professional Camera Lens", "description": "High-quality 50mm f/1.8 prime lens perfect for portrait photography", "price": 399.99, "originalPrice": 499.99, "image": "/api/placeholder/300/300", "rating": 4.7, "reviews": 156, "inStock": true, "tags": ["Photography", "Prime Lens", "Professional"]}',
    ARRAY['detailed', 'product', 'card', 'e-commerce', 'ratings']::text[],
    '2025-07-17T03:46:56.375435',
    '2025-07-17T03:46:56.375576'
);
