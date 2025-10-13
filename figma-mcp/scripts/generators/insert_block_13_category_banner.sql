-- Block 13: Category Banner
-- Description: Hero banner for product category pages with navigation
-- Generated: 2025-07-17T03:46:56.382614

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'f3d9dd47-de9c-4b23-9ead-65ddb13a64b0',
    'Category Banner',
    'Hero banner for product category pages with navigation',
    'category-banner',
    'e-commerce',
    'import React from ''react'';
import { Button } from ''@/components/ui/button'';
import { Badge } from ''@/components/ui/badge'';
import { ArrowRight, Star, TrendingUp } from ''lucide-react'';

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
}',
    '{"npm": ["lucide-react"], "components": ["Button", "Badge"]}',
    '{"type": "object", "properties": {"category": {"type": "object", "properties": {"name": {"type": "string"}, "description": {"type": "string"}, "image": {"type": "string"}, "productCount": {"type": "number"}, "featured": {"type": "boolean"}, "trending": {"type": "boolean"}}, "required": ["name", "description", "image", "productCount"]}, "subcategories": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "image": {"type": "string"}, "productCount": {"type": "number"}}, "required": ["id", "name", "image", "productCount"]}}, "onExploreCategory": {"type": "function"}, "onSelectSubcategory": {"type": "function"}}, "required": ["category"]}',
    '{"category": {"name": "Electronics", "description": "Discover the latest technology and gadgets from top brands. From smartphones to smart home devices, find everything you need to stay connected and productive.", "image": "/api/placeholder/800/400", "productCount": 1247, "featured": true, "trending": true}, "subcategories": [{"id": "smartphones", "name": "Smartphones", "image": "/api/placeholder/200/200", "productCount": 156}, {"id": "laptops", "name": "Laptops", "image": "/api/placeholder/200/200", "productCount": 89}, {"id": "headphones", "name": "Headphones", "image": "/api/placeholder/200/200", "productCount": 234}, {"id": "cameras", "name": "Cameras", "image": "/api/placeholder/200/200", "productCount": 67}, {"id": "gaming", "name": "Gaming", "image": "/api/placeholder/200/200", "productCount": 178}, {"id": "accessories", "name": "Accessories", "image": "/api/placeholder/200/200", "productCount": 523}]}',
    ARRAY['category-banner', 'hero', 'e-commerce', 'navigation', 'subcategories']::text[],
    '2025-07-17T03:46:56.375833',
    '2025-07-17T03:46:56.375835'
);
