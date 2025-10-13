-- Block 3: Product Card - Simple
-- Description: Simple product card with minimal information
-- Generated: 2025-07-17T03:46:56.379405

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '8b57a3b0-35dd-4f97-a59f-a6ab056f2b49',
    'Product Card - Simple',
    'Simple product card with minimal information',
    'product-card',
    'e-commerce',
    'import React from ''react'';
import { Card, CardContent } from ''@/components/ui/card'';
import { Button } from ''@/components/ui/button'';

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
}',
    '{"npm": [], "components": ["Card", "Button"]}',
    '{"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "image": {"type": "string"}, "onSelect": {"type": "function"}}, "required": ["id", "name", "price", "image"]}',
    '{"id": "1", "name": "Minimalist Desk Lamp", "price": 89.99, "image": "/api/placeholder/300/300"}',
    ARRAY['simple', 'product', 'card', 'e-commerce']::text[],
    '2025-07-17T03:46:56.375390',
    '2025-07-17T03:46:56.375397'
);
