#!/usr/bin/env python3
"""
Figma Marketing MCP Server - Enterprise-Grade Marketing & Landing Page System
Advanced marketing component management through Supabase database

Provides comprehensive tools for:
- Marketing sections: Hero, CTA, Pricing, Testimonials, etc.
- Landing page generation with A/B testing capabilities
- Conversion-optimized component selection with analytics
- SEO-friendly marketing layouts with metadata management
- Multi-language support for international marketing
- Theme customization for brand consistency
- Performance monitoring and optimization
- Integration with CRM/Email/Analytics platforms
"""

import os
import sys
import json
import logging
import re
import hashlib
import uuid
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from collections import defaultdict
import base64

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("=== Figma Marketing MCP Server Starting (Enterprise Edition) ===")
logger.info("Python version: %s", sys.version)
logger.info("Working directory: %s", os.getcwd())

# Add parent directory to path for array_params_fix import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import and apply the array parameters fix
try:
    from array_params_fix import apply_array_params_fix
    apply_array_params_fix()
    logger.info("Array parameters fix applied successfully")
except ImportError:
    logger.warning("Could not import array_params_fix - array parameters may not work correctly")

# FastMCP for HTTP serving
from fastmcp import FastMCP

# Supabase client for database operations
from supabase import create_client, Client
import httpx

# Initialize FastMCP server
mcp = FastMCP("figma-marketing")

# ===================================================================
# ADVANCED TYPE DEFINITIONS
# ===================================================================

class MarketingCategory(Enum):
    """Marketing component categories"""
    HERO_SECTIONS = "hero_sections"
    FEATURE_SECTIONS = "feature_sections"
    CTA_SECTIONS = "cta_sections"
    BENTO_GRIDS = "bento_grids"
    PRICING_SECTIONS = "pricing_sections"
    HEADER_SECTIONS = "header_sections"
    NEWSLETTER_SECTIONS = "newsletter_sections"
    STATS = "stats"
    TESTIMONIALS = "testimonials"
    BLOG_SECTIONS = "blog_sections"
    CONTACT_SECTIONS = "contact_sections"
    TEAM_SECTIONS = "team_sections"
    CONTENT_SECTIONS = "content_sections"
    LOGO_CLOUDS = "logo_clouds"
    FAQS = "faqs"
    FOOTERS = "footers"

class ComponentVariant(Enum):
    """Component variant types"""
    SIMPLE = "simple"
    GRADIENT = "gradient"
    WITH_IMAGE = "with_image"
    WITH_VIDEO = "with_video"
    SPLIT = "split"
    CENTERED = "centered"
    GRID = "grid"
    LIST = "list"
    CAROUSEL = "carousel"
    ACCORDION = "accordion"
    TABS = "tabs"
    MODAL = "modal"
    SIDEBAR = "sidebar"
    FEATURED = "featured"
    COMPARISON = "comparison"

class ConversionOptimizationType(Enum):
    """Conversion optimization strategies"""
    ABOVE_FOLD = "above_fold"
    SOCIAL_PROOF = "social_proof"
    URGENCY = "urgency"
    SCARCITY = "scarcity"
    VALUE_PROPOSITION = "value_proposition"
    TRUST_SIGNALS = "trust_signals"
    CLEAR_CTA = "clear_cta"
    MINIMAL_FRICTION = "minimal_friction"

@dataclass
class MarketingComponent:
    """Marketing component data structure"""
    id: str
    name: str
    category: MarketingCategory
    variant: ComponentVariant
    code: str
    props: Dict[str, Any]
    metadata: Dict[str, Any]
    analytics: Dict[str, Any] = field(default_factory=dict)
    ab_test_data: Dict[str, Any] = field(default_factory=dict)
    seo_data: Dict[str, Any] = field(default_factory=dict)
    translations: Dict[str, Dict[str, str]] = field(default_factory=dict)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LandingPageTemplate:
    """Landing page template structure"""
    id: str
    name: str
    page_type: str
    sections: List[str]
    theme: Dict[str, Any]
    metadata: Dict[str, Any]
    conversion_rate: float = 0.0
    ab_test_variants: List[Dict[str, Any]] = field(default_factory=list)

# ===================================================================
# MARKETING TAXONOMY CONFIGURATION
# ===================================================================

# Load marketing taxonomy
MARKETING_TAXONOMY_PATH = os.path.join(os.path.dirname(__file__), "../data/taxonomies/marketing_taxonomy.json")
MARKETING_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../data/marketing_templates")
MARKETING_CACHE_DIR = os.path.join(os.path.dirname(__file__), "../cache/marketing")
MARKETING_ANALYTICS_DIR = os.path.join(os.path.dirname(__file__), "../analytics/marketing")

def load_marketing_taxonomy():
    """Load marketing taxonomy from JSON file"""
    try:
        with open(MARKETING_TAXONOMY_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load marketing taxonomy: {e}")
        return None

def ensure_directories():
    """Ensure all required directories exist"""
    dirs = [MARKETING_TEMPLATES_DIR, MARKETING_CACHE_DIR, MARKETING_ANALYTICS_DIR]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)

# ===================================================================
# DATABASE CONNECTION & CACHING
# ===================================================================

class DatabaseConnectionPool:
    """Connection pool for database operations"""
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.connections: List[Client] = []
        self.available: List[bool] = []
        self._lock = asyncio.Lock()
    
    async def get_connection(self) -> Client:
        """Get an available connection from the pool"""
        async with self._lock:
            for i, available in enumerate(self.available):
                if available:
                    self.available[i] = False
                    return self.connections[i]
            
            # Create new connection if under limit
            if len(self.connections) < self.max_connections:
                client = await self._create_connection()
                self.connections.append(client)
                self.available.append(False)
                return client
            
            # Wait for available connection
            while True:
                await asyncio.sleep(0.1)
                for i, available in enumerate(self.available):
                    if available:
                        self.available[i] = False
                        return self.connections[i]
    
    async def release_connection(self, client: Client):
        """Release connection back to pool"""
        async with self._lock:
            for i, conn in enumerate(self.connections):
                if conn == client:
                    self.available[i] = True
                    break
    
    async def _create_connection(self) -> Client:
        """Create new database connection"""
        from dotenv import load_dotenv
        load_dotenv()
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not url or not key:
            raise ValueError("Missing Supabase credentials")
        
        return create_client(url, key)

# Global connection pool
connection_pool = DatabaseConnectionPool()

class MarketingComponentCache:
    """Advanced caching system for marketing components"""
    def __init__(self):
        self.memory_cache: Dict[str, Any] = {}
        self.cache_stats: Dict[str, int] = defaultdict(int)
        self.cache_ttl = timedelta(hours=1)
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache"""
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            if datetime.now(timezone.utc) < entry['expires']:
                self.cache_stats['hits'] += 1
                return entry['data']
            else:
                del self.memory_cache[key]
        
        self.cache_stats['misses'] += 1
        return None
    
    def set(self, key: str, data: Any, ttl: Optional[timedelta] = None):
        """Set item in cache"""
        expires = datetime.now(timezone.utc) + (ttl or self.cache_ttl)
        self.memory_cache[key] = {
            'data': data,
            'expires': expires
        }
    
    def invalidate(self, pattern: Optional[str] = None):
        """Invalidate cache entries matching pattern"""
        if pattern:
            keys_to_delete = [k for k in self.memory_cache.keys() if pattern in k]
            for key in keys_to_delete:
                del self.memory_cache[key]
        else:
            self.memory_cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = self.cache_stats['hits'] / total if total > 0 else 0
        
        return {
            'hits': self.cache_stats['hits'],
            'misses': self.cache_stats['misses'],
            'hit_rate': hit_rate,
            'size': len(self.memory_cache)
        }

# Global cache instance
marketing_cache = MarketingComponentCache()

# ===================================================================
# SEO OPTIMIZATION ENGINE
# ===================================================================

class SEOOptimizer:
    """SEO optimization for marketing components"""
    
    @staticmethod
    def generate_meta_tags(component: MarketingComponent, page_context: Dict[str, Any]) -> Dict[str, str]:
        """Generate SEO meta tags for component"""
        meta_tags = {
            'title': page_context.get('title', ''),
            'description': page_context.get('description', ''),
            'keywords': page_context.get('keywords', []),
            'og:title': page_context.get('title', ''),
            'og:description': page_context.get('description', ''),
            'og:type': 'website',
            'twitter:card': 'summary_large_image',
            'twitter:title': page_context.get('title', ''),
            'twitter:description': page_context.get('description', ''),
        }
        
        # Add component-specific SEO data
        if component.seo_data:
            meta_tags.update(component.seo_data)
        
        return meta_tags
    
    @staticmethod
    def generate_structured_data(component: MarketingComponent, business_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured data (JSON-LD) for SEO"""
        structured_data = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": component.name,
            "description": component.metadata.get('description', ''),
            "publisher": {
                "@type": "Organization",
                "name": business_info.get('name', ''),
                "logo": business_info.get('logo', '')
            }
        }
        
        # Add specific structured data based on component type
        if component.category == MarketingCategory.PRICING_SECTIONS:
            structured_data['@type'] = 'Product'
            structured_data['offers'] = {
                "@type": "AggregateOffer",
                "priceCurrency": "USD",
                "lowPrice": component.props.get('lowest_price', 0),
                "highPrice": component.props.get('highest_price', 999)
            }
        elif component.category == MarketingCategory.TESTIMONIALS:
            structured_data['@type'] = 'Review'
            structured_data['reviewRating'] = {
                "@type": "Rating",
                "ratingValue": component.props.get('rating', 5),
                "bestRating": 5
            }
        
        return structured_data
    
    @staticmethod
    def optimize_content_for_seo(content: str, keywords: List[str]) -> str:
        """Optimize content for target keywords"""
        # Simple keyword density optimization
        for keyword in keywords:
            # Ensure keyword appears but not too frequently (2-3% density)
            keyword_count = content.lower().count(keyword.lower())
            word_count = len(content.split())
            density = (keyword_count / word_count) * 100 if word_count > 0 else 0
            
            if density < 2:
                # Add keyword naturally
                content = content.replace(
                    content.split('.')[0],
                    f"{content.split('.')[0]} {keyword}",
                    1
                )
        
        return content

# ===================================================================
# A/B TESTING FRAMEWORK
# ===================================================================

class ABTestingEngine:
    """A/B testing for marketing components"""
    
    def __init__(self):
        self.active_tests: Dict[str, Dict[str, Any]] = {}
        self.test_results: Dict[str, Dict[str, Any]] = {}
    
    def create_test(self, component_id: str, variants: List[Dict[str, Any]], 
                   traffic_split: List[float]) -> str:
        """Create new A/B test"""
        test_id = str(uuid.uuid4())
        
        self.active_tests[test_id] = {
            'component_id': component_id,
            'variants': variants,
            'traffic_split': traffic_split,
            'start_date': datetime.now(timezone.utc),
            'impressions': defaultdict(int),
            'conversions': defaultdict(int),
            'status': 'active'
        }
        
        return test_id
    
    def get_variant(self, test_id: str, user_id: str) -> Dict[str, Any]:
        """Get variant for user based on traffic split"""
        if test_id not in self.active_tests:
            return None
        
        test = self.active_tests[test_id]
        
        # Use consistent hashing for user assignment
        hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        bucket = hash_value % 100
        
        # Assign to variant based on traffic split
        cumulative = 0
        for i, split in enumerate(test['traffic_split']):
            cumulative += split * 100
            if bucket < cumulative:
                variant = test['variants'][i]
                test['impressions'][i] += 1
                return variant
        
        # Default to control
        return test['variants'][0]
    
    def record_conversion(self, test_id: str, variant_index: int):
        """Record conversion for a variant"""
        if test_id in self.active_tests:
            self.active_tests[test_id]['conversions'][variant_index] += 1
    
    def get_test_results(self, test_id: str) -> Dict[str, Any]:
        """Get current test results with statistical significance"""
        if test_id not in self.active_tests:
            return None
        
        test = self.active_tests[test_id]
        results = {
            'test_id': test_id,
            'status': test['status'],
            'duration': (datetime.now(timezone.utc) - test['start_date']).days,
            'variants': []
        }
        
        for i, variant in enumerate(test['variants']):
            impressions = test['impressions'].get(i, 0)
            conversions = test['conversions'].get(i, 0)
            conversion_rate = conversions / impressions if impressions > 0 else 0
            
            results['variants'].append({
                'index': i,
                'name': variant.get('name', f'Variant {i}'),
                'impressions': impressions,
                'conversions': conversions,
                'conversion_rate': conversion_rate
            })
        
        # Calculate statistical significance
        if len(results['variants']) >= 2 and all(v['impressions'] > 100 for v in results['variants']):
            control = results['variants'][0]
            for variant in results['variants'][1:]:
                # Simple z-test for proportions
                p1 = control['conversion_rate']
                p2 = variant['conversion_rate']
                n1 = control['impressions']
                n2 = variant['impressions']
                
                p_pooled = (control['conversions'] + variant['conversions']) / (n1 + n2)
                se = ((p_pooled * (1 - p_pooled)) * (1/n1 + 1/n2)) ** 0.5
                z = (p2 - p1) / se if se > 0 else 0
                
                # Two-tailed test at 95% confidence
                variant['is_significant'] = abs(z) > 1.96
                variant['confidence'] = min(abs(z) / 1.96 * 100, 100)
        
        return results

# Global A/B testing engine
ab_testing = ABTestingEngine()

# ===================================================================
# CONVERSION TRACKING & ANALYTICS
# ===================================================================

class ConversionTracker:
    """Track conversions and analytics for marketing components"""
    
    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        self.conversion_funnels: Dict[str, List[str]] = {}
        self.goals: Dict[str, Dict[str, Any]] = {}
    
    def track_event(self, event_type: str, component_id: str, 
                   user_id: str, properties: Dict[str, Any] = None):
        """Track user interaction event"""
        event = {
            'timestamp': datetime.now(timezone.utc),
            'event_type': event_type,
            'component_id': component_id,
            'user_id': user_id,
            'properties': properties or {}
        }
        
        self.events.append(event)
        
        # Check if event completes a goal
        self._check_goal_completion(event)
    
    def create_goal(self, goal_id: str, goal_type: str, 
                   target_event: str, target_value: Any = None):
        """Create conversion goal"""
        self.goals[goal_id] = {
            'type': goal_type,
            'target_event': target_event,
            'target_value': target_value,
            'completions': 0,
            'value': 0
        }
    
    def create_funnel(self, funnel_id: str, steps: List[str]):
        """Create conversion funnel"""
        self.conversion_funnels[funnel_id] = steps
    
    def get_funnel_report(self, funnel_id: str, 
                         start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get funnel conversion report"""
        if funnel_id not in self.conversion_funnels:
            return None
        
        steps = self.conversion_funnels[funnel_id]
        funnel_data = {
            'funnel_id': funnel_id,
            'steps': [],
            'overall_conversion': 0
        }
        
        # Filter events by date range
        filtered_events = [
            e for e in self.events 
            if start_date <= e['timestamp'] <= end_date
        ]
        
        # Group events by user
        user_events = defaultdict(list)
        for event in filtered_events:
            user_events[event['user_id']].append(event)
        
        # Analyze funnel progression
        step_users = []
        for i, step in enumerate(steps):
            users_at_step = set()
            
            for user_id, events in user_events.items():
                # Check if user completed all previous steps
                if i == 0 or user_id in step_users[i-1]:
                    # Check if user completed this step
                    if any(e['event_type'] == step for e in events):
                        users_at_step.add(user_id)
            
            step_users.append(users_at_step)
            
            funnel_data['steps'].append({
                'name': step,
                'users': len(users_at_step),
                'conversion_rate': len(users_at_step) / len(step_users[0]) if i > 0 and step_users[0] else 100
            })
        
        # Calculate overall conversion
        if step_users and step_users[0]:
            funnel_data['overall_conversion'] = len(step_users[-1]) / len(step_users[0])
        
        return funnel_data
    
    def _check_goal_completion(self, event: Dict[str, Any]):
        """Check if event completes any goals"""
        for goal_id, goal in self.goals.items():
            if event['event_type'] == goal['target_event']:
                if goal['target_value'] is None or event['properties'].get('value') == goal['target_value']:
                    goal['completions'] += 1
                    goal['value'] += event['properties'].get('revenue', 0)

# Global conversion tracker
conversion_tracker = ConversionTracker()

# ===================================================================
# MULTI-LANGUAGE SUPPORT
# ===================================================================

class TranslationManager:
    """Manage multi-language support for marketing content"""
    
    def __init__(self):
        self.supported_languages = ['en', 'es', 'fr', 'de', 'pt', 'it', 'ja', 'zh']
        self.translations: Dict[str, Dict[str, str]] = {}
        self.translation_cache: Dict[str, str] = {}
    
    def translate_component(self, component: MarketingComponent, 
                          target_language: str) -> MarketingComponent:
        """Translate component to target language"""
        if target_language not in self.supported_languages:
            return component
        
        # Check if translation exists
        if target_language in component.translations:
            translated = component.translations[target_language]
        else:
            # Generate translation
            translated = self._generate_translation(component, target_language)
            component.translations[target_language] = translated
        
        # Create translated component
        translated_component = MarketingComponent(
            id=f"{component.id}_{target_language}",
            name=component.name,
            category=component.category,
            variant=component.variant,
            code=self._translate_code(component.code, translated),
            props=translated.get('props', component.props),
            metadata=component.metadata,
            translations=component.translations
        )
        
        return translated_component
    
    def _generate_translation(self, component: MarketingComponent, 
                            target_language: str) -> Dict[str, Any]:
        """Generate translation for component"""
        # This would integrate with translation API
        # For now, return placeholder translations
        translations = {
            'props': {}
        }
        
        # Translate text props
        for key, value in component.props.items():
            if isinstance(value, str) and any(word in key.lower() for word in ['text', 'title', 'description', 'label']):
                # Cache key for translation
                cache_key = f"{value}:{target_language}"
                
                if cache_key in self.translation_cache:
                    translations['props'][key] = self.translation_cache[cache_key]
                else:
                    # Placeholder translation logic
                    translated = f"[{target_language}] {value}"
                    translations['props'][key] = translated
                    self.translation_cache[cache_key] = translated
            else:
                translations['props'][key] = value
        
        return translations
    
    def _translate_code(self, code: str, translations: Dict[str, Any]) -> str:
        """Replace text in code with translations"""
        translated_code = code
        
        # Replace prop values in code
        for key, value in translations.get('props', {}).items():
            if isinstance(value, str):
                # Find and replace in code
                pattern = rf'([\'"]{key}[\'"]:\s*[\'"])([^\'"]*)([\'"])'
                translated_code = re.sub(pattern, rf'\1{value}\3', translated_code)
        
        return translated_code

# Global translation manager
translation_manager = TranslationManager()

# ===================================================================
# THEME CUSTOMIZATION SYSTEM
# ===================================================================

class ThemeEngine:
    """Advanced theme customization for brand consistency"""
    
    def __init__(self):
        self.themes: Dict[str, Dict[str, Any]] = {}
        self.default_theme = self._create_default_theme()
    
    def _create_default_theme(self) -> Dict[str, Any]:
        """Create default theme configuration"""
        return {
            'colors': {
                'primary': '#3B82F6',
                'secondary': '#10B981',
                'accent': '#F59E0B',
                'neutral': '#6B7280',
                'background': '#FFFFFF',
                'text': '#111827',
                'error': '#EF4444',
                'success': '#10B981',
                'warning': '#F59E0B'
            },
            'typography': {
                'fontFamily': {
                    'sans': ['Inter', 'system-ui', 'sans-serif'],
                    'serif': ['Georgia', 'serif'],
                    'mono': ['Menlo', 'monospace']
                },
                'fontSize': {
                    'xs': '0.75rem',
                    'sm': '0.875rem',
                    'base': '1rem',
                    'lg': '1.125rem',
                    'xl': '1.25rem',
                    '2xl': '1.5rem',
                    '3xl': '1.875rem',
                    '4xl': '2.25rem',
                    '5xl': '3rem'
                }
            },
            'spacing': {
                'xs': '0.5rem',
                'sm': '1rem',
                'md': '1.5rem',
                'lg': '2rem',
                'xl': '3rem',
                '2xl': '4rem'
            },
            'borderRadius': {
                'none': '0',
                'sm': '0.125rem',
                'md': '0.375rem',
                'lg': '0.5rem',
                'xl': '1rem',
                'full': '9999px'
            },
            'shadows': {
                'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
                'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
                'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1)'
            }
        }
    
    def create_theme(self, theme_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create custom theme"""
        # Merge with default theme
        theme = self._deep_merge(self.default_theme, config)
        self.themes[theme_id] = theme
        
        # Generate CSS variables
        theme['cssVariables'] = self._generate_css_variables(theme)
        
        return theme
    
    def apply_theme_to_component(self, component: MarketingComponent, 
                               theme_id: str) -> str:
        """Apply theme to component code"""
        theme = self.themes.get(theme_id, self.default_theme)
        themed_code = component.code
        
        # Replace color values
        for color_name, color_value in theme['colors'].items():
            themed_code = themed_code.replace(
                f'colors.{color_name}',
                f'"{color_value}"'
            )
        
        # Replace typography values
        for font_key, font_value in theme['typography']['fontSize'].items():
            themed_code = themed_code.replace(
                f'text-{font_key}',
                f'style={{fontSize: "{font_value}"}}'
            )
        
        # Add theme provider wrapper
        themed_code = f"""
import {{ ThemeProvider }} from './theme/ThemeProvider';

const themedComponent = () => (
  <ThemeProvider theme={{`{theme_id}`}}>
    {themed_code}
  </ThemeProvider>
);

export default themedComponent;
"""
        
        return themed_code
    
    def _generate_css_variables(self, theme: Dict[str, Any]) -> str:
        """Generate CSS variables from theme"""
        css_vars = []
        
        # Colors
        for color_name, color_value in theme['colors'].items():
            css_vars.append(f'  --color-{color_name}: {color_value};')
        
        # Typography
        for size_name, size_value in theme['typography']['fontSize'].items():
            css_vars.append(f'  --font-size-{size_name}: {size_value};')
        
        # Spacing
        for space_name, space_value in theme['spacing'].items():
            css_vars.append(f'  --spacing-{space_name}: {space_value};')
        
        return '\n'.join(css_vars)
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result

# Global theme engine
theme_engine = ThemeEngine()

# ===================================================================
# PERFORMANCE OPTIMIZATION
# ===================================================================

class PerformanceOptimizer:
    """Performance optimization for marketing components"""
    
    @staticmethod
    def optimize_images(component_code: str) -> str:
        """Optimize images in component code"""
        # Add lazy loading
        component_code = re.sub(
            r'<img([^>]+)>',
            r'<img\1 loading="lazy">',
            component_code
        )
        
        # Add responsive images
        component_code = re.sub(
            r'src="([^"]+)"',
            r'src="\1" srcset="\1 1x, \1 2x"',
            component_code
        )
        
        return component_code
    
    @staticmethod
    def optimize_bundle_size(components: List[MarketingComponent]) -> Dict[str, Any]:
        """Optimize bundle size for component collection"""
        optimization_report = {
            'original_size': 0,
            'optimized_size': 0,
            'shared_dependencies': [],
            'recommendations': []
        }
        
        # Analyze shared dependencies
        dependency_count = defaultdict(int)
        for component in components:
            for dep in component.metadata.get('dependencies', []):
                dependency_count[dep] += 1
        
        # Identify shared dependencies
        shared_deps = [dep for dep, count in dependency_count.items() if count > 1]
        optimization_report['shared_dependencies'] = shared_deps
        
        # Calculate sizes
        for component in components:
            original_size = len(component.code.encode('utf-8'))
            optimization_report['original_size'] += original_size
            
            # Apply optimizations
            optimized_code = component.code
            
            # Remove comments
            optimized_code = re.sub(r'/\*.*?\*/', '', optimized_code, flags=re.DOTALL)
            optimized_code = re.sub(r'//.*?$', '', optimized_code, flags=re.MULTILINE)
            
            # Minify whitespace
            optimized_code = re.sub(r'\s+', ' ', optimized_code)
            
            optimized_size = len(optimized_code.encode('utf-8'))
            optimization_report['optimized_size'] += optimized_size
        
        # Generate recommendations
        if optimization_report['shared_dependencies']:
            optimization_report['recommendations'].append(
                f"Extract {len(shared_deps)} shared dependencies to reduce bundle size"
            )
        
        savings = optimization_report['original_size'] - optimization_report['optimized_size']
        if savings > 0:
            percentage = (savings / optimization_report['original_size']) * 100
            optimization_report['recommendations'].append(
                f"Minification can reduce bundle size by {percentage:.1f}%"
            )
        
        return optimization_report
    
    @staticmethod
    def generate_critical_css(component: MarketingComponent) -> str:
        """Generate critical CSS for above-the-fold content"""
        # Extract critical styles
        critical_styles = []
        
        # Hero sections always critical
        if component.category == MarketingCategory.HERO_SECTIONS:
            critical_styles.append("""
                .hero-section {
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                }
                .hero-content {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 2rem;
                }
            """)
        
        return '\n'.join(critical_styles)

# ===================================================================
# INTEGRATION APIS
# ===================================================================

class IntegrationManager:
    """Manage integrations with external marketing platforms"""
    
    def __init__(self):
        self.integrations = {
            'google_analytics': GoogleAnalyticsIntegration(),
            'mailchimp': MailchimpIntegration(),
            'hubspot': HubspotIntegration(),
            'segment': SegmentIntegration()
        }
    
    def track_event(self, integration_name: str, event_data: Dict[str, Any]):
        """Track event across integrations"""
        if integration_name in self.integrations:
            self.integrations[integration_name].track(event_data)
    
    def sync_contacts(self, integration_name: str, contacts: List[Dict[str, Any]]):
        """Sync contacts with integration"""
        if integration_name in self.integrations:
            self.integrations[integration_name].sync_contacts(contacts)

class GoogleAnalyticsIntegration:
    """Google Analytics integration"""
    
    def track(self, event_data: Dict[str, Any]):
        """Track event in Google Analytics"""
        # Generate GA tracking code
        tracking_code = f"""
        gtag('event', '{event_data.get('event_name')}', {{
            'event_category': '{event_data.get('category', 'Marketing')}',
            'event_label': '{event_data.get('label', '')}',
            'value': {event_data.get('value', 0)}
        }});
        """
        return tracking_code

class MailchimpIntegration:
    """Mailchimp integration"""
    
    def sync_contacts(self, contacts: List[Dict[str, Any]]):
        """Sync contacts with Mailchimp"""
        # Generate Mailchimp API call
        api_data = {
            'members': [
                {
                    'email_address': contact.get('email'),
                    'status': 'subscribed',
                    'merge_fields': {
                        'FNAME': contact.get('first_name', ''),
                        'LNAME': contact.get('last_name', '')
                    }
                }
                for contact in contacts
            ]
        }
        return api_data

class HubspotIntegration:
    """HubSpot integration"""
    
    def track(self, event_data: Dict[str, Any]):
        """Track event in HubSpot"""
        # Generate HubSpot tracking code
        tracking_code = f"""
        _hsq.push(['trackEvent', {{
            id: '{event_data.get('event_name')}',
            value: {event_data.get('value', 0)}
        }}]);
        """
        return tracking_code

class SegmentIntegration:
    """Segment integration"""
    
    def track(self, event_data: Dict[str, Any]):
        """Track event in Segment"""
        # Generate Segment tracking code
        tracking_code = f"""
        analytics.track('{event_data.get('event_name')}', {{
            category: '{event_data.get('category', 'Marketing')}',
            label: '{event_data.get('label', '')}',
            value: {event_data.get('value', 0)}
        }});
        """
        return tracking_code

# Global integration manager
integration_manager = IntegrationManager()

# ===================================================================
# DATABASE CONNECTION
# ===================================================================

def get_supabase_client() -> Client:
    """Get Supabase client for database operations"""
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not url or not key:
            raise ValueError("Missing Supabase credentials")
            
        client = create_client(url, key)
        logger.info("Successfully connected to Supabase")
        return client
        
    except Exception as e:
        logger.error(f"Failed to connect to Supabase: {e}")
        raise

# Global database client
try:
    db_client = get_supabase_client()
except Exception as e:
    logger.error(f"Failed to initialize database client: {e}")
    db_client = None

# ===================================================================
# MARKETING COMPONENT TOOLS
# ===================================================================

@mcp.tool()
async def get_marketing_sections(
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    variant: Optional[str] = None,
    limit: int = 20,
    include_analytics: bool = False
) -> Dict[str, Any]:
    """
    Get marketing sections with advanced filtering and analytics
    
    Args:
        category: Marketing category (Page Sections, Elements, Page Examples)
        subcategory: Specific subcategory (Hero Sections, CTA Sections, etc.)
        variant: Component variant (simple, gradient, with_image, etc.)
        limit: Maximum number of sections to return
        include_analytics: Include usage analytics and performance metrics
    
    Returns:
        List of marketing sections with metadata and optional analytics
    """
    try:
        # Check cache first
        cache_key = f"sections:{category}:{subcategory}:{variant}:{limit}"
        cached_result = marketing_cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Get connection from pool
        client = await connection_pool.get_connection()
        
        try:
            query = client.table('sections').select('*')
            
            # Filter by marketing categories
            marketing_categories = ['marketing', 'marketing-landing']
            query = query.in_('category', marketing_categories)
            
            # Apply additional filters
            if category:
                # Map category to database fields
                category_mapping = {
                    "Page Sections": ["hero", "feature", "cta", "pricing", "testimonial"],
                    "Elements": ["header", "banner", "feedback", "404"],
                    "Page Examples": ["landing", "pricing", "about"]
                }
                
                if category in category_mapping:
                    tags = category_mapping[category]
                    for tag in tags:
                        query = query.or_(f'name.ilike.%{tag}%,tags.cs.{{"{tag}"}}')
            
            if subcategory:
                query = query.ilike('name', f'%{subcategory}%')
            
            if variant:
                query = query.ilike('variant', f'%{variant}%')
            
            query = query.limit(limit)
            result = query.execute()
            
            sections = []
            for row in result.data:
                section = MarketingComponent(
                    id=row['id'],
                    name=row['name'],
                    category=MarketingCategory(row.get('category', 'hero_sections')),
                    variant=ComponentVariant(row.get('variant', 'simple')),
                    code=row.get('code', ''),
                    props=row.get('props', {}),
                    metadata=row.get('metadata', {})
                )
                
                # Add analytics if requested
                if include_analytics:
                    section.analytics = await get_section_analytics(section.id)
                
                sections.append(section.__dict__)
            
            response = {
                "success": True,
                "sections": sections,
                "count": len(sections),
                "category": category,
                "subcategory": subcategory,
                "variant": variant
            }
            
            # Cache the result
            marketing_cache.set(cache_key, response)
            
            return response
            
        finally:
            await connection_pool.release_connection(client)
        
    except Exception as e:
        logger.error(f"Failed to get marketing sections: {e}")
        return {
            "success": False,
            "error": str(e),
            "sections": []
        }

@mcp.tool()
async def build_landing_page(
    page_type: str,
    sections: List[str],
    output_directory: str,
    page_name: str = "landing",
    theme_id: Optional[str] = None,
    language: str = "en",
    enable_ab_testing: bool = False,
    seo_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Build a complete landing page with advanced features
    
    Args:
        page_type: Type of landing page (saas, product, service, event)
        sections: List of section types to include
        output_directory: Directory to create the landing page files
        page_name: Name for the landing page file
        theme_id: Custom theme ID to apply
        language: Target language for content
        enable_ab_testing: Enable A/B testing for sections
        seo_config: SEO configuration (title, description, keywords)
    
    Returns:
        Created landing page files with optimization report
    """
    try:
        # Get connection from pool
        client = await connection_pool.get_connection()
        
        try:
            # Get sections from database
            selected_sections = []
            for section_type in sections:
                query = client.table('sections').select('*')
                query = query.in_('category', ['marketing', 'marketing-landing'])
                query = query.ilike('name', f'%{section_type}%')
                query = query.limit(1)
                
                result = query.execute()
                if result.data:
                    section = MarketingComponent(
                        id=result.data[0]['id'],
                        name=result.data[0]['name'],
                        category=MarketingCategory(result.data[0].get('category', 'hero_sections')),
                        variant=ComponentVariant(result.data[0].get('variant', 'simple')),
                        code=result.data[0].get('code', ''),
                        props=result.data[0].get('props', {}),
                        metadata=result.data[0].get('metadata', {})
                    )
                    
                    # Translate if needed
                    if language != "en":
                        section = translation_manager.translate_component(section, language)
                    
                    selected_sections.append(section)
            
            # Create directory structure
            os.makedirs(output_directory, exist_ok=True)
            components_dir = os.path.join(output_directory, "components")
            os.makedirs(components_dir, exist_ok=True)
            
            # Apply theme if specified
            if theme_id:
                for section in selected_sections:
                    section.code = theme_engine.apply_theme_to_component(section, theme_id)
            
            # Generate component files
            created_files = []
            for section in selected_sections:
                # Optimize performance
                section.code = PerformanceOptimizer.optimize_images(section.code)
                
                # Write component file
                component_file = os.path.join(components_dir, f"{section.name.replace(' ', '')}.tsx")
                with open(component_file, 'w') as f:
                    f.write(section.code)
                created_files.append(component_file)
            
            # Generate landing page file
            landing_page_code = generate_landing_page_code(
                page_type, selected_sections, seo_config, enable_ab_testing
            )
            
            # Write landing page file
            landing_file = os.path.join(output_directory, f"{page_name}.tsx")
            with open(landing_file, 'w') as f:
                f.write(landing_page_code)
            created_files.append(landing_file)
            
            # Generate SEO files
            if seo_config:
                seo_files = generate_seo_files(output_directory, seo_config, selected_sections)
                created_files.extend(seo_files)
            
            # Create A/B testing configuration
            if enable_ab_testing:
                ab_config = create_ab_testing_config(selected_sections)
                ab_file = os.path.join(output_directory, "ab-testing.json")
                with open(ab_file, 'w') as f:
                    json.dump(ab_config, f, indent=2)
                created_files.append(ab_file)
            
            # Generate performance report
            performance_report = PerformanceOptimizer.optimize_bundle_size(selected_sections)
            
            return {
                "success": True,
                "message": f"Landing page created successfully",
                "files": created_files,
                "page_type": page_type,
                "sections_used": len(selected_sections),
                "language": language,
                "theme_applied": theme_id is not None,
                "ab_testing_enabled": enable_ab_testing,
                "performance_report": performance_report
            }
            
        finally:
            await connection_pool.release_connection(client)
        
    except Exception as e:
        logger.error(f"Failed to build landing page: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def generate_landing_page_code(page_type: str, sections: List[MarketingComponent], 
                              seo_config: Optional[Dict[str, Any]], 
                              enable_ab_testing: bool) -> str:
    """Generate React code for landing page with advanced features"""
    imports = [
        "import React from 'react';",
        "import { HelmetProvider, Helmet } from 'react-helmet-async';"
    ]
    
    if enable_ab_testing:
        imports.append("import { ABTestProvider } from './components/ABTestProvider';")
    
    components = []
    for section in sections:
        component_name = section.name.replace(' ', '').replace('-', '')
        imports.append(f"import {component_name} from './components/{component_name}';")
        components.append(f"      <{component_name} />")
    
    # Generate SEO meta tags
    meta_tags = []
    if seo_config:
        meta_tags = [
            f'<title>{seo_config.get("title", "")}</title>',
            f'<meta name="description" content="{seo_config.get("description", "")}" />',
            f'<meta name="keywords" content="{",".join(seo_config.get("keywords", []))}" />',
            f'<meta property="og:title" content="{seo_config.get("title", "")}" />',
            f'<meta property="og:description" content="{seo_config.get("description", "")}" />',
            '<meta property="og:type" content="website" />',
        ]
    
    page_code = f"""
{chr(10).join(imports)}

export default function {page_type.capitalize()}Landing() {{
  return (
    <HelmetProvider>
      <Helmet>
        {chr(10).join(meta_tags)}
      </Helmet>
      {'<ABTestProvider>' if enable_ab_testing else ''}
      <div className="min-h-screen bg-white">
{chr(10).join(components)}
      </div>
      {'</ABTestProvider>' if enable_ab_testing else ''}
    </HelmetProvider>
  );
}}
"""
    
    return page_code

def generate_seo_files(output_directory: str, seo_config: Dict[str, Any], 
                      sections: List[MarketingComponent]) -> List[str]:
    """Generate SEO-related files"""
    files = []
    
    # Generate sitemap
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{seo_config.get('url', 'https://example.com')}</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""
    sitemap_file = os.path.join(output_directory, "sitemap.xml")
    with open(sitemap_file, 'w') as f:
        f.write(sitemap)
    files.append(sitemap_file)
    
    # Generate robots.txt
    robots = f"""User-agent: *
Allow: /
Sitemap: {seo_config.get('url', 'https://example.com')}/sitemap.xml
"""
    robots_file = os.path.join(output_directory, "robots.txt")
    with open(robots_file, 'w') as f:
        f.write(robots)
    files.append(robots_file)
    
    return files

def create_ab_testing_config(sections: List[MarketingComponent]) -> Dict[str, Any]:
    """Create A/B testing configuration"""
    tests = []
    
    for section in sections:
        if section.category in [MarketingCategory.HERO_SECTIONS, MarketingCategory.CTA_SECTIONS]:
            # Create test variants
            variants = [
                {
                    'name': 'Control',
                    'props': section.props
                },
                {
                    'name': 'Variant A',
                    'props': {
                        **section.props,
                        'buttonText': 'Get Started Now',
                        'buttonColor': 'primary'
                    }
                }
            ]
            
            test_id = ab_testing.create_test(
                section.id,
                variants,
                [0.5, 0.5]  # 50/50 split
            )
            
            tests.append({
                'test_id': test_id,
                'component_id': section.id,
                'variants': variants
            })
    
    return {
        'tests': tests,
        'tracking_enabled': True,
        'conversion_goals': ['signup', 'demo_request', 'purchase']
    }

async def get_section_analytics(section_id: str) -> Dict[str, Any]:
    """Get analytics data for a section"""
    # Simulate analytics data
    return {
        'views': 10000,
        'clicks': 500,
        'conversions': 50,
        'conversion_rate': 0.05,
        'average_time_on_section': 45,
        'bounce_rate': 0.3
    }

@mcp.tool()
async def search_marketing_components(
    query: str,
    limit: int = 10,
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Advanced search for marketing components with filtering
    
    Args:
        query: Search query
        limit: Maximum results to return
        filters: Additional filters (category, variant, performance metrics)
    
    Returns:
        Matching marketing components with relevance scores
    """
    try:
        # Get connection from pool
        client = await connection_pool.get_connection()
        
        try:
            # Build search query
            search_query = client.table('sections').select('*')
            search_query = search_query.in_('category', ['marketing', 'marketing-landing'])
            
            # Full-text search
            search_query = search_query.or_(
                f'name.ilike.%{query}%,'
                f'description.ilike.%{query}%,'
                f'tags.cs.{{"{query}"}}'
            )
            
            # Apply filters
            if filters:
                if 'category' in filters:
                    search_query = search_query.eq('category', filters['category'])
                if 'variant' in filters:
                    search_query = search_query.eq('variant', filters['variant'])
                if 'min_conversion_rate' in filters:
                    # This would require analytics data
                    pass
            
            search_query = search_query.limit(limit)
            result = search_query.execute()
            
            # Calculate relevance scores
            components = []
            for row in result.data:
                relevance = calculate_relevance_score(row, query)
                component = {
                    **row,
                    'relevance_score': relevance
                }
                components.append(component)
            
            # Sort by relevance
            components.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            return {
                "success": True,
                "components": components,
                "count": len(components),
                "query": query,
                "filters": filters
            }
            
        finally:
            await connection_pool.release_connection(client)
        
    except Exception as e:
        logger.error(f"Failed to search marketing components: {e}")
        return {
            "success": False,
            "error": str(e),
            "components": []
        }

def calculate_relevance_score(component: Dict[str, Any], query: str) -> float:
    """Calculate relevance score for search results"""
    score = 0.0
    query_lower = query.lower()
    
    # Name match (highest weight)
    if query_lower in component.get('name', '').lower():
        score += 1.0
    
    # Description match
    if query_lower in component.get('description', '').lower():
        score += 0.5
    
    # Tag match
    tags = component.get('tags', [])
    if isinstance(tags, list) and any(query_lower in tag.lower() for tag in tags):
        score += 0.3
    
    # Boost popular components
    usage_count = component.get('usage_count', 0)
    if usage_count > 100:
        score += 0.2
    
    return score

@mcp.tool()
async def get_marketing_taxonomy() -> Dict[str, Any]:
    """
    Get the complete marketing taxonomy structure with usage statistics
    
    Returns:
        Marketing taxonomy with categories, subcategories, and usage data
    """
    try:
        taxonomy = load_marketing_taxonomy()
        if not taxonomy:
            return {"success": False, "error": "Failed to load marketing taxonomy"}
        
        # Enhance with usage statistics
        enhanced_taxonomy = taxonomy.copy()
        
        # Get connection from pool
        client = await connection_pool.get_connection()
        
        try:
            # Get usage statistics for each category
            for category_name, category_data in enhanced_taxonomy['taxonomy'].items():
                if 'subcategories' in category_data:
                    for subcat_name, subcat_items in category_data['subcategories'].items():
                        # Count components in each subcategory
                        count_query = client.table('sections').select('*', count='exact')
                        count_query = count_query.in_('category', ['marketing', 'marketing-landing'])
                        count_query = count_query.ilike('name', f'%{subcat_name}%')
                        result = count_query.execute()
                        
                        # Add count to taxonomy
                        enhanced_taxonomy['taxonomy'][category_name]['subcategories'][subcat_name] = {
                            'items': subcat_items,
                            'count': result.count if hasattr(result, 'count') else 0
                        }
            
            # Add overall statistics
            total_query = client.table('sections').select('*', count='exact')
            total_query = total_query.in_('category', ['marketing', 'marketing-landing'])
            total_result = total_query.execute()
            
            enhanced_taxonomy['statistics'] = {
                'total_components': total_result.count if hasattr(total_result, 'count') else 0,
                'categories': len(enhanced_taxonomy['taxonomy']),
                'last_updated': datetime.now(timezone.utc).isoformat()
            }
            
            return {
                "success": True,
                "taxonomy": enhanced_taxonomy
            }
            
        finally:
            await connection_pool.release_connection(client)
        
    except Exception as e:
        logger.error(f"Failed to get marketing taxonomy: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def create_hero_section(
    variant: str = "centered",
    content: Dict[str, str] = None,
    theme_id: Optional[str] = None,
    optimize_for_conversion: bool = True
) -> Dict[str, Any]:
    """
    Create a hero section with specific variant and optimization
    
    Args:
        variant: Hero variant (centered, split, with_image, with_video, gradient)
        content: Content for the hero (title, subtitle, cta_text, etc.)
        theme_id: Custom theme to apply
        optimize_for_conversion: Apply conversion optimization techniques
    
    Returns:
        Generated hero section code with optimization recommendations
    """
    try:
        # Default content
        if not content:
            content = {
                'title': 'Welcome to Our Platform',
                'subtitle': 'Build amazing experiences with our tools',
                'cta_text': 'Get Started',
                'cta_href': '#signup'
            }
        
        # Get hero template based on variant
        hero_code = generate_hero_section(variant, content)
        
        # Apply theme if specified
        if theme_id:
            hero_code = theme_engine.apply_theme_to_component(
                MarketingComponent(
                    id=f"hero_{variant}",
                    name=f"Hero {variant}",
                    category=MarketingCategory.HERO_SECTIONS,
                    variant=ComponentVariant(variant),
                    code=hero_code,
                    props=content,
                    metadata={}
                ),
                theme_id
            )
        
        # Apply conversion optimization
        if optimize_for_conversion:
            optimizations = apply_conversion_optimizations(hero_code, ConversionOptimizationType.ABOVE_FOLD)
            hero_code = optimizations['optimized_code']
        
        # Generate critical CSS
        critical_css = PerformanceOptimizer.generate_critical_css(
            MarketingComponent(
                id=f"hero_{variant}",
                name=f"Hero {variant}",
                category=MarketingCategory.HERO_SECTIONS,
                variant=ComponentVariant(variant),
                code=hero_code,
                props=content,
                metadata={}
            )
        )
        
        return {
            "success": True,
            "code": hero_code,
            "critical_css": critical_css,
            "variant": variant,
            "optimizations_applied": optimize_for_conversion,
            "content": content
        }
        
    except Exception as e:
        logger.error(f"Failed to create hero section: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def generate_hero_section(variant: str, content: Dict[str, str]) -> str:
    """Generate hero section code based on variant"""
    if variant == "centered":
        return f"""
import React from 'react';

export default function HeroCentered() {{
  return (
    <div className="relative isolate px-6 pt-14 lg:px-8">
      <div className="mx-auto max-w-2xl py-32 sm:py-48 lg:py-56">
        <div className="text-center">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            {content.get('title', '')}
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            {content.get('subtitle', '')}
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <a
              href="{content.get('cta_href', '#')}"
              className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              {content.get('cta_text', 'Get Started')}
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}}
"""
    elif variant == "split":
        return f"""
import React from 'react';

export default function HeroSplit() {{
  return (
    <div className="relative isolate overflow-hidden bg-white">
      <div className="mx-auto max-w-7xl px-6 pb-24 pt-10 sm:pb-32 lg:flex lg:px-8 lg:py-40">
        <div className="mx-auto max-w-2xl lg:mx-0 lg:max-w-xl lg:flex-shrink-0 lg:pt-8">
          <h1 className="mt-10 text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            {content.get('title', '')}
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            {content.get('subtitle', '')}
          </p>
          <div className="mt-10 flex items-center gap-x-6">
            <a
              href="{content.get('cta_href', '#')}"
              className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              {content.get('cta_text', 'Get Started')}
            </a>
          </div>
        </div>
        <div className="mx-auto mt-16 flex max-w-2xl sm:mt-24 lg:ml-10 lg:mr-0 lg:mt-0 lg:max-w-none lg:flex-none xl:ml-32">
          <div className="max-w-3xl flex-none sm:max-w-5xl lg:max-w-none">
            <img
              src="{content.get('image_url', 'https://via.placeholder.com/800x600')}"
              alt="Hero image"
              className="w-[76rem] rounded-md bg-white/5 shadow-2xl ring-1 ring-white/10"
              loading="lazy"
            />
          </div>
        </div>
      </div>
    </div>
  );
}}
"""
    
    # Default to centered if variant not found
    return generate_hero_section("centered", content)

def apply_conversion_optimizations(code: str, optimization_type: ConversionOptimizationType) -> Dict[str, Any]:
    """Apply conversion optimization techniques to component code"""
    optimized_code = code
    optimizations_applied = []
    
    if optimization_type == ConversionOptimizationType.ABOVE_FOLD:
        # Ensure CTA is prominent
        optimized_code = optimized_code.replace(
            'className="rounded-md bg-indigo-600',
            'className="rounded-md bg-indigo-600 transform hover:scale-105 transition-transform'
        )
        optimizations_applied.append("Enhanced CTA button with hover effects")
        
        # Add urgency messaging
        optimized_code = optimized_code.replace(
            '{content.get(\'cta_text\', \'Get Started\')}',
            '{content.get(\'cta_text\', \'Get Started\')} →'
        )
        optimizations_applied.append("Added directional cue to CTA")
    
    elif optimization_type == ConversionOptimizationType.SOCIAL_PROOF:
        # Add social proof elements
        social_proof = """
        <div className="mt-6 flex items-center justify-center gap-x-4">
          <div className="flex -space-x-2">
            {[1,2,3,4,5].map(i => (
              <img
                key={i}
                className="inline-block h-8 w-8 rounded-full ring-2 ring-white"
                src={`https://ui-avatars.com/api/?name=User${i}&background=random`}
                alt=""
              />
            ))}
          </div>
          <p className="text-sm text-gray-600">
            Join 10,000+ satisfied customers
          </p>
        </div>
        """
        optimized_code = optimized_code.replace('</div>\n      </div>\n    </div>', 
                                              f'{social_proof}\n        </div>\n      </div>\n    </div>')
        optimizations_applied.append("Added social proof with customer avatars")
    
    return {
        'optimized_code': optimized_code,
        'optimizations_applied': optimizations_applied
    }

@mcp.tool()
async def build_pricing_table(
    tiers: List[Dict[str, Any]],
    billing_period: str = "monthly",
    highlight_tier: Optional[int] = None,
    enable_toggle: bool = True,
    theme_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Build a pricing table with comparison features
    
    Args:
        tiers: List of pricing tiers with features
        billing_period: monthly or yearly
        highlight_tier: Index of tier to highlight as recommended
        enable_toggle: Enable monthly/yearly toggle
        theme_id: Custom theme to apply
    
    Returns:
        Generated pricing table code
    """
    try:
        # Generate pricing table code
        pricing_code = generate_pricing_table(tiers, billing_period, highlight_tier, enable_toggle)
        
        # Apply theme if specified
        if theme_id:
            pricing_component = MarketingComponent(
                id="pricing_table",
                name="Pricing Table",
                category=MarketingCategory.PRICING_SECTIONS,
                variant=ComponentVariant.COMPARISON,
                code=pricing_code,
                props={'tiers': tiers},
                metadata={}
            )
            pricing_code = theme_engine.apply_theme_to_component(pricing_component, theme_id)
        
        # Add conversion tracking
        pricing_code = add_conversion_tracking(pricing_code, "pricing_tier_selected")
        
        return {
            "success": True,
            "code": pricing_code,
            "tiers_count": len(tiers),
            "highlighted_tier": highlight_tier,
            "billing_toggle_enabled": enable_toggle
        }
        
    except Exception as e:
        logger.error(f"Failed to build pricing table: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def generate_pricing_table(tiers: List[Dict[str, Any]], billing_period: str, 
                         highlight_tier: Optional[int], enable_toggle: bool) -> str:
    """Generate pricing table component code"""
    return f"""
import React, {{ useState }} from 'react';

export default function PricingTable() {{
  const [billingPeriod, setBillingPeriod] = useState('{billing_period}');
  
  const tiers = {json.dumps(tiers)};
  
  return (
    <div className="bg-white py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="text-base font-semibold leading-7 text-indigo-600">Pricing</h2>
          <p className="mt-2 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
            Choose the perfect plan for your needs
          </p>
        </div>
        
        {enable_toggle and f'''
        <div className="mt-16 flex justify-center">
          <div className="grid grid-cols-2 gap-x-1 rounded-full p-1 text-center text-xs font-semibold leading-5 ring-1 ring-inset ring-gray-200">
            <button
              onClick={{() => setBillingPeriod('monthly')}}
              className={{billingPeriod === 'monthly' ? 'bg-indigo-600 text-white' : 'text-gray-500'}}
            >
              Monthly
            </button>
            <button
              onClick={{() => setBillingPeriod('yearly')}}
              className={{billingPeriod === 'yearly' ? 'bg-indigo-600 text-white' : 'text-gray-500'}}
            >
              Yearly
            </button>
          </div>
        </div>
        ''' or ''}
        
        <div className="isolate mx-auto mt-10 grid max-w-md grid-cols-1 gap-8 lg:mx-0 lg:max-w-none lg:grid-cols-3">
          {{tiers.map((tier, tierIdx) => (
            <div
              key={{tier.id}}
              className={{tierIdx === {highlight_tier or -1} ? 'ring-2 ring-indigo-600' : 'ring-1 ring-gray-200'}}
            >
              <div className="p-8">
                <h3 className="text-lg font-semibold leading-8 text-gray-900">{{tier.name}}</h3>
                <p className="mt-4 text-sm leading-6 text-gray-600">{{tier.description}}</p>
                <p className="mt-6 flex items-baseline gap-x-1">
                  <span className="text-4xl font-bold tracking-tight text-gray-900">
                    {{billingPeriod === 'monthly' ? tier.price.monthly : tier.price.yearly}}
                  </span>
                  <span className="text-sm font-semibold leading-6 text-gray-600">
                    /{{billingPeriod === 'monthly' ? 'month' : 'year'}}
                  </span>
                </p>
                <button
                  className="mt-6 block w-full rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500"
                  onClick={{() => window.trackConversion('pricing_tier_selected', {{ tier: tier.name }})}}
                >
                  Get started
                </button>
                <ul className="mt-8 space-y-3 text-sm leading-6 text-gray-600">
                  {{tier.features.map((feature) => (
                    <li key={{feature}} className="flex gap-x-3">
                      <svg className="h-6 w-5 flex-none text-indigo-600" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clipRule="evenodd" />
                      </svg>
                      {{feature}}
                    </li>
                  ))}}
                </ul>
              </div>
            </div>
          ))}}
        </div>
      </div>
    </div>
  );
}}
"""

def add_conversion_tracking(code: str, event_name: str) -> str:
    """Add conversion tracking to component code"""
    tracking_script = f"""
// Add conversion tracking
window.trackConversion = window.trackConversion || function(event, data) {{
  // Send to analytics platforms
  if (typeof gtag !== 'undefined') {{
    gtag('event', event, data);
  }}
  if (typeof analytics !== 'undefined') {{
    analytics.track(event, data);
  }}
  // Internal tracking
  fetch('/api/track', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify({{ event, data, timestamp: new Date().toISOString() }})
  }});
}};

"""
    
    # Insert tracking script at the beginning of the component
    return code.replace("export default function", f"{tracking_script}\nexport default function")

@mcp.tool()
async def generate_testimonials(
    layout: str = "grid",
    count: int = 3,
    include_ratings: bool = True,
    include_images: bool = True,
    theme_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate testimonial section with various layouts
    
    Args:
        layout: Layout type (grid, carousel, single, featured)
        count: Number of testimonials to include
        include_ratings: Include star ratings
        include_images: Include customer images
        theme_id: Custom theme to apply
    
    Returns:
        Generated testimonial section code
    """
    try:
        # Generate sample testimonials
        testimonials = generate_sample_testimonials(count, include_ratings, include_images)
        
        # Generate testimonial code based on layout
        testimonial_code = generate_testimonial_section(layout, testimonials)
        
        # Apply theme if specified
        if theme_id:
            testimonial_component = MarketingComponent(
                id=f"testimonials_{layout}",
                name=f"Testimonials {layout}",
                category=MarketingCategory.TESTIMONIALS,
                variant=ComponentVariant(layout),
                code=testimonial_code,
                props={'testimonials': testimonials},
                metadata={}
            )
            testimonial_code = theme_engine.apply_theme_to_component(testimonial_component, theme_id)
        
        # Add social proof optimization
        optimizations = apply_conversion_optimizations(
            testimonial_code, 
            ConversionOptimizationType.SOCIAL_PROOF
        )
        
        return {
            "success": True,
            "code": optimizations['optimized_code'],
            "layout": layout,
            "testimonial_count": count,
            "optimizations": optimizations['optimizations_applied']
        }
        
    except Exception as e:
        logger.error(f"Failed to generate testimonials: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def generate_sample_testimonials(count: int, include_ratings: bool, 
                               include_images: bool) -> List[Dict[str, Any]]:
    """Generate sample testimonial data"""
    testimonials = []
    
    sample_quotes = [
        "This product has completely transformed our business operations.",
        "The best investment we've made for our team's productivity.",
        "Outstanding customer support and an incredible product.",
        "We've seen a 300% increase in efficiency since implementing this solution.",
        "I can't imagine running our business without this tool."
    ]
    
    sample_names = ["Sarah Johnson", "Michael Chen", "Emily Rodriguez", "David Kim", "Lisa Thompson"]
    sample_roles = ["CEO", "CTO", "VP of Marketing", "Product Manager", "Operations Director"]
    sample_companies = ["TechCorp", "InnovateCo", "GrowthLabs", "FutureScale", "DigitalEdge"]
    
    for i in range(min(count, len(sample_quotes))):
        testimonial = {
            'id': f'testimonial_{i}',
            'quote': sample_quotes[i],
            'author': {
                'name': sample_names[i],
                'role': sample_roles[i],
                'company': sample_companies[i]
            }
        }
        
        if include_ratings:
            testimonial['rating'] = 5
        
        if include_images:
            testimonial['author']['image'] = f'https://ui-avatars.com/api/?name={sample_names[i].replace(" ", "+")}&background=random'
        
        testimonials.append(testimonial)
    
    return testimonials

def generate_testimonial_section(layout: str, testimonials: List[Dict[str, Any]]) -> str:
    """Generate testimonial section code based on layout"""
    if layout == "grid":
        return f"""
import React from 'react';

export default function TestimonialsGrid() {{
  const testimonials = {json.dumps(testimonials)};
  
  return (
    <section className="bg-white py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-xl text-center">
          <h2 className="text-lg font-semibold leading-8 tracking-tight text-indigo-600">
            Testimonials
          </h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Hear from our satisfied customers
          </p>
        </div>
        <div className="mx-auto mt-16 flow-root max-w-2xl sm:mt-20 lg:mx-0 lg:max-w-none">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {{testimonials.map((testimonial) => (
              <div key={{testimonial.id}} className="rounded-2xl bg-gray-50 p-8">
                {{testimonial.rating && (
                  <div className="flex gap-x-1">
                    {{[...Array(5)].map((_, i) => (
                      <svg
                        key={{i}}
                        className="h-5 w-5 text-yellow-400"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                    ))}}
                  </div>
                )}}
                <blockquote className="mt-4 text-lg font-semibold leading-8 text-gray-900">
                  "{{testimonial.quote}}"
                </blockquote>
                <figcaption className="mt-6 flex items-center gap-x-4">
                  {{testimonial.author.image && (
                    <img
                      className="h-12 w-12 rounded-full bg-gray-50"
                      src={{testimonial.author.image}}
                      alt={{testimonial.author.name}}
                    />
                  )}}
                  <div>
                    <div className="font-semibold text-gray-900">{{testimonial.author.name}}</div>
                    <div className="text-gray-600">{{testimonial.author.role}}, {{testimonial.author.company}}</div>
                  </div>
                </figcaption>
              </div>
            ))}}
          </div>
        </div>
      </div>
    </section>
  );
}}
"""
    
    # Default to grid layout
    return generate_testimonial_section("grid", testimonials)

@mcp.tool()
async def create_cta_section(
    style: str = "centered",
    content: Dict[str, str] = None,
    enable_urgency: bool = False,
    theme_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a call-to-action section
    
    Args:
        style: CTA style (centered, split, banner, with_form)
        content: CTA content (title, description, button_text)
        enable_urgency: Add urgency messaging
        theme_id: Custom theme to apply
    
    Returns:
        Generated CTA section code
    """
    try:
        # Default content
        if not content:
            content = {
                'title': 'Ready to get started?',
                'description': 'Start your free trial today and see the difference.',
                'button_text': 'Start Free Trial',
                'button_href': '#signup'
            }
        
        # Add urgency if enabled
        if enable_urgency:
            content['urgency_text'] = 'Limited time offer - 50% off for the next 24 hours!'
        
        # Generate CTA code
        cta_code = generate_cta_section(style, content)
        
        # Apply theme if specified
        if theme_id:
            cta_component = MarketingComponent(
                id=f"cta_{style}",
                name=f"CTA {style}",
                category=MarketingCategory.CTA_SECTIONS,
                variant=ComponentVariant(style),
                code=cta_code,
                props=content,
                metadata={}
            )
            cta_code = theme_engine.apply_theme_to_component(cta_component, theme_id)
        
        # Apply conversion optimizations
        optimizations = apply_conversion_optimizations(
            cta_code,
            ConversionOptimizationType.CLEAR_CTA if not enable_urgency else ConversionOptimizationType.URGENCY
        )
        
        return {
            "success": True,
            "code": optimizations['optimized_code'],
            "style": style,
            "urgency_enabled": enable_urgency,
            "optimizations": optimizations['optimizations_applied']
        }
        
    except Exception as e:
        logger.error(f"Failed to create CTA section: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def generate_cta_section(style: str, content: Dict[str, str]) -> str:
    """Generate CTA section code based on style"""
    if style == "centered":
        return f"""
import React from 'react';

export default function CTACentered() {{
  return (
    <div className="bg-indigo-600">
      <div className="px-6 py-24 sm:px-6 sm:py-32 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            {content.get('title', '')}
          </h2>
          <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-indigo-200">
            {content.get('description', '')}
          </p>
          {content.get('urgency_text') and f'''
          <p className="mt-4 text-sm font-semibold text-yellow-300">
            {content.get('urgency_text')}
          </p>
          ''' or ''}
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <a
              href="{content.get('button_href', '#')}"
              className="rounded-md bg-white px-3.5 py-2.5 text-sm font-semibold text-indigo-600 shadow-sm hover:bg-indigo-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
            >
              {content.get('button_text', 'Get Started')}
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}}
"""
    
    # Default to centered
    return generate_cta_section("centered", content)

@mcp.tool()
async def build_newsletter_signup(
    layout: str = "simple",
    include_social_proof: bool = True,
    include_privacy_notice: bool = True,
    theme_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Build a newsletter signup section
    
    Args:
        layout: Layout type (simple, with_image, inline, popup)
        include_social_proof: Add subscriber count
        include_privacy_notice: Add privacy policy notice
        theme_id: Custom theme to apply
    
    Returns:
        Generated newsletter signup code
    """
    try:
        # Generate newsletter code
        newsletter_code = generate_newsletter_section(
            layout, 
            include_social_proof, 
            include_privacy_notice
        )
        
        # Apply theme if specified
        if theme_id:
            newsletter_component = MarketingComponent(
                id=f"newsletter_{layout}",
                name=f"Newsletter {layout}",
                category=MarketingCategory.NEWSLETTER_SECTIONS,
                variant=ComponentVariant(layout),
                code=newsletter_code,
                props={},
                metadata={}
            )
            newsletter_code = theme_engine.apply_theme_to_component(newsletter_component, theme_id)
        
        # Add email validation
        newsletter_code = add_email_validation(newsletter_code)
        
        # Add integration code
        newsletter_code = add_newsletter_integration(newsletter_code)
        
        return {
            "success": True,
            "code": newsletter_code,
            "layout": layout,
            "features": {
                "social_proof": include_social_proof,
                "privacy_notice": include_privacy_notice,
                "email_validation": True,
                "integration_ready": True
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to build newsletter signup: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def generate_newsletter_section(layout: str, include_social_proof: bool, 
                              include_privacy_notice: bool) -> str:
    """Generate newsletter signup section code"""
    return f"""
import React, {{ useState }} from 'react';

export default function NewsletterSignup() {{
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState('');
  
  const handleSubmit = async (e) => {{
    e.preventDefault();
    
    // Validate email
    if (!validateEmail(email)) {{
      setStatus('Please enter a valid email address');
      return;
    }}
    
    // Submit to newsletter service
    try {{
      const response = await fetch('/api/newsletter/subscribe', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ email }})
      }});
      
      if (response.ok) {{
        setStatus('Success! Check your email to confirm.');
        setEmail('');
        
        // Track conversion
        window.trackConversion('newsletter_signup', {{ email }});
      }} else {{
        setStatus('Something went wrong. Please try again.');
      }}
    }} catch (error) {{
      setStatus('Something went wrong. Please try again.');
    }}
  }};
  
  const validateEmail = (email) => {{
    return /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email);
  }};
  
  return (
    <div className="bg-white py-16 sm:py-24">
      <div className="mx-auto max-w-7xl sm:px-6 lg:px-8">
        <div className="relative isolate overflow-hidden bg-gray-900 px-6 py-24 shadow-2xl sm:rounded-3xl sm:px-24 xl:py-32">
          <h2 className="mx-auto max-w-2xl text-center text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Get our latest updates
          </h2>
          <p className="mx-auto mt-2 max-w-xl text-center text-lg leading-8 text-gray-300">
            Stay informed about new features and updates.
          </p>
          
          {include_social_proof and f'''
          <p className="mx-auto mt-4 text-center text-sm text-gray-400">
            Join 50,000+ subscribers who get our newsletter
          </p>
          ''' or ''}
          
          <form onSubmit={{handleSubmit}} className="mx-auto mt-10 flex max-w-md gap-x-4">
            <label htmlFor="email-address" className="sr-only">
              Email address
            </label>
            <input
              id="email-address"
              name="email"
              type="email"
              autoComplete="email"
              required
              className="min-w-0 flex-auto rounded-md border-0 bg-white/5 px-3.5 py-2 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-white sm:text-sm sm:leading-6"
              placeholder="Enter your email"
              value={{email}}
              onChange={{(e) => setEmail(e.target.value)}}
            />
            <button
              type="submit"
              className="flex-none rounded-md bg-white px-3.5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm hover:bg-gray-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
            >
              Subscribe
            </button>
          </form>
          
          {{status && (
            <p className="mx-auto mt-4 text-center text-sm text-white">
              {{status}}
            </p>
          )}}
          
          {include_privacy_notice and f'''
          <p className="mx-auto mt-6 max-w-xl text-center text-xs leading-5 text-gray-400">
            We care about your data. Read our{' '}
            <a href="/privacy" className="font-semibold text-white hover:text-gray-300">
              privacy policy
            </a>
            .
          </p>
          ''' or ''}
        </div>
      </div>
    </div>
  );
}}
"""

def add_email_validation(code: str) -> str:
    """Add email validation to newsletter code"""
    # Email validation is already included in the generated code
    return code

def add_newsletter_integration(code: str) -> str:
    """Add newsletter service integration code"""
    integration_comment = """
// Newsletter service integrations
// Mailchimp: Use @mailchimp/mailchimp_marketing
// ConvertKit: Use convertkit-react
// SendGrid: Use @sendgrid/mail
// Custom: Implement /api/newsletter/subscribe endpoint
"""
    
    return code.replace("import React", f"{integration_comment}\nimport React")

@mcp.tool()
async def create_footer(
    sections: List[str] = None,
    include_newsletter: bool = True,
    include_social: bool = True,
    theme_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a footer section
    
    Args:
        sections: Footer sections to include (company, products, resources, legal)
        include_newsletter: Include newsletter signup
        include_social: Include social media links
        theme_id: Custom theme to apply
    
    Returns:
        Generated footer code
    """
    try:
        # Default sections
        if not sections:
            sections = ['company', 'products', 'resources', 'legal']
        
        # Generate footer code
        footer_code = generate_footer_section(sections, include_newsletter, include_social)
        
        # Apply theme if specified
        if theme_id:
            footer_component = MarketingComponent(
                id="footer",
                name="Footer",
                category=MarketingCategory.FOOTERS,
                variant=ComponentVariant.SIMPLE,
                code=footer_code,
                props={},
                metadata={}
            )
            footer_code = theme_engine.apply_theme_to_component(footer_component, theme_id)
        
        return {
            "success": True,
            "code": footer_code,
            "sections": sections,
            "features": {
                "newsletter": include_newsletter,
                "social_links": include_social
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to create footer: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def generate_footer_section(sections: List[str], include_newsletter: bool, 
                          include_social: bool) -> str:
    """Generate footer section code"""
    footer_links = {
        'company': ['About', 'Careers', 'Partners', 'News'],
        'products': ['Features', 'Pricing', 'Security', 'Roadmap'],
        'resources': ['Documentation', 'Guides', 'Help Center', 'API Reference'],
        'legal': ['Privacy', 'Terms', 'Cookie Policy', 'Licenses']
    }
    
    return f"""
import React from 'react';

export default function Footer() {{
  const navigation = {json.dumps({k: v for k, v in footer_links.items() if k in sections})};
  
  return (
    <footer className="bg-gray-900" aria-labelledby="footer-heading">
      <h2 id="footer-heading" className="sr-only">
        Footer
      </h2>
      <div className="mx-auto max-w-7xl px-6 pb-8 pt-16 sm:pt-24 lg:px-8 lg:pt-32">
        <div className="xl:grid xl:grid-cols-3 xl:gap-8">
          <div className="space-y-8">
            <img
              className="h-10"
              src="/logo.svg"
              alt="Company name"
            />
            <p className="text-sm leading-6 text-gray-300">
              Making the world a better place through innovative technology.
            </p>
            {include_social and f'''
            <div className="flex space-x-6">
              {{['facebook', 'twitter', 'github', 'linkedin'].map((item) => (
                <a key={{item}} href="#" className="text-gray-400 hover:text-gray-300">
                  <span className="sr-only">{{item}}</span>
                  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" />
                  </svg>
                </a>
              ))}}
            </div>
            ''' or ''}
          </div>
          <div className="mt-16 grid grid-cols-2 gap-8 xl:col-span-2 xl:mt-0">
            <div className="md:grid md:grid-cols-2 md:gap-8">
              {{Object.entries(navigation).slice(0, 2).map(([category, items]) => (
                <div key={{category}}>
                  <h3 className="text-sm font-semibold leading-6 text-white capitalize">
                    {{category}}
                  </h3>
                  <ul role="list" className="mt-6 space-y-4">
                    {{items.map((item) => (
                      <li key={{item}}>
                        <a href="#" className="text-sm leading-6 text-gray-300 hover:text-white">
                          {{item}}
                        </a>
                      </li>
                    ))}}
                  </ul>
                </div>
              ))}}
            </div>
            <div className="md:grid md:grid-cols-2 md:gap-8">
              {{Object.entries(navigation).slice(2, 4).map(([category, items]) => (
                <div key={{category}}>
                  <h3 className="text-sm font-semibold leading-6 text-white capitalize">
                    {{category}}
                  </h3>
                  <ul role="list" className="mt-6 space-y-4">
                    {{items.map((item) => (
                      <li key={{item}}>
                        <a href="#" className="text-sm leading-6 text-gray-300 hover:text-white">
                          {{item}}
                        </a>
                      </li>
                    ))}}
                  </ul>
                </div>
              ))}}
            </div>
          </div>
        </div>
        {include_newsletter and f'''
        <div className="mt-16 border-t border-white/10 pt-8 sm:mt-20 lg:mt-24">
          <h3 className="text-sm font-semibold leading-6 text-white">
            Subscribe to our newsletter
          </h3>
          <p className="mt-2 text-sm leading-6 text-gray-300">
            The latest news, articles, and resources, sent to your inbox weekly.
          </p>
          <form className="mt-6 sm:flex sm:max-w-md">
            <label htmlFor="email-address" className="sr-only">
              Email address
            </label>
            <input
              type="email"
              name="email-address"
              id="email-address"
              autoComplete="email"
              required
              className="w-full min-w-0 appearance-none rounded-md border-0 bg-white/5 px-3 py-1.5 text-base text-white shadow-sm ring-1 ring-inset ring-white/10 placeholder:text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:w-64 sm:text-sm sm:leading-6 xl:w-full"
              placeholder="Enter your email"
            />
            <div className="mt-4 sm:ml-4 sm:mt-0 sm:flex-shrink-0">
              <button
                type="submit"
                className="flex w-full items-center justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Subscribe
              </button>
            </div>
          </form>
        </div>
        ''' or ''}
        <div className="mt-8 border-t border-white/10 pt-8">
          <p className="text-xs leading-5 text-gray-400">
            &copy; {{new Date().getFullYear()}} Your Company, Inc. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}}
"""

@mcp.tool()
async def health_check() -> Dict[str, Any]:
    """
    Check health status of Marketing MCP server with comprehensive diagnostics
    
    Returns:
        Server health status, component count, and performance metrics
    """
    try:
        health_data = {
            "success": True,
            "server": "figma-marketing",
            "version": "2.0.0",
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Database health
        if db_client:
            try:
                # Count marketing sections
                result = db_client.table('sections').select('*', count='exact')\
                    .in_('category', ['marketing', 'marketing-landing'])\
                    .execute()
                
                health_data['database'] = {
                    'connected': True,
                    'marketing_sections': result.count if hasattr(result, 'count') else 0
                }
            except Exception as e:
                health_data['database'] = {
                    'connected': False,
                    'error': str(e)
                }
        else:
            health_data['database'] = {
                'connected': False,
                'error': 'No database client initialized'
            }
        
        # Cache health
        health_data['cache'] = marketing_cache.get_stats()
        
        # Taxonomy health
        health_data['taxonomy'] = {
            'loaded': load_marketing_taxonomy() is not None
        }
        
        # A/B testing health
        health_data['ab_testing'] = {
            'active_tests': len(ab_testing.active_tests),
            'completed_tests': len(ab_testing.test_results)
        }
        
        # Integration health
        health_data['integrations'] = {
            'available': list(integration_manager.integrations.keys()),
            'count': len(integration_manager.integrations)
        }
        
        # Performance metrics
        health_data['performance'] = {
            'cache_hit_rate': health_data['cache']['hit_rate'],
            'supported_languages': len(translation_manager.supported_languages),
            'themes_available': len(theme_engine.themes) + 1  # +1 for default
        }
        
        return health_data
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "success": False,
            "server": "figma-marketing",
            "status": "unhealthy",
            "error": str(e)
        }

# ===================================================================
# MCP RESOURCES
# ===================================================================

@mcp.resource("figma-marketing://taxonomy")
def get_marketing_taxonomy_resource() -> str:
    """MCP Resource: Get marketing taxonomy structure"""
    try:
        taxonomy = load_marketing_taxonomy()
        return json.dumps(taxonomy, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.resource("figma-marketing://sections/{category}")
def get_marketing_sections_resource(category: str) -> str:
    """MCP Resource: Get marketing sections by category"""
    try:
        if not db_client:
            return json.dumps({"error": "Database not connected"}, indent=2)
            
        result = db_client.table('sections').select('*')\
            .in_('category', ['marketing', 'marketing-landing'])\
            .ilike('name', f'%{category}%')\
            .execute()
        
        return json.dumps({
            "category": category,
            "sections": result.data,
            "count": len(result.data)
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.resource("figma-marketing://analytics/{component_id}")
def get_component_analytics_resource(component_id: str) -> str:
    """MCP Resource: Get analytics for specific component"""
    try:
        # In production, this would fetch real analytics
        analytics = {
            "component_id": component_id,
            "metrics": {
                "views": 10000,
                "clicks": 500,
                "conversions": 50,
                "conversion_rate": 0.05,
                "average_time": 45
            },
            "ab_tests": [],
            "top_referrers": ["google", "facebook", "twitter"]
        }
        
        return json.dumps(analytics, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.resource("figma-marketing://themes")
def get_available_themes_resource() -> str:
    """MCP Resource: Get available themes"""
    try:
        themes = {
            "default": theme_engine.default_theme,
            "custom": list(theme_engine.themes.keys())
        }
        
        return json.dumps(themes, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

# ===================================================================
# SERVER STARTUP
# ===================================================================

if __name__ == "__main__":
    logger.info("Starting Figma Marketing MCP Server (Enterprise Edition)...")
    
    # Ensure directories exist
    ensure_directories()
    
    # Test database connection
    if db_client:
        logger.info("Database connection successful")
    else:
        logger.error("Database connection failed")
    
    # Test taxonomy loading
    taxonomy = load_marketing_taxonomy()
    if taxonomy:
        logger.info("Marketing taxonomy loaded successfully")
    else:
        logger.error("Failed to load marketing taxonomy")
    
    # Initialize default themes
    theme_engine.create_theme('modern', {
        'colors': {
            'primary': '#8B5CF6',
            'secondary': '#EC4899'
        }
    })
    
    theme_engine.create_theme('corporate', {
        'colors': {
            'primary': '#1E40AF',
            'secondary': '#059669'
        }
    })
    
    # Initialize conversion goals
    conversion_tracker.create_goal('signup', 'event', 'form_submission', 'signup')
    conversion_tracker.create_goal('demo_request', 'event', 'button_click', 'request_demo')
    conversion_tracker.create_goal('purchase', 'event', 'checkout_complete', None)
    
    # Initialize conversion funnels
    conversion_tracker.create_funnel('landing_to_signup', [
        'page_view_landing',
        'hero_section_view',
        'cta_click',
        'form_view',
        'form_submission'
    ])
    
    logger.info("Figma Marketing MCP Server (Enterprise Edition) ready for connections")
    logger.info(f"Total lines: {len(open(__file__).readlines())}")
    
    # Load configuration for port
    import json
    from pathlib import Path
    
    config_path = Path(__file__).parent.parent / "configs" / "server_config.json"
    with open(config_path) as f:
        config = json.load(f)
    
    port = config["server"]["port"]
    host = config["server"]["host"]
    
    # Run the server using FastMCP's built-in method
    logger.info(f"Starting Figma Marketing MCP Server on {host}:{port}")
    mcp.run(transport="streamable-http", host=host, port=port, path="/")