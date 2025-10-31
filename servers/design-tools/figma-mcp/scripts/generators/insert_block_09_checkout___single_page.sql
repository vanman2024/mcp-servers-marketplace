-- Block 9: Checkout - Single Page
-- Description: Complete single-page checkout with all steps
-- Generated: 2025-07-17T03:46:56.381216

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '44a4c245-1a40-4f57-bde4-1a11f550a298',
    'Checkout - Single Page',
    'Complete single-page checkout with all steps',
    'checkout',
    'e-commerce',
    'import React, { useState } from ''react'';
import { Card, CardContent, CardHeader, CardTitle } from ''@/components/ui/card'';
import { Button } from ''@/components/ui/button'';
import { Input } from ''@/components/ui/input'';
import { Label } from ''@/components/ui/label'';
import { Checkbox } from ''@/components/ui/checkbox'';
import { RadioGroup, RadioGroupItem } from ''@/components/ui/radio-group'';
import { Separator } from ''@/components/ui/separator'';
import { CreditCard, Truck, Shield, Check } from ''lucide-react'';

interface CheckoutItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
  image: string;
}

interface CheckoutSinglePageProps {
  items: CheckoutItem[];
  onPlaceOrder: (orderData: any) => void;
}

export function CheckoutSinglePage({ items, onPlaceOrder }: CheckoutSinglePageProps) {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    email: '''',
    firstName: '''',
    lastName: '''',
    address: '''',
    city: '''',
    postalCode: '''',
    country: '''',
    shippingMethod: ''standard'',
    paymentMethod: ''card'',
    cardNumber: '''',
    expiryDate: '''',
    cvv: '''',
    saveInfo: false
  });

  const subtotal = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const shipping = formData.shippingMethod === ''express'' ? 15.99 : 5.99;
  const tax = subtotal * 0.08;
  const total = subtotal + shipping + tax;

  const handleInputChange = (field: string, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = () => {
    onPlaceOrder({
      items,
      shippingAddress: {
        firstName: formData.firstName,
        lastName: formData.lastName,
        address: formData.address,
        city: formData.city,
        postalCode: formData.postalCode,
        country: formData.country
      },
      payment: {
        method: formData.paymentMethod,
        amount: total
      },
      shippingMethod: formData.shippingMethod
    });
  };

  return (
    <div className="max-w-6xl mx-auto p-6 grid lg:grid-cols-3 gap-8">
      {/* Checkout Form */}
      <div className="lg:col-span-2 space-y-6">
        {/* Progress Steps */}
        <div className="flex items-center gap-4 mb-8">
          {[1, 2, 3].map((s) => (
            <div key={s} className="flex items-center">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
                s <= step ? ''bg-primary text-primary-foreground'' : ''bg-muted text-muted-foreground''
              }`}>
                {s < step ? <Check className="w-4 h-4" /> : s}
              </div>
              {s < 3 && <div className={`w-16 h-1 mx-2 ${s < step ? ''bg-primary'' : ''bg-muted''}`} />}
            </div>
          ))}
        </div>

        {/* Step 1: Contact & Shipping */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Truck className="w-5 h-5" />
              Contact & Shipping Information
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="email">Email Address</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange(''email'', e.target.value)}
                placeholder="your@email.com"
              />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="firstName">First Name</Label>
                <Input
                  id="firstName"
                  value={formData.firstName}
                  onChange={(e) => handleInputChange(''firstName'', e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="lastName">Last Name</Label>
                <Input
                  id="lastName"
                  value={formData.lastName}
                  onChange={(e) => handleInputChange(''lastName'', e.target.value)}
                />
              </div>
            </div>
            
            <div>
              <Label htmlFor="address">Street Address</Label>
              <Input
                id="address"
                value={formData.address}
                onChange={(e) => handleInputChange(''address'', e.target.value)}
              />
            </div>
            
            <div className="grid grid-cols-3 gap-4">
              <div>
                <Label htmlFor="city">City</Label>
                <Input
                  id="city"
                  value={formData.city}
                  onChange={(e) => handleInputChange(''city'', e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="postalCode">Postal Code</Label>
                <Input
                  id="postalCode"
                  value={formData.postalCode}
                  onChange={(e) => handleInputChange(''postalCode'', e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="country">Country</Label>
                <Input
                  id="country"
                  value={formData.country}
                  onChange={(e) => handleInputChange(''country'', e.target.value)}
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Step 2: Shipping Method */}
        <Card>
          <CardHeader>
            <CardTitle>Shipping Method</CardTitle>
          </CardHeader>
          <CardContent>
            <RadioGroup
              value={formData.shippingMethod}
              onValueChange={(value) => handleInputChange(''shippingMethod'', value)}
            >
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="standard" id="standard" />
                  <Label htmlFor="standard">
                    <div>
                      <p className="font-semibold">Standard Shipping</p>
                      <p className="text-sm text-muted-foreground">5-7 business days</p>
                    </div>
                  </Label>
                </div>
                <p className="font-semibold">$5.99</p>
              </div>
              
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="express" id="express" />
                  <Label htmlFor="express">
                    <div>
                      <p className="font-semibold">Express Shipping</p>
                      <p className="text-sm text-muted-foreground">2-3 business days</p>
                    </div>
                  </Label>
                </div>
                <p className="font-semibold">$15.99</p>
              </div>
            </RadioGroup>
          </CardContent>
        </Card>

        {/* Step 3: Payment */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CreditCard className="w-5 h-5" />
              Payment Information
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <RadioGroup
              value={formData.paymentMethod}
              onValueChange={(value) => handleInputChange(''paymentMethod'', value)}
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="card" id="card" />
                <Label htmlFor="card">Credit/Debit Card</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="paypal" id="paypal" />
                <Label htmlFor="paypal">PayPal</Label>
              </div>
            </RadioGroup>
            
            {formData.paymentMethod === ''card'' && (
              <div className="space-y-4">
                <div>
                  <Label htmlFor="cardNumber">Card Number</Label>
                  <Input
                    id="cardNumber"
                    value={formData.cardNumber}
                    onChange={(e) => handleInputChange(''cardNumber'', e.target.value)}
                    placeholder="1234 5678 9012 3456"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="expiryDate">Expiry Date</Label>
                    <Input
                      id="expiryDate"
                      value={formData.expiryDate}
                      onChange={(e) => handleInputChange(''expiryDate'', e.target.value)}
                      placeholder="MM/YY"
                    />
                  </div>
                  <div>
                    <Label htmlFor="cvv">CVV</Label>
                    <Input
                      id="cvv"
                      value={formData.cvv}
                      onChange={(e) => handleInputChange(''cvv'', e.target.value)}
                      placeholder="123"
                    />
                  </div>
                </div>
              </div>
            )}
            
            <div className="flex items-center space-x-2">
              <Checkbox
                id="saveInfo"
                checked={formData.saveInfo}
                onCheckedChange={(checked) => handleInputChange(''saveInfo'', checked)}
              />
              <Label htmlFor="saveInfo" className="text-sm">
                Save this information for next time
              </Label>
            </div>
          </CardContent>
        </Card>

        <Button size="lg" className="w-full" onClick={handleSubmit}>
          <Shield className="w-5 h-5 mr-2" />
          Place Order - ${total.toFixed(2)}
        </Button>
      </div>

      {/* Order Summary */}
      <div>
        <Card className="sticky top-6">
          <CardHeader>
            <CardTitle>Order Summary</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-4">
              {items.map((item) => (
                <div key={item.id} className="flex gap-3">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="w-16 h-16 object-cover rounded"
                  />
                  <div className="flex-1">
                    <p className="font-semibold text-sm">{item.name}</p>
                    <p className="text-xs text-muted-foreground">Qty: {item.quantity}</p>
                    <p className="font-semibold">${(item.price * item.quantity).toFixed(2)}</p>
                  </div>
                </div>
              ))}
            </div>
            
            <Separator />
            
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Subtotal</span>
                <span>${subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Shipping</span>
                <span>${shipping.toFixed(2)}</span>
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
      </div>
    </div>
  );
}',
    '{"npm": ["lucide-react"], "components": ["Card", "Button", "Input", "Label", "Checkbox", "RadioGroup", "Separator"]}',
    '{"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}, "price": {"type": "number"}, "quantity": {"type": "number"}, "image": {"type": "string"}}, "required": ["id", "name", "price", "quantity", "image"]}}, "onPlaceOrder": {"type": "function"}}, "required": ["items", "onPlaceOrder"]}',
    '{"items": [{"id": "1", "name": "Wireless Headphones", "price": 79.99, "quantity": 1, "image": "/api/placeholder/64/64"}, {"id": "2", "name": "Phone Case", "price": 24.99, "quantity": 2, "image": "/api/placeholder/64/64"}]}',
    ARRAY['checkout', 'single-page', 'e-commerce', 'payment', 'shipping']::text[],
    '2025-07-17T03:46:56.375727',
    '2025-07-17T03:46:56.375728'
);
