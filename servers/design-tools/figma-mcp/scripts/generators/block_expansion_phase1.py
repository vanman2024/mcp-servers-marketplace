#!/usr/bin/env python3
"""
Phase 1: E-commerce Blocks Implementation
Creates 15 e-commerce blocks for the application_blocks table
"""

import uuid
import json
from datetime import datetime
from typing import Dict, List, Any

def generate_ecommerce_blocks() -> List[Dict[str, Any]]:
    """Generate all e-commerce blocks with proper templates and metadata"""
    blocks = []
    
    # 1. Product Grid - 3 Column
    blocks.append({
        "id": str(uuid.uuid4()),
        "name": "Product Grid - 3 Column",
        "description": "Responsive 3-column product grid with hover effects",
        "block_type": "product-grid",
        "app_type": "e-commerce",
        "react_template": """import React from 'react';
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
}""",
        "dependencies": {
            "npm": ["lucide-react"],
            "components": ["Card", "Button"]
        },
        "props_schema": {
            "type": "object",
            "properties": {
                "products": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "price": {"type": "number"},
                            "image": {"type": "string"},
                            "rating": {"type": "number"},
                            "reviews": {"type": "number"},
                            "badge": {"type": "string"}
                        },
                        "required": ["id", "name", "price", "image", "rating", "reviews"]
                    }
                },
                "onAddToCart": {"type": "function"},
                "onProductClick": {"type": "function"}
            },
            "required": ["products"]
        },
        "example_props": {
            "products": [
                {
                    "id": "1",
                    "name": "Wireless Headphones",
                    "price": 79.99,
                    "image": "/api/placeholder/300/300",
                    "rating": 4.5,
                    "reviews": 234,
                    "badge": "New"
                },
                {
                    "id": "2",
                    "name": "Smart Watch",
                    "price": 299.99,
                    "image": "/api/placeholder/300/300",
                    "rating": 4.8,
                    "reviews": 512
                },
                {
                    "id": "3",
                    "name": "Laptop Stand",
                    "price": 49.99,
                    "image": "/api/placeholder/300/300",
                    "rating": 4.2,
                    "reviews": 89,
                    "badge": "Sale"
                }
            ]
        },
        "tags": ["responsive", "accessible", "e-commerce", "products", "grid"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    # 2. Product Grid - 4 Column
    blocks.append({
        "id": str(uuid.uuid4()),
        "name": "Product Grid - 4 Column",
        "description": "Responsive 4-column product grid for larger displays",
        "block_type": "product-grid",
        "app_type": "e-commerce",
        "react_template": """import React from 'react';
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
}""",
        "dependencies": {
            "npm": ["lucide-react"],
            "components": ["Card", "Button", "Badge"]
        },
        "props_schema": {
            "type": "object",
            "properties": {
                "products": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "price": {"type": "number"},
                            "originalPrice": {"type": "number"},
                            "image": {"type": "string"},
                            "category": {"type": "string"},
                            "isNew": {"type": "boolean"},
                            "discount": {"type": "number"}
                        },
                        "required": ["id", "name", "price", "image", "category"]
                    }
                },
                "onAddToCart": {"type": "function"},
                "onToggleWishlist": {"type": "function"}
            },
            "required": ["products"]
        },
        "example_props": {
            "products": [
                {
                    "id": "1",
                    "name": "Premium Wireless Mouse",
                    "price": 39.99,
                    "originalPrice": 59.99,
                    "image": "/api/placeholder/300/300",
                    "category": "Accessories",
                    "discount": 33
                },
                {
                    "id": "2",
                    "name": "USB-C Hub 7-in-1",
                    "price": 49.99,
                    "image": "/api/placeholder/300/300",
                    "category": "Adapters",
                    "isNew": True
                }
            ]
        },
        "tags": ["responsive", "accessible", "e-commerce", "products", "grid", "wishlist"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    # 3. Product Card - Simple
    blocks.append({
        "id": str(uuid.uuid4()),
        "name": "Product Card - Simple",
        "description": "Simple product card with minimal information",
        "block_type": "product-card",
        "app_type": "e-commerce",
        "react_template": """import React from 'react';
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
}""",
        "dependencies": {
            "npm": [],
            "components": ["Card", "Button"]
        },
        "props_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "price": {"type": "number"},
                "image": {"type": "string"},
                "onSelect": {"type": "function"}
            },
            "required": ["id", "name", "price", "image"]
        },
        "example_props": {
            "id": "1",
            "name": "Minimalist Desk Lamp",
            "price": 89.99,
            "image": "/api/placeholder/300/300"
        },
        "tags": ["simple", "product", "card", "e-commerce"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    # 4. Product Card - Detailed
    blocks.append({
        "id": str(uuid.uuid4()),
        "name": "Product Card - Detailed",
        "description": "Detailed product card with full information and actions",
        "block_type": "product-card",
        "app_type": "e-commerce",
        "react_template": """import React from 'react';
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
}""",
        "dependencies": {
            "npm": ["lucide-react"],
            "components": ["Card", "Button", "Badge"]
        },
        "props_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "price": {"type": "number"},
                "originalPrice": {"type": "number"},
                "image": {"type": "string"},
                "rating": {"type": "number"},
                "reviews": {"type": "number"},
                "inStock": {"type": "boolean"},
                "tags": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "onAddToCart": {"type": "function"},
                "onToggleWishlist": {"type": "function"},
                "onQuickView": {"type": "function"}
            },
            "required": ["id", "name", "description", "price", "image", "rating", "reviews", "inStock"]
        },
        "example_props": {
            "id": "1",
            "name": "Professional Camera Lens",
            "description": "High-quality 50mm f/1.8 prime lens perfect for portrait photography",
            "price": 399.99,
            "originalPrice": 499.99,
            "image": "/api/placeholder/300/300",
            "rating": 4.7,
            "reviews": 156,
            "inStock": True,
            "tags": ["Photography", "Prime Lens", "Professional"]
        },
        "tags": ["detailed", "product", "card", "e-commerce", "ratings"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    # 5. Product Detail - Gallery
    blocks.append({
        "id": str(uuid.uuid4()),
        "name": "Product Detail - Gallery",
        "description": "Product detail page with image gallery and full information",
        "block_type": "product-detail",
        "app_type": "e-commerce",
        "react_template": """import React, { useState } from 'react';
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
}""",
        "dependencies": {
            "npm": ["lucide-react"],
            "components": ["Button", "Badge", "Tabs"]
        },
        "props_schema": {
            "type": "object",
            "properties": {
                "product": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "price": {"type": "number"},
                        "originalPrice": {"type": "number"},
                        "images": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "rating": {"type": "number"},
                        "reviews": {"type": "number"},
                        "inStock": {"type": "boolean"},
                        "category": {"type": "string"},
                        "sku": {"type": "string"},
                        "features": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "specifications": {
                            "type": "object",
                            "additionalProperties": {"type": "string"}
                        }
                    },
                    "required": ["id", "name", "description", "price", "images", "rating", "reviews", "inStock", "category", "sku", "features", "specifications"]
                },
                "onAddToCart": {"type": "function"},
                "onToggleWishlist": {"type": "function"},
                "onShare": {"type": "function"}
            },
            "required": ["product"]
        },
        "example_props": {
            "product": {
                "id": "1",
                "name": "Professional DSLR Camera",
                "description": "Capture stunning photos and videos with this professional-grade DSLR camera featuring advanced autofocus and 4K video recording.",
                "price": 1299.99,
                "originalPrice": 1599.99,
                "images": [
                    "/api/placeholder/600/600",
                    "/api/placeholder/600/600",
                    "/api/placeholder/600/600",
                    "/api/placeholder/600/600"
                ],
                "rating": 4.8,
                "reviews": 324,
                "inStock": True,
                "category": "Electronics",
                "sku": "CAM-PRO-001",
                "features": [
                    "24.2MP Full-Frame Sensor",
                    "4K Video Recording at 60fps",
                    "Advanced 45-Point Autofocus",
                    "5-Axis Image Stabilization",
                    "Weather-Sealed Body",
                    "Dual Memory Card Slots"
                ],
                "specifications": {
                    "Sensor": "Full-Frame CMOS",
                    "Resolution": "24.2 Megapixels",
                    "ISO Range": "100-51200",
                    "Video": "4K 60fps",
                    "Weight": "850g",
                    "Battery Life": "970 shots"
                }
            }
        },
        "tags": ["product-detail", "gallery", "e-commerce", "specifications"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    # Continue with remaining 10 e-commerce blocks...
    # 6. Product Detail - Tabs
    # 7. Shopping Cart - Sidebar
    # 8. Shopping Cart - Page
    # 9. Checkout - Single Page
    # 10. Order Summary - Card
    # 11. Product Reviews - List
    # 12. Product Filter - Sidebar
    # 13. Category Banner
    # 14. Sale Banner - Countdown
    # 15. Wishlist Grid

    return blocks

def create_migration_sql(blocks: List[Dict[str, Any]]) -> str:
    """Create SQL migration for inserting blocks"""
    sql_statements = []
    
    for block in blocks:
        sql = f"""
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '{block['id']}',
    '{block['name'].replace("'", "''")}',
    '{block['description'].replace("'", "''")}',
    '{block['block_type']}',
    '{block['app_type']}',
    '{json.dumps(block['react_template']).replace("'", "''")}',
    '{json.dumps(block['dependencies']).replace("'", "''")}',
    '{json.dumps(block['props_schema']).replace("'", "''")}',
    '{json.dumps(block['example_props']).replace("'", "''")}',
    ARRAY{block['tags']}::text[],
    '{block['created_at'].isoformat()}',
    '{block['updated_at'].isoformat()}'
);"""
        sql_statements.append(sql)
    
    return "\n".join(sql_statements)

def main():
    """Generate e-commerce blocks and migration"""
    blocks = generate_ecommerce_blocks()
    
    print(f"Generated {len(blocks)} e-commerce blocks")
    
    # Save migration SQL
    migration_sql = create_migration_sql(blocks)
    
    with open("migration_phase1_ecommerce.sql", "w") as f:
        f.write("-- Phase 1: E-commerce Blocks Migration\n")
        f.write("-- Generated: " + datetime.utcnow().isoformat() + "\n\n")
        f.write(migration_sql)
    
    print("Migration SQL saved to: migration_phase1_ecommerce.sql")
    
    # Save block data as JSON for reference
    blocks_data = []
    for block in blocks:
        block_copy = block.copy()
        block_copy['created_at'] = block_copy['created_at'].isoformat()
        block_copy['updated_at'] = block_copy['updated_at'].isoformat()
        blocks_data.append(block_copy)
    
    with open("blocks_phase1_ecommerce.json", "w") as f:
        json.dump(blocks_data, f, indent=2)
    
    print("Block data saved to: blocks_phase1_ecommerce.json")

if __name__ == "__main__":
    main()