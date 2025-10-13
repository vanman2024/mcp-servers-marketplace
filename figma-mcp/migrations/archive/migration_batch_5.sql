BEGIN;

Category Banner
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'bd0cef99-032b-4138-905d-74b4b9b9b977',
    'Category Banner',
    'Hero banner for product category pages with navigation',
    'category-banner',
    'e-commerce',
    $$13$$import React from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ArrowRight, Star, TrendingUp } from 'lucide-react';

interface CategoryBannerProps {
  category: {
    name: string;
    description: string;
    image: string;
    productCount: number;
    featured?: boolean;
    trending?: boolean;
  };
  subcategories?: Array<{
    id: string;
    name: string;
    image: string;
    productCount: number;
  }>;
  onExploreCategory?: () => void;
  onSelectSubcategory?: (subcategoryId: string) => void;
}

export function CategoryBanner({
  category,
  subcategories = [],
  onExploreCategory,
  onSelectSubcategory
}: CategoryBannerProps) {
  return (
    <div className="relative">
      {/* Main Category Banner */}
      <div className="relative h-96 overflow-hidden rounded-lg bg-gradient-to-r from-primary/20 to-secondary/20">
        <img
          src={category.image}
          alt={category.name}
          className="absolute inset-0 w-full h-full object-cover mix-blend-overlay"
        />
        
        <div className="absolute inset-0 bg-gradient-to-r from-black/60 to-black/20" />
        
        <div className="relative h-full flex items-center">
          <div className="max-w-7xl mx-auto px-6 text-white">
            <div className="max-w-2xl">
              <div className="flex items-center gap-3 mb-4">
                <h1 className="text-4xl md:text-5xl font-bold">{category.name}</h1>
                {category.featured && (
                  <Badge variant="secondary" className="bg-primary text-primary-foreground">
                    <Star className="w-3 h-3 mr-1" />
                    Featured
                  </Badge>
                )}
                {category.trending && (
                  <Badge variant="secondary" className="bg-green-600 text-white">
                    <TrendingUp className="w-3 h-3 mr-1" />
                    Trending
                  </Badge>
                )}
              </div>
              
              <p className="text-lg md:text-xl text-gray-200 mb-6 leading-relaxed">
                {category.description}
              </p>
              
              <div className="flex items-center gap-6 mb-8">
                <div className="text-sm">
                  <span className="text-2xl font-semibold">{category.productCount.toLocaleString()}</span>
                  <p className="text-gray-300">Products Available</p>
                </div>
                
                <div className="h-8 w-px bg-gray-400" />
                
                <div className="text-sm">
                  <span className="text-2xl font-semibold">{subcategories.length}</span>
                  <p className="text-gray-300">Subcategories</p>
                </div>
              </div>
              
              <Button size="lg" onClick={onExploreCategory} className="group">
                Explore {category.name}
                <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
              </Button>
            </div>
          </div>
        </div>
        
        {/* Decorative Elements */}
        <div className="absolute top-8 right-8 w-32 h-32 bg-white/10 rounded-full blur-3xl" />
        <div className="absolute bottom-12 right-24 w-20 h-20 bg-primary/20 rounded-full blur-2xl" />
      </div>

      {/* Subcategories Grid */}
      {subcategories.length > 0 && (
        <div className="mt-12">
          <h2 className="text-2xl font-semibold mb-6">Shop by Category</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
            {subcategories.map((subcategory) => (
              <button
                key={subcategory.id}
                onClick={() => onSelectSubcategory?.(subcategory.id)}
                className="group text-left"
              >
                <div className="aspect-square relative overflow-hidden rounded-lg bg-muted mb-3 group-hover:shadow-lg transition-shadow">
                  <img
                    src={subcategory.image}
                    alt={subcategory.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                </div>
                <h3 className="font-semibold text-sm mb-1 group-hover:text-primary transition-colors">
                  {subcategory.name}
                </h3>
                <p className="text-xs text-muted-foreground">
                  {subcategory.productCount} items
                </p>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}$$13$$,
    '{"npm": ["lucide-react"], "components": ["Button", "Badge"]}',
    '{"type": "object", "properties": {"category": {"type": "object", "properties": {"name": {"type": "string"}, "description": {"type": "string"}, "image": {"type": "string"}, "productCount": {"type": "number"}, "featured": {"type": "boolean"}, "trending": {"type": "boolean"}}, "required": ["name", "description", "image", "productCount"]}, "subcategories": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "image": {"type": "string"}, "productCount": {"type": "number"}}, "required": ["id", "name", "image", "productCount"]}}, "onExploreCategory": {"type": "function"}, "onSelectSubcategory": {"type": "function"}}, "required": ["category"]}',
    '{"category": {"name": "Electronics", "description": "Discover the latest technology and gadgets from top brands. From smartphones to smart home devices, find everything you need to stay connected and productive.", "image": "/api/placeholder/800/400", "productCount": 1247, "featured": true, "trending": true}, "subcategories": [{"id": "smartphones", "name": "Smartphones", "image": "/api/placeholder/200/200", "productCount": 156}, {"id": "laptops", "name": "Laptops", "image": "/api/placeholder/200/200", "productCount": 89}, {"id": "headphones", "name": "Headphones", "image": "/api/placeholder/200/200", "productCount": 234}, {"id": "cameras", "name": "Cameras", "image": "/api/placeholder/200/200", "productCount": 67}, {"id": "gaming", "name": "Gaming", "image": "/api/placeholder/200/200", "productCount": 178}, {"id": "accessories", "name": "Accessories", "image": "/api/placeholder/200/200", "productCount": 523}]}',
    ARRAY['category-banner', 'hero', 'e-commerce', 'navigation', 'subcategories']::text[],
    '2025-07-17T03:50:42.150591',
    '2025-07-17T03:50:42.150593'
);

Sale Banner - Countdown
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '1683c11c-27e8-4dc9-ad70-8b03215a3f95',
    'Sale Banner - Countdown',
    'Promotional sale banner with countdown timer',
    'sale-banner',
    'e-commerce',
    $$14$$import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import { Flame, Clock, ArrowRight, Zap } from 'lucide-react';

interface SaleBannerCountdownProps {
  sale: {
    title: string;
    subtitle?: string;
    description: string;
    discountPercentage: number;
    endDate: string;
    image?: string;
    backgroundColor?: string;
    textColor?: string;
  };
  onShopNow?: () => void;
  compact?: boolean;
}

export function SaleBannerCountdown({ sale, onShopNow, compact = false }: SaleBannerCountdownProps) {
  const [timeLeft, setTimeLeft] = useState({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0
  });

  useEffect(() => {
    const calculateTimeLeft = () => {
      const endTime = new Date(sale.endDate).getTime();
      const now = new Date().getTime();
      const difference = endTime - now;

      if (difference > 0) {
        setTimeLeft({
          days: Math.floor(difference / (1000 * 60 * 60 * 24)),
          hours: Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
          minutes: Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60)),
          seconds: Math.floor((difference % (1000 * 60)) / 1000)
        });
      } else {
        setTimeLeft({ days: 0, hours: 0, minutes: 0, seconds: 0 });
      }
    };

    calculateTimeLeft();
    const timer = setInterval(calculateTimeLeft, 1000);

    return () => clearInterval(timer);
  }, [sale.endDate]);

  const isExpired = timeLeft.days === 0 && timeLeft.hours === 0 && timeLeft.minutes === 0 && timeLeft.seconds === 0;

  if (compact) {
    return (
      <Card className="relative overflow-hidden border-2 border-red-200 bg-gradient-to-r from-red-50 to-orange-50">
        <div className="flex items-center justify-between p-4">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <Flame className="w-5 h-5 text-red-500" />
              <span className="font-semibold text-red-900">{sale.title}</span>
              <Badge variant="destructive" className="animate-pulse">
                {sale.discountPercentage}% OFF
              </Badge>
            </div>
            <div className="flex items-center gap-1 text-sm text-red-700">
              <Clock className="w-4 h-4" />
              <span>
                {timeLeft.days}d {timeLeft.hours}h {timeLeft.minutes}m {timeLeft.seconds}s
              </span>
            </div>
          </div>
          <Button size="sm" onClick={onShopNow} disabled={isExpired}>
            Shop Now
            <ArrowRight className="w-4 h-4 ml-1" />
          </Button>
        </div>
      </Card>
    );
  }

  return (
    <div 
      className="relative overflow-hidden rounded-lg"
      style={{ 
        backgroundColor: sale.backgroundColor || '#ef4444',
        color: sale.textColor || 'white'
      }}
    >
      {sale.image && (
        <div className="absolute inset-0">
          <img
            src={sale.image}
            alt={sale.title}
            className="w-full h-full object-cover opacity-20"
          />
        </div>
      )}
      
      <div className="relative p-8 md:p-12">
        <div className="max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-8 items-center">
            <div className="space-y-6">
              <div className="space-y-2">
                <div className="flex items-center gap-3">
                  <Zap className="w-8 h-8" />
                  <Badge variant="secondary" className="bg-white/20 text-white border-white/30">
                    Limited Time
                  </Badge>
                </div>
                <h1 className="text-4xl md:text-5xl font-bold leading-tight">
                  {sale.title}
                </h1>
                {sale.subtitle && (
                  <p className="text-xl md:text-2xl opacity-90">
                    {sale.subtitle}
                  </p>
                )}
              </div>
              
              <p className="text-lg opacity-80 leading-relaxed">
                {sale.description}
              </p>
              
              <div className="flex items-center gap-4">
                <div className="text-6xl font-bold">
                  {sale.discountPercentage}%
                </div>
                <div>
                  <p className="text-2xl font-semibold">OFF</p>
                  <p className="text-sm opacity-75">Everything</p>
                </div>
              </div>
              
              <Button 
                size="lg" 
                variant="secondary"
                onClick={onShopNow}
                disabled={isExpired}
                className="group bg-white text-black hover:bg-gray-100"
              >
                {isExpired ? 'Sale Ended' : 'Shop Now'}
                {!isExpired && (
                  <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                )}
              </Button>
            </div>
            
            <div className="flex justify-center">
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 text-center">
                <div className="flex items-center gap-2 justify-center mb-6">
                  <Clock className="w-6 h-6" />
                  <h3 className="text-xl font-semibold">Sale Ends In</h3>
                </div>
                
                {isExpired ? (
                  <div className="text-4xl font-bold">
                    EXPIRED
                  </div>
                ) : (
                  <div className="grid grid-cols-4 gap-4">
                    {[
                      { label: 'Days', value: timeLeft.days },
                      { label: 'Hours', value: timeLeft.hours },
                      { label: 'Minutes', value: timeLeft.minutes },
                      { label: 'Seconds', value: timeLeft.seconds }
                    ].map((item) => (
                      <div key={item.label} className="bg-white/20 rounded-lg p-4">
                        <div className="text-3xl font-bold">
                          {item.value.toString().padStart(2, '0')}
                        </div>
                        <div className="text-sm opacity-75">
                          {item.label}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                
                <p className="text-sm opacity-75 mt-4">
                  Hurry! Don't miss out on these amazing deals
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Decorative Elements */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-32 translate-x-32" />
      <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full translate-y-24 -translate-x-24" />
    </div>
  );
}$$14$$,
    '{"npm": ["lucide-react"], "components": ["Button", "Badge", "Card"]}',
    '{"type": "object", "properties": {"sale": {"type": "object", "properties": {"title": {"type": "string"}, "subtitle": {"type": "string"}, "description": {"type": "string"}, "discountPercentage": {"type": "number"}, "endDate": {"type": "string"}, "image": {"type": "string"}, "backgroundColor": {"type": "string"}, "textColor": {"type": "string"}}, "required": ["title", "description", "discountPercentage", "endDate"]}, "onShopNow": {"type": "function"}, "compact": {"type": "boolean"}}, "required": ["sale"]}',
    '{"sale": {"title": "Black Friday Sale", "subtitle": "Biggest Sale of the Year", "description": "Get incredible discounts on thousands of products across all categories. From electronics to fashion, home goods to beauty products.", "discountPercentage": 50, "endDate": "2024-11-30T23:59:59Z", "backgroundColor": "#dc2626", "textColor": "#ffffff"}, "compact": false}',
    ARRAY['sale-banner', 'countdown', 'e-commerce', 'promotion', 'urgency']::text[],
    '2025-07-17T03:50:42.150601',
    '2025-07-17T03:50:42.150603'
);

Wishlist Grid
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '00fea1c8-7bb2-4fc9-af42-100afe145b7e',
    'Wishlist Grid',
    'User wishlist display with product management',
    'wishlist',
    'e-commerce',
    $$15$$import React from 'react';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Heart, ShoppingCart, Share2, X, Star } from 'lucide-react';

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
          My Wishlist ({items.length} {items.length === 1 ? 'item' : 'items'})
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
                                ? 'fill-primary text-primary'
                                : 'text-muted'
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
                  {item.inStock ? 'Add to Cart' : 'Out of Stock'}
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
}$$15$$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge"]}',
    '{"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "image": {"type": "string"}, "inStock": {"type": "boolean"}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "addedDate": {"type": "string"}}, "required": ["id", "name", "price", "image", "inStock", "addedDate"]}}, "onRemoveFromWishlist": {"type": "function"}, "onAddToCart": {"type": "function"}, "onShare": {"type": "function"}, "onViewProduct": {"type": "function"}, "emptyMessage": {"type": "string"}}, "required": ["items", "onRemoveFromWishlist", "onAddToCart"]}',
    '{"items": [{"id": "1", "name": "Wireless Noise-Cancelling Headphones", "price": 199.99, "originalPrice": 249.99, "image": "/api/placeholder/300/300", "inStock": true, "rating": 4.5, "reviews": 128, "addedDate": "2024-01-15T10:30:00Z"}, {"id": "2", "name": "Smart Fitness Watch", "price": 299.99, "image": "/api/placeholder/300/300", "inStock": false, "rating": 4.2, "reviews": 89, "addedDate": "2024-01-10T14:20:00Z"}, {"id": "3", "name": "Portable Bluetooth Speaker", "price": 79.99, "originalPrice": 99.99, "image": "/api/placeholder/300/300", "inStock": true, "rating": 4.7, "reviews": 234, "addedDate": "2024-01-05T09:15:00Z"}]}',
    ARRAY['wishlist', 'e-commerce', 'favorites', 'user-account', 'product-management']::text[],
    '2025-07-17T03:50:42.150691',
    '2025-07-17T03:50:42.150694'
);


COMMIT;

-- Migration completed successfully!

COMMIT;