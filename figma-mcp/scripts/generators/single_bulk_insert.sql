INSERT INTO application_blocks (id, name, description, block_type, app_type, react_template, dependencies, props_schema, example_props, tags, created_at, updated_at) VALUES
('9b3ceacc-6b75-4c88-9ea7-48290ec1f116', 'Product Grid - 3 Column', 'Responsive 3-column product grid with hover effects', 'product-grid', 'e-commerce', $$import React from 'react';
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
}$$, '{"npm": ["lucide-react"], "components": ["Card", "Button"]}'::jsonb, '{"type": "object", "properties": {"products": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "image": {"type": "string"}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "badge": {"type": "string"}}, "required": ["id", "name", "price", "image", "rating", "reviews"]}}, "onAddToCart": {"type": "function"}, "onProductClick": {"type": "function"}}, "required": ["products"]}'::jsonb, '{"products": [{"id": "1", "name": "Wireless Headphones", "price": 79.99, "image": "/api/placeholder/300/300", "rating": 4.5, "reviews": 234, "badge": "New"}, {"id": "2", "name": "Smart Watch", "price": 299.99, "image": "/api/placeholder/300/300", "rating": 4.8, "reviews": 512}, {"id": "3", "name": "Laptop Stand", "price": 49.99, "image": "/api/placeholder/300/300", "rating": 4.2, "reviews": 89, "badge": "Sale"}]}'::jsonb, ARRAY['responsive','accessible','e-commerce','products','grid'], NOW(), NOW()),('bf274b4f-da43-4230-8ce1-0d06972bed0f', 'Product Grid - 4 Column', 'Responsive 4-column product grid for larger displays', 'product-grid', 'e-commerce', $$import React from 'react';
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
}$$, '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge"]}'::jsonb, '{"type": "object", "properties": {"products": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "image": {"type": "string"}, "category": {"type": "string"}, "isNew": {"type": "boolean"}, "discount": {"type": "number"}}, "required": ["id", "name", "price", "image", "category"]}}, "onAddToCart": {"type": "function"}, "onToggleWishlist": {"type": "function"}}, "required": ["products"]}'::jsonb, '{"products": [{"id": "1", "name": "Premium Wireless Mouse", "price": 39.99, "originalPrice": 59.99, "image": "/api/placeholder/300/300", "category": "Accessories", "discount": 33}, {"id": "2", "name": "USB-C Hub 7-in-1", "price": 49.99, "image": "/api/placeholder/300/300", "category": "Adapters", "isNew": true}]}'::jsonb, ARRAY['responsive','accessible','e-commerce','products','grid','wishlist'], NOW(), NOW()),('57cc76a4-777a-4378-ada1-fdb741a2a184', 'Product Card - Simple', 'Simple product card with minimal information', 'product-card', 'e-commerce', $$import React from 'react';
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
}$$, '{"npm": [], "components": ["Card", "Button"]}'::jsonb, '{"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "image": {"type": "string"}, "onSelect": {"type": "function"}}, "required": ["id", "name", "price", "image"]}'::jsonb, '{"id": "1", "name": "Minimalist Desk Lamp", "price": 89.99, "image": "/api/placeholder/300/300"}'::jsonb, ARRAY['simple','product','card','e-commerce'], NOW(), NOW()),('d417d7ab-b8e3-42ee-b956-a5819aadc5ff', 'Product Card - Detailed', 'Detailed product card with full information and actions', 'product-card', 'e-commerce', $$import React from 'react';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Star, ShoppingCart, Heart, Eye } from 'lucide-react';

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
                    ? 'fill-primary text-primary'
                    : 'text-muted'
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
        
        <p className={`text-sm font-semibold ${inStock ? 'text-success' : 'text-destructive'}`}>
          {inStock ? 'In Stock' : 'Out of Stock'}
        </p>
      </CardContent>
      
      <CardFooter className="p-4 pt-0">
        <Button
          className="w-full"
          disabled={!inStock}
          onClick={onAddToCart}
        >
          <ShoppingCart className="w-4 h-4 mr-2" />
          {inStock ? 'Add to Cart' : 'Out of Stock'}
        </Button>
      </CardFooter>
    </Card>
  );
}$$, '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge"]}'::jsonb, '{"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "description": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "image": {"type": "string"}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "inStock": {"type": "boolean"}, "tags": {"type": "array", "items": {"type": "string"}}, "onAddToCart": {"type": "function"}, "onToggleWishlist": {"type": "function"}, "onQuickView": {"type": "function"}}, "required": ["id", "name", "description", "price", "image", "rating", "reviews", "inStock"]}'::jsonb, '{"id": "1", "name": "Professional Camera Lens", "description": "High-quality 50mm f/1.8 prime lens perfect for portrait photography", "price": 399.99, "originalPrice": 499.99, "image": "/api/placeholder/300/300", "rating": 4.7, "reviews": 156, "inStock": true, "tags": ["Photography", "Prime Lens", "Professional"]}'::jsonb, ARRAY['detailed','product','card','e-commerce','ratings'], NOW(), NOW()),('6a8ed4db-b0c2-46fe-9c76-7fd541c80423', 'Product Detail - Gallery', 'Product detail page with image gallery and full information', 'product-detail', 'e-commerce', $$import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Star, ShoppingCart, Heart, Share2, Truck, Shield, RefreshCw } from 'lucide-react';

interface ProductDetailGalleryProps {
  product: {
    id: string;
    name: string;
    description: string;
    price: number;
    originalPrice?: number;
    images: string[];
    rating: number;
    reviews: number;
    inStock: boolean;
    category: string;
    sku: string;
    features: string[];
    specifications: Record<string, string>;
  };
  onAddToCart?: (quantity: number) => void;
  onToggleWishlist?: () => void;
  onShare?: () => void;
}

export function ProductDetailGallery({ 
  product,
  onAddToCart,
  onToggleWishlist,
  onShare
}: ProductDetailGalleryProps) {
  const [selectedImage, setSelectedImage] = useState(0);
  const [quantity, setQuantity] = useState(1);
  
  const discount = product.originalPrice 
    ? Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100) 
    : 0;

  return (
    <div className="grid lg:grid-cols-2 gap-8">
      {/* Image Gallery */}
      <div className="space-y-4">
        <div className="aspect-square relative overflow-hidden rounded-lg bg-muted">
          <img
            src={product.images[selectedImage]}
            alt={product.name}
            className="w-full h-full object-cover"
          />
          {discount > 0 && (
            <Badge className="absolute top-4 left-4" variant="destructive">
              -{discount}%
            </Badge>
          )}
        </div>
        <div className="grid grid-cols-4 gap-4">
          {product.images.map((image, index) => (
            <button
              key={index}
              onClick={() => setSelectedImage(index)}
              className={`aspect-square rounded-lg overflow-hidden border-2 transition-colors ${
                selectedImage === index ? 'border-primary' : 'border-transparent'
              }`}
            >
              <img
                src={image}
                alt={`${product.name} ${index + 1}`}
                className="w-full h-full object-cover"
              />
            </button>
          ))}
        </div>
      </div>

      {/* Product Information */}
      <div className="space-y-6">
        <div>
          <p className="text-sm text-muted-foreground mb-2">{product.category}</p>
          <h1 className="text-3xl font-semibold mb-2">{product.name}</h1>
          <p className="text-sm text-muted-foreground">SKU: {product.sku}</p>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center">
            {[...Array(5)].map((_, i) => (
              <Star
                key={i}
                className={`w-5 h-5 ${
                  i < Math.floor(product.rating)
                    ? 'fill-primary text-primary'
                    : 'text-muted'
                }`}
              />
            ))}
          </div>
          <span className="text-sm text-muted-foreground">
            {product.rating} ({product.reviews} reviews)
          </span>
        </div>

        <div className="space-y-2">
          <div className="flex items-baseline gap-2">
            <p className="text-3xl font-semibold">${product.price.toFixed(2)}</p>
            {product.originalPrice && (
              <p className="text-lg text-muted-foreground line-through">
                ${product.originalPrice.toFixed(2)}
              </p>
            )}
          </div>
          <p className={`text-sm font-semibold ${product.inStock ? 'text-success' : 'text-destructive'}`}>
            {product.inStock ? 'In Stock' : 'Out of Stock'}
          </p>
        </div>

        <p className="text-muted-foreground">{product.description}</p>

        <div className="space-y-4">
          <div className="flex items-center gap-4">
            <div className="flex items-center border rounded-lg">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                disabled={!product.inStock}
              >
                -
              </Button>
              <span className="px-4 py-2 min-w-[3rem] text-center">{quantity}</span>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setQuantity(quantity + 1)}
                disabled={!product.inStock}
              >
                +
              </Button>
            </div>
            <Button
              className="flex-1"
              size="lg"
              disabled={!product.inStock}
              onClick={() => onAddToCart?.(quantity)}
            >
              <ShoppingCart className="w-5 h-5 mr-2" />
              Add to Cart
            </Button>
          </div>

          <div className="flex gap-2">
            <Button variant="outline" size="lg" onClick={onToggleWishlist}>
              <Heart className="w-5 h-5 mr-2" />
              Wishlist
            </Button>
            <Button variant="outline" size="lg" onClick={onShare}>
              <Share2 className="w-5 h-5 mr-2" />
              Share
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 py-4 border-y">
          <div className="flex flex-col items-center text-center">
            <Truck className="w-6 h-6 mb-2 text-muted-foreground" />
            <p className="text-sm font-semibold">Free Shipping</p>
            <p className="text-xs text-muted-foreground">Orders over $50</p>
          </div>
          <div className="flex flex-col items-center text-center">
            <Shield className="w-6 h-6 mb-2 text-muted-foreground" />
            <p className="text-sm font-semibold">Warranty</p>
            <p className="text-xs text-muted-foreground">2 Year Coverage</p>
          </div>
          <div className="flex flex-col items-center text-center">
            <RefreshCw className="w-6 h-6 mb-2 text-muted-foreground" />
            <p className="text-sm font-semibold">Easy Returns</p>
            <p className="text-xs text-muted-foreground">30 Day Policy</p>
          </div>
        </div>

        <Tabs defaultValue="features" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="features">Features</TabsTrigger>
            <TabsTrigger value="specifications">Specifications</TabsTrigger>
          </TabsList>
          <TabsContent value="features" className="space-y-2">
            <ul className="list-disc list-inside space-y-1">
              {product.features.map((feature, index) => (
                <li key={index} className="text-sm">{feature}</li>
              ))}
            </ul>
          </TabsContent>
          <TabsContent value="specifications" className="space-y-2">
            <dl className="space-y-2">
              {Object.entries(product.specifications).map(([key, value]) => (
                <div key={key} className="flex justify-between text-sm">
                  <dt className="font-semibold">{key}:</dt>
                  <dd className="text-muted-foreground">{value}</dd>
                </div>
              ))}
            </dl>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}$$, '{"npm": ["lucide-react"], "components": ["Button", "Badge", "Tabs"]}'::jsonb, '{"type": "object", "properties": {"product": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "description": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "images": {"type": "array", "items": {"type": "string"}}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "inStock": {"type": "boolean"}, "category": {"type": "string"}, "sku": {"type": "string"}, "features": {"type": "array", "items": {"type": "string"}}, "specifications": {"type": "object", "additionalProperties": {"type": "string"}}}, "required": ["id", "name", "description", "price", "images", "rating", "reviews", "inStock", "category", "sku", "features", "specifications"]}, "onAddToCart": {"type": "function"}, "onToggleWishlist": {"type": "function"}, "onShare": {"type": "function"}}, "required": ["product"]}'::jsonb, '{"product": {"id": "1", "name": "Professional DSLR Camera", "description": "Capture stunning photos and videos with this professional-grade DSLR camera featuring advanced autofocus and 4K video recording.", "price": 1299.99, "originalPrice": 1599.99, "images": ["/api/placeholder/600/600", "/api/placeholder/600/600", "/api/placeholder/600/600", "/api/placeholder/600/600"], "rating": 4.8, "reviews": 324, "inStock": true, "category": "Electronics", "sku": "CAM-PRO-001", "features": ["24.2MP Full-Frame Sensor", "4K Video Recording at 60fps", "Advanced 45-Point Autofocus", "5-Axis Image Stabilization", "Weather-Sealed Body", "Dual Memory Card Slots"], "specifications": {"Sensor": "Full-Frame CMOS", "Resolution": "24.2 Megapixels", "ISO Range": "100-51200", "Video": "4K 60fps", "Weight": "850g", "Battery Life": "970 shots"}}}'::jsonb, ARRAY['product-detail','gallery','e-commerce','specifications'], NOW(), NOW()),('c8345a28-b4ad-401f-b27c-167ec4a9fa41', 'Product Detail - Tabs', 'Product detail with tabbed content sections', 'product-detail', 'e-commerce', $$import React from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Star, Package, Truck, Shield } from 'lucide-react';

interface ProductDetailTabsProps {
  product: {
    description: string;
    features: string[];
    specifications: Record<string, string>;
    shipping: {
      methods: Array<{
        name: string;
        price: string;
        duration: string;
      }>;
      returns: string;
    };
    warranty: {
      period: string;
      coverage: string[];
    };
  };
  reviews?: Array<{
    id: string;
    author: string;
    rating: number;
    date: string;
    comment: string;
    verified: boolean;
  }>;
}

export function ProductDetailTabs({ product, reviews = [] }: ProductDetailTabsProps) {
  return (
    <Tabs defaultValue="description" className="w-full">
      <TabsList className="grid w-full grid-cols-5">
        <TabsTrigger value="description">Description</TabsTrigger>
        <TabsTrigger value="features">Features</TabsTrigger>
        <TabsTrigger value="specifications">Specs</TabsTrigger>
        <TabsTrigger value="shipping">Shipping</TabsTrigger>
        <TabsTrigger value="reviews">Reviews ({reviews.length})</TabsTrigger>
      </TabsList>
      
      <TabsContent value="description" className="mt-6">
        <Card>
          <CardContent className="p-6">
            <h3 className="font-semibold text-lg mb-4">Product Description</h3>
            <p className="text-muted-foreground">{product.description}</p>
          </CardContent>
        </Card>
      </TabsContent>
      
      <TabsContent value="features" className="mt-6">
        <Card>
          <CardContent className="p-6">
            <h3 className="font-semibold text-lg mb-4">Key Features</h3>
            <ul className="space-y-2">
              {product.features.map((feature, index) => (
                <li key={index} className="flex items-start">
                  <Package className="w-4 h-4 mt-0.5 mr-2 text-primary" />
                  <span className="text-sm">{feature}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </TabsContent>
      
      <TabsContent value="specifications" className="mt-6">
        <Card>
          <CardContent className="p-6">
            <h3 className="font-semibold text-lg mb-4">Technical Specifications</h3>
            <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(product.specifications).map(([key, value]) => (
                <div key={key} className="border-b pb-2">
                  <dt className="font-semibold text-sm">{key}</dt>
                  <dd className="text-sm text-muted-foreground">{value}</dd>
                </div>
              ))}
            </dl>
          </CardContent>
        </Card>
      </TabsContent>
      
      <TabsContent value="shipping" className="mt-6">
        <div className="grid md:grid-cols-2 gap-6">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center mb-4">
                <Truck className="w-5 h-5 mr-2 text-primary" />
                <h3 className="font-semibold text-lg">Shipping Methods</h3>
              </div>
              <div className="space-y-4">
                {product.shipping.methods.map((method, index) => (
                  <div key={index} className="flex justify-between items-center p-3 border rounded-lg">
                    <div>
                      <p className="font-semibold text-sm">{method.name}</p>
                      <p className="text-xs text-muted-foreground">{method.duration}</p>
                    </div>
                    <p className="font-semibold">{method.price}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center mb-4">
                <Shield className="w-5 h-5 mr-2 text-primary" />
                <h3 className="font-semibold text-lg">Returns & Warranty</h3>
              </div>
              <div className="space-y-4">
                <div>
                  <p className="font-semibold text-sm mb-2">Return Policy</p>
                  <p className="text-sm text-muted-foreground">{product.shipping.returns}</p>
                </div>
                <div>
                  <p className="font-semibold text-sm mb-2">Warranty Period</p>
                  <p className="text-sm text-muted-foreground">{product.warranty.period}</p>
                  <ul className="mt-2 space-y-1">
                    {product.warranty.coverage.map((item, index) => (
                      <li key={index} className="text-xs text-muted-foreground">• {item}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </TabsContent>
      
      <TabsContent value="reviews" className="mt-6">
        <div className="space-y-4">
          {reviews.length === 0 ? (
            <Card>
              <CardContent className="p-6 text-center">
                <p className="text-muted-foreground">No reviews yet. Be the first to review!</p>
              </CardContent>
            </Card>
          ) : (
            reviews.map((review) => (
              <Card key={review.id}>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <div className="flex items-center gap-2">
                        <p className="font-semibold">{review.author}</p>
                        {review.verified && (
                          <Badge variant="secondary" className="text-xs">Verified</Badge>
                        )}
                      </div>
                      <div className="flex items-center gap-2 mt-1">
                        <div className="flex">
                          {[...Array(5)].map((_, i) => (
                            <Star
                              key={i}
                              className={`w-4 h-4 ${
                                i < review.rating
                                  ? 'fill-primary text-primary'
                                  : 'text-muted'
                              }`}
                            />
                          ))}
                        </div>
                        <span className="text-sm text-muted-foreground">{review.date}</span>
                      </div>
                    </div>
                  </div>
                  <p className="text-sm">{review.comment}</p>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </TabsContent>
    </Tabs>
  );
}$$, '{"npm": ["lucide-react"], "components": ["Tabs", "Card", "Badge"]}'::jsonb, '{"type": "object", "properties": {"product": {"type": "object", "required": ["description", "features", "specifications", "shipping", "warranty"]}, "reviews": {"type": "array", "items": {"type": "object"}}}, "required": ["product"]}'::jsonb, '{"product": {"description": "This premium product delivers exceptional performance and reliability for all your needs.", "features": ["Advanced technology integration", "Energy efficient design", "Durable construction", "User-friendly interface"], "specifications": {"Dimensions": "10 x 8 x 6 inches", "Weight": "2.5 lbs", "Material": "Aluminum alloy", "Power": "USB-C charging"}, "shipping": {"methods": [{"name": "Standard Shipping", "price": "$5.99", "duration": "5-7 business days"}, {"name": "Express Shipping", "price": "$12.99", "duration": "2-3 business days"}, {"name": "Next Day", "price": "$24.99", "duration": "1 business day"}], "returns": "30-day return policy. Items must be in original condition."}, "warranty": {"period": "2 Year Limited Warranty", "coverage": ["Manufacturing defects", "Component failures", "Free repairs or replacement"]}}}'::jsonb, ARRAY['product-detail','tabs','e-commerce','reviews','specifications'], NOW(), NOW()),('037131fe-fc47-4276-99d8-4b31cf23459b', 'Shopping Cart - Sidebar', 'Slide-out shopping cart sidebar with items and checkout', 'shopping-cart', 'e-commerce', $$import React from 'react';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetFooter } from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { X, Plus, Minus, ShoppingBag } from 'lucide-react';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
  image: string;
  variant?: string;
}

interface ShoppingCartSidebarProps {
  isOpen: boolean;
  onClose: () => void;
  items: CartItem[];
  onUpdateQuantity: (itemId: string, quantity: number) => void;
  onRemoveItem: (itemId: string) => void;
  onCheckout: () => void;
}

export function ShoppingCartSidebar({
  isOpen,
  onClose,
  items,
  onUpdateQuantity,
  onRemoveItem,
  onCheckout
}: ShoppingCartSidebarProps) {
  const subtotal = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const shipping = subtotal > 50 ? 0 : 5.99;
  const tax = subtotal * 0.08;
  const total = subtotal + shipping + tax;

  return (
    <Sheet open={isOpen} onOpenChange={onClose}>
      <SheetContent className="w-full sm:max-w-md">
        <SheetHeader>
          <SheetTitle className="flex items-center gap-2">
            <ShoppingBag className="w-5 h-5" />
            Shopping Cart ({items.length})
          </SheetTitle>
        </SheetHeader>
        
        <div className="flex-1 overflow-y-auto py-4">
          {items.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <ShoppingBag className="w-16 h-16 text-muted-foreground mb-4" />
              <p className="text-lg font-semibold mb-2">Your cart is empty</p>
              <p className="text-sm text-muted-foreground">Add items to get started</p>
            </div>
          ) : (
            <div className="space-y-4">
              {items.map((item) => (
                <div key={item.id} className="flex gap-4 p-4 border rounded-lg">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="w-20 h-20 object-cover rounded"
                  />
                  <div className="flex-1">
                    <h4 className="font-semibold text-sm">{item.name}</h4>
                    {item.variant && (
                      <p className="text-xs text-muted-foreground">{item.variant}</p>
                    )}
                    <p className="text-sm font-semibold mt-1">${item.price.toFixed(2)}</p>
                    
                    <div className="flex items-center gap-2 mt-2">
                      <div className="flex items-center border rounded">
                        <Button
                          size="icon"
                          variant="ghost"
                          className="h-8 w-8"
                          onClick={() => onUpdateQuantity(item.id, Math.max(1, item.quantity - 1))}
                        >
                          <Minus className="w-3 h-3" />
                        </Button>
                        <span className="px-3 text-sm">{item.quantity}</span>
                        <Button
                          size="icon"
                          variant="ghost"
                          className="h-8 w-8"
                          onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
                        >
                          <Plus className="w-3 h-3" />
                        </Button>
                      </div>
                      <Button
                        size="icon"
                        variant="ghost"
                        className="h-8 w-8 ml-auto"
                        onClick={() => onRemoveItem(item.id)}
                      >
                        <X className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
        
        {items.length > 0 && (
          <SheetFooter className="flex-col gap-4">
            <Separator />
            <div className="space-y-2 w-full">
              <div className="flex justify-between text-sm">
                <span>Subtotal</span>
                <span>${subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Shipping</span>
                <span>{shipping === 0 ? 'FREE' : `$${shipping.toFixed(2)}`}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Tax</span>
                <span>${tax.toFixed(2)}</span>
              </div>
              <Separator />
              <div className="flex justify-between font-semibold text-lg">
                <span>Total</span>
                <span>${total.toFixed(2)}</span>
              </div>
            </div>
            
            <div className="w-full space-y-2">
              <Button className="w-full" size="lg" onClick={onCheckout}>
                Proceed to Checkout
              </Button>
              <Button variant="outline" className="w-full" onClick={onClose}>
                Continue Shopping
              </Button>
            </div>
            
            {shipping > 0 && (
              <p className="text-xs text-center text-muted-foreground">
                Add ${(50 - subtotal).toFixed(2)} more for free shipping
              </p>
            )}
          </SheetFooter>
        )}
      </SheetContent>
    </Sheet>
  );
}$$, '{"npm": ["lucide-react"], "components": ["Sheet", "Button", "Separator"]}'::jsonb, '{"type": "object", "properties": {"isOpen": {"type": "boolean"}, "onClose": {"type": "function"}, "items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "quantity": {"type": "number"}, "image": {"type": "string"}, "variant": {"type": "string"}}, "required": ["id", "name", "price", "quantity", "image"]}}, "onUpdateQuantity": {"type": "function"}, "onRemoveItem": {"type": "function"}, "onCheckout": {"type": "function"}}, "required": ["isOpen", "onClose", "items", "onUpdateQuantity", "onRemoveItem", "onCheckout"]}'::jsonb, '{"isOpen": true, "items": [{"id": "1", "name": "Wireless Mouse", "price": 29.99, "quantity": 2, "image": "/api/placeholder/80/80", "variant": "Black"}, {"id": "2", "name": "USB-C Cable", "price": 12.99, "quantity": 1, "image": "/api/placeholder/80/80"}]}'::jsonb, ARRAY['shopping-cart','sidebar','e-commerce','checkout'], NOW(), NOW()),('ba970fff-565d-4d7a-8ecf-f733370214f8', 'Shopping Cart - Page', 'Full page shopping cart with detailed item management', 'shopping-cart', 'e-commerce', $$import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';
import { Trash2, Plus, Minus, ShoppingBag, ArrowRight, Tag } from 'lucide-react';

interface CartItem {
  id: string;
  name: string;
  description: string;
  price: number;
  originalPrice?: number;
  quantity: number;
  image: string;
  variant?: string;
  inStock: boolean;
}

interface ShoppingCartPageProps {
  items: CartItem[];
  onUpdateQuantity: (itemId: string, quantity: number) => void;
  onRemoveItem: (itemId: string) => void;
  onApplyCoupon: (code: string) => void;
  onCheckout: () => void;
  appliedCoupon?: {
    code: string;
    discount: number;
  };
}

export function ShoppingCartPage({
  items,
  onUpdateQuantity,
  onRemoveItem,
  onApplyCoupon,
  onCheckout,
  appliedCoupon
}: ShoppingCartPageProps) {
  const [couponCode, setCouponCode] = React.useState('');
  
  const subtotal = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const discount = appliedCoupon ? subtotal * (appliedCoupon.discount / 100) : 0;
  const shipping = subtotal > 50 ? 0 : 5.99;
  const tax = (subtotal - discount) * 0.08;
  const total = subtotal - discount + shipping + tax;

  if (items.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] text-center">
        <ShoppingBag className="w-24 h-24 text-muted-foreground mb-4" />
        <h2 className="text-2xl font-semibold mb-2">Your cart is empty</h2>
        <p className="text-muted-foreground mb-8">Add items to your cart to continue shopping</p>
        <Button size="lg">
          Continue Shopping
          <ArrowRight className="w-4 h-4 ml-2" />
        </Button>
      </div>
    );
  }

  return (
    <div className="grid lg:grid-cols-3 gap-8">
      <div className="lg:col-span-2 space-y-4">
        <h1 className="text-2xl font-semibold mb-6">Shopping Cart ({items.length} items)</h1>
        
        {items.map((item) => (
          <Card key={item.id}>
            <CardContent className="p-6">
              <div className="flex gap-4">
                <img
                  src={item.image}
                  alt={item.name}
                  className="w-32 h-32 object-cover rounded-lg"
                />
                
                <div className="flex-1 space-y-2">
                  <div className="flex justify-between">
                    <div>
                      <h3 className="font-semibold text-lg">{item.name}</h3>
                      {item.variant && (
                        <p className="text-sm text-muted-foreground">{item.variant}</p>
                      )}
                    </div>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => onRemoveItem(item.id)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                  
                  <p className="text-sm text-muted-foreground line-clamp-2">
                    {item.description}
                  </p>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="flex items-center border rounded-lg">
                        <Button
                          size="icon"
                          variant="ghost"
                          className="h-8 w-8"
                          onClick={() => onUpdateQuantity(item.id, Math.max(1, item.quantity - 1))}
                          disabled={!item.inStock}
                        >
                          <Minus className="w-3 h-3" />
                        </Button>
                        <span className="px-4 text-sm">{item.quantity}</span>
                        <Button
                          size="icon"
                          variant="ghost"
                          className="h-8 w-8"
                          onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
                          disabled={!item.inStock}
                        >
                          <Plus className="w-3 h-3" />
                        </Button>
                      </div>
                      
                      {!item.inStock && (
                        <Badge variant="destructive">Out of Stock</Badge>
                      )}
                    </div>
                    
                    <div className="text-right">
                      <p className="text-lg font-semibold">${(item.price * item.quantity).toFixed(2)}</p>
                      {item.originalPrice && (
                        <p className="text-sm text-muted-foreground line-through">
                          ${(item.originalPrice * item.quantity).toFixed(2)}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
      
      <div className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Order Summary</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Subtotal</span>
                <span>${subtotal.toFixed(2)}</span>
              </div>
              
              {appliedCoupon && (
                <div className="flex justify-between text-sm text-success">
                  <span>Discount ({appliedCoupon.code})</span>
                  <span>-${discount.toFixed(2)}</span>
                </div>
              )}
              
              <div className="flex justify-between text-sm">
                <span>Shipping</span>
                <span>{shipping === 0 ? 'FREE' : `$${shipping.toFixed(2)}`}</span>
              </div>
              
              <div className="flex justify-between text-sm">
                <span>Tax</span>
                <span>${tax.toFixed(2)}</span>
              </div>
              
              <Separator />
              
              <div className="flex justify-between font-semibold text-lg">
                <span>Total</span>
                <span>${total.toFixed(2)}</span>
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex gap-2">
                <Input
                  placeholder="Enter coupon code"
                  value={couponCode}
                  onChange={(e) => setCouponCode(e.target.value)}
                />
                <Button
                  variant="outline"
                  onClick={() => {
                    onApplyCoupon(couponCode);
                    setCouponCode('');
                  }}
                >
                  <Tag className="w-4 h-4" />
                </Button>
              </div>
              
              {shipping > 0 && (
                <p className="text-xs text-muted-foreground">
                  Add ${(50 - subtotal).toFixed(2)} more for free shipping
                </p>
              )}
            </div>
            
            <Button className="w-full" size="lg" onClick={onCheckout}>
              Proceed to Checkout
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
            
            <Button variant="outline" className="w-full">
              Continue Shopping
            </Button>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <p className="text-sm text-muted-foreground">
              ✓ Secure checkout<br />
              ✓ Free returns within 30 days<br />
              ✓ Customer support 24/7
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}$$, '{"npm": ["lucide-react"], "components": ["Card", "Button", "Input", "Separator", "Badge"]}'::jsonb, '{"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "description": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "quantity": {"type": "number"}, "image": {"type": "string"}, "variant": {"type": "string"}, "inStock": {"type": "boolean"}}, "required": ["id", "name", "description", "price", "quantity", "image", "inStock"]}}, "onUpdateQuantity": {"type": "function"}, "onRemoveItem": {"type": "function"}, "onApplyCoupon": {"type": "function"}, "onCheckout": {"type": "function"}, "appliedCoupon": {"type": "object", "properties": {"code": {"type": "string"}, "discount": {"type": "number"}}}}, "required": ["items", "onUpdateQuantity", "onRemoveItem", "onApplyCoupon", "onCheckout"]}'::jsonb, '{"items": [{"id": "1", "name": "Wireless Keyboard", "description": "Bluetooth mechanical keyboard with RGB backlighting", "price": 89.99, "originalPrice": 119.99, "quantity": 1, "image": "/api/placeholder/128/128", "variant": "Cherry MX Blue", "inStock": true}]}'::jsonb, ARRAY['shopping-cart','page','e-commerce','checkout','order-summary'], NOW(), NOW()),('f2985822-7443-4381-8786-738e96c74640', 'Checkout - Single Page', 'Complete single-page checkout with all steps', 'checkout', 'e-commerce', $$import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Separator } from '@/components/ui/separator';
import { CreditCard, Truck, Shield, Check } from 'lucide-react';

interface CheckoutItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
  image: string;
}

interface CheckoutSinglePageProps {
  items: CheckoutItem[];
  onPlaceOrder: (orderData: any) => void;
}

export function CheckoutSinglePage({ items, onPlaceOrder }: CheckoutSinglePageProps) {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    email: '',
    firstName: '',
    lastName: '',
    address: '',
    city: '',
    postalCode: '',
    country: '',
    shippingMethod: 'standard',
    paymentMethod: 'card',
    cardNumber: '',
    expiryDate: '',
    cvv: '',
    saveInfo: false
  });

  const subtotal = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const shipping = formData.shippingMethod === 'express' ? 15.99 : 5.99;
  const tax = subtotal * 0.08;
  const total = subtotal + shipping + tax;

  const handleInputChange = (field: string, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = () => {
    onPlaceOrder({
      items,
      shippingAddress: {
        firstName: formData.firstName,
        lastName: formData.lastName,
        address: formData.address,
        city: formData.city,
        postalCode: formData.postalCode,
        country: formData.country
      },
      payment: {
        method: formData.paymentMethod,
        amount: total
      },
      shippingMethod: formData.shippingMethod
    });
  };

  return (
    <div className="max-w-6xl mx-auto p-6 grid lg:grid-cols-3 gap-8">
      {/* Checkout Form */}
      <div className="lg:col-span-2 space-y-6">
        {/* Progress Steps */}
        <div className="flex items-center gap-4 mb-8">
          {[1, 2, 3].map((s) => (
            <div key={s} className="flex items-center">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
                s <= step ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'
              }`}>
                {s < step ? <Check className="w-4 h-4" /> : s}
              </div>
              {s < 3 && <div className={`w-16 h-1 mx-2 ${s < step ? 'bg-primary' : 'bg-muted'}`} />}
            </div>
          ))}
        </div>

        {/* Step 1: Contact & Shipping */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Truck className="w-5 h-5" />
              Contact & Shipping Information
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="email">Email Address</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                placeholder="your@email.com"
              />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="firstName">First Name</Label>
                <Input
                  id="firstName"
                  value={formData.firstName}
                  onChange={(e) => handleInputChange('firstName', e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="lastName">Last Name</Label>
                <Input
                  id="lastName"
                  value={formData.lastName}
                  onChange={(e) => handleInputChange('lastName', e.target.value)}
                />
              </div>
            </div>
            
            <div>
              <Label htmlFor="address">Street Address</Label>
              <Input
                id="address"
                value={formData.address}
                onChange={(e) => handleInputChange('address', e.target.value)}
              />
            </div>
            
            <div className="grid grid-cols-3 gap-4">
              <div>
                <Label htmlFor="city">City</Label>
                <Input
                  id="city"
                  value={formData.city}
                  onChange={(e) => handleInputChange('city', e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="postalCode">Postal Code</Label>
                <Input
                  id="postalCode"
                  value={formData.postalCode}
                  onChange={(e) => handleInputChange('postalCode', e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="country">Country</Label>
                <Input
                  id="country"
                  value={formData.country}
                  onChange={(e) => handleInputChange('country', e.target.value)}
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Step 2: Shipping Method */}
        <Card>
          <CardHeader>
            <CardTitle>Shipping Method</CardTitle>
          </CardHeader>
          <CardContent>
            <RadioGroup
              value={formData.shippingMethod}
              onValueChange={(value) => handleInputChange('shippingMethod', value)}
            >
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="standard" id="standard" />
                  <Label htmlFor="standard">
                    <div>
                      <p className="font-semibold">Standard Shipping</p>
                      <p className="text-sm text-muted-foreground">5-7 business days</p>
                    </div>
                  </Label>
                </div>
                <p className="font-semibold">$5.99</p>
              </div>
              
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="express" id="express" />
                  <Label htmlFor="express">
                    <div>
                      <p className="font-semibold">Express Shipping</p>
                      <p className="text-sm text-muted-foreground">2-3 business days</p>
                    </div>
                  </Label>
                </div>
                <p className="font-semibold">$15.99</p>
              </div>
            </RadioGroup>
          </CardContent>
        </Card>

        {/* Step 3: Payment */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CreditCard className="w-5 h-5" />
              Payment Information
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <RadioGroup
              value={formData.paymentMethod}
              onValueChange={(value) => handleInputChange('paymentMethod', value)}
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="card" id="card" />
                <Label htmlFor="card">Credit/Debit Card</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="paypal" id="paypal" />
                <Label htmlFor="paypal">PayPal</Label>
              </div>
            </RadioGroup>
            
            {formData.paymentMethod === 'card' && (
              <div className="space-y-4">
                <div>
                  <Label htmlFor="cardNumber">Card Number</Label>
                  <Input
                    id="cardNumber"
                    value={formData.cardNumber}
                    onChange={(e) => handleInputChange('cardNumber', e.target.value)}
                    placeholder="1234 5678 9012 3456"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="expiryDate">Expiry Date</Label>
                    <Input
                      id="expiryDate"
                      value={formData.expiryDate}
                      onChange={(e) => handleInputChange('expiryDate', e.target.value)}
                      placeholder="MM/YY"
                    />
                  </div>
                  <div>
                    <Label htmlFor="cvv">CVV</Label>
                    <Input
                      id="cvv"
                      value={formData.cvv}
                      onChange={(e) => handleInputChange('cvv', e.target.value)}
                      placeholder="123"
                    />
                  </div>
                </div>
              </div>
            )}
            
            <div className="flex items-center space-x-2">
              <Checkbox
                id="saveInfo"
                checked={formData.saveInfo}
                onCheckedChange={(checked) => handleInputChange('saveInfo', checked)}
              />
              <Label htmlFor="saveInfo" className="text-sm">
                Save this information for next time
              </Label>
            </div>
          </CardContent>
        </Card>

        <Button size="lg" className="w-full" onClick={handleSubmit}>
          <Shield className="w-5 h-5 mr-2" />
          Place Order - ${total.toFixed(2)}
        </Button>
      </div>

      {/* Order Summary */}
      <div>
        <Card className="sticky top-6">
          <CardHeader>
            <CardTitle>Order Summary</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-4">
              {items.map((item) => (
                <div key={item.id} className="flex gap-3">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="w-16 h-16 object-cover rounded"
                  />
                  <div className="flex-1">
                    <p className="font-semibold text-sm">{item.name}</p>
                    <p className="text-xs text-muted-foreground">Qty: {item.quantity}</p>
                    <p className="font-semibold">${(item.price * item.quantity).toFixed(2)}</p>
                  </div>
                </div>
              ))}
            </div>
            
            <Separator />
            
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Subtotal</span>
                <span>${subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Shipping</span>
                <span>${shipping.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Tax</span>
                <span>${tax.toFixed(2)}</span>
              </div>
              <Separator />
              <div className="flex justify-between font-semibold text-lg">
                <span>Total</span>
                <span>${total.toFixed(2)}</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}$$, '{"npm": ["lucide-react"], "components": ["Card", "Button", "Input", "Label", "Checkbox", "RadioGroup", "Separator"]}'::jsonb, '{"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "quantity": {"type": "number"}, "image": {"type": "string"}}, "required": ["id", "name", "price", "quantity", "image"]}}, "onPlaceOrder": {"type": "function"}}, "required": ["items", "onPlaceOrder"]}'::jsonb, '{"items": [{"id": "1", "name": "Wireless Headphones", "price": 79.99, "quantity": 1, "image": "/api/placeholder/64/64"}, {"id": "2", "name": "Phone Case", "price": 24.99, "quantity": 2, "image": "/api/placeholder/64/64"}]}'::jsonb, ARRAY['checkout','single-page','e-commerce','payment','shipping'], NOW(), NOW()),('117398c2-0a9d-4bf5-80cd-4208d424b675', 'Order Summary - Card', 'Compact order summary card for checkout and review', 'order-summary', 'e-commerce', $$import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Truck, Package, Clock, MapPin } from 'lucide-react';

interface OrderSummaryCardProps {
  order: {
    id: string;
    status: 'pending' | 'confirmed' | 'shipped' | 'delivered';
    date: string;
    total: number;
    subtotal: number;
    shipping: number;
    tax: number;
    items: Array<{
      id: string;
      name: string;
      quantity: number;
      price: number;
      image: string;
    }>;
    shipping_address: {
      name: string;
      address: string;
      city: string;
      postal_code: string;
    };
    estimated_delivery?: string;
  };
  onTrackOrder?: () => void;
  onViewDetails?: () => void;
}

export function OrderSummaryCard({ order, onTrackOrder, onViewDetails }: OrderSummaryCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'confirmed': return 'bg-blue-100 text-blue-800';
      case 'shipped': return 'bg-purple-100 text-purple-800';
      case 'delivered': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending': return <Clock className="w-4 h-4" />;
      case 'confirmed': return <Package className="w-4 h-4" />;
      case 'shipped': return <Truck className="w-4 h-4" />;
      case 'delivered': return <MapPin className="w-4 h-4" />;
      default: return <Package className="w-4 h-4" />;
    }
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">Order #{order.id}</CardTitle>
          <Badge className={getStatusColor(order.status)}>
            <div className="flex items-center gap-1">
              {getStatusIcon(order.status)}
              {order.status.toUpperCase()}
            </div>
          </Badge>
        </div>
        <p className="text-sm text-muted-foreground">
          Ordered on {new Date(order.date).toLocaleDateString()}
        </p>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Order Items */}
        <div className="space-y-3">
          {order.items.map((item) => (
            <div key={item.id} className="flex gap-3">
              <img
                src={item.image}
                alt={item.name}
                className="w-12 h-12 object-cover rounded"
              />
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-sm truncate">{item.name}</p>
                <p className="text-xs text-muted-foreground">
                  Qty: {item.quantity} × ${item.price.toFixed(2)}
                </p>
              </div>
              <p className="text-sm font-semibold">
                ${(item.price * item.quantity).toFixed(2)}
              </p>
            </div>
          ))}
        </div>
        
        <Separator />
        
        {/* Order Totals */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span>Subtotal</span>
            <span>${order.subtotal.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span>Shipping</span>
            <span>${order.shipping.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span>Tax</span>
            <span>${order.tax.toFixed(2)}</span>
          </div>
          <Separator />
          <div className="flex justify-between font-semibold">
            <span>Total</span>
            <span>${order.total.toFixed(2)}</span>
          </div>
        </div>
        
        <Separator />
        
        {/* Shipping Address */}
        <div>
          <p className="font-semibold text-sm mb-2">Shipping Address</p>
          <div className="text-sm text-muted-foreground">
            <p>{order.shipping_address.name}</p>
            <p>{order.shipping_address.address}</p>
            <p>{order.shipping_address.city}, {order.shipping_address.postal_code}</p>
          </div>
        </div>
        
        {/* Delivery Estimate */}
        {order.estimated_delivery && (
          <div className="bg-muted p-3 rounded-lg">
            <div className="flex items-center gap-2">
              <Truck className="w-4 h-4 text-muted-foreground" />
              <p className="text-sm font-semibold">Estimated Delivery</p>
            </div>
            <p className="text-sm text-muted-foreground mt-1">
              {new Date(order.estimated_delivery).toLocaleDateString()}
            </p>
          </div>
        )}
        
        {/* Action Buttons */}
        <div className="flex gap-2 pt-2">
          {order.status !== 'pending' && (
            <Button variant="outline" size="sm" onClick={onTrackOrder} className="flex-1">
              <Truck className="w-4 h-4 mr-2" />
              Track Order
            </Button>
          )}
          <Button variant="outline" size="sm" onClick={onViewDetails} className="flex-1">
            View Details
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}$$, '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge", "Separator"]}'::jsonb, '{"type": "object", "properties": {"order": {"type": "object", "properties": {"id": {"type": "string"}, "status": {"type": "string", "enum": ["pending", "confirmed", "shipped", "delivered"]}, "date": {"type": "string"}, "total": {"type": "number"}, "subtotal": {"type": "number"}, "shipping": {"type": "number"}, "tax": {"type": "number"}, "items": {"type": "array"}, "shipping_address": {"type": "object"}, "estimated_delivery": {"type": "string"}}, "required": ["id", "status", "date", "total", "subtotal", "shipping", "tax", "items", "shipping_address"]}, "onTrackOrder": {"type": "function"}, "onViewDetails": {"type": "function"}}, "required": ["order"]}'::jsonb, '{"order": {"id": "ORD-2024-001", "status": "shipped", "date": "2024-01-15T10:30:00Z", "total": 124.97, "subtotal": 109.98, "shipping": 5.99, "tax": 8.8, "items": [{"id": "1", "name": "Wireless Mouse", "quantity": 2, "price": 29.99, "image": "/api/placeholder/48/48"}, {"id": "2", "name": "USB Cable", "quantity": 1, "price": 49.99, "image": "/api/placeholder/48/48"}], "shipping_address": {"name": "John Doe", "address": "123 Main St", "city": "Anytown", "postal_code": "12345"}, "estimated_delivery": "2024-01-20T00:00:00Z"}}'::jsonb, ARRAY['order-summary','card','e-commerce','tracking','delivery'], NOW(), NOW()),('6d9fd83a-b6f2-4e41-b2da-11902df49d28', 'Product Reviews - List', 'Product reviews list with ratings and filtering', 'product-reviews', 'e-commerce', $$import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Star, ThumbsUp, ThumbsDown, Filter, MoreHorizontal } from 'lucide-react';

interface Review {
  id: string;
  author: string;
  rating: number;
  title: string;
  content: string;
  date: string;
  verified: boolean;
  helpful: number;
  images?: string[];
}

interface ProductReviewsListProps {
  productName: string;
  averageRating: number;
  totalReviews: number;
  ratingDistribution: {
    5: number;
    4: number;
    3: number;
    2: number;
    1: number;
  };
  reviews: Review[];
  onWriteReview?: () => void;
  onHelpfulVote?: (reviewId: string, helpful: boolean) => void;
}

export function ProductReviewsList({
  productName,
  averageRating,
  totalReviews,
  ratingDistribution,
  reviews,
  onWriteReview,
  onHelpfulVote
}: ProductReviewsListProps) {
  const [sortBy, setSortBy] = useState('newest');
  const [filterRating, setFilterRating] = useState('all');

  const filteredReviews = reviews.filter(review => {
    if (filterRating === 'all') return true;
    return review.rating === parseInt(filterRating);
  });

  const sortedReviews = [...filteredReviews].sort((a, b) => {
    switch (sortBy) {
      case 'newest':
        return new Date(b.date).getTime() - new Date(a.date).getTime();
      case 'oldest':
        return new Date(a.date).getTime() - new Date(b.date).getTime();
      case 'highest':
        return b.rating - a.rating;
      case 'lowest':
        return a.rating - b.rating;
      case 'helpful':
        return b.helpful - a.helpful;
      default:
        return 0;
    }
  });

  return (
    <div className="space-y-6">
      {/* Reviews Overview */}
      <Card>
        <CardHeader>
          <CardTitle>Customer Reviews</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div className="text-center">
                <div className="text-4xl font-bold">{averageRating.toFixed(1)}</div>
                <div className="flex items-center justify-center gap-1 mt-2">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      className={`w-5 h-5 ${
                        i < Math.floor(averageRating)
                          ? 'fill-primary text-primary'
                          : 'text-muted'
                      }`}
                    />
                  ))}
                </div>
                <p className="text-sm text-muted-foreground mt-1">
                  Based on {totalReviews} reviews
                </p>
              </div>
              
              <Button onClick={onWriteReview} className="w-full">
                Write a Review
              </Button>
            </div>
            
            <div className="space-y-2">
              {[5, 4, 3, 2, 1].map((rating) => {
                const count = ratingDistribution[rating as keyof typeof ratingDistribution];
                const percentage = totalReviews > 0 ? (count / totalReviews) * 100 : 0;
                
                return (
                  <div key={rating} className="flex items-center gap-2">
                    <span className="text-sm w-8">{rating}★</span>
                    <Progress value={percentage} className="flex-1" />
                    <span className="text-sm text-muted-foreground w-12">
                      ({count})
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Filters and Sorting */}
      <div className="flex flex-wrap gap-4 items-center justify-between">
        <Tabs value={filterRating} onValueChange={setFilterRating}>
          <TabsList>
            <TabsTrigger value="all">All ({totalReviews})</TabsTrigger>
            <TabsTrigger value="5">5★ ({ratingDistribution[5]})</TabsTrigger>
            <TabsTrigger value="4">4★ ({ratingDistribution[4]})</TabsTrigger>
            <TabsTrigger value="3">3★ ({ratingDistribution[3]})</TabsTrigger>
            <TabsTrigger value="2">2★ ({ratingDistribution[2]})</TabsTrigger>
            <TabsTrigger value="1">1★ ({ratingDistribution[1]})</TabsTrigger>
          </TabsList>
        </Tabs>
        
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4" />
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="text-sm border rounded px-2 py-1"
          >
            <option value="newest">Newest first</option>
            <option value="oldest">Oldest first</option>
            <option value="highest">Highest rated</option>
            <option value="lowest">Lowest rated</option>
            <option value="helpful">Most helpful</option>
          </select>
        </div>
      </div>

      {/* Reviews List */}
      <div className="space-y-4">
        {sortedReviews.length === 0 ? (
          <Card>
            <CardContent className="p-8 text-center">
              <p className="text-muted-foreground">No reviews match your filters.</p>
            </CardContent>
          </Card>
        ) : (
          sortedReviews.map((review) => (
            <Card key={review.id}>
              <CardContent className="p-6">
                <div className="space-y-4">
                  <div className="flex items-start justify-between">
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <p className="font-semibold">{review.author}</p>
                        {review.verified && (
                          <Badge variant="secondary" className="text-xs">
                            Verified Purchase
                          </Badge>
                        )}
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <div className="flex">
                          {[...Array(5)].map((_, i) => (
                            <Star
                              key={i}
                              className={`w-4 h-4 ${
                                i < review.rating
                                  ? 'fill-primary text-primary'
                                  : 'text-muted'
                              }`}
                            />
                          ))}
                        </div>
                        <span className="text-sm text-muted-foreground">
                          {new Date(review.date).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                    
                    <Button variant="ghost" size="icon">
                      <MoreHorizontal className="w-4 h-4" />
                    </Button>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold mb-2">{review.title}</h4>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {review.content}
                    </p>
                  </div>
                  
                  {review.images && review.images.length > 0 && (
                    <div className="flex gap-2">
                      {review.images.map((image, index) => (
                        <img
                          key={index}
                          src={image}
                          alt={`Review image ${index + 1}`}
                          className="w-16 h-16 object-cover rounded border"
                        />
                      ))}
                    </div>
                  )}
                  
                  <div className="flex items-center gap-4 pt-2">
                    <p className="text-sm text-muted-foreground">
                      Was this helpful?
                    </p>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => onHelpfulVote?.(review.id, true)}
                      >
                        <ThumbsUp className="w-3 h-3 mr-1" />
                        Yes ({review.helpful})
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => onHelpfulVote?.(review.id, false)}
                      >
                        <ThumbsDown className="w-3 h-3 mr-1" />
                        No
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}$$, '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge", "Progress", "Tabs"]}'::jsonb, '{"type": "object", "properties": {"productName": {"type": "string"}, "averageRating": {"type": "number"}, "totalReviews": {"type": "number"}, "ratingDistribution": {"type": "object", "properties": {"5": {"type": "number"}, "4": {"type": "number"}, "3": {"type": "number"}, "2": {"type": "number"}, "1": {"type": "number"}}, "required": ["5", "4", "3", "2", "1"]}, "reviews": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "author": {"type": "string"}, "rating": {"type": "number"}, "title": {"type": "string"}, "content": {"type": "string"}, "date": {"type": "string"}, "verified": {"type": "boolean"}, "helpful": {"type": "number"}, "images": {"type": "array", "items": {"type": "string"}}}, "required": ["id", "author", "rating", "title", "content", "date", "verified", "helpful"]}}, "onWriteReview": {"type": "function"}, "onHelpfulVote": {"type": "function"}}, "required": ["productName", "averageRating", "totalReviews", "ratingDistribution", "reviews"]}'::jsonb, '{"productName": "Wireless Headphones", "averageRating": 4.3, "totalReviews": 89, "ratingDistribution": {"5": 42, "4": 23, "3": 15, "2": 6, "1": 3}, "reviews": [{"id": "1", "author": "Sarah Johnson", "rating": 5, "title": "Excellent sound quality!", "content": "These headphones exceeded my expectations. The sound quality is crystal clear and the noise cancellation works perfectly.", "date": "2024-01-15T00:00:00Z", "verified": true, "helpful": 12, "images": ["/api/placeholder/64/64"]}, {"id": "2", "author": "Mike Chen", "rating": 4, "title": "Good value for money", "content": "Solid headphones for the price. Battery life is impressive and they're comfortable for long listening sessions.", "date": "2024-01-10T00:00:00Z", "verified": true, "helpful": 8}]}'::jsonb, ARRAY['product-reviews','ratings','e-commerce','feedback','social-proof'], NOW(), NOW()),('a6228e2a-8d7d-484c-be32-ffdf4fc023ed', 'Product Filter - Sidebar', 'Advanced product filtering sidebar with multiple filter types', 'product-filter', 'e-commerce', $$import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { ChevronDown, X, Filter } from 'lucide-react';

interface FilterState {
  categories: string[];
  brands: string[];
  priceRange: [number, number];
  ratings: number[];
  inStock: boolean;
  onSale: boolean;
}

interface ProductFilterSidebarProps {
  filters: FilterState;
  onFiltersChange: (filters: FilterState) => void;
  onClearFilters: () => void;
  availableFilters: {
    categories: Array<{ id: string; name: string; count: number }>;
    brands: Array<{ id: string; name: string; count: number }>;
    priceRange: { min: number; max: number };
  };
  resultCount: number;
}

export function ProductFilterSidebar({
  filters,
  onFiltersChange,
  onClearFilters,
  availableFilters,
  resultCount
}: ProductFilterSidebarProps) {
  const [openSections, setOpenSections] = useState({
    categories: true,
    brands: true,
    price: true,
    ratings: true,
    availability: true
  });

  const handleCategoryToggle = (categoryId: string) => {
    const newCategories = filters.categories.includes(categoryId)
      ? filters.categories.filter(id => id !== categoryId)
      : [...filters.categories, categoryId];
    
    onFiltersChange({ ...filters, categories: newCategories });
  };

  const handleBrandToggle = (brandId: string) => {
    const newBrands = filters.brands.includes(brandId)
      ? filters.brands.filter(id => id !== brandId)
      : [...filters.brands, brandId];
    
    onFiltersChange({ ...filters, brands: newBrands });
  };

  const handleRatingToggle = (rating: number) => {
    const newRatings = filters.ratings.includes(rating)
      ? filters.ratings.filter(r => r !== rating)
      : [...filters.ratings, rating];
    
    onFiltersChange({ ...filters, ratings: newRatings });
  };

  const getActiveFilterCount = () => {
    return filters.categories.length + 
           filters.brands.length + 
           filters.ratings.length + 
           (filters.inStock ? 1 : 0) + 
           (filters.onSale ? 1 : 0);
  };

  return (
    <div className="w-full max-w-sm space-y-4">
      {/* Filter Header */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Filter className="w-5 h-5" />
              Filters
              {getActiveFilterCount() > 0 && (
                <Badge variant="secondary" className="ml-2">
                  {getActiveFilterCount()}
                </Badge>
              )}
            </CardTitle>
            {getActiveFilterCount() > 0 && (
              <Button variant="ghost" size="sm" onClick={onClearFilters}>
                Clear All
              </Button>
            )}
          </div>
          <p className="text-sm text-muted-foreground">
            {resultCount} products found
          </p>
        </CardHeader>
      </Card>

      {/* Categories Filter */}
      <Card>
        <Collapsible
          open={openSections.categories}
          onOpenChange={(open) => setOpenSections(prev => ({ ...prev, categories: open }))}
        >
          <CollapsibleTrigger asChild>
            <CardHeader className="cursor-pointer pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-base">Categories</CardTitle>
                <ChevronDown className={`w-4 h-4 transition-transform ${
                  openSections.categories ? 'rotate-180' : ''
                }`} />
              </div>
            </CardHeader>
          </CollapsibleTrigger>
          <CollapsibleContent>
            <CardContent className="pt-0">
              <div className="space-y-3">
                {availableFilters.categories.map((category) => (
                  <div key={category.id} className="flex items-center space-x-2">
                    <Checkbox
                      id={`category-${category.id}`}
                      checked={filters.categories.includes(category.id)}
                      onCheckedChange={() => handleCategoryToggle(category.id)}
                    />
                    <Label 
                      htmlFor={`category-${category.id}`}
                      className="flex-1 text-sm cursor-pointer"
                    >
                      {category.name}
                    </Label>
                    <span className="text-xs text-muted-foreground">
                      ({category.count})
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </CollapsibleContent>
        </Collapsible>
      </Card>

      {/* Price Range Filter */}
      <Card>
        <Collapsible
          open={openSections.price}
          onOpenChange={(open) => setOpenSections(prev => ({ ...prev, price: open }))}
        >
          <CollapsibleTrigger asChild>
            <CardHeader className="cursor-pointer pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-base">Price Range</CardTitle>
                <ChevronDown className={`w-4 h-4 transition-transform ${
                  openSections.price ? 'rotate-180' : ''
                }`} />
              </div>
            </CardHeader>
          </CollapsibleTrigger>
          <CollapsibleContent>
            <CardContent className="pt-0">
              <div className="space-y-4">
                <Slider
                  value={filters.priceRange}
                  onValueChange={(value) => onFiltersChange({ 
                    ...filters, 
                    priceRange: value as [number, number]
                  })}
                  max={availableFilters.priceRange.max}
                  min={availableFilters.priceRange.min}
                  step={10}
                  className="w-full"
                />
                <div className="flex items-center justify-between text-sm">
                  <span>${filters.priceRange[0]}</span>
                  <span>${filters.priceRange[1]}</span>
                </div>
              </div>
            </CardContent>
          </CollapsibleContent>
        </Collapsible>
      </Card>

      {/* Brands Filter */}
      <Card>
        <Collapsible
          open={openSections.brands}
          onOpenChange={(open) => setOpenSections(prev => ({ ...prev, brands: open }))}
        >
          <CollapsibleTrigger asChild>
            <CardHeader className="cursor-pointer pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-base">Brands</CardTitle>
                <ChevronDown className={`w-4 h-4 transition-transform ${
                  openSections.brands ? 'rotate-180' : ''
                }`} />
              </div>
            </CardHeader>
          </CollapsibleTrigger>
          <CollapsibleContent>
            <CardContent className="pt-0">
              <div className="space-y-3">
                {availableFilters.brands.map((brand) => (
                  <div key={brand.id} className="flex items-center space-x-2">
                    <Checkbox
                      id={`brand-${brand.id}`}
                      checked={filters.brands.includes(brand.id)}
                      onCheckedChange={() => handleBrandToggle(brand.id)}
                    />
                    <Label 
                      htmlFor={`brand-${brand.id}`}
                      className="flex-1 text-sm cursor-pointer"
                    >
                      {brand.name}
                    </Label>
                    <span className="text-xs text-muted-foreground">
                      ({brand.count})
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </CollapsibleContent>
        </Collapsible>
      </Card>

      {/* Ratings Filter */}
      <Card>
        <Collapsible
          open={openSections.ratings}
          onOpenChange={(open) => setOpenSections(prev => ({ ...prev, ratings: open }))}
        >
          <CollapsibleTrigger asChild>
            <CardHeader className="cursor-pointer pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-base">Customer Rating</CardTitle>
                <ChevronDown className={`w-4 h-4 transition-transform ${
                  openSections.ratings ? 'rotate-180' : ''
                }`} />
              </div>
            </CardHeader>
          </CollapsibleTrigger>
          <CollapsibleContent>
            <CardContent className="pt-0">
              <div className="space-y-3">
                {[5, 4, 3, 2, 1].map((rating) => (
                  <div key={rating} className="flex items-center space-x-2">
                    <Checkbox
                      id={`rating-${rating}`}
                      checked={filters.ratings.includes(rating)}
                      onCheckedChange={() => handleRatingToggle(rating)}
                    />
                    <Label 
                      htmlFor={`rating-${rating}`}
                      className="flex items-center text-sm cursor-pointer"
                    >
                      <span className="mr-1">{rating}</span>
                      {'★'.repeat(rating)}{'☆'.repeat(5-rating)}
                      <span className="ml-1">& up</span>
                    </Label>
                  </div>
                ))}
              </div>
            </CardContent>
          </CollapsibleContent>
        </Collapsible>
      </Card>

      {/* Availability Filter */}
      <Card>
        <Collapsible
          open={openSections.availability}
          onOpenChange={(open) => setOpenSections(prev => ({ ...prev, availability: open }))}
        >
          <CollapsibleTrigger asChild>
            <CardHeader className="cursor-pointer pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-base">Availability</CardTitle>
                <ChevronDown className={`w-4 h-4 transition-transform ${
                  openSections.availability ? 'rotate-180' : ''
                }`} />
              </div>
            </CardHeader>
          </CollapsibleTrigger>
          <CollapsibleContent>
            <CardContent className="pt-0">
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="inStock"
                    checked={filters.inStock}
                    onCheckedChange={(checked) => 
                      onFiltersChange({ ...filters, inStock: !!checked })
                    }
                  />
                  <Label htmlFor="inStock" className="text-sm cursor-pointer">
                    In Stock Only
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="onSale"
                    checked={filters.onSale}
                    onCheckedChange={(checked) => 
                      onFiltersChange({ ...filters, onSale: !!checked })
                    }
                  />
                  <Label htmlFor="onSale" className="text-sm cursor-pointer">
                    On Sale
                  </Label>
                </div>
              </div>
            </CardContent>
          </CollapsibleContent>
        </Collapsible>
      </Card>
    </div>
  );
}$$, '{"npm": ["lucide-react"], "components": ["Card", "Button", "Checkbox", "Label", "Slider", "Badge", "Collapsible"]}'::jsonb, '{"type": "object", "properties": {"filters": {"type": "object", "properties": {"categories": {"type": "array", "items": {"type": "string"}}, "brands": {"type": "array", "items": {"type": "string"}}, "priceRange": {"type": "array", "items": {"type": "number"}}, "ratings": {"type": "array", "items": {"type": "number"}}, "inStock": {"type": "boolean"}, "onSale": {"type": "boolean"}}}, "onFiltersChange": {"type": "function"}, "onClearFilters": {"type": "function"}, "availableFilters": {"type": "object"}, "resultCount": {"type": "number"}}, "required": ["filters", "onFiltersChange", "onClearFilters", "availableFilters", "resultCount"]}'::jsonb, '{"filters": {"categories": ["electronics"], "brands": [], "priceRange": [0, 1000], "ratings": [4, 5], "inStock": true, "onSale": false}, "resultCount": 42, "availableFilters": {"categories": [{"id": "electronics", "name": "Electronics", "count": 156}, {"id": "clothing", "name": "Clothing", "count": 89}, {"id": "books", "name": "Books", "count": 234}], "brands": [{"id": "apple", "name": "Apple", "count": 45}, {"id": "samsung", "name": "Samsung", "count": 67}], "priceRange": {"min": 0, "max": 2000}}}'::jsonb, ARRAY['product-filter','sidebar','e-commerce','search','categories'], NOW(), NOW()),('dfb4bf4c-c80e-40e7-aa2c-d69495f51d9f', 'Category Banner', 'Hero banner for product category pages with navigation', 'category-banner', 'e-commerce', $$import React from 'react';
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
}$$, '{"npm": ["lucide-react"], "components": ["Button", "Badge"]}'::jsonb, '{"type": "object", "properties": {"category": {"type": "object", "properties": {"name": {"type": "string"}, "description": {"type": "string"}, "image": {"type": "string"}, "productCount": {"type": "number"}, "featured": {"type": "boolean"}, "trending": {"type": "boolean"}}, "required": ["name", "description", "image", "productCount"]}, "subcategories": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "image": {"type": "string"}, "productCount": {"type": "number"}}, "required": ["id", "name", "image", "productCount"]}}, "onExploreCategory": {"type": "function"}, "onSelectSubcategory": {"type": "function"}}, "required": ["category"]}'::jsonb, '{"category": {"name": "Electronics", "description": "Discover the latest technology and gadgets from top brands. From smartphones to smart home devices, find everything you need to stay connected and productive.", "image": "/api/placeholder/800/400", "productCount": 1247, "featured": true, "trending": true}, "subcategories": [{"id": "smartphones", "name": "Smartphones", "image": "/api/placeholder/200/200", "productCount": 156}, {"id": "laptops", "name": "Laptops", "image": "/api/placeholder/200/200", "productCount": 89}, {"id": "headphones", "name": "Headphones", "image": "/api/placeholder/200/200", "productCount": 234}, {"id": "cameras", "name": "Cameras", "image": "/api/placeholder/200/200", "productCount": 67}, {"id": "gaming", "name": "Gaming", "image": "/api/placeholder/200/200", "productCount": 178}, {"id": "accessories", "name": "Accessories", "image": "/api/placeholder/200/200", "productCount": 523}]}'::jsonb, ARRAY['category-banner','hero','e-commerce','navigation','subcategories'], NOW(), NOW()),('8be83848-0699-4ab4-9ebf-7ca353edd2a6', 'Sale Banner - Countdown', 'Promotional sale banner with countdown timer', 'sale-banner', 'e-commerce', $$import React, { useState, useEffect } from 'react';
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
}$$, '{"npm": ["lucide-react"], "components": ["Button", "Badge", "Card"]}'::jsonb, '{"type": "object", "properties": {"sale": {"type": "object", "properties": {"title": {"type": "string"}, "subtitle": {"type": "string"}, "description": {"type": "string"}, "discountPercentage": {"type": "number"}, "endDate": {"type": "string"}, "image": {"type": "string"}, "backgroundColor": {"type": "string"}, "textColor": {"type": "string"}}, "required": ["title", "description", "discountPercentage", "endDate"]}, "onShopNow": {"type": "function"}, "compact": {"type": "boolean"}}, "required": ["sale"]}'::jsonb, '{"sale": {"title": "Black Friday Sale", "subtitle": "Biggest Sale of the Year", "description": "Get incredible discounts on thousands of products across all categories. From electronics to fashion, home goods to beauty products.", "discountPercentage": 50, "endDate": "2024-11-30T23:59:59Z", "backgroundColor": "#dc2626", "textColor": "#ffffff"}, "compact": false}'::jsonb, ARRAY['sale-banner','countdown','e-commerce','promotion','urgency'], NOW(), NOW()),('d2b1c233-29e5-42aa-812d-b08c55c0c6e3', 'Wishlist Grid', 'User wishlist display with product management', 'wishlist', 'e-commerce', $$import React from 'react';
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
}$$, '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge"]}'::jsonb, '{"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "image": {"type": "string"}, "inStock": {"type": "boolean"}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "addedDate": {"type": "string"}}, "required": ["id", "name", "price", "image", "inStock", "addedDate"]}}, "onRemoveFromWishlist": {"type": "function"}, "onAddToCart": {"type": "function"}, "onShare": {"type": "function"}, "onViewProduct": {"type": "function"}, "emptyMessage": {"type": "string"}}, "required": ["items", "onRemoveFromWishlist", "onAddToCart"]}'::jsonb, '{"items": [{"id": "1", "name": "Wireless Noise-Cancelling Headphones", "price": 199.99, "originalPrice": 249.99, "image": "/api/placeholder/300/300", "inStock": true, "rating": 4.5, "reviews": 128, "addedDate": "2024-01-15T10:30:00Z"}, {"id": "2", "name": "Smart Fitness Watch", "price": 299.99, "image": "/api/placeholder/300/300", "inStock": false, "rating": 4.2, "reviews": 89, "addedDate": "2024-01-10T14:20:00Z"}, {"id": "3", "name": "Portable Bluetooth Speaker", "price": 79.99, "originalPrice": 99.99, "image": "/api/placeholder/300/300", "inStock": true, "rating": 4.7, "reviews": 234, "addedDate": "2024-01-05T09:15:00Z"}]}'::jsonb, ARRAY['wishlist','e-commerce','favorites','user-account','product-management'], NOW(), NOW());