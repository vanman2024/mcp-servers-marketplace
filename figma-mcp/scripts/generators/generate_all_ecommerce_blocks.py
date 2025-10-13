#!/usr/bin/env python3
"""
Complete E-commerce Blocks Generation Script
Generates all 15 e-commerce blocks and creates migration SQL
"""

import os
import sys
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any

# Add src directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import Supabase client
try:
    from supabase import create_client, Client
except ImportError:
    print("Please install supabase: pip install supabase")
    sys.exit(1)

# Import from block generation modules
from block_expansion_phase1 import generate_ecommerce_blocks
from block_expansion_phase1_part2 import generate_remaining_ecommerce_blocks

# Additional blocks (9-15) that weren't in part2
def generate_final_ecommerce_blocks() -> List[Dict[str, Any]]:
    """Generate final set of e-commerce blocks (9-15)"""
    blocks = []
    
    # 9. Checkout - Single Page
    blocks.append({
        "id": str(uuid.uuid4()),
        "name": "Checkout - Single Page",
        "description": "Complete single-page checkout with billing, shipping, and payment",
        "block_type": "checkout",
        "app_type": "e-commerce",
        "react_template": """import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Checkbox } from '@/components/ui/checkbox';
import { Separator } from '@/components/ui/separator';
import { CreditCard, Truck, Lock } from 'lucide-react';

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
    email: '',
    firstName: '',
    lastName: '',
    address: '',
    city: '',
    state: '',
    zip: '',
    country: 'US'
  });
  
  const [sameAsShipping, setSameAsShipping] = React.useState(true);
  const [paymentMethod, setPaymentMethod] = React.useState('card');

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
                
                {paymentMethod === 'card' && (
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
}""",
        "dependencies": {
            "npm": ["lucide-react"],
            "components": ["Card", "Input", "Label", "Button", "RadioGroup", "Checkbox", "Separator"]
        },
        "tags": ["checkout", "e-commerce", "payment", "billing", "shipping"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    # 10. Order Summary - Card
    blocks.append({
        "id": str(uuid.uuid4()),
        "name": "Order Summary - Card",
        "description": "Compact order summary card for checkout pages",
        "block_type": "order-summary",
        "app_type": "e-commerce",
        "react_template": """import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';

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
      </CardContent>
    </Card>
  );
}""",
        "dependencies": {
            "npm": [],
            "components": ["Card", "Separator", "Badge"]
        },
        "tags": ["order-summary", "checkout", "e-commerce"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    # 11. Product Reviews - List
    blocks.append({
        "id": str(uuid.uuid4()),
        "name": "Product Reviews - List",
        "description": "Product reviews list with ratings, filters, and helpful votes",
        "block_type": "reviews",
        "app_type": "e-commerce",
        "react_template": """import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Star, ThumbsUp, CheckCircle } from 'lucide-react';

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
                      ? 'fill-primary text-primary'
                      : 'text-muted'
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
}""",
        "dependencies": {
            "npm": ["lucide-react"],
            "components": ["Card", "Button", "Badge", "Progress", "Select"]
        },
        "tags": ["reviews", "ratings", "e-commerce", "product-feedback"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    # 12. Product Filter - Sidebar
    blocks.append({
        "id": str(uuid.uuid4()),
        "name": "Product Filter - Sidebar",
        "description": "Product filtering sidebar with multiple filter options",
        "block_type": "product-filter",
        "app_type": "e-commerce",
        "react_template": """import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';
import { X } from 'lucide-react';

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
}""",
        "dependencies": {
            "npm": ["lucide-react"],
            "components": ["Card", "Checkbox", "Label", "Slider", "Button", "Separator", "Badge"]
        },
        "tags": ["filter", "sidebar", "e-commerce", "product-filter"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    # 13. Category Banner
    blocks.append({
        "id": str(uuid.uuid4()),
        "name": "Category Banner",
        "description": "Category page banner with breadcrumb and description",
        "block_type": "category-banner",
        "app_type": "e-commerce",
        "react_template": """import React from 'react';
import { ChevronRight } from 'lucide-react';

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
}""",
        "dependencies": {
            "npm": ["lucide-react"],
            "components": []
        },
        "tags": ["category", "banner", "e-commerce", "breadcrumb"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    # 14. Sale Banner - Countdown
    blocks.append({
        "id": str(uuid.uuid4()),
        "name": "Sale Banner - Countdown",
        "description": "Promotional sale banner with countdown timer",
        "block_type": "sale-banner",
        "app_type": "e-commerce",
        "react_template": """import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Clock, Zap } from 'lucide-react';

interface SaleBannerCountdownProps {
  title: string;
  subtitle: string;
  endDate: Date;
  discountPercentage: number;
  ctaText: string;
  onCtaClick: () => void;
  variant?: 'default' | 'flash' | 'seasonal';
}

export function SaleBannerCountdown({
  title,
  subtitle,
  endDate,
  discountPercentage,
  ctaText,
  onCtaClick,
  variant = 'default'
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
    default: 'bg-gradient-to-r from-primary to-primary/80',
    flash: 'bg-gradient-to-r from-destructive to-orange-500',
    seasonal: 'bg-gradient-to-r from-green-500 to-red-500'
  };

  return (
    <Card className={`${bgClass[variant]} text-primary-foreground overflow-hidden`}>
      <CardContent className="p-6 md:p-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="text-center md:text-left">
            <div className="flex items-center gap-2 mb-2">
              {variant === 'flash' && <Zap className="w-5 h-5" />}
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
}""",
        "dependencies": {
            "npm": ["lucide-react"],
            "components": ["Card", "Button", "Badge"]
        },
        "tags": ["sale", "banner", "countdown", "promotion", "e-commerce"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    # 15. Wishlist Grid
    blocks.append({
        "id": str(uuid.uuid4()),
        "name": "Wishlist Grid",
        "description": "User wishlist grid with product management",
        "block_type": "wishlist",
        "app_type": "e-commerce",
        "react_template": """import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Heart, ShoppingCart, X, Share2 } from 'lucide-react';

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
}""",
        "dependencies": {
            "npm": ["lucide-react"],
            "components": ["Card", "Button", "Badge"]
        },
        "tags": ["wishlist", "favorites", "e-commerce", "saved-items"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    return blocks

def generate_complete_migration():
    """Generate complete migration for all e-commerce blocks"""
    
    # Collect all blocks
    all_blocks = []
    
    # Get blocks from all generation functions
    blocks_1_5 = generate_ecommerce_blocks()
    blocks_6_8 = generate_remaining_ecommerce_blocks()
    blocks_9_15 = generate_final_ecommerce_blocks()
    
    all_blocks.extend(blocks_1_5)
    all_blocks.extend(blocks_6_8)
    all_blocks.extend(blocks_9_15)
    
    print(f"Total blocks generated: {len(all_blocks)}")
    
    # Create migration SQL
    migration_lines = [
        "-- Phase 1: E-commerce Blocks Migration",
        f"-- Generated: {datetime.utcnow().isoformat()}",
        "-- Total blocks: 15",
        "",
        "-- Insert e-commerce blocks into application_blocks table"
    ]
    
    for i, block in enumerate(all_blocks):
        # Properly escape single quotes in strings
        def escape_quotes(s):
            if isinstance(s, str):
                return s.replace("'", "''")
            return s
        
        # Convert example_props to JSON string
        example_props_json = json.dumps(block.get('example_props', {}))
        props_schema_json = json.dumps(block.get('props_schema', {}))
        dependencies_json = json.dumps(block.get('dependencies', {}))
        
        sql = f"""
-- Block {i+1}: {block['name']}
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
    '{block['id']}',
    '{escape_quotes(block['name'])}',
    '{escape_quotes(block['description'])}',
    '{block['block_type']}',
    '{block['app_type']}',
    '{escape_quotes(block['react_template'])}',
    '{escape_quotes(dependencies_json)}',
    '{escape_quotes(props_schema_json)}',
    '{escape_quotes(example_props_json)}',
    ARRAY{block.get('tags', [])}::text[],
    '{block['created_at'].isoformat()}',
    '{block['updated_at'].isoformat()}'
);"""
        migration_lines.append(sql)
    
    # Save migration file
    migration_content = "\n".join(migration_lines)
    
    with open("migration_phase1_complete_ecommerce.sql", "w") as f:
        f.write(migration_content)
    
    print("Migration SQL saved to: migration_phase1_complete_ecommerce.sql")
    
    # Also save as JSON for reference
    blocks_data = []
    for block in all_blocks:
        block_copy = block.copy()
        block_copy['created_at'] = block_copy['created_at'].isoformat()
        block_copy['updated_at'] = block_copy['updated_at'].isoformat()
        blocks_data.append(block_copy)
    
    with open("phase1_ecommerce_blocks_complete.json", "w") as f:
        json.dump(blocks_data, f, indent=2)
    
    print("Block data saved to: phase1_ecommerce_blocks_complete.json")
    
    # Generate summary
    block_types = {}
    for block in all_blocks:
        bt = block['block_type']
        block_types[bt] = block_types.get(bt, 0) + 1
    
    print("\nBlock type summary:")
    for bt, count in sorted(block_types.items()):
        print(f"  {bt}: {count} blocks")

def main():
    """Main execution"""
    print("="*60)
    print("E-commerce Blocks Generation - Phase 1")
    print("="*60)
    
    generate_complete_migration()
    
    print("\n✅ Phase 1 Complete!")
    print("Next steps:")
    print("1. Review the generated SQL migration")
    print("2. Apply migration to Supabase database")
    print("3. Test block generation with figma_server_db.py")
    print("4. Move to Phase 2: Navigation & Forms blocks")

if __name__ == "__main__":
    main()