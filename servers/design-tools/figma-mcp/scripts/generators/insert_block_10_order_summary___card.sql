-- Block 10: Order Summary - Card
-- Description: Compact order summary card for checkout and review
-- Generated: 2025-07-17T03:46:56.381537

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '72be2470-b4a5-4de7-b6b1-117fe2a0a486',
    'Order Summary - Card',
    'Compact order summary card for checkout and review',
    'order-summary',
    'e-commerce',
    'import React from ''react'';
import { Card, CardContent, CardHeader, CardTitle } from ''@/components/ui/card'';
import { Button } from ''@/components/ui/button'';
import { Badge } from ''@/components/ui/badge'';
import { Separator } from ''@/components/ui/separator'';
import { Truck, Package, Clock, MapPin } from ''lucide-react'';

interface OrderSummaryCardProps {
  order: {
    id: string;
    status: ''pending'' | ''confirmed'' | ''shipped'' | ''delivered'';
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
      case ''pending'': return ''bg-yellow-100 text-yellow-800'';
      case ''confirmed'': return ''bg-blue-100 text-blue-800'';
      case ''shipped'': return ''bg-purple-100 text-purple-800'';
      case ''delivered'': return ''bg-green-100 text-green-800'';
      default: return ''bg-gray-100 text-gray-800'';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case ''pending'': return <Clock className="w-4 h-4" />;
      case ''confirmed'': return <Package className="w-4 h-4" />;
      case ''shipped'': return <Truck className="w-4 h-4" />;
      case ''delivered'': return <MapPin className="w-4 h-4" />;
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
          {order.status !== ''pending'' && (
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
}',
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Badge", "Separator"]}',
    '{"type": "object", "properties": {"order": {"type": "object", "properties": {"id": {"type": "string"}, "status": {"type": "string", "enum": ["pending", "confirmed", "shipped", "delivered"]}, "date": {"type": "string"}, "total": {"type": "number"}, "subtotal": {"type": "number"}, "shipping": {"type": "number"}, "tax": {"type": "number"}, "items": {"type": "array"}, "shipping_address": {"type": "object"}, "estimated_delivery": {"type": "string"}}, "required": ["id", "status", "date", "total", "subtotal", "shipping", "tax", "items", "shipping_address"]}, "onTrackOrder": {"type": "function"}, "onViewDetails": {"type": "function"}}, "required": ["order"]}',
    '{"order": {"id": "ORD-2024-001", "status": "shipped", "date": "2024-01-15T10:30:00Z", "total": 124.97, "subtotal": 109.98, "shipping": 5.99, "tax": 8.8, "items": [{"id": "1", "name": "Wireless Mouse", "quantity": 2, "price": 29.99, "image": "/api/placeholder/48/48"}, {"id": "2", "name": "USB Cable", "quantity": 1, "price": 49.99, "image": "/api/placeholder/48/48"}], "shipping_address": {"name": "John Doe", "address": "123 Main St", "city": "Anytown", "postal_code": "12345"}, "estimated_delivery": "2024-01-20T00:00:00Z"}}',
    ARRAY['order-summary', 'card', 'e-commerce', 'tracking', 'delivery']::text[],
    '2025-07-17T03:46:56.375744',
    '2025-07-17T03:46:56.375749'
);
