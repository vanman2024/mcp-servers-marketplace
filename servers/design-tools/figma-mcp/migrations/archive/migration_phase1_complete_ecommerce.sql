-- Phase 1: E-commerce Blocks Migration
-- Generated: 2025-07-17T03:26:39.928038
-- Total blocks: 15

-- Insert e-commerce blocks into application_blocks table

-- Block 1: Product Grid - 3 Column
INSERT INTO application_blocks (
    id,
    name,
    description,
    block_type,
    app_type,
    react_template,
    dependencies,
    props_schema,
    example_props,
    tags,
    created_at,
    updated_at
) VALUES (
    '614efba7-3900-4808-9814-f06307831732',
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
    '2025-07-17T03:26:39.927431',
    '2025-07-17T03:26:39.927436'
);

-- Block 2: Product Grid - 4 Column
INSERT INTO application_blocks (
    id,
    name,
    description,
    block_type,
    app_type,
    react_template,
    dependencies,
    props_schema,
    example_props,
    tags,
    created_at,
    updated_at
) VALUES (
    '55f75d8e-3f41-4bab-ad57-9db77304bea4',
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
    '2025-07-17T03:26:39.927453',
    '2025-07-17T03:26:39.927454'
);

-- Block 3: Product Card - Simple
INSERT INTO application_blocks (
    id,
    name,
    description,
    block_type,
    app_type,
    react_template,
    dependencies,
    props_schema,
    example_props,
    tags,
    created_at,
    updated_at
) VALUES (
    '7de61eea-e238-4c04-a107-46be5db68ad0',
    'Product Card - Simple',
    'Simple product card with minimal information',
    'product-card',
    'e-commerce',
    'import React from ''react'';
import { Card, CardContent } from ''@/components/ui/card'';
import { Button } from ''@/components/ui/button'';

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
}',
    '{"npm": [], "components": ["Card", "Button"]}',
    '{"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "image": {"type": "string"}, "onSelect": {"type": "function"}}, "required": ["id", "name", "price", "image"]}',
    '{"id": "1", "name": "Minimalist Desk Lamp", "price": 89.99, "image": "/api/placeholder/300/300"}',
    ARRAY['simple', 'product', 'card', 'e-commerce']::text[],
    '2025-07-17T03:26:39.927464',
    '2025-07-17T03:26:39.927465'
);

-- Block 4: Product Card - Detailed
INSERT INTO application_blocks (
    id,
    name,
    description,
    block_type,
    app_type,
    react_template,
    dependencies,
    props_schema,
    example_props,
    tags,
    created_at,
    updated_at
) VALUES (
    '6a97f8af-f495-48fe-b2be-4502015f8046',
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
    '2025-07-17T03:26:39.927478',
    '2025-07-17T03:26:39.927516'
);

-- Block 5: Product Detail - Gallery
INSERT INTO application_blocks (
    id,
    name,
    description,
    block_type,
    app_type,
    react_template,
    dependencies,
    props_schema,
    example_props,
    tags,
    created_at,
    updated_at
) VALUES (
    'abcef374-e7b0-4cf6-871b-243b2299fb19',
    'Product Detail - Gallery',
    'Product detail page with image gallery and full information',
    'product-detail',
    'e-commerce',
    'import React, { useState } from ''react'';
import { Button } from ''@/components/ui/button'';
import { Badge } from ''@/components/ui/badge'';
import { Tabs, TabsContent, TabsList, TabsTrigger } from ''@/components/ui/tabs'';
import { Star, ShoppingCart, Heart, Share2, Truck, Shield, RefreshCw } from ''lucide-react'';

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
                selectedImage === index ? ''border-primary'' : ''border-transparent''
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
                    ? ''fill-primary text-primary''
                    : ''text-muted''
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
          <p className={`text-sm font-semibold ${product.inStock ? ''text-success'' : ''text-destructive''}`}>
            {product.inStock ? ''In Stock'' : ''Out of Stock''}
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
}',
    '{"npm": ["lucide-react"], "components": ["Button", "Badge", "Tabs"]}',
    '{"type": "object", "properties": {"product": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "description": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "images": {"type": "array", "items": {"type": "string"}}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "inStock": {"type": "boolean"}, "category": {"type": "string"}, "sku": {"type": "string"}, "features": {"type": "array", "items": {"type": "string"}}, "specifications": {"type": "object", "additionalProperties": {"type": "string"}}}, "required": ["id", "name", "description", "price", "images", "rating", "reviews", "inStock", "category", "sku", "features", "specifications"]}, "onAddToCart": {"type": "function"}, "onToggleWishlist": {"type": "function"}, "onShare": {"type": "function"}}, "required": ["product"]}',
    '{"product": {"id": "1", "name": "Professional DSLR Camera", "description": "Capture stunning photos and videos with this professional-grade DSLR camera featuring advanced autofocus and 4K video recording.", "price": 1299.99, "originalPrice": 1599.99, "images": ["/api/placeholder/600/600", "/api/placeholder/600/600", "/api/placeholder/600/600", "/api/placeholder/600/600"], "rating": 4.8, "reviews": 324, "inStock": true, "category": "Electronics", "sku": "CAM-PRO-001", "features": ["24.2MP Full-Frame Sensor", "4K Video Recording at 60fps", "Advanced 45-Point Autofocus", "5-Axis Image Stabilization", "Weather-Sealed Body", "Dual Memory Card Slots"], "specifications": {"Sensor": "Full-Frame CMOS", "Resolution": "24.2 Megapixels", "ISO Range": "100-51200", "Video": "4K 60fps", "Weight": "850g", "Battery Life": "970 shots"}}}',
    ARRAY['product-detail', 'gallery', 'e-commerce', 'specifications']::text[],
    '2025-07-17T03:26:39.927537',
    '2025-07-17T03:26:39.927540'
);

-- Block 6: Product Detail - Tabs
INSERT INTO application_blocks (
    id,
    name,
    description,
    block_type,
    app_type,
    react_template,
    dependencies,
    props_schema,
    example_props,
    tags,
    created_at,
    updated_at
) VALUES (
    'a31c9c08-e18d-4ab4-a4ef-131b9c3bbc59',
    'Product Detail - Tabs',
    'Product detail with tabbed content sections',
    'product-detail',
    'e-commerce',
    'import React from ''react'';
import { Tabs, TabsContent, TabsList, TabsTrigger } from ''@/components/ui/tabs'';
import { Card, CardContent } from ''@/components/ui/card'';
import { Badge } from ''@/components/ui/badge'';
import { Star, Package, Truck, Shield } from ''lucide-react'';

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
                                  ? ''fill-primary text-primary''
                                  : ''text-muted''
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
}',
    '{"npm": ["lucide-react"], "components": ["Tabs", "Card", "Badge"]}',
    '{"type": "object", "properties": {"product": {"type": "object", "required": ["description", "features", "specifications", "shipping", "warranty"]}, "reviews": {"type": "array", "items": {"type": "object"}}}, "required": ["product"]}',
    '{"product": {"description": "This premium product delivers exceptional performance and reliability for all your needs.", "features": ["Advanced technology integration", "Energy efficient design", "Durable construction", "User-friendly interface"], "specifications": {"Dimensions": "10 x 8 x 6 inches", "Weight": "2.5 lbs", "Material": "Aluminum alloy", "Power": "USB-C charging"}, "shipping": {"methods": [{"name": "Standard Shipping", "price": "$5.99", "duration": "5-7 business days"}, {"name": "Express Shipping", "price": "$12.99", "duration": "2-3 business days"}, {"name": "Next Day", "price": "$24.99", "duration": "1 business day"}], "returns": "30-day return policy. Items must be in original condition."}, "warranty": {"period": "2 Year Limited Warranty", "coverage": ["Manufacturing defects", "Component failures", "Free repairs or replacement"]}}}',
    ARRAY['product-detail', 'tabs', 'e-commerce', 'reviews', 'specifications']::text[],
    '2025-07-17T03:26:39.927551',
    '2025-07-17T03:26:39.927552'
);

-- Block 7: Shopping Cart - Sidebar
INSERT INTO application_blocks (
    id,
    name,
    description,
    block_type,
    app_type,
    react_template,
    dependencies,
    props_schema,
    example_props,
    tags,
    created_at,
    updated_at
) VALUES (
    'a95df8b0-4de6-4e3d-a1cb-2fa18714b172',
    'Shopping Cart - Sidebar',
    'Slide-out shopping cart sidebar with items and checkout',
    'shopping-cart',
    'e-commerce',
    'import React from ''react'';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetFooter } from ''@/components/ui/sheet'';
import { Button } from ''@/components/ui/button'';
import { Separator } from ''@/components/ui/separator'';
import { X, Plus, Minus, ShoppingBag } from ''lucide-react'';

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
                <span>{shipping === 0 ? ''FREE'' : `$${shipping.toFixed(2)}`}</span>
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
}',
    '{"npm": ["lucide-react"], "components": ["Sheet", "Button", "Separator"]}',
    '{"type": "object", "properties": {"isOpen": {"type": "boolean"}, "onClose": {"type": "function"}, "items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "quantity": {"type": "number"}, "image": {"type": "string"}, "variant": {"type": "string"}}, "required": ["id", "name", "price", "quantity", "image"]}}, "onUpdateQuantity": {"type": "function"}, "onRemoveItem": {"type": "function"}, "onCheckout": {"type": "function"}}, "required": ["isOpen", "onClose", "items", "onUpdateQuantity", "onRemoveItem", "onCheckout"]}',
    '{"isOpen": true, "items": [{"id": "1", "name": "Wireless Mouse", "price": 29.99, "quantity": 2, "image": "/api/placeholder/80/80", "variant": "Black"}, {"id": "2", "name": "USB-C Cable", "price": 12.99, "quantity": 1, "image": "/api/placeholder/80/80"}]}',
    ARRAY['shopping-cart', 'sidebar', 'e-commerce', 'checkout']::text[],
    '2025-07-17T03:26:39.927561',
    '2025-07-17T03:26:39.927563'
);

-- Block 8: Shopping Cart - Page
INSERT INTO application_blocks (
    id,
    name,
    description,
    block_type,
    app_type,
    react_template,
    dependencies,
    props_schema,
    example_props,
    tags,
    created_at,
    updated_at
) VALUES (
    '91011965-c721-490d-ab4c-af896a022723',
    'Shopping Cart - Page',
    'Full page shopping cart with detailed item management',
    'shopping-cart',
    'e-commerce',
    'import React from ''react'';
import { Card, CardContent, CardHeader, CardTitle } from ''@/components/ui/card'';
import { Button } from ''@/components/ui/button'';
import { Input } from ''@/components/ui/input'';
import { Separator } from ''@/components/ui/separator'';
import { Badge } from ''@/components/ui/badge'';
import { Trash2, Plus, Minus, ShoppingBag, ArrowRight, Tag } from ''lucide-react'';

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
  const [couponCode, setCouponCode] = React.useState('''');
  
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
                <span>{shipping === 0 ? ''FREE'' : `$${shipping.toFixed(2)}`}</span>
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
                    setCouponCode('''');
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
}',
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Input", "Separator", "Badge"]}',
    '{"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "description": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "quantity": {"type": "number"}, "image": {"type": "string"}, "variant": {"type": "string"}, "inStock": {"type": "boolean"}}, "required": ["id", "name", "description", "price", "quantity", "image", "inStock"]}}, "onUpdateQuantity": {"type": "function"}, "onRemoveItem": {"type": "function"}, "onApplyCoupon": {"type": "function"}, "onCheckout": {"type": "function"}, "appliedCoupon": {"type": "object", "properties": {"code": {"type": "string"}, "discount": {"type": "number"}}}}, "required": ["items", "onUpdateQuantity", "onRemoveItem", "onApplyCoupon", "onCheckout"]}',
    '{"items": [{"id": "1", "name": "Wireless Keyboard", "description": "Bluetooth mechanical keyboard with RGB backlighting", "price": 89.99, "originalPrice": 119.99, "quantity": 1, "image": "/api/placeholder/128/128", "variant": "Cherry MX Blue", "inStock": true}]}',
    ARRAY['shopping-cart', 'page', 'e-commerce', 'checkout', 'order-summary']::text[],
    '2025-07-17T03:26:39.927572',
    '2025-07-17T03:26:39.927573'
);

-- Block 9: Checkout - Single Page
INSERT INTO application_blocks (
    id,
    name,
    description,
    block_type,
    app_type,
    react_template,
    dependencies,
    props_schema,
    example_props,
    tags,
    created_at,
    updated_at
) VALUES (
    'f51aa48a-72ec-4589-b776-158513e5e567',
    'Checkout - Single Page',
    'Complete single-page checkout with billing, shipping, and payment',
    'checkout',
    'e-commerce',
    'import React from ''react'';
import { Card, CardContent, CardHeader, CardTitle } from ''@/components/ui/card'';
import { Input } from ''@/components/ui/input'';
import { Label } from ''@/components/ui/label'';
import { Button } from ''@/components/ui/button'';
import { RadioGroup, RadioGroupItem } from ''@/components/ui/radio-group'';
import { Checkbox } from ''@/components/ui/checkbox'';
import { Separator } from ''@/components/ui/separator'';
import { CreditCard, Truck, Lock } from ''lucide-react'';

interface CheckoutSinglePageProps {
  orderSummary: {
    subtotal: number;
    shipping: number;
    tax: number;
    total: number;
    items: number;
  };
  onSubmit: (formData: any) => void;
}

export function CheckoutSinglePage({ orderSummary, onSubmit }: CheckoutSinglePageProps) {
  const [billingData, setBillingData] = React.useState({
    email: '''',
    firstName: '''',
    lastName: '''',
    address: '''',
    city: '''',
    state: '''',
    zip: '''',
    country: ''US''
  });
  
  const [sameAsShipping, setSameAsShipping] = React.useState(true);
  const [paymentMethod, setPaymentMethod] = React.useState(''card'');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ billing: billingData, sameAsShipping, paymentMethod });
  };

  return (
    <form onSubmit={handleSubmit} className="grid lg:grid-cols-3 gap-8">
      <div className="lg:col-span-2 space-y-6">
        {/* Contact Information */}
        <Card>
          <CardHeader>
            <CardTitle>Contact Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="email">Email Address</Label>
              <Input
                id="email"
                type="email"
                required
                value={billingData.email}
                onChange={(e) => setBillingData({...billingData, email: e.target.value})}
                placeholder="john@example.com"
              />
            </div>
          </CardContent>
        </Card>

        {/* Billing Address */}
        <Card>
          <CardHeader>
            <CardTitle>Billing Address</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="firstName">First Name</Label>
                <Input
                  id="firstName"
                  required
                  value={billingData.firstName}
                  onChange={(e) => setBillingData({...billingData, firstName: e.target.value})}
                />
              </div>
              <div>
                <Label htmlFor="lastName">Last Name</Label>
                <Input
                  id="lastName"
                  required
                  value={billingData.lastName}
                  onChange={(e) => setBillingData({...billingData, lastName: e.target.value})}
                />
              </div>
            </div>
            
            <div>
              <Label htmlFor="address">Street Address</Label>
              <Input
                id="address"
                required
                value={billingData.address}
                onChange={(e) => setBillingData({...billingData, address: e.target.value})}
                placeholder="123 Main St"
              />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="city">City</Label>
                <Input
                  id="city"
                  required
                  value={billingData.city}
                  onChange={(e) => setBillingData({...billingData, city: e.target.value})}
                />
              </div>
              <div>
                <Label htmlFor="state">State</Label>
                <Input
                  id="state"
                  required
                  value={billingData.state}
                  onChange={(e) => setBillingData({...billingData, state: e.target.value})}
                  placeholder="CA"
                />
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="zip">ZIP Code</Label>
                <Input
                  id="zip"
                  required
                  value={billingData.zip}
                  onChange={(e) => setBillingData({...billingData, zip: e.target.value})}
                  placeholder="12345"
                />
              </div>
              <div>
                <Label htmlFor="country">Country</Label>
                <Input
                  id="country"
                  required
                  value={billingData.country}
                  onChange={(e) => setBillingData({...billingData, country: e.target.value})}
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Shipping Address */}
        <Card>
          <CardHeader>
            <CardTitle>Shipping Address</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-2">
              <Checkbox
                id="sameAsShipping"
                checked={sameAsShipping}
                onCheckedChange={(checked) => setSameAsShipping(checked as boolean)}
              />
              <Label htmlFor="sameAsShipping">Same as billing address</Label>
            </div>
            {!sameAsShipping && (
              <div className="mt-4 text-sm text-muted-foreground">
                {/* Add shipping form fields here */}
                Shipping address form would appear here
              </div>
            )}
          </CardContent>
        </Card>

        {/* Payment Method */}
        <Card>
          <CardHeader>
            <CardTitle>Payment Method</CardTitle>
          </CardHeader>
          <CardContent>
            <RadioGroup value={paymentMethod} onValueChange={setPaymentMethod}>
              <div className="space-y-4">
                <div className="flex items-center space-x-2 p-4 border rounded-lg">
                  <RadioGroupItem value="card" id="card" />
                  <Label htmlFor="card" className="flex-1 cursor-pointer flex items-center">
                    <CreditCard className="w-4 h-4 mr-2" />
                    Credit/Debit Card
                  </Label>
                </div>
                
                {paymentMethod === ''card'' && (
                  <div className="ml-6 space-y-4">
                    <div>
                      <Label htmlFor="cardNumber">Card Number</Label>
                      <Input
                        id="cardNumber"
                        placeholder="1234 5678 9012 3456"
                        required
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="expiry">Expiry Date</Label>
                        <Input
                          id="expiry"
                          placeholder="MM/YY"
                          required
                        />
                      </div>
                      <div>
                        <Label htmlFor="cvv">CVV</Label>
                        <Input
                          id="cvv"
                          placeholder="123"
                          required
                        />
                      </div>
                    </div>
                  </div>
                )}
                
                <div className="flex items-center space-x-2 p-4 border rounded-lg">
                  <RadioGroupItem value="paypal" id="paypal" />
                  <Label htmlFor="paypal" className="flex-1 cursor-pointer">
                    PayPal
                  </Label>
                </div>
              </div>
            </RadioGroup>
          </CardContent>
        </Card>
      </div>
      
      {/* Order Summary */}
      <div className="space-y-4">
        <Card className="sticky top-4">
          <CardHeader>
            <CardTitle>Order Summary</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Subtotal ({orderSummary.items} items)</span>
                <span>${orderSummary.subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Shipping</span>
                <span>${orderSummary.shipping.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Tax</span>
                <span>${orderSummary.tax.toFixed(2)}</span>
              </div>
              <Separator />
              <div className="flex justify-between font-semibold text-lg">
                <span>Total</span>
                <span>${orderSummary.total.toFixed(2)}</span>
              </div>
            </div>
            
            <Button type="submit" className="w-full" size="lg">
              <Lock className="w-4 h-4 mr-2" />
              Place Order
            </Button>
            
            <div className="text-xs text-center text-muted-foreground space-y-1">
              <p className="flex items-center justify-center">
                <Lock className="w-3 h-3 mr-1" />
                Secure checkout
              </p>
              <p>By placing your order, you agree to our Terms of Service</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </form>
  );
}',
    '{"npm": ["lucide-react"], "components": ["Card", "Input", "Label", "Button", "RadioGroup", "Checkbox", "Separator"]}',
    '{}',
    '{}',
    ARRAY['checkout', 'e-commerce', 'payment', 'billing', 'shipping']::text[],
    '2025-07-17T03:26:39.927857',
    '2025-07-17T03:26:39.927877'
);

-- Block 10: Order Summary - Card
INSERT INTO application_blocks (
    id,
    name,
    description,
    block_type,
    app_type,
    react_template,
    dependencies,
    props_schema,
    example_props,
    tags,
    created_at,
    updated_at
) VALUES (
    '02880d57-ded9-4e9e-92b2-9fa655b06cdf',
    'Order Summary - Card',
    'Compact order summary card for checkout pages',
    'order-summary',
    'e-commerce',
    'import React from ''react'';
import { Card, CardContent, CardHeader, CardTitle } from ''@/components/ui/card'';
import { Separator } from ''@/components/ui/separator'';
import { Badge } from ''@/components/ui/badge'';

interface OrderItem {
  id: string;
  name: string;
  quantity: number;
  price: number;
  image: string;
}

interface OrderSummaryCardProps {
  items: OrderItem[];
  subtotal: number;
  shipping: number;
  tax: number;
  discount?: number;
  discountCode?: string;
  showItems?: boolean;
}

export function OrderSummaryCard({
  items,
  subtotal,
  shipping,
  tax,
  discount = 0,
  discountCode,
  showItems = true
}: OrderSummaryCardProps) {
  const total = subtotal - discount + shipping + tax;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Order Summary</span>
          <Badge variant="secondary">{items.length} items</Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {showItems && (
          <>
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {items.map((item) => (
                <div key={item.id} className="flex gap-3">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="w-12 h-12 object-cover rounded"
                  />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold truncate">{item.name}</p>
                    <p className="text-xs text-muted-foreground">
                      Qty: {item.quantity} × ${item.price.toFixed(2)}
                    </p>
                  </div>
                  <p className="text-sm font-semibold">
                    ${(item.quantity * item.price).toFixed(2)}
                  </p>
                </div>
              ))}
            </div>
            <Separator />
          </>
        )}
        
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span>Subtotal</span>
            <span>${subtotal.toFixed(2)}</span>
          </div>
          
          {discount > 0 && (
            <div className="flex justify-between text-sm text-success">
              <span>Discount {discountCode && `(${discountCode})`}</span>
              <span>-${discount.toFixed(2)}</span>
            </div>
          )}
          
          <div className="flex justify-between text-sm">
            <span>Shipping</span>
            <span>{shipping === 0 ? ''FREE'' : `$${shipping.toFixed(2)}`}</span>
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
  );
}',
    '{"npm": [], "components": ["Card", "Separator", "Badge"]}',
    '{}',
    '{}',
    ARRAY['order-summary', 'checkout', 'e-commerce']::text[],
    '2025-07-17T03:26:39.927899',
    '2025-07-17T03:26:39.927906'
);

-- Block 11: Product Reviews - List
INSERT INTO application_blocks (
    id,
    name,
    description,
    block_type,
    app_type,
    react_template,
    dependencies,
    props_schema,
    example_props,
    tags,
    created_at,
    updated_at
) VALUES (
    'a7a7802f-8cc1-4c90-a491-af711cd573b5',
    'Product Reviews - List',
    'Product reviews list with ratings, filters, and helpful votes',
    'reviews',
    'e-commerce',
    'import React from ''react'';
import { Card, CardContent } from ''@/components/ui/card'';
import { Button } from ''@/components/ui/button'';
import { Badge } from ''@/components/ui/badge'';
import { Progress } from ''@/components/ui/progress'';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from ''@/components/ui/select'';
import { Star, ThumbsUp, CheckCircle } from ''lucide-react'';

interface Review {
  id: string;
  author: string;
  rating: number;
  date: string;
  title: string;
  comment: string;
  helpful: number;
  verified: boolean;
  images?: string[];
}

interface ProductReviewsListProps {
  reviews: Review[];
  averageRating: number;
  totalReviews: number;
  ratingBreakdown: Record<number, number>;
  onSortChange?: (sort: string) => void;
  onHelpful?: (reviewId: string) => void;
}

export function ProductReviewsList({
  reviews,
  averageRating,
  totalReviews,
  ratingBreakdown,
  onSortChange,
  onHelpful
}: ProductReviewsListProps) {
  return (
    <div className="space-y-6">
      {/* Reviews Summary */}
      <div className="grid md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="p-6 text-center">
            <div className="text-4xl font-semibold mb-2">{averageRating.toFixed(1)}</div>
            <div className="flex justify-center mb-2">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  className={`w-5 h-5 ${
                    i < Math.floor(averageRating)
                      ? ''fill-primary text-primary''
                      : ''text-muted''
                  }`}
                />
              ))}
            </div>
            <p className="text-sm text-muted-foreground">
              Based on {totalReviews} reviews
            </p>
          </CardContent>
        </Card>
        
        <Card className="md:col-span-2">
          <CardContent className="p-6">
            <h3 className="font-semibold mb-4">Rating Breakdown</h3>
            <div className="space-y-2">
              {[5, 4, 3, 2, 1].map((rating) => (
                <div key={rating} className="flex items-center gap-3">
                  <span className="text-sm w-4">{rating}</span>
                  <Star className="w-4 h-4 fill-primary text-primary" />
                  <Progress 
                    value={(ratingBreakdown[rating] / totalReviews) * 100} 
                    className="flex-1"
                  />
                  <span className="text-sm text-muted-foreground w-12 text-right">
                    {ratingBreakdown[rating]}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
      
      {/* Reviews Controls */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Customer Reviews</h3>
        <Select onValueChange={onSortChange} defaultValue="recent">
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="recent">Most Recent</SelectItem>
            <SelectItem value="helpful">Most Helpful</SelectItem>
            <SelectItem value="rating-high">Highest Rating</SelectItem>
            <SelectItem value="rating-low">Lowest Rating</SelectItem>
          </SelectContent>
        </Select>
      </div>
      
      {/* Reviews List */}
      <div className="space-y-4">
        {reviews.map((review) => (
          <Card key={review.id}>
            <CardContent className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-semibold">{review.author}</span>
                    {review.verified && (
                      <Badge variant="secondary" className="text-xs">
                        <CheckCircle className="w-3 h-3 mr-1" />
                        Verified Purchase
                      </Badge>
                    )}
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="flex">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`w-4 h-4 ${
                            i < review.rating
                              ? ''fill-primary text-primary''
                              : ''text-muted''
                          }`}
                        />
                      ))}
                    </div>
                    <span className="text-sm text-muted-foreground">{review.date}</span>
                  </div>
                </div>
              </div>
              
              <h4 className="font-semibold mb-2">{review.title}</h4>
              <p className="text-sm mb-4">{review.comment}</p>
              
              {review.images && review.images.length > 0 && (
                <div className="flex gap-2 mb-4">
                  {review.images.map((image, index) => (
                    <img
                      key={index}
                      src={image}
                      alt={`Review image ${index + 1}`}
                      className="w-20 h-20 object-cover rounded"
                    />
                  ))}
                </div>
              )}
              
              <div className="flex items-center gap-4">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onHelpful?.(review.id)}
                >
                  <ThumbsUp className="w-4 h-4 mr-2" />
                  Helpful ({review.helpful})
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}',
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge", "Progress", "Select"]}',
    '{}',
    '{}',
    ARRAY['reviews', 'ratings', 'e-commerce', 'product-feedback']::text[],
    '2025-07-17T03:26:39.927921',
    '2025-07-17T03:26:39.927927'
);

-- Block 12: Product Filter - Sidebar
INSERT INTO application_blocks (
    id,
    name,
    description,
    block_type,
    app_type,
    react_template,
    dependencies,
    props_schema,
    example_props,
    tags,
    created_at,
    updated_at
) VALUES (
    'ff1cdff5-486a-45f3-8b70-9ffb6ee0ec09',
    'Product Filter - Sidebar',
    'Product filtering sidebar with multiple filter options',
    'product-filter',
    'e-commerce',
    'import React from ''react'';
import { Card, CardContent, CardHeader, CardTitle } from ''@/components/ui/card'';
import { Checkbox } from ''@/components/ui/checkbox'';
import { Label } from ''@/components/ui/label'';
import { Slider } from ''@/components/ui/slider'';
import { Button } from ''@/components/ui/button'';
import { Separator } from ''@/components/ui/separator'';
import { Badge } from ''@/components/ui/badge'';
import { X } from ''lucide-react'';

interface FilterOption {
  id: string;
  label: string;
  count: number;
}

interface ProductFilterSidebarProps {
  categories: FilterOption[];
  brands: FilterOption[];
  priceRange: { min: number; max: number };
  selectedFilters: {
    categories: string[];
    brands: string[];
    price: [number, number];
    inStock: boolean;
    onSale: boolean;
  };
  onFilterChange: (filters: any) => void;
  onClearAll: () => void;
}

export function ProductFilterSidebar({
  categories,
  brands,
  priceRange,
  selectedFilters,
  onFilterChange,
  onClearAll
}: ProductFilterSidebarProps) {
  const activeFilterCount = 
    selectedFilters.categories.length + 
    selectedFilters.brands.length +
    (selectedFilters.inStock ? 1 : 0) +
    (selectedFilters.onSale ? 1 : 0);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Filters</span>
          {activeFilterCount > 0 && (
            <div className="flex items-center gap-2">
              <Badge variant="secondary">{activeFilterCount}</Badge>
              <Button
                variant="ghost"
                size="sm"
                onClick={onClearAll}
                className="h-auto p-1"
              >
                Clear all
              </Button>
            </div>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Categories */}
        <div>
          <h4 className="font-semibold mb-3">Categories</h4>
          <div className="space-y-2">
            {categories.map((category) => (
              <div key={category.id} className="flex items-center space-x-2">
                <Checkbox
                  id={category.id}
                  checked={selectedFilters.categories.includes(category.id)}
                  onCheckedChange={(checked) => {
                    const newCategories = checked
                      ? [...selectedFilters.categories, category.id]
                      : selectedFilters.categories.filter(c => c !== category.id);
                    onFilterChange({ ...selectedFilters, categories: newCategories });
                  }}
                />
                <Label
                  htmlFor={category.id}
                  className="flex-1 cursor-pointer text-sm"
                >
                  {category.label}
                </Label>
                <span className="text-xs text-muted-foreground">
                  ({category.count})
                </span>
              </div>
            ))}
          </div>
        </div>
        
        <Separator />
        
        {/* Price Range */}
        <div>
          <h4 className="font-semibold mb-3">Price Range</h4>
          <div className="space-y-4">
            <Slider
              value={selectedFilters.price}
              min={priceRange.min}
              max={priceRange.max}
              step={10}
              onValueChange={(value) => {
                onFilterChange({ ...selectedFilters, price: value as [number, number] });
              }}
              className="w-full"
            />
            <div className="flex items-center justify-between text-sm">
              <span>${selectedFilters.price[0]}</span>
              <span>${selectedFilters.price[1]}</span>
            </div>
          </div>
        </div>
        
        <Separator />
        
        {/* Brands */}
        <div>
          <h4 className="font-semibold mb-3">Brands</h4>
          <div className="space-y-2">
            {brands.map((brand) => (
              <div key={brand.id} className="flex items-center space-x-2">
                <Checkbox
                  id={brand.id}
                  checked={selectedFilters.brands.includes(brand.id)}
                  onCheckedChange={(checked) => {
                    const newBrands = checked
                      ? [...selectedFilters.brands, brand.id]
                      : selectedFilters.brands.filter(b => b !== brand.id);
                    onFilterChange({ ...selectedFilters, brands: newBrands });
                  }}
                />
                <Label
                  htmlFor={brand.id}
                  className="flex-1 cursor-pointer text-sm"
                >
                  {brand.label}
                </Label>
                <span className="text-xs text-muted-foreground">
                  ({brand.count})
                </span>
              </div>
            ))}
          </div>
        </div>
        
        <Separator />
        
        {/* Additional Filters */}
        <div>
          <h4 className="font-semibold mb-3">Availability</h4>
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <Checkbox
                id="inStock"
                checked={selectedFilters.inStock}
                onCheckedChange={(checked) => {
                  onFilterChange({ ...selectedFilters, inStock: checked as boolean });
                }}
              />
              <Label htmlFor="inStock" className="cursor-pointer text-sm">
                In Stock Only
              </Label>
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox
                id="onSale"
                checked={selectedFilters.onSale}
                onCheckedChange={(checked) => {
                  onFilterChange({ ...selectedFilters, onSale: checked as boolean });
                }}
              />
              <Label htmlFor="onSale" className="cursor-pointer text-sm">
                On Sale
              </Label>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}',
    '{"npm": ["lucide-react"], "components": ["Card", "Checkbox", "Label", "Slider", "Button", "Separator", "Badge"]}',
    '{}',
    '{}',
    ARRAY['filter', 'sidebar', 'e-commerce', 'product-filter']::text[],
    '2025-07-17T03:26:39.927944',
    '2025-07-17T03:26:39.927950'
);

-- Block 13: Category Banner
INSERT INTO application_blocks (
    id,
    name,
    description,
    block_type,
    app_type,
    react_template,
    dependencies,
    props_schema,
    example_props,
    tags,
    created_at,
    updated_at
) VALUES (
    '790365a8-61c3-4eee-ae1b-5a3fe4d655d4',
    'Category Banner',
    'Category page banner with breadcrumb and description',
    'category-banner',
    'e-commerce',
    'import React from ''react'';
import { ChevronRight } from ''lucide-react'';

interface CategoryBannerProps {
  category: {
    name: string;
    description: string;
    image: string;
    itemCount: number;
  };
  breadcrumbs: Array<{
    label: string;
    href?: string;
  }>;
}

export function CategoryBanner({ category, breadcrumbs }: CategoryBannerProps) {
  return (
    <div className="relative overflow-hidden rounded-lg">
      {/* Background Image */}
      <div className="absolute inset-0">
        <img
          src={category.image}
          alt={category.name}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-background/90 to-background/50" />
      </div>
      
      {/* Content */}
      <div className="relative p-8 md:p-12 lg:p-16">
        {/* Breadcrumb */}
        <nav className="flex items-center space-x-2 text-sm mb-4">
          {breadcrumbs.map((crumb, index) => (
            <React.Fragment key={index}>
              {index > 0 && <ChevronRight className="w-4 h-4" />}
              {crumb.href ? (
                <a
                  href={crumb.href}
                  className="hover:text-primary transition-colors"
                >
                  {crumb.label}
                </a>
              ) : (
                <span className="text-muted-foreground">{crumb.label}</span>
              )}
            </React.Fragment>
          ))}
        </nav>
        
        {/* Category Info */}
        <h1 className="text-4xl md:text-5xl font-semibold mb-4">
          {category.name}
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mb-4">
          {category.description}
        </p>
        <p className="text-sm font-semibold">
          {category.itemCount} Products
        </p>
      </div>
    </div>
  );
}',
    '{"npm": ["lucide-react"], "components": []}',
    '{}',
    '{}',
    ARRAY['category', 'banner', 'e-commerce', 'breadcrumb']::text[],
    '2025-07-17T03:26:39.927962',
    '2025-07-17T03:26:39.927968'
);

-- Block 14: Sale Banner - Countdown
INSERT INTO application_blocks (
    id,
    name,
    description,
    block_type,
    app_type,
    react_template,
    dependencies,
    props_schema,
    example_props,
    tags,
    created_at,
    updated_at
) VALUES (
    '7a59da55-5eef-46f2-aaee-f114e37ad25f',
    'Sale Banner - Countdown',
    'Promotional sale banner with countdown timer',
    'sale-banner',
    'e-commerce',
    'import React from ''react'';
import { Card, CardContent } from ''@/components/ui/card'';
import { Button } from ''@/components/ui/button'';
import { Badge } from ''@/components/ui/badge'';
import { Clock, Zap } from ''lucide-react'';

interface SaleBannerCountdownProps {
  title: string;
  subtitle: string;
  endDate: Date;
  discountPercentage: number;
  ctaText: string;
  onCtaClick: () => void;
  variant?: ''default'' | ''flash'' | ''seasonal'';
}

export function SaleBannerCountdown({
  title,
  subtitle,
  endDate,
  discountPercentage,
  ctaText,
  onCtaClick,
  variant = ''default''
}: SaleBannerCountdownProps) {
  const [timeLeft, setTimeLeft] = React.useState({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0
  });

  React.useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date().getTime();
      const distance = endDate.getTime() - now;

      if (distance > 0) {
        setTimeLeft({
          days: Math.floor(distance / (1000 * 60 * 60 * 24)),
          hours: Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
          minutes: Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)),
          seconds: Math.floor((distance % (1000 * 60)) / 1000)
        });
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [endDate]);

  const bgClass = {
    default: ''bg-gradient-to-r from-primary to-primary/80'',
    flash: ''bg-gradient-to-r from-destructive to-orange-500'',
    seasonal: ''bg-gradient-to-r from-green-500 to-red-500''
  };

  return (
    <Card className={`${bgClass[variant]} text-primary-foreground overflow-hidden`}>
      <CardContent className="p-6 md:p-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="text-center md:text-left">
            <div className="flex items-center gap-2 mb-2">
              {variant === ''flash'' && <Zap className="w-5 h-5" />}
              <Badge variant="secondary" className="text-sm">
                Save up to {discountPercentage}%
              </Badge>
            </div>
            <h2 className="text-2xl md:text-3xl font-semibold mb-2">{title}</h2>
            <p className="text-lg opacity-90">{subtitle}</p>
          </div>
          
          <div className="flex flex-col items-center gap-4">
            <div className="flex items-center gap-2">
              <Clock className="w-5 h-5" />
              <span className="text-sm font-semibold">Sale ends in:</span>
            </div>
            <div className="grid grid-cols-4 gap-2 text-center">
              <div className="bg-background/20 backdrop-blur rounded p-3">
                <div className="text-2xl font-semibold">{timeLeft.days}</div>
                <div className="text-xs opacity-80">Days</div>
              </div>
              <div className="bg-background/20 backdrop-blur rounded p-3">
                <div className="text-2xl font-semibold">{timeLeft.hours}</div>
                <div className="text-xs opacity-80">Hours</div>
              </div>
              <div className="bg-background/20 backdrop-blur rounded p-3">
                <div className="text-2xl font-semibold">{timeLeft.minutes}</div>
                <div className="text-xs opacity-80">Mins</div>
              </div>
              <div className="bg-background/20 backdrop-blur rounded p-3">
                <div className="text-2xl font-semibold">{timeLeft.seconds}</div>
                <div className="text-xs opacity-80">Secs</div>
              </div>
            </div>
            <Button
              size="lg"
              variant="secondary"
              onClick={onCtaClick}
              className="w-full md:w-auto"
            >
              {ctaText}
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}',
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge"]}',
    '{}',
    '{}',
    ARRAY['sale', 'banner', 'countdown', 'promotion', 'e-commerce']::text[],
    '2025-07-17T03:26:39.927981',
    '2025-07-17T03:26:39.927987'
);

-- Block 15: Wishlist Grid
INSERT INTO application_blocks (
    id,
    name,
    description,
    block_type,
    app_type,
    react_template,
    dependencies,
    props_schema,
    example_props,
    tags,
    created_at,
    updated_at
) VALUES (
    '5d6a47cd-2aac-44cc-b617-80e6bcb2de77',
    'Wishlist Grid',
    'User wishlist grid with product management',
    'wishlist',
    'e-commerce',
    'import React from ''react'';
import { Card, CardContent } from ''@/components/ui/card'';
import { Button } from ''@/components/ui/button'';
import { Badge } from ''@/components/ui/badge'';
import { Heart, ShoppingCart, X, Share2 } from ''lucide-react'';

interface WishlistItem {
  id: string;
  name: string;
  price: number;
  originalPrice?: number;
  image: string;
  inStock: boolean;
  addedDate: string;
}

interface WishlistGridProps {
  items: WishlistItem[];
  onRemove: (itemId: string) => void;
  onAddToCart: (itemId: string) => void;
  onShare: (itemId: string) => void;
}

export function WishlistGrid({
  items,
  onRemove,
  onAddToCart,
  onShare
}: WishlistGridProps) {
  if (items.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] text-center">
        <Heart className="w-16 h-16 text-muted-foreground mb-4" />
        <h2 className="text-2xl font-semibold mb-2">Your wishlist is empty</h2>
        <p className="text-muted-foreground mb-8">
          Save items you love to your wishlist
        </p>
        <Button>Start Shopping</Button>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-semibold">
          My Wishlist ({items.length} items)
        </h2>
        <Button variant="outline" size="sm">
          <Share2 className="w-4 h-4 mr-2" />
          Share Wishlist
        </Button>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {items.map((item) => (
          <Card key={item.id} className="relative group">
            <Button
              variant="ghost"
              size="icon"
              className="absolute top-2 right-2 z-10 opacity-0 group-hover:opacity-100 transition-opacity"
              onClick={() => onRemove(item.id)}
            >
              <X className="w-4 h-4" />
            </Button>
            
            <CardContent className="p-4">
              <div className="aspect-square relative mb-4">
                <img
                  src={item.image}
                  alt={item.name}
                  className="w-full h-full object-cover rounded"
                />
                {!item.inStock && (
                  <div className="absolute inset-0 bg-background/80 flex items-center justify-center rounded">
                    <Badge variant="secondary">Out of Stock</Badge>
                  </div>
                )}
              </div>
              
              <h3 className="font-semibold text-sm mb-2 line-clamp-2">{item.name}</h3>
              
              <div className="flex items-baseline gap-2 mb-2">
                <p className="text-lg font-semibold">${item.price.toFixed(2)}</p>
                {item.originalPrice && (
                  <p className="text-sm text-muted-foreground line-through">
                    ${item.originalPrice.toFixed(2)}
                  </p>
                )}
              </div>
              
              <p className="text-xs text-muted-foreground mb-4">
                Added {item.addedDate}
              </p>
              
              <div className="flex gap-2">
                <Button
                  size="sm"
                  className="flex-1"
                  disabled={!item.inStock}
                  onClick={() => onAddToCart(item.id)}
                >
                  <ShoppingCart className="w-4 h-4 mr-2" />
                  Add to Cart
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => onShare(item.id)}
                >
                  <Share2 className="w-4 h-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}',
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge"]}',
    '{}',
    '{}',
    ARRAY['wishlist', 'favorites', 'e-commerce', 'saved-items']::text[],
    '2025-07-17T03:26:39.927999',
    '2025-07-17T03:26:39.928005'
);