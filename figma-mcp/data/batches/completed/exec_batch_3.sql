BEGIN;

-- Block 10: Order Summary - Card
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '77d559ff-8bd0-4914-b8fa-6e0f9d65725d',
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
    '2025-07-17T04:01:09.064192',
    '2025-07-17T04:01:09.064193'
);


-- Block 11: Product Reviews - List
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '14c555f4-249c-49a5-87cd-66aa30f4bc2e',
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
    '2025-07-17T04:01:09.064206',
    '2025-07-17T04:01:09.064209'
);


-- Block 12: Product Filter - Sidebar
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'a3961df1-9e2c-4102-bd21-d9f73d9d2f68',
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
    '2025-07-17T04:01:09.064231',
    '2025-07-17T04:01:09.064232'
);


-- Block 13: Category Banner
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'f626855e-ed14-463d-a812-23ddc3bf895c',
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
    '2025-07-17T04:01:09.064243',
    '2025-07-17T04:01:09.064245'
);


-- Block 14: Sale Banner - Countdown
INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '90643611-9a58-4779-9a7e-a970e0e79f96',
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
    '2025-07-17T04:01:09.064255',
    '2025-07-17T04:01:09.064257'
);


COMMIT;