-- Block 14: Sale Banner - Countdown
-- Description: Promotional sale banner with countdown timer
-- Generated: 2025-07-17T03:46:56.382832

INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '7be6f714-0e0b-4596-8cc8-f25ab75f4ca8',
    'Sale Banner - Countdown',
    'Promotional sale banner with countdown timer',
    'sale-banner',
    'e-commerce',
    'import React, { useState, useEffect } from ''react'';
import { Button } from ''@/components/ui/button'';
import { Badge } from ''@/components/ui/badge'';
import { Card } from ''@/components/ui/card'';
import { Flame, Clock, ArrowRight, Zap } from ''lucide-react'';

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
        backgroundColor: sale.backgroundColor || ''#ef4444'',
        color: sale.textColor || ''white''
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
                {isExpired ? ''Sale Ended'' : ''Shop Now''}
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
                      { label: ''Days'', value: timeLeft.days },
                      { label: ''Hours'', value: timeLeft.hours },
                      { label: ''Minutes'', value: timeLeft.minutes },
                      { label: ''Seconds'', value: timeLeft.seconds }
                    ].map((item) => (
                      <div key={item.label} className="bg-white/20 rounded-lg p-4">
                        <div className="text-3xl font-bold">
                          {item.value.toString().padStart(2, ''0'')}
                        </div>
                        <div className="text-sm opacity-75">
                          {item.label}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                
                <p className="text-sm opacity-75 mt-4">
                  Hurry! Don''t miss out on these amazing deals
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
}',
    '{"npm": ["lucide-react"], "components": ["Button", "Badge", "Card"]}',
    '{"type": "object", "properties": {"sale": {"type": "object", "properties": {"title": {"type": "string"}, "subtitle": {"type": "string"}, "description": {"type": "string"}, "discountPercentage": {"type": "number"}, "endDate": {"type": "string"}, "image": {"type": "string"}, "backgroundColor": {"type": "string"}, "textColor": {"type": "string"}}, "required": ["title", "description", "discountPercentage", "endDate"]}, "onShopNow": {"type": "function"}, "compact": {"type": "boolean"}}, "required": ["sale"]}',
    '{"sale": {"title": "Black Friday Sale", "subtitle": "Biggest Sale of the Year", "description": "Get incredible discounts on thousands of products across all categories. From electronics to fashion, home goods to beauty products.", "discountPercentage": 50, "endDate": "2024-11-30T23:59:59Z", "backgroundColor": "#dc2626", "textColor": "#ffffff"}, "compact": false}',
    ARRAY['sale-banner', 'countdown', 'e-commerce', 'promotion', 'urgency']::text[],
    '2025-07-17T03:46:56.375849',
    '2025-07-17T03:46:56.375852'
);
