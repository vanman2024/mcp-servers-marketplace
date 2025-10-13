-- Block 7: Shopping Cart - Sidebar
-- Description: Slide-out shopping cart sidebar with items and checkout
-- Generated: 2025-07-17T03:46:56.380544

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    'b6dbd9ed-66f3-4342-9fd4-aa85d962970b',
    'Shopping Cart - Sidebar',
    'Slide-out shopping cart sidebar with items and checkout',
    'shopping-cart',
    'e-commerce',
    'import React from ''react'';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetFooter } from ''@/components/ui/sheet'';
import { Button } from ''@/components/ui/button'';
import { Separator } from ''@/components/ui/separator'';
import { X, Plus, Minus, ShoppingBag } from ''lucide-react'';

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
                <span>{shipping === 0 ? ''FREE'' : `$${shipping.toFixed(2)}`}</span>
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
}',
    '{"npm": ["lucide-react"], "components": ["Sheet", "Button", "Separator"]}',
    '{"type": "object", "properties": {"isOpen": {"type": "boolean"}, "onClose": {"type": "function"}, "items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "quantity": {"type": "number"}, "image": {"type": "string"}, "variant": {"type": "string"}}, "required": ["id", "name", "price", "quantity", "image"]}}, "onUpdateQuantity": {"type": "function"}, "onRemoveItem": {"type": "function"}, "onCheckout": {"type": "function"}}, "required": ["isOpen", "onClose", "items", "onUpdateQuantity", "onRemoveItem", "onCheckout"]}',
    '{"isOpen": true, "items": [{"id": "1", "name": "Wireless Mouse", "price": 29.99, "quantity": 2, "image": "/api/placeholder/80/80", "variant": "Black"}, {"id": "2", "name": "USB-C Cable", "price": 12.99, "quantity": 1, "image": "/api/placeholder/80/80"}]}',
    ARRAY['shopping-cart', 'sidebar', 'e-commerce', 'checkout']::text[],
    '2025-07-17T03:46:56.375683',
    '2025-07-17T03:46:56.375685'
);
