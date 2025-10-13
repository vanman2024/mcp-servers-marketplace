INSERT INTO application_blocks (id, name, description, block_type, app_type, react_template, dependencies, props_schema, example_props, tags) VALUES (
'e5cd0ce9-b848-4645-bf5b-1a3c15ece3d2',
'Product Card - Detailed',
'Detailed product card with full information and actions',
'product-card',
'e-commerce',
3747117import React from 'react';
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
}3747117,
'{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge"]}'::jsonb,
'{"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "description": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "image": {"type": "string"}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "inStock": {"type": "boolean"}, "tags": {"type": "array", "items": {"type": "string"}}, "onAddToCart": {"type": "function"}, "onToggleWishlist": {"type": "function"}, "onQuickView": {"type": "function"}}, "required": ["id", "name", "description", "price", "image", "rating", "reviews", "inStock"]}'::jsonb,
'{"id": "1", "name": "Professional Camera Lens", "description": "High-quality 50mm f/1.8 prime lens perfect for portrait photography", "price": 399.99, "originalPrice": 499.99, "image": "/api/placeholder/300/300", "rating": 4.7, "reviews": 156, "inStock": true, "tags": ["Photography", "Prime Lens", "Professional"]}'::jsonb,
ARRAY['detailed','product','card','e-commerce','ratings']
);

INSERT INTO application_blocks (id, name, description, block_type, app_type, react_template, dependencies, props_schema, example_props, tags) VALUES (
'9c149aa9-6cc2-437b-9680-ae1d354c375f',
'Product Detail - Gallery',
'Product detail page with image gallery and full information',
'product-detail',
'e-commerce',
3747117import React, { useState } from 'react';
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
}3747117,
'{"npm": ["lucide-react"], "components": ["Button", "Badge", "Tabs"]}'::jsonb,
'{"type": "object", "properties": {"product": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "description": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "images": {"type": "array", "items": {"type": "string"}}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "inStock": {"type": "boolean"}, "category": {"type": "string"}, "sku": {"type": "string"}, "features": {"type": "array", "items": {"type": "string"}}, "specifications": {"type": "object", "additionalProperties": {"type": "string"}}}, "required": ["id", "name", "description", "price", "images", "rating", "reviews", "inStock", "category", "sku", "features", "specifications"]}, "onAddToCart": {"type": "function"}, "onToggleWishlist": {"type": "function"}, "onShare": {"type": "function"}}, "required": ["product"]}'::jsonb,
'{"product": {"id": "1", "name": "Professional DSLR Camera", "description": "Capture stunning photos and videos with this professional-grade DSLR camera featuring advanced autofocus and 4K video recording.", "price": 1299.99, "originalPrice": 1599.99, "images": ["/api/placeholder/600/600", "/api/placeholder/600/600", "/api/placeholder/600/600", "/api/placeholder/600/600"], "rating": 4.8, "reviews": 324, "inStock": true, "category": "Electronics", "sku": "CAM-PRO-001", "features": ["24.2MP Full-Frame Sensor", "4K Video Recording at 60fps", "Advanced 45-Point Autofocus", "5-Axis Image Stabilization", "Weather-Sealed Body", "Dual Memory Card Slots"], "specifications": {"Sensor": "Full-Frame CMOS", "Resolution": "24.2 Megapixels", "ISO Range": "100-51200", "Video": "4K 60fps", "Weight": "850g", "Battery Life": "970 shots"}}}'::jsonb,
ARRAY['product-detail','gallery','e-commerce','specifications']
);

INSERT INTO application_blocks (id, name, description, block_type, app_type, react_template, dependencies, props_schema, example_props, tags) VALUES (
'a3226659-e881-45b0-ab3c-b8ce9ee697dd',
'Product Detail - Tabs',
'Product detail with tabbed content sections',
'product-detail',
'e-commerce',
3747117import React from 'react';
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
}3747117,
'{"npm": ["lucide-react"], "components": ["Tabs", "Card", "Badge"]}'::jsonb,
'{"type": "object", "properties": {"product": {"type": "object", "required": ["description", "features", "specifications", "shipping", "warranty"]}, "reviews": {"type": "array", "items": {"type": "object"}}}, "required": ["product"]}'::jsonb,
'{"product": {"description": "This premium product delivers exceptional performance and reliability for all your needs.", "features": ["Advanced technology integration", "Energy efficient design", "Durable construction", "User-friendly interface"], "specifications": {"Dimensions": "10 x 8 x 6 inches", "Weight": "2.5 lbs", "Material": "Aluminum alloy", "Power": "USB-C charging"}, "shipping": {"methods": [{"name": "Standard Shipping", "price": "$5.99", "duration": "5-7 business days"}, {"name": "Express Shipping", "price": "$12.99", "duration": "2-3 business days"}, {"name": "Next Day", "price": "$24.99", "duration": "1 business day"}], "returns": "30-day return policy. Items must be in original condition."}, "warranty": {"period": "2 Year Limited Warranty", "coverage": ["Manufacturing defects", "Component failures", "Free repairs or replacement"]}}}'::jsonb,
ARRAY['product-detail','tabs','e-commerce','reviews','specifications']
);

INSERT INTO application_blocks (id, name, description, block_type, app_type, react_template, dependencies, props_schema, example_props, tags) VALUES (
'd7e104a6-7add-4b0e-a418-a4913c26c1e9',
'Shopping Cart - Sidebar',
'Slide-out shopping cart sidebar with items and checkout',
'shopping-cart',
'e-commerce',
3747117import React from 'react';
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
}3747117,
'{"npm": ["lucide-react"], "components": ["Sheet", "Button", "Separator"]}'::jsonb,
'{"type": "object", "properties": {"isOpen": {"type": "boolean"}, "onClose": {"type": "function"}, "items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "quantity": {"type": "number"}, "image": {"type": "string"}, "variant": {"type": "string"}}, "required": ["id", "name", "price", "quantity", "image"]}}, "onUpdateQuantity": {"type": "function"}, "onRemoveItem": {"type": "function"}, "onCheckout": {"type": "function"}}, "required": ["isOpen", "onClose", "items", "onUpdateQuantity", "onRemoveItem", "onCheckout"]}'::jsonb,
'{"isOpen": true, "items": [{"id": "1", "name": "Wireless Mouse", "price": 29.99, "quantity": 2, "image": "/api/placeholder/80/80", "variant": "Black"}, {"id": "2", "name": "USB-C Cable", "price": 12.99, "quantity": 1, "image": "/api/placeholder/80/80"}]}'::jsonb,
ARRAY['shopping-cart','sidebar','e-commerce','checkout']
);