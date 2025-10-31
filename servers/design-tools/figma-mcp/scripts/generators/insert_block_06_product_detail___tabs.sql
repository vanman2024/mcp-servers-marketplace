-- Block 6: Product Detail - Tabs
-- Description: Product detail with tabbed content sections
-- Generated: 2025-07-17T03:46:56.380206

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'b9b6f274-6397-4311-a1d3-906e96034636',
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
    '2025-07-17T03:46:56.375628',
    '2025-07-17T03:46:56.375630'
);
