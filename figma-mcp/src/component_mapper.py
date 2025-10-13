"""
ShadCN Component Mapper
Maps normalized Figma components to ShadCN UI components
"""

import logging
from typing import Dict, Any, List, Optional
import json
import re

logger = logging.getLogger(__name__)


class ShadcnComponentMapper:
    """Maps Figma components to ShadCN UI library components"""
    
    # Component type mappings based on common patterns
    COMPONENT_PATTERNS = {
        "button": {
            "patterns": [r"button", r"btn", r"cta"],
            "shadcn": "Button",
            "props": ["variant", "size", "disabled", "asChild"],
            "variants": {
                "default": "default",
                "primary": "default",
                "secondary": "secondary",
                "destructive": "destructive",
                "outline": "outline",
                "ghost": "ghost",
                "link": "link"
            }
        },
        "card": {
            "patterns": [r"card", r"panel"],
            "shadcn": "Card",
            "props": ["className"],
            "subcomponents": ["CardHeader", "CardTitle", "CardDescription", "CardContent", "CardFooter"]
        },
        "input": {
            "patterns": [r"input", r"text\s*field", r"form\s*field"],
            "shadcn": "Input",
            "props": ["type", "placeholder", "disabled", "value", "onChange"]
        },
        "select": {
            "patterns": [r"select", r"dropdown", r"combobox"],
            "shadcn": "Select",
            "props": ["placeholder", "disabled", "value", "onValueChange"],
            "subcomponents": ["SelectTrigger", "SelectContent", "SelectItem", "SelectValue"]
        },
        "checkbox": {
            "patterns": [r"checkbox", r"check\s*box"],
            "shadcn": "Checkbox",
            "props": ["checked", "onCheckedChange", "disabled"]
        },
        "radio": {
            "patterns": [r"radio"],
            "shadcn": "RadioGroup",
            "props": ["value", "onValueChange"],
            "subcomponents": ["RadioGroupItem"]
        },
        "switch": {
            "patterns": [r"switch", r"toggle\s*switch"],
            "shadcn": "Switch",
            "props": ["checked", "onCheckedChange", "disabled"]
        },
        "badge": {
            "patterns": [r"badge", r"tag", r"chip"],
            "shadcn": "Badge",
            "props": ["variant"],
            "variants": {
                "default": "default",
                "secondary": "secondary",
                "destructive": "destructive",
                "outline": "outline"
            }
        },
        "avatar": {
            "patterns": [r"avatar", r"profile\s*pic"],
            "shadcn": "Avatar",
            "props": ["className"],
            "subcomponents": ["AvatarImage", "AvatarFallback"]
        },
        "dialog": {
            "patterns": [r"dialog", r"modal", r"popup"],
            "shadcn": "Dialog",
            "props": ["open", "onOpenChange"],
            "subcomponents": ["DialogTrigger", "DialogContent", "DialogHeader", "DialogTitle", "DialogDescription", "DialogFooter"]
        },
        "alert": {
            "patterns": [r"alert", r"notification", r"toast"],
            "shadcn": "Alert",
            "props": ["variant"],
            "subcomponents": ["AlertTitle", "AlertDescription"]
        },
        "tabs": {
            "patterns": [r"tabs", r"tab\s*panel"],
            "shadcn": "Tabs",
            "props": ["defaultValue", "value", "onValueChange"],
            "subcomponents": ["TabsList", "TabsTrigger", "TabsContent"]
        },
        "accordion": {
            "patterns": [r"accordion", r"collapse", r"expandable"],
            "shadcn": "Accordion",
            "props": ["type", "collapsible"],
            "subcomponents": ["AccordionItem", "AccordionTrigger", "AccordionContent"]
        },
        "separator": {
            "patterns": [r"separator", r"divider", r"hr"],
            "shadcn": "Separator",
            "props": ["orientation", "decorative"]
        },
        "tooltip": {
            "patterns": [r"tooltip", r"hint"],
            "shadcn": "Tooltip",
            "props": [],
            "subcomponents": ["TooltipTrigger", "TooltipContent", "TooltipProvider"]
        },
        "form": {
            "patterns": [r"form"],
            "shadcn": "Form",
            "props": [],
            "subcomponents": ["FormField", "FormItem", "FormLabel", "FormControl", "FormDescription", "FormMessage"]
        }
    }
    
    def map_component(self, normalized_component: Dict[str, Any]) -> Dict[str, Any]:
        """Map normalized component to ShadCN component"""
        component_name = normalized_component.get("name", "").lower()
        component_type = self._detect_component_type(component_name, normalized_component)
        
        mapping = {
            "type": component_type,
            "component": self.COMPONENT_PATTERNS.get(component_type, {}).get("shadcn", "div"),
            "confidence": 0.0,
            "tags": self._extract_tags(component_name, component_type),
            "props": {},
            "children": []
        }
        
        # Extract props based on component type
        if component_type in self.COMPONENT_PATTERNS:
            mapping["props"] = self._extract_props(normalized_component, component_type)
            mapping["confidence"] = 0.9  # High confidence for matched patterns
        else:
            mapping["confidence"] = 0.3  # Low confidence for unmatched
        
        # Process children
        if "children" in normalized_component:
            for child in normalized_component["children"]:
                child_mapping = self.map_component(child)
                mapping["children"].append(child_mapping)
        
        return mapping
    
    def _detect_component_type(self, name: str, component: Dict[str, Any]) -> str:
        """Detect component type from name and structure"""
        name_lower = name.lower()
        
        # Check each pattern
        for comp_type, config in self.COMPONENT_PATTERNS.items():
            for pattern in config["patterns"]:
                if re.search(pattern, name_lower):
                    return comp_type
        
        # Fallback detection based on structure
        if component.get("type") == "TEXT":
            # Check if it might be a heading or label
            style = component.get("textStyle", {})
            font_size = style.get("fontSize", 14)
            if font_size > 24:
                return "heading"
            elif font_size < 12:
                return "caption"
            else:
                return "text"
        
        # Check for frame patterns
        if component.get("type") in ["FRAME", "COMPONENT"]:
            # Check if it has auto-layout (might be a container)
            if component.get("autoLayout"):
                return "container"
            # Check aspect ratio for common patterns
            layout = component.get("layout", {})
            width = layout.get("width", 1)
            height = layout.get("height", 1)
            aspect_ratio = width / height if height > 0 else 1
            
            if 0.9 <= aspect_ratio <= 1.1:  # Square-ish
                return "avatar" if width < 100 else "card"
            elif aspect_ratio > 3:  # Wide
                return "banner"
        
        return "custom"
    
    def _extract_tags(self, name: str, component_type: str) -> List[str]:
        """Extract relevant tags from component name and type"""
        tags = [component_type]
        
        # Extract state tags
        states = ["hover", "active", "disabled", "focus", "pressed", "selected"]
        for state in states:
            if state in name.lower():
                tags.append(state)
        
        # Extract variant tags
        variants = ["primary", "secondary", "success", "danger", "warning", "info"]
        for variant in variants:
            if variant in name.lower():
                tags.append(variant)
        
        # Extract size tags
        sizes = ["small", "medium", "large", "xs", "sm", "md", "lg", "xl"]
        for size in sizes:
            if size in name.lower():
                tags.append(size)
        
        return list(set(tags))  # Remove duplicates
    
    def _extract_props(self, component: Dict[str, Any], component_type: str) -> Dict[str, Any]:
        """Extract props based on component type"""
        props = {}
        config = self.COMPONENT_PATTERNS.get(component_type, {})
        
        # Extract variant from name or appearance
        if "variants" in config:
            variant = self._detect_variant(component, config["variants"])
            if variant:
                props["variant"] = variant
        
        # Extract size
        size = self._detect_size(component)
        if size and "size" in config.get("props", []):
            props["size"] = size
        
        # Extract common props
        if component.get("opacity", 1.0) < 0.5:
            props["disabled"] = True
        
        # Component-specific props
        if component_type == "input":
            # Check for placeholder text
            if "children" in component:
                for child in component["children"]:
                    if child.get("type") == "TEXT" and child.get("opacity", 1.0) < 0.7:
                        props["placeholder"] = child.get("text", "")
        
        elif component_type == "button":
            # Check for icon
            has_icon = any(child.get("type") == "VECTOR" for child in component.get("children", []))
            if has_icon:
                props["icon"] = True
        
        return props
    
    def _detect_variant(self, component: Dict[str, Any], variants: Dict[str, str]) -> Optional[str]:
        """Detect component variant from appearance"""
        name_lower = component.get("name", "").lower()
        
        # Check name for variant keywords
        for key, value in variants.items():
            if key in name_lower:
                return value
        
        # Check visual properties
        fills = component.get("background", [])
        if fills:
            primary_fill = fills[0] if isinstance(fills, list) else fills
            if primary_fill.get("type") == "SOLID":
                color = primary_fill.get("color", "")
                # Simple color detection
                if "ff0000" in color or "red" in name_lower:
                    return "destructive"
                elif "0000ff" in color or "blue" in name_lower:
                    return "default"
        
        # Check for outline
        if component.get("border"):
            return "outline"
        
        return None
    
    def _detect_size(self, component: Dict[str, Any]) -> Optional[str]:
        """Detect component size from dimensions"""
        layout = component.get("layout", {})
        height = layout.get("height", 0)
        
        # Common height breakpoints
        if height < 28:
            return "sm"
        elif height < 40:
            return "default"
        elif height < 48:
            return "lg"
        else:
            return "xl"
    
    def generate_shadcn_code(self, component: Dict[str, Any]) -> str:
        """Generate ShadCN component code"""
        mapping = self.map_component(component.get("json_layout", component))
        
        return self._generate_jsx(mapping)
    
    def _generate_jsx(self, mapping: Dict[str, Any], indent: int = 0) -> str:
        """Generate JSX code from mapping"""
        indent_str = "  " * indent
        component_name = mapping["component"]
        props = mapping.get("props", {})
        children = mapping.get("children", [])
        
        # Build props string
        props_str = ""
        for key, value in props.items():
            if isinstance(value, bool):
                props_str += f' {key}' if value else ''
            elif isinstance(value, str):
                props_str += f' {key}="{value}"'
            else:
                props_str += f' {key}={{{json.dumps(value)}}}'
        
        # Handle self-closing components
        if not children and component_name not in ["Card", "Dialog", "Form"]:
            return f'{indent_str}<{component_name}{props_str} />'
        
        # Build component with children
        jsx = f'{indent_str}<{component_name}{props_str}>\n'
        
        for child in children:
            jsx += self._generate_jsx(child, indent + 1) + '\n'
        
        jsx += f'{indent_str}</{component_name}>'
        
        return jsx
    
    def get_import_statements(self, component_types: List[str]) -> str:
        """Generate import statements for used components"""
        imports = set()
        
        for comp_type in component_types:
            if comp_type in self.COMPONENT_PATTERNS:
                config = self.COMPONENT_PATTERNS[comp_type]
                imports.add(config["shadcn"])
                
                # Add subcomponents
                for subcomp in config.get("subcomponents", []):
                    imports.add(subcomp)
        
        if imports:
            return f"import {{ {', '.join(sorted(imports))} }} from '@/components/ui'"
        
        return ""
    
    def map_component_quick(self, component_name: str) -> Dict[str, Any]:
        """
        Quick component mapping based only on name (for preview purposes)
        
        Args:
            component_name: Name of the component from Figma
            
        Returns:
            Basic mapping information with type and shadcn component
        """
        component_type = self._detect_component_type(component_name, {})
        
        # Get ShadCN component from pattern
        shadcn_component = "div"  # Default fallback
        if component_type in self.COMPONENT_PATTERNS:
            shadcn_component = self.COMPONENT_PATTERNS[component_type]["shadcn"]
        
        return {
            "type": component_type,
            "component": shadcn_component,
            "tags": [component_type]
        }