"""
Page Generation Module for Figma MCP Server
Implements the missing page composition layer that assembles blocks into complete pages
"""

import os
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class PageGenerator:
    """Generates complete pages by composing blocks and components"""
    
    def __init__(self):
        self.page_templates = self._initialize_page_templates()
        self.page_layouts = self._initialize_page_layouts()
        
    def _initialize_page_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize page templates for different app types"""
        return {
            "dashboard": {
                "imports": [
                    "import React from 'react';",
                    "import { AppShell } from '@/components/app-shell/AppShell';",
                    "import { StatsCards } from '@/components/dashboard/StatsCards';",
                    "import { Charts } from '@/components/dashboard/Charts';",
                    "import { RecentActivity } from '@/components/dashboard/RecentActivity';",
                    "import { DataTable } from '@/components/dashboard/DataTable';"
                ],
                "layout": "app-shell",
                "sections": ["stats", "charts", "activity", "data-table"]
            },
            "home": {
                "imports": [
                    "import React from 'react';",
                    "import { Hero } from '@/components/landing/Hero';",
                    "import { Features } from '@/components/landing/Features';",
                    "import { Testimonials } from '@/components/landing/Testimonials';",
                    "import { CTA } from '@/components/landing/CTA';",
                    "import { Footer } from '@/components/layout/Footer';"
                ],
                "layout": "marketing",
                "sections": ["hero", "features", "testimonials", "cta", "footer"]
            },
            "login": {
                "imports": [
                    "import React from 'react';",
                    "import { SignIn } from '@/components/auth/SignIn';",
                    "import { AuthLayout } from '@/components/auth/AuthLayout';"
                ],
                "layout": "auth",
                "sections": ["signin-form"]
            },
            "signup": {
                "imports": [
                    "import React from 'react';",
                    "import { SignUp } from '@/components/auth/SignUp';",
                    "import { AuthLayout } from '@/components/auth/AuthLayout';"
                ],
                "layout": "auth",
                "sections": ["signup-form"]
            },
            "products": {
                "imports": [
                    "import React from 'react';",
                    "import { AppShell } from '@/components/app-shell/AppShell';",
                    "import { ProductGrid } from '@/components/ecommerce/ProductGrid';",
                    "import { CategoryFilter } from '@/components/ecommerce/CategoryFilter';",
                    "import { SearchBar } from '@/components/ui/SearchBar';"
                ],
                "layout": "app-shell",
                "sections": ["search", "filters", "product-grid"]
            },
            "product-detail": {
                "imports": [
                    "import React from 'react';",
                    "import { useParams } from 'react-router-dom';",
                    "import { AppShell } from '@/components/app-shell/AppShell';",
                    "import { ProductDetail } from '@/components/ecommerce/ProductDetail';",
                    "import { Reviews } from '@/components/ecommerce/Reviews';",
                    "import { RelatedProducts } from '@/components/ecommerce/RelatedProducts';"
                ],
                "layout": "app-shell",
                "sections": ["product-detail", "reviews", "related"]
            },
            "cart": {
                "imports": [
                    "import React from 'react';",
                    "import { AppShell } from '@/components/app-shell/AppShell';",
                    "import { ShoppingCart } from '@/components/ecommerce/ShoppingCart';",
                    "import { OrderSummary } from '@/components/ecommerce/OrderSummary';"
                ],
                "layout": "app-shell",
                "sections": ["cart", "summary"]
            },
            "checkout": {
                "imports": [
                    "import React from 'react';",
                    "import { CheckoutLayout } from '@/components/checkout/CheckoutLayout';",
                    "import { CheckoutForm } from '@/components/checkout/CheckoutForm';",
                    "import { PaymentForm } from '@/components/checkout/PaymentForm';",
                    "import { OrderReview } from '@/components/checkout/OrderReview';"
                ],
                "layout": "checkout",
                "sections": ["shipping", "payment", "review"]
            },
            "profile": {
                "imports": [
                    "import React from 'react';",
                    "import { AppShell } from '@/components/app-shell/AppShell';",
                    "import { UserProfile } from '@/components/profile/UserProfile';",
                    "import { ProfileSettings } from '@/components/profile/ProfileSettings';",
                    "import { ActivityFeed } from '@/components/profile/ActivityFeed';"
                ],
                "layout": "app-shell",
                "sections": ["profile-header", "settings", "activity"]
            },
            "settings": {
                "imports": [
                    "import React from 'react';",
                    "import { AppShell } from '@/components/app-shell/AppShell';",
                    "import { SettingsTabs } from '@/components/settings/SettingsTabs';",
                    "import { AccountSettings } from '@/components/settings/AccountSettings';",
                    "import { NotificationSettings } from '@/components/settings/NotificationSettings';",
                    "import { SecuritySettings } from '@/components/settings/SecuritySettings';"
                ],
                "layout": "app-shell",
                "sections": ["settings-tabs"]
            },
            "404": {
                "imports": [
                    "import React from 'react';",
                    "import { Error404 } from '@/components/errors/Error404';"
                ],
                "layout": "minimal",
                "sections": ["error-404"]
            },
            "500": {
                "imports": [
                    "import React from 'react';",
                    "import { Error500 } from '@/components/errors/Error500';"
                ],
                "layout": "minimal",
                "sections": ["error-500"]
            }
        }
    
    def _initialize_page_layouts(self) -> Dict[str, str]:
        """Initialize layout templates"""
        return {
            "app-shell": '''export default function {PageName}Page() {
  return (
    <AppShell>
      <div className="container mx-auto px-4 py-8">
        {content}
      </div>
    </AppShell>
  );
}''',
            "marketing": '''export default function {PageName}Page() {
  return (
    <div className="min-h-screen">
      {content}
    </div>
  );
}''',
            "auth": '''export default function {PageName}Page() {
  return (
    <AuthLayout>
      <div className="flex min-h-screen items-center justify-center">
        {content}
      </div>
    </AuthLayout>
  );
}''',
            "checkout": '''export default function {PageName}Page() {
  return (
    <CheckoutLayout>
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {content}
      </div>
    </CheckoutLayout>
  );
}''',
            "minimal": '''export default function {PageName}Page() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      {content}
    </div>
  );
}'''
        }
    
    def generate_page(
        self,
        page_name: str,
        page_type: str,
        app_type: str,
        available_blocks: List[str],
        custom_sections: Optional[List[str]] = None
    ) -> str:
        """Generate a complete page by composing blocks"""
        
        # Get page template
        template = self.page_templates.get(page_type, self.page_templates.get("home"))
        layout = self.page_layouts.get(template["layout"], self.page_layouts["minimal"])
        
        # Build imports
        imports = template["imports"].copy()
        
        # Generate content based on sections
        sections = custom_sections or template["sections"]
        content_parts = []
        
        for section in sections:
            content = self._generate_section_content(section, page_type, app_type, available_blocks)
            if content:
                content_parts.append(content)
        
        # Compose the page
        page_content = "\n".join(imports) + "\n\n"
        
        # Build the component with state management
        content_jsx = "\n        ".join(content_parts)
        page_component = layout.replace("{PageName}", self._format_page_name(page_name))
        page_component = page_component.replace("{content}", content_jsx)
        
        # Add state management inside the component if needed
        if page_type in ["dashboard", "products", "cart"]:
            state_code = self._add_state_management(page_type)
            # Insert state management after the function opening brace
            page_component = page_component.replace(
                "Page() {\n  return (",
                f"Page() {{\n{state_code}  return ("
            )
        
        page_content += page_component
        
        return page_content
    
    def _generate_section_content(
        self,
        section: str,
        page_type: str,
        app_type: str,
        available_blocks: List[str]
    ) -> str:
        """Generate content for a specific section"""
        
        section_templates = {
            "hero": '<Hero />',
            "features": '<Features />',
            "testimonials": '<Testimonials />',
            "cta": '<CTA />',
            "footer": '<Footer />',
            "stats": '<StatsCards data={statsData} />',
            "charts": '<Charts data={chartData} />',
            "activity": '<RecentActivity items={recentItems} />',
            "data-table": '<DataTable data={tableData} columns={columns} />',
            "signin-form": '<SignIn onSubmit={handleSignIn} />',
            "signup-form": '<SignUp onSubmit={handleSignUp} />',
            "product-grid": '<ProductGrid products={products} onProductClick={handleProductClick} />',
            "filters": '<CategoryFilter categories={categories} onFilterChange={handleFilterChange} />',
            "search": '<SearchBar onSearch={handleSearch} />',
            "product-detail": '<ProductDetail product={product} />',
            "reviews": '<Reviews productId={productId} />',
            "related": '<RelatedProducts productId={productId} />',
            "cart": '<ShoppingCart items={cartItems} onUpdate={handleCartUpdate} />',
            "summary": '<OrderSummary subtotal={subtotal} shipping={shipping} tax={tax} />',
            "profile-header": '<UserProfile user={currentUser} />',
            "settings-tabs": '<SettingsTabs activeTab={activeTab} onTabChange={setActiveTab} />',
            "error-404": '<Error404 />',
            "error-500": '<Error500 />'
        }
        
        return section_templates.get(section, f'{{/* TODO: Implement {section} section */}}')
    
    def _add_state_management(self, page_type: str) -> str:
        """Add state management code for interactive pages"""
        
        state_templates = {
            "dashboard": '''  const [statsData, setStatsData] = React.useState([]);
  const [chartData, setChartData] = React.useState({});
  const [recentItems, setRecentItems] = React.useState([]);
  const [tableData, setTableData] = React.useState([]);
  const [columns] = React.useState([
    { key: 'name', label: 'Name' },
    { key: 'status', label: 'Status' },
    { key: 'date', label: 'Date' }
  ]);

  React.useEffect(() => {
    // Fetch dashboard data
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    // TODO: Implement data fetching
  };

''',
            "products": '''  const [products, setProducts] = React.useState([]);
  const [categories, setCategories] = React.useState([]);
  const [filters, setFilters] = React.useState({});

  const handleProductClick = (product) => {
    // Navigate to product detail
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    // Refetch products with filters
  };

  const handleSearch = (searchTerm) => {
    // Search products
  };

''',
            "cart": '''  const [cartItems, setCartItems] = React.useState([]);
  const [subtotal, setSubtotal] = React.useState(0);
  const [shipping] = React.useState(10);
  const [tax, setTax] = React.useState(0);

  const handleCartUpdate = (itemId, quantity) => {
    // Update cart item quantity
  };

  React.useEffect(() => {
    // Calculate totals
    const sub = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    setSubtotal(sub);
    setTax(sub * 0.08); // 8% tax
  }, [cartItems]);

'''
        }
        
        return state_templates.get(page_type, "")
    
    def _format_page_name(self, page_name: str) -> str:
        """Format page name for component naming"""
        # Convert kebab-case to PascalCase
        parts = page_name.split('-')
        return ''.join(word.capitalize() for word in parts)
    
    def generate_pages_for_app(
        self,
        app_type: str,
        output_directory: str,
        available_blocks: List[str]
    ) -> List[Dict[str, Any]]:
        """Generate all pages for a specific app type"""
        
        # Define pages needed for each app type
        app_pages = {
            "saas": ["home", "dashboard", "login", "signup", "profile", "settings", "404"],
            "e-commerce": ["home", "products", "product-detail", "cart", "checkout", "login", "signup", "profile"],
            "blog": ["home", "blog-list", "blog-post", "about", "contact", "404"],
            "dashboard": ["dashboard", "reports", "analytics", "settings", "profile", "login"],
            "social": ["home", "feed", "profile", "messages", "settings", "login", "signup"],
            "portfolio": ["home", "about", "work", "contact", "404"],
            "landing": ["home", "about", "services", "pricing", "contact", "404"]
        }
        
        pages_to_generate = app_pages.get(app_type, ["home", "login", "404"])
        generated_pages = []
        
        pages_dir = os.path.join(output_directory, "pages")
        os.makedirs(pages_dir, exist_ok=True)
        
        for page_name in pages_to_generate:
            try:
                # Determine page type from name
                page_type = self._determine_page_type(page_name)
                
                # Generate page content
                page_content = self.generate_page(
                    page_name=page_name,
                    page_type=page_type,
                    app_type=app_type,
                    available_blocks=available_blocks
                )
                
                # Write page file
                filename = f"{page_name}.tsx"
                file_path = os.path.join(pages_dir, filename)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(page_content)
                
                generated_pages.append({
                    "filename": filename,
                    "path": file_path,
                    "type": "page",
                    "page_type": page_type,
                    "size": len(page_content)
                })
                
                logger.info(f"✅ Generated page: {filename}")
                
            except Exception as e:
                logger.error(f"Failed to generate page {page_name}: {e}")
        
        # Generate index file for pages
        self._generate_pages_index(pages_dir, generated_pages)
        
        return generated_pages
    
    def _determine_page_type(self, page_name: str) -> str:
        """Determine the page type from its name"""
        
        type_mappings = {
            "home": "home",
            "index": "home",
            "dashboard": "dashboard",
            "login": "login",
            "signin": "login",
            "signup": "signup",
            "register": "signup",
            "profile": "profile",
            "settings": "settings",
            "products": "products",
            "product-detail": "product-detail",
            "cart": "cart",
            "checkout": "checkout",
            "404": "404",
            "error": "500",
            "about": "home",
            "contact": "home",
            "blog-list": "products",  # Similar layout
            "blog-post": "product-detail",  # Similar layout
            "feed": "dashboard",  # Similar layout
            "messages": "dashboard"  # Similar layout
        }
        
        return type_mappings.get(page_name, "home")
    
    def _generate_pages_index(self, pages_dir: str, pages: List[Dict[str, Any]]) -> None:
        """Generate index.ts file for pages"""
        
        index_content = "// Auto-generated pages index\n\n"
        
        for page in pages:
            page_name = page["filename"].replace(".tsx", "")
            formatted_name = self._format_page_name(page_name)
            index_content += f"export {{ default as {formatted_name}Page }} from './{page_name}';\n"
        
        index_path = os.path.join(pages_dir, "index.ts")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        logger.info("✅ Generated pages index file")


# Integration function to be called from main server
async def generate_pages(
    app_type: str,
    output_directory: str,
    available_blocks: List[str]
) -> List[Dict[str, Any]]:
    """Main entry point for page generation"""
    
    generator = PageGenerator()
    return generator.generate_pages_for_app(app_type, output_directory, available_blocks)