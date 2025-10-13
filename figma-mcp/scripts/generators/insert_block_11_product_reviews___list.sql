-- Block 11: Product Reviews - List
-- Description: Product reviews list with ratings and filtering
-- Generated: 2025-07-17T03:46:56.381824

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'bc16c4e6-e6ab-4daa-9b14-4d06d9e78979',
    'Product Reviews - List',
    'Product reviews list with ratings and filtering',
    'product-reviews',
    'e-commerce',
    'import React, { useState } from ''react'';
import { Card, CardContent, CardHeader, CardTitle } from ''@/components/ui/card'';
import { Button } from ''@/components/ui/button'';
import { Badge } from ''@/components/ui/badge'';
import { Progress } from ''@/components/ui/progress'';
import { Tabs, TabsContent, TabsList, TabsTrigger } from ''@/components/ui/tabs'';
import { Star, ThumbsUp, ThumbsDown, Filter, MoreHorizontal } from ''lucide-react'';

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
  const [sortBy, setSortBy] = useState(''newest'');
  const [filterRating, setFilterRating] = useState(''all'');

  const filteredReviews = reviews.filter(review => {
    if (filterRating === ''all'') return true;
    return review.rating === parseInt(filterRating);
  });

  const sortedReviews = [...filteredReviews].sort((a, b) => {
    switch (sortBy) {
      case ''newest'':
        return new Date(b.date).getTime() - new Date(a.date).getTime();
      case ''oldest'':
        return new Date(a.date).getTime() - new Date(b.date).getTime();
      case ''highest'':
        return b.rating - a.rating;
      case ''lowest'':
        return a.rating - b.rating;
      case ''helpful'':
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
                          ? ''fill-primary text-primary''
                          : ''text-muted''
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
                                  ? ''fill-primary text-primary''
                                  : ''text-muted''
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
}',
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge", "Progress", "Tabs"]}',
    '{"type": "object", "properties": {"productName": {"type": "string"}, "averageRating": {"type": "number"}, "totalReviews": {"type": "number"}, "ratingDistribution": {"type": "object", "properties": {"5": {"type": "number"}, "4": {"type": "number"}, "3": {"type": "number"}, "2": {"type": "number"}, "1": {"type": "number"}}, "required": ["5", "4", "3", "2", "1"]}, "reviews": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "author": {"type": "string"}, "rating": {"type": "number"}, "title": {"type": "string"}, "content": {"type": "string"}, "date": {"type": "string"}, "verified": {"type": "boolean"}, "helpful": {"type": "number"}, "images": {"type": "array", "items": {"type": "string"}}}, "required": ["id", "author", "rating", "title", "content", "date", "verified", "helpful"]}}, "onWriteReview": {"type": "function"}, "onHelpfulVote": {"type": "function"}}, "required": ["productName", "averageRating", "totalReviews", "ratingDistribution", "reviews"]}',
    '{"productName": "Wireless Headphones", "averageRating": 4.3, "totalReviews": 89, "ratingDistribution": {"5": 42, "4": 23, "3": 15, "2": 6, "1": 3}, "reviews": [{"id": "1", "author": "Sarah Johnson", "rating": 5, "title": "Excellent sound quality!", "content": "These headphones exceeded my expectations. The sound quality is crystal clear and the noise cancellation works perfectly.", "date": "2024-01-15T00:00:00Z", "verified": true, "helpful": 12, "images": ["/api/placeholder/64/64"]}, {"id": "2", "author": "Mike Chen", "rating": 4, "title": "Good value for money", "content": "Solid headphones for the price. Battery life is impressive and they''re comfortable for long listening sessions.", "date": "2024-01-10T00:00:00Z", "verified": true, "helpful": 8}]}',
    ARRAY['product-reviews', 'ratings', 'e-commerce', 'feedback', 'social-proof']::text[],
    '2025-07-17T03:46:56.375783',
    '2025-07-17T03:46:56.375790'
);
