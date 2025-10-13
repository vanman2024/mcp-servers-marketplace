BEGIN;

-- Block 5: Product Detail - Gallery
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '078629cc-821b-4b89-8fd8-b975e32e6a11',
    'Product Detail - Gallery',
    'Product detail page with image gallery and full information',
    'product-detail',
    'e-commerce',
    $$5$$import React, { useState } from 'react';
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
}$$5$$,
    '{"npm": ["lucide-react"], "components": ["Button", "Badge", "Tabs"]}',
    '{"type": "object", "properties": {"product": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "description": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "images": {"type": "array", "items": {"type": "string"}}, "rating": {"type": "number"}, "reviews": {"type": "number"}, "inStock": {"type": "boolean"}, "category": {"type": "string"}, "sku": {"type": "string"}, "features": {"type": "array", "items": {"type": "string"}}, "specifications": {"type": "object", "additionalProperties": {"type": "string"}}}, "required": ["id", "name", "description", "price", "images", "rating", "reviews", "inStock", "category", "sku", "features", "specifications"]}, "onAddToCart": {"type": "function"}, "onToggleWishlist": {"type": "function"}, "onShare": {"type": "function"}}, "required": ["product"]}',
    '{"product": {"id": "1", "name": "Professional DSLR Camera", "description": "Capture stunning photos and videos with this professional-grade DSLR camera featuring advanced autofocus and 4K video recording.", "price": 1299.99, "originalPrice": 1599.99, "images": ["/api/placeholder/600/600", "/api/placeholder/600/600", "/api/placeholder/600/600", "/api/placeholder/600/600"], "rating": 4.8, "reviews": 324, "inStock": true, "category": "Electronics", "sku": "CAM-PRO-001", "features": ["24.2MP Full-Frame Sensor", "4K Video Recording at 60fps", "Advanced 45-Point Autofocus", "5-Axis Image Stabilization", "Weather-Sealed Body", "Dual Memory Card Slots"], "specifications": {"Sensor": "Full-Frame CMOS", "Resolution": "24.2 Megapixels", "ISO Range": "100-51200", "Video": "4K 60fps", "Weight": "850g", "Battery Life": "970 shots"}}}',
    ARRAY['product-detail', 'gallery', 'e-commerce', 'specifications']::text[],
    '2025-07-17T04:01:09.064129',
    '2025-07-17T04:01:09.064131'
);


-- Block 6: Product Detail - Tabs
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '1c468f02-8e94-4ef9-ae8b-e575ae7ddf30',
    'Product Detail - Tabs',
    'Product detail with tabbed content sections',
    'product-detail',
    'e-commerce',
    $$6$$import React from 'react';
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
}$$6$$,
    '{"npm": ["lucide-react"], "components": ["Tabs", "Card", "Badge"]}',
    '{"type": "object", "properties": {"product": {"type": "object", "required": ["description", "features", "specifications", "shipping", "warranty"]}, "reviews": {"type": "array", "items": {"type": "object"}}}, "required": ["product"]}',
    '{"product": {"description": "This premium product delivers exceptional performance and reliability for all your needs.", "features": ["Advanced technology integration", "Energy efficient design", "Durable construction", "User-friendly interface"], "specifications": {"Dimensions": "10 x 8 x 6 inches", "Weight": "2.5 lbs", "Material": "Aluminum alloy", "Power": "USB-C charging"}, "shipping": {"methods": [{"name": "Standard Shipping", "price": "$5.99", "duration": "5-7 business days"}, {"name": "Express Shipping", "price": "$12.99", "duration": "2-3 business days"}, {"name": "Next Day", "price": "$24.99", "duration": "1 business day"}], "returns": "30-day return policy. Items must be in original condition."}, "warranty": {"period": "2 Year Limited Warranty", "coverage": ["Manufacturing defects", "Component failures", "Free repairs or replacement"]}}}',
    ARRAY['product-detail', 'tabs', 'e-commerce', 'reviews', 'specifications']::text[],
    '2025-07-17T04:01:09.064142',
    '2025-07-17T04:01:09.064144'
);


-- Block 7: Shopping Cart - Sidebar
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '2c46e160-6252-4039-9a81-1f27f8db57e7',
    'Shopping Cart - Sidebar',
    'Slide-out shopping cart sidebar with items and checkout',
    'shopping-cart',
    'e-commerce',
    $$7$$import React from 'react';
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
}$$7$$,
    '{"npm": ["lucide-react"], "components": ["Sheet", "Button", "Separator"]}',
    '{"type": "object", "properties": {"isOpen": {"type": "boolean"}, "onClose": {"type": "function"}, "items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "quantity": {"type": "number"}, "image": {"type": "string"}, "variant": {"type": "string"}}, "required": ["id", "name", "price", "quantity", "image"]}}, "onUpdateQuantity": {"type": "function"}, "onRemoveItem": {"type": "function"}, "onCheckout": {"type": "function"}}, "required": ["isOpen", "onClose", "items", "onUpdateQuantity", "onRemoveItem", "onCheckout"]}',
    '{"isOpen": true, "items": [{"id": "1", "name": "Wireless Mouse", "price": 29.99, "quantity": 2, "image": "/api/placeholder/80/80", "variant": "Black"}, {"id": "2", "name": "USB-C Cable", "price": 12.99, "quantity": 1, "image": "/api/placeholder/80/80"}]}',
    ARRAY['shopping-cart', 'sidebar', 'e-commerce', 'checkout']::text[],
    '2025-07-17T04:01:09.064156',
    '2025-07-17T04:01:09.064158'
);


-- Block 8: Shopping Cart - Page
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'd712dfc9-1472-459a-ba26-7eded9c2805f',
    'Shopping Cart - Page',
    'Full page shopping cart with detailed item management',
    'shopping-cart',
    'e-commerce',
    $$8$$import React from 'react';
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
}$$8$$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Input", "Separator", "Badge"]}',
    '{"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "description": {"type": "string"}, "price": {"type": "number"}, "originalPrice": {"type": "number"}, "quantity": {"type": "number"}, "image": {"type": "string"}, "variant": {"type": "string"}, "inStock": {"type": "boolean"}}, "required": ["id", "name", "description", "price", "quantity", "image", "inStock"]}}, "onUpdateQuantity": {"type": "function"}, "onRemoveItem": {"type": "function"}, "onApplyCoupon": {"type": "function"}, "onCheckout": {"type": "function"}, "appliedCoupon": {"type": "object", "properties": {"code": {"type": "string"}, "discount": {"type": "number"}}}}, "required": ["items", "onUpdateQuantity", "onRemoveItem", "onApplyCoupon", "onCheckout"]}',
    '{"items": [{"id": "1", "name": "Wireless Keyboard", "description": "Bluetooth mechanical keyboard with RGB backlighting", "price": 89.99, "originalPrice": 119.99, "quantity": 1, "image": "/api/placeholder/128/128", "variant": "Cherry MX Blue", "inStock": true}]}',
    ARRAY['shopping-cart', 'page', 'e-commerce', 'checkout', 'order-summary']::text[],
    '2025-07-17T04:01:09.064167',
    '2025-07-17T04:01:09.064169'
);


-- Block 9: Checkout - Single Page
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '65be938f-ecf8-4f32-a868-01e5778d3696',
    'Checkout - Single Page',
    'Complete single-page checkout with all steps',
    'checkout',
    'e-commerce',
    $$9$$import React, { useState } from 'react';
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
}$$9$$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Input", "Label", "Checkbox", "RadioGroup", "Separator"]}',
    '{"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "quantity": {"type": "number"}, "image": {"type": "string"}}, "required": ["id", "name", "price", "quantity", "image"]}}, "onPlaceOrder": {"type": "function"}}, "required": ["items", "onPlaceOrder"]}',
    '{"items": [{"id": "1", "name": "Wireless Headphones", "price": 79.99, "quantity": 1, "image": "/api/placeholder/64/64"}, {"id": "2", "name": "Phone Case", "price": 24.99, "quantity": 2, "image": "/api/placeholder/64/64"}]}',
    ARRAY['checkout', 'single-page', 'e-commerce', 'payment', 'shipping']::text[],
    '2025-07-17T04:01:09.064182',
    '2025-07-17T04:01:09.064183'
);


COMMIT;