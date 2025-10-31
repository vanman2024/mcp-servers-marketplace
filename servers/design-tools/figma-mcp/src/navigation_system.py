"""
Navigation System for Figma MCP Server
Implements comprehensive navigation patterns for all app types
"""

import os
from typing import Dict, List, Any, Optional
from enum import Enum

class NavigationType(Enum):
    """Navigation pattern types"""
    SIDEBAR = "sidebar"
    TOPBAR = "topbar"
    COMBINED = "combined"  # Sidebar + Topbar
    BOTTOM_TABS = "bottom-tabs"  # Mobile
    MEGA_MENU = "mega-menu"
    BREADCRUMB = "breadcrumb"
    TABS = "tabs"
    STEPS = "steps"  # Wizard navigation

class NavigationSystem:
    """Manages navigation generation for different app types"""
    
    def __init__(self):
        self.navigation_templates = self._initialize_navigation_templates()
        self.app_type_configs = self._initialize_app_type_configs()
    
    def _initialize_navigation_templates(self) -> Dict[str, str]:
        """Initialize navigation component templates"""
        return {
            "sidebar": '''import React from 'react';
import { cn } from '@/lib/utils';
import { 
  Home, 
  Package, 
  ShoppingCart, 
  Users, 
  Settings,
  ChevronLeft,
  Menu
} from 'lucide-react';

interface SidebarProps {
  className?: string;
  collapsed?: boolean;
  onToggle?: () => void;
}

export function Sidebar({ className, collapsed = false, onToggle }: SidebarProps) {
  const [isCollapsed, setIsCollapsed] = React.useState(collapsed);
  
  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
    onToggle?.();
  };

  const navItems = [
    { icon: Home, label: 'Dashboard', href: '/' },
    { icon: Package, label: 'Products', href: '/products' },
    { icon: ShoppingCart, label: 'Orders', href: '/orders' },
    { icon: Users, label: 'Customers', href: '/customers' },
    { icon: Settings, label: 'Settings', href: '/settings' },
  ];

  return (
    <aside className={cn(
      "bg-sidebar text-sidebar-foreground border-r border-sidebar-border transition-all duration-300",
      isCollapsed ? "w-16" : "w-64",
      className
    )}>
      <div className="flex h-16 items-center justify-between px-4">
        {!isCollapsed && (
          <h2 className="text-lg font-semibold">Dashboard</h2>
        )}
        <button
          onClick={toggleSidebar}
          className="p-2 hover:bg-sidebar-accent rounded-md"
        >
          {isCollapsed ? <Menu size={20} /> : <ChevronLeft size={20} />}
        </button>
      </div>
      
      <nav className="px-2 py-4">
        <ul className="space-y-2">
          {navItems.map((item) => (
            <li key={item.href}>
              <a
                href={item.href}
                className={cn(
                  "flex items-center gap-3 px-3 py-2 rounded-md",
                  "hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
                  "transition-colors"
                )}
              >
                <item.icon size={20} />
                {!isCollapsed && <span>{item.label}</span>}
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}''',

            "topbar": '''import React from 'react';
import { cn } from '@/lib/utils';
import { Search, Bell, User, Menu } from 'lucide-react';

interface TopbarProps {
  className?: string;
  onMenuClick?: () => void;
}

export function Topbar({ className, onMenuClick }: TopbarProps) {
  return (
    <header className={cn(
      "h-16 bg-background border-b border-border",
      "flex items-center justify-between px-6",
      className
    )}>
      <div className="flex items-center gap-4">
        <button
          onClick={onMenuClick}
          className="p-2 hover:bg-accent rounded-md lg:hidden"
        >
          <Menu size={20} />
        </button>
        
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={16} />
          <input
            type="search"
            placeholder="Search..."
            className="pl-10 pr-4 py-2 bg-secondary rounded-md w-64 focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        <button className="p-2 hover:bg-accent rounded-md relative">
          <Bell size={20} />
          <span className="absolute top-0 right-0 w-2 h-2 bg-destructive rounded-full"></span>
        </button>
        
        <button className="p-2 hover:bg-accent rounded-md">
          <User size={20} />
        </button>
      </div>
    </header>
  );
}''',

            "mobile-bottom-tabs": '''import React from 'react';
import { cn } from '@/lib/utils';
import { Home, Search, ShoppingCart, Heart, User } from 'lucide-react';

interface BottomTabsProps {
  className?: string;
  activeTab?: string;
}

export function BottomTabs({ className, activeTab = 'home' }: BottomTabsProps) {
  const tabs = [
    { id: 'home', icon: Home, label: 'Home', href: '/' },
    { id: 'search', icon: Search, label: 'Search', href: '/search' },
    { id: 'cart', icon: ShoppingCart, label: 'Cart', href: '/cart', badge: 3 },
    { id: 'wishlist', icon: Heart, label: 'Wishlist', href: '/wishlist' },
    { id: 'profile', icon: User, label: 'Profile', href: '/profile' },
  ];

  return (
    <nav className={cn(
      "fixed bottom-0 left-0 right-0 bg-background border-t border-border",
      "flex items-center justify-around h-16 lg:hidden",
      className
    )}>
      {tabs.map((tab) => (
        <a
          key={tab.id}
          href={tab.href}
          className={cn(
            "flex flex-col items-center gap-1 p-2 relative",
            activeTab === tab.id ? "text-primary" : "text-muted-foreground"
          )}
        >
          <tab.icon size={24} />
          <span className="text-xs">{tab.label}</span>
          {tab.badge && (
            <span className="absolute -top-1 -right-1 bg-destructive text-destructive-foreground text-xs rounded-full w-5 h-5 flex items-center justify-center">
              {tab.badge}
            </span>
          )}
        </a>
      ))}
    </nav>
  );
}''',

            "breadcrumb": '''import React from 'react';
import { ChevronRight, Home } from 'lucide-react';
import { cn } from '@/lib/utils';

interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  className?: string;
}

export function Breadcrumb({ items, className }: BreadcrumbProps) {
  return (
    <nav className={cn("flex items-center gap-2 text-sm", className)}>
      <a href="/" className="text-muted-foreground hover:text-foreground">
        <Home size={16} />
      </a>
      
      {items.map((item, index) => (
        <React.Fragment key={index}>
          <ChevronRight size={16} className="text-muted-foreground" />
          {item.href ? (
            <a 
              href={item.href}
              className="text-muted-foreground hover:text-foreground"
            >
              {item.label}
            </a>
          ) : (
            <span className="text-foreground font-medium">{item.label}</span>
          )}
        </React.Fragment>
      ))}
    </nav>
  );
}''',

            "mega-menu": '''import React from 'react';
import { cn } from '@/lib/utils';
import { ChevronDown } from 'lucide-react';

interface MegaMenuProps {
  className?: string;
}

export function MegaMenu({ className }: MegaMenuProps) {
  const [activeMenu, setActiveMenu] = React.useState<string | null>(null);

  const categories = {
    'Electronics': {
      featured: ['New Arrivals', 'Best Sellers', 'Sale'],
      subcategories: {
        'Computers': ['Laptops', 'Desktops', 'Tablets', 'Accessories'],
        'Mobile': ['Smartphones', 'Cases', 'Chargers', 'Headphones'],
        'Audio': ['Speakers', 'Headphones', 'Soundbars', 'Microphones'],
        'Gaming': ['Consoles', 'Games', 'Controllers', 'VR']
      }
    },
    'Fashion': {
      featured: ['Trending Now', 'Season Sale', 'New Collection'],
      subcategories: {
        'Men': ['Shirts', 'Pants', 'Shoes', 'Accessories'],
        'Women': ['Dresses', 'Tops', 'Shoes', 'Bags'],
        'Kids': ['Boys', 'Girls', 'Baby', 'Toys']
      }
    }
  };

  return (
    <nav className={cn("bg-background border-b border-border", className)}>
      <div className="container mx-auto">
        <ul className="flex items-center h-16">
          {Object.entries(categories).map(([category, data]) => (
            <li 
              key={category}
              className="relative"
              onMouseEnter={() => setActiveMenu(category)}
              onMouseLeave={() => setActiveMenu(null)}
            >
              <button className="flex items-center gap-1 px-4 py-2 hover:text-primary">
                {category}
                <ChevronDown size={16} />
              </button>
              
              {activeMenu === category && (
                <div className="absolute top-full left-0 w-screen max-w-4xl bg-popover shadow-lg rounded-b-lg p-6 grid grid-cols-4 gap-6">
                  <div>
                    <h3 className="font-semibold mb-4 text-primary">Featured</h3>
                    <ul className="space-y-2">
                      {data.featured.map((item) => (
                        <li key={item}>
                          <a href="#" className="text-sm hover:text-primary">
                            {item}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                  
                  {Object.entries(data.subcategories).map(([subcat, items]) => (
                    <div key={subcat}>
                      <h3 className="font-semibold mb-4">{subcat}</h3>
                      <ul className="space-y-2">
                        {items.map((item) => (
                          <li key={item}>
                            <a href="#" className="text-sm text-muted-foreground hover:text-foreground">
                              {item}
                            </a>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}''',

            "app-shell": '''import React from 'react';
import { Sidebar } from './Sidebar';
import { Topbar } from './Topbar';
import { cn } from '@/lib/utils';

interface AppShellProps {
  children: React.ReactNode;
  className?: string;
}

export function AppShell({ children, className }: AppShellProps) {
  const [sidebarCollapsed, setSidebarCollapsed] = React.useState(false);
  const [mobileSidebarOpen, setMobileSidebarOpen] = React.useState(false);

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Desktop Sidebar */}
      <div className="hidden lg:block">
        <Sidebar 
          collapsed={sidebarCollapsed}
          onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
        />
      </div>
      
      {/* Mobile Sidebar Overlay */}
      {mobileSidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 lg:hidden z-40"
          onClick={() => setMobileSidebarOpen(false)}
        />
      )}
      
      {/* Mobile Sidebar */}
      <div className={cn(
        "fixed left-0 top-0 h-full z-50 lg:hidden transition-transform",
        mobileSidebarOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <Sidebar onToggle={() => setMobileSidebarOpen(false)} />
      </div>
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <Topbar onMenuClick={() => setMobileSidebarOpen(true)} />
        <main className={cn(
          "flex-1 overflow-y-auto bg-background p-6",
          className
        )}>
          {children}
        </main>
      </div>
    </div>
  );
}'''
        }
    
    def _initialize_app_type_configs(self) -> Dict[str, Dict[str, Any]]:
        """Initialize navigation configurations for each app type"""
        return {
            "e-commerce": {
                "primary": NavigationType.COMBINED,
                "mobile": NavigationType.BOTTOM_TABS,
                "secondary": [NavigationType.MEGA_MENU, NavigationType.BREADCRUMB],
                "components": ["mega-menu", "breadcrumb", "mobile-bottom-tabs", "topbar"]
            },
            "dashboard": {
                "primary": NavigationType.COMBINED,
                "mobile": NavigationType.SIDEBAR,
                "secondary": [NavigationType.BREADCRUMB, NavigationType.TABS],
                "components": ["app-shell", "sidebar", "topbar", "breadcrumb"]
            },
            "saas": {
                "primary": NavigationType.COMBINED,
                "mobile": NavigationType.SIDEBAR,
                "secondary": [NavigationType.BREADCRUMB],
                "components": ["app-shell", "sidebar", "topbar", "breadcrumb"]
            },
            "marketing": {
                "primary": NavigationType.TOPBAR,
                "mobile": NavigationType.TOPBAR,
                "secondary": [],
                "components": ["topbar", "mobile-menu"]
            },
            "blog": {
                "primary": NavigationType.TOPBAR,
                "mobile": NavigationType.TOPBAR,
                "secondary": [NavigationType.BREADCRUMB],
                "components": ["topbar", "breadcrumb", "mobile-menu"]
            },
            "social": {
                "primary": NavigationType.COMBINED,
                "mobile": NavigationType.BOTTOM_TABS,
                "secondary": [],
                "components": ["app-shell", "sidebar", "topbar", "mobile-bottom-tabs"]
            }
        }
    
    def generate_navigation_components(
        self,
        app_type: str,
        output_directory: str
    ) -> List[Dict[str, Any]]:
        """Generate navigation components for an app type"""
        
        config = self.app_type_configs.get(
            app_type,
            self.app_type_configs["saas"]
        )
        
        generated_components = []
        nav_dir = os.path.join(output_directory, "components", "navigation")
        os.makedirs(nav_dir, exist_ok=True)
        
        # Generate each navigation component
        for component_name in config["components"]:
            if component_name in self.navigation_templates:
                template = self.navigation_templates[component_name]
                
                # Convert component name to PascalCase
                file_name = ''.join(word.capitalize() for word in component_name.split('-'))
                file_path = os.path.join(nav_dir, f"{file_name}.tsx")
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(template)
                
                generated_components.append({
                    "name": file_name,
                    "path": file_path,
                    "type": "navigation",
                    "size": len(template)
                })
        
        # Generate index file
        self._generate_navigation_index(nav_dir, generated_components)
        
        return generated_components
    
    def _generate_navigation_index(
        self,
        nav_dir: str,
        components: List[Dict[str, Any]]
    ) -> None:
        """Generate index.ts for navigation components"""
        
        index_content = "// Auto-generated navigation components index\n\n"
        
        for component in components:
            name = component["name"]
            index_content += f"export {{ {name} }} from './{name}';\n"
        
        index_path = os.path.join(nav_dir, "index.ts")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)


# Export function to be used by the Figma server
async def generate_navigation(
    app_type: str,
    output_directory: str
) -> List[Dict[str, Any]]:
    """Generate navigation components for an app type"""
    
    nav_system = NavigationSystem()
    return nav_system.generate_navigation_components(app_type, output_directory)