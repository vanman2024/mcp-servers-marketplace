#!/usr/bin/env python3
"""
Phase 1 Part 2: Remaining E-commerce Blocks (6-15)
Continuation of e-commerce blocks implementation
"""

import uuid
import json
from datetime import datetime
from typing import Dict, List, Any

def generate_remaining_ecommerce_blocks() -> List[Dict[str, Any]]:
    """Generate remaining e-commerce blocks (6-15)"""
    blocks = []
    
    # 6. Product Detail - Tabs
    blocks.append({
        "id": str(uuid.uuid4()),
        "name": "Product Detail - Tabs",
        "description": "Product detail with tabbed content sections",
        "block_type": "product-detail",
        "app_type": "e-commerce",
        "react_template": """import React from 'react';
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
}""",
        "dependencies": {
            "npm": ["lucide-react"],
            "components": ["Tabs", "Card", "Badge"]
        },
        "props_schema": {
            "type": "object",
            "properties": {
                "product": {
                    "type": "object",
                    "required": ["description", "features", "specifications", "shipping", "warranty"]
                },
                "reviews": {
                    "type": "array",
                    "items": {
                        "type": "object"
                    }
                }
            },
            "required": ["product"]
        },
        "example_props": {
            "product": {
                "description": "This premium product delivers exceptional performance and reliability for all your needs.",
                "features": [
                    "Advanced technology integration",
                    "Energy efficient design",
                    "Durable construction",
                    "User-friendly interface"
                ],
                "specifications": {
                    "Dimensions": "10 x 8 x 6 inches",
                    "Weight": "2.5 lbs",
                    "Material": "Aluminum alloy",
                    "Power": "USB-C charging"
                },
                "shipping": {
                    "methods": [
                        {"name": "Standard Shipping", "price": "$5.99", "duration": "5-7 business days"},
                        {"name": "Express Shipping", "price": "$12.99", "duration": "2-3 business days"},
                        {"name": "Next Day", "price": "$24.99", "duration": "1 business day"}
                    ],
                    "returns": "30-day return policy. Items must be in original condition."
                },
                "warranty": {
                    "period": "2 Year Limited Warranty",
                    "coverage": [
                        "Manufacturing defects",
                        "Component failures",
                        "Free repairs or replacement"
                    ]
                }
            }
        },
        "tags": ["product-detail", "tabs", "e-commerce", "reviews", "specifications"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    # 7. Shopping Cart - Sidebar
    blocks.append({
        "id": str(uuid.uuid4()),
        "name": "Shopping Cart - Sidebar",
        "description": "Slide-out shopping cart sidebar with items and checkout",
        "block_type": "shopping-cart",
        "app_type": "e-commerce",
        "react_template": """import React from 'react';
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
}""",
        "dependencies": {
            "npm": ["lucide-react"],
            "components": ["Sheet", "Button", "Separator"]
        },
        "props_schema": {
            "type": "object",
            "properties": {
                "isOpen": {"type": "boolean"},
                "onClose": {"type": "function"},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "price": {"type": "number"},
                            "quantity": {"type": "number"},
                            "image": {"type": "string"},
                            "variant": {"type": "string"}
                        },
                        "required": ["id", "name", "price", "quantity", "image"]
                    }
                },
                "onUpdateQuantity": {"type": "function"},
                "onRemoveItem": {"type": "function"},
                "onCheckout": {"type": "function"}
            },
            "required": ["isOpen", "onClose", "items", "onUpdateQuantity", "onRemoveItem", "onCheckout"]
        },
        "example_props": {
            "isOpen": True,
            "items": [
                {
                    "id": "1",
                    "name": "Wireless Mouse",
                    "price": 29.99,
                    "quantity": 2,
                    "image": "/api/placeholder/80/80",
                    "variant": "Black"
                },
                {
                    "id": "2",
                    "name": "USB-C Cable",
                    "price": 12.99,
                    "quantity": 1,
                    "image": "/api/placeholder/80/80"
                }
            ]
        },
        "tags": ["shopping-cart", "sidebar", "e-commerce", "checkout"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    # 8. Shopping Cart - Page
    blocks.append({
        "id": str(uuid.uuid4()),
        "name": "Shopping Cart - Page",
        "description": "Full page shopping cart with detailed item management",
        "block_type": "shopping-cart",
        "app_type": "e-commerce",
        "react_template": """import React from 'react';
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
}""",
        "dependencies": {
            "npm": ["lucide-react"],
            "components": ["Card", "Button", "Input", "Separator", "Badge"]
        },
        "props_schema": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "price": {"type": "number"},
                            "originalPrice": {"type": "number"},
                            "quantity": {"type": "number"},
                            "image": {"type": "string"},
                            "variant": {"type": "string"},
                            "inStock": {"type": "boolean"}
                        },
                        "required": ["id", "name", "description", "price", "quantity", "image", "inStock"]
                    }
                },
                "onUpdateQuantity": {"type": "function"},
                "onRemoveItem": {"type": "function"},
                "onApplyCoupon": {"type": "function"},
                "onCheckout": {"type": "function"},
                "appliedCoupon": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "discount": {"type": "number"}
                    }
                }
            },
            "required": ["items", "onUpdateQuantity", "onRemoveItem", "onApplyCoupon", "onCheckout"]
        },
        "example_props": {
            "items": [
                {
                    "id": "1",
                    "name": "Wireless Keyboard",
                    "description": "Bluetooth mechanical keyboard with RGB backlighting",
                    "price": 89.99,
                    "originalPrice": 119.99,
                    "quantity": 1,
                    "image": "/api/placeholder/128/128",
                    "variant": "Cherry MX Blue",
                    "inStock": True
                }
            ]
        },
        "tags": ["shopping-cart", "page", "e-commerce", "checkout", "order-summary"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    # Continue with remaining blocks...
    # 9. Checkout - Single Page
    # 10. Order Summary - Card
    # 11. Product Reviews - List
    # 12. Product Filter - Sidebar
    # 13. Category Banner
    # 14. Sale Banner - Countdown
    # 15. Wishlist Grid
    
    return blocks

def main():
    """Generate remaining e-commerce blocks"""
    blocks = generate_remaining_ecommerce_blocks()
    print(f"Generated {len(blocks)} additional e-commerce blocks")
    
    # You would append these to the existing migration file
    # or create a separate part 2 migration
    
if __name__ == "__main__":
    main()