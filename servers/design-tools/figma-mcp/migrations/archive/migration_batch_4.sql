BEGIN;

Order Summary - Card
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '32ebd742-362a-49e3-879b-f49d0e78a2f2',
    'Order Summary - Card',
    'Compact order summary card for checkout and review',
    'order-summary',
    'e-commerce',
    $$10$$import React from 'react';
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
}$$10$$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge", "Separator"]}',
    '{"type": "object", "properties": {"order": {"type": "object", "properties": {"id": {"type": "string"}, "status": {"type": "string", "enum": ["pending", "confirmed", "shipped", "delivered"]}, "date": {"type": "string"}, "total": {"type": "number"}, "subtotal": {"type": "number"}, "shipping": {"type": "number"}, "tax": {"type": "number"}, "items": {"type": "array"}, "shipping_address": {"type": "object"}, "estimated_delivery": {"type": "string"}}, "required": ["id", "status", "date", "total", "subtotal", "shipping", "tax", "items", "shipping_address"]}, "onTrackOrder": {"type": "function"}, "onViewDetails": {"type": "function"}}, "required": ["order"]}',
    '{"order": {"id": "ORD-2024-001", "status": "shipped", "date": "2024-01-15T10:30:00Z", "total": 124.97, "subtotal": 109.98, "shipping": 5.99, "tax": 8.8, "items": [{"id": "1", "name": "Wireless Mouse", "quantity": 2, "price": 29.99, "image": "/api/placeholder/48/48"}, {"id": "2", "name": "USB Cable", "quantity": 1, "price": 49.99, "image": "/api/placeholder/48/48"}], "shipping_address": {"name": "John Doe", "address": "123 Main St", "city": "Anytown", "postal_code": "12345"}, "estimated_delivery": "2024-01-20T00:00:00Z"}}',
    ARRAY['order-summary', 'card', 'e-commerce', 'tracking', 'delivery']::text[],
    '2025-07-17T03:50:42.150548',
    '2025-07-17T03:50:42.150549'
);

Product Reviews - List
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '0a0566f9-fd27-4b79-bab6-01527641e9ac',
    'Product Reviews - List',
    'Product reviews list with ratings and filtering',
    'product-reviews',
    'e-commerce',
    $$11$$import React, { useState } from 'react';
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
}$$11$$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge", "Progress", "Tabs"]}',
    '{"type": "object", "properties": {"productName": {"type": "string"}, "averageRating": {"type": "number"}, "totalReviews": {"type": "number"}, "ratingDistribution": {"type": "object", "properties": {"5": {"type": "number"}, "4": {"type": "number"}, "3": {"type": "number"}, "2": {"type": "number"}, "1": {"type": "number"}}, "required": ["5", "4", "3", "2", "1"]}, "reviews": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "author": {"type": "string"}, "rating": {"type": "number"}, "title": {"type": "string"}, "content": {"type": "string"}, "date": {"type": "string"}, "verified": {"type": "boolean"}, "helpful": {"type": "number"}, "images": {"type": "array", "items": {"type": "string"}}}, "required": ["id", "author", "rating", "title", "content", "date", "verified", "helpful"]}}, "onWriteReview": {"type": "function"}, "onHelpfulVote": {"type": "function"}}, "required": ["productName", "averageRating", "totalReviews", "ratingDistribution", "reviews"]}',
    '{"productName": "Wireless Headphones", "averageRating": 4.3, "totalReviews": 89, "ratingDistribution": {"5": 42, "4": 23, "3": 15, "2": 6, "1": 3}, "reviews": [{"id": "1", "author": "Sarah Johnson", "rating": 5, "title": "Excellent sound quality!", "content": "These headphones exceeded my expectations. The sound quality is crystal clear and the noise cancellation works perfectly.", "date": "2024-01-15T00:00:00Z", "verified": true, "helpful": 12, "images": ["/api/placeholder/64/64"]}, {"id": "2", "author": "Mike Chen", "rating": 4, "title": "Good value for money", "content": "Solid headphones for the price. Battery life is impressive and they''re comfortable for long listening sessions.", "date": "2024-01-10T00:00:00Z", "verified": true, "helpful": 8}]}',
    ARRAY['product-reviews', 'ratings', 'e-commerce', 'feedback', 'social-proof']::text[],
    '2025-07-17T03:50:42.150563',
    '2025-07-17T03:50:42.150566'
);

Product Filter - Sidebar
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'ddf9fdc3-fa59-4255-85b2-973037a7940d',
    'Product Filter - Sidebar',
    'Advanced product filtering sidebar with multiple filter types',
    'product-filter',
    'e-commerce',
    $$12$$import React, { useState } from 'react';
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
}$$12$$,
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Checkbox", "Label", "Slider", "Badge", "Collapsible"]}',
    '{"type": "object", "properties": {"filters": {"type": "object", "properties": {"categories": {"type": "array", "items": {"type": "string"}}, "brands": {"type": "array", "items": {"type": "string"}}, "priceRange": {"type": "array", "items": {"type": "number"}}, "ratings": {"type": "array", "items": {"type": "number"}}, "inStock": {"type": "boolean"}, "onSale": {"type": "boolean"}}}, "onFiltersChange": {"type": "function"}, "onClearFilters": {"type": "function"}, "availableFilters": {"type": "object"}, "resultCount": {"type": "number"}}, "required": ["filters", "onFiltersChange", "onClearFilters", "availableFilters", "resultCount"]}',
    '{"filters": {"categories": ["electronics"], "brands": [], "priceRange": [0, 1000], "ratings": [4, 5], "inStock": true, "onSale": false}, "resultCount": 42, "availableFilters": {"categories": [{"id": "electronics", "name": "Electronics", "count": 156}, {"id": "clothing", "name": "Clothing", "count": 89}, {"id": "books", "name": "Books", "count": 234}], "brands": [{"id": "apple", "name": "Apple", "count": 45}, {"id": "samsung", "name": "Samsung", "count": 67}], "priceRange": {"min": 0, "max": 2000}}}',
    ARRAY['product-filter', 'sidebar', 'e-commerce', 'search', 'categories']::text[],
    '2025-07-17T03:50:42.150579',
    '2025-07-17T03:50:42.150580'
);

COMMIT;