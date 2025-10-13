-- Block 15: Wishlist Grid
-- Description: User wishlist display with product management
-- Generated: 2025-07-17T03:46:56.383179

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '6e82c3b4-bc6b-4eb0-9563-90b94548bb83',
    'Wishlist Grid',
    'User wishlist display with product management',
    'wishlist',
    'e-commerce',
    'import React from ''react'';
import { Card, CardContent, CardFooter } from ''@/components/ui/card'';
import { Button } from ''@/components/ui/button'';
import { Badge } from ''@/components/ui/badge'';
import { Heart, ShoppingCart, Share2, X, Star } from ''lucide-react'';

interface WishlistItem {
  id: string;
  name: string;
  price: number;
  originalPrice?: number;
  image: string;
  inStock: boolean;
  rating?: number;
  reviews?: number;
  addedDate: string;
}

interface WishlistGridProps {
  items: WishlistItem[];
  onRemoveFromWishlist: (itemId: string) => void;
  onAddToCart: (itemId: string) => void;
  onShare?: (itemId: string) => void;
  onViewProduct?: (itemId: string) => void;
  emptyMessage?: string;
}

export function WishlistGrid({
  items,
  onRemoveFromWishlist,
  onAddToCart,
  onShare,
  onViewProduct,
  emptyMessage = "Your wishlist is empty. Start adding items you love!"
}: WishlistGridProps) {
  if (items.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 px-4">
        <div className="w-32 h-32 rounded-full bg-muted flex items-center justify-center mb-6">
          <Heart className="w-16 h-16 text-muted-foreground" />
        </div>
        <h2 className="text-2xl font-semibold mb-4">Your Wishlist is Empty</h2>
        <p className="text-muted-foreground text-center max-w-md mb-8">
          {emptyMessage}
        </p>
        <Button size="lg">
          Start Shopping
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">
          My Wishlist ({items.length} {items.length === 1 ? ''item'' : ''items''})
        </h1>
        <div className="text-sm text-muted-foreground">
          Last updated: {new Date().toLocaleDateString()}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {items.map((item) => {
          const discount = item.originalPrice 
            ? Math.round(((item.originalPrice - item.price) / item.originalPrice) * 100)
            : 0;

          return (
            <Card key={item.id} className="group relative">
              <button
                onClick={() => onRemoveFromWishlist(item.id)}
                className="absolute top-3 right-3 z-10 p-2 bg-background/80 backdrop-blur rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                title="Remove from wishlist"
              >
                <X className="w-4 h-4" />
              </button>

              {discount > 0 && (
                <Badge 
                  variant="destructive" 
                  className="absolute top-3 left-3 z-10"
                >
                  -{discount}%
                </Badge>
              )}

              {!item.inStock && (
                <Badge 
                  variant="secondary" 
                  className="absolute top-3 left-3 z-10 bg-gray-500 text-white"
                >
                  Out of Stock
                </Badge>
              )}

              <div 
                className="cursor-pointer"
                onClick={() => onViewProduct?.(item.id)}
              >
                <div className="aspect-square relative overflow-hidden">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                </div>

                <CardContent className="p-4">
                  <h3 className="font-semibold text-base mb-2 line-clamp-2 group-hover:text-primary transition-colors">
                    {item.name}
                  </h3>

                  {item.rating && item.reviews && (
                    <div className="flex items-center gap-2 mb-2">
                      <div className="flex items-center">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            className={`w-3 h-3 ${
                              i < Math.floor(item.rating!)
                                ? ''fill-primary text-primary''
                                : ''text-muted''
                            }`}
                          />
                        ))}
                      </div>
                      <span className="text-xs text-muted-foreground">
                        ({item.reviews})
                      </span>
                    </div>
                  )}

                  <div className="flex items-center gap-2 mb-2">
                    <p className="text-lg font-semibold">
                      ${item.price.toFixed(2)}
                    </p>
                    {item.originalPrice && (
                      <p className="text-sm text-muted-foreground line-through">
                        ${item.originalPrice.toFixed(2)}
                      </p>
                    )}
                  </div>

                  <p className="text-xs text-muted-foreground">
                    Added {new Date(item.addedDate).toLocaleDateString()}
                  </p>
                </CardContent>
              </div>

              <CardFooter className="p-4 pt-0 space-y-2">
                <Button
                  className="w-full"
                  onClick={() => onAddToCart(item.id)}
                  disabled={!item.inStock}
                >
                  <ShoppingCart className="w-4 h-4 mr-2" />
                  {item.inStock ? ''Add to Cart'' : ''Out of Stock''}
                </Button>

                <div className="flex gap-2 w-full">
                  <Button
                    variant="outline"
                    size="sm"
                    className="flex-1"
                    onClick={() => onShare?.(item.id)}
                  >
                    <Share2 className="w-3 h-3 mr-1" />
                    Share
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    className="flex-1"
                    onClick={() => onRemoveFromWishlist(item.id)}
                  >
                    <Heart className="w-3 h-3 mr-1 fill-current" />
                    Remove
                  </Button>
                </div>
              </CardFooter>
            </Card>
          );
        })}
      </div>
    </div>
  );
}',
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge"]}',
    '{"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "image": {"type": "string"}, "inStock": {"type": "boolean"}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "addedDate": {"type": "string"}}, "required": ["id", "name", "price", "image", "inStock", "addedDate"]}}, "onRemoveFromWishlist": {"type": "function"}, "onAddToCart": {"type": "function"}, "onShare": {"type": "function"}, "onViewProduct": {"type": "function"}, "emptyMessage": {"type": "string"}}, "required": ["items", "onRemoveFromWishlist", "onAddToCart"]}',
    '{"items": [{"id": "1", "name": "Wireless Noise-Cancelling Headphones", "price": 199.99, "originalPrice": 249.99, "image": "/api/placeholder/300/300", "inStock": true, "rating": 4.5, "reviews": 128, "addedDate": "2024-01-15T10:30:00Z"}, {"id": "2", "name": "Smart Fitness Watch", "price": 299.99, "image": "/api/placeholder/300/300", "inStock": false, "rating": 4.2, "reviews": 89, "addedDate": "2024-01-10T14:20:00Z"}, {"id": "3", "name": "Portable Bluetooth Speaker", "price": 79.99, "originalPrice": 99.99, "image": "/api/placeholder/300/300", "inStock": true, "rating": 4.7, "reviews": 234, "addedDate": "2024-01-05T09:15:00Z"}]}',
    ARRAY['wishlist', 'e-commerce', 'favorites', 'user-account', 'product-management']::text[],
    '2025-07-17T03:46:56.375863',
    '2025-07-17T03:46:56.375865'
);
