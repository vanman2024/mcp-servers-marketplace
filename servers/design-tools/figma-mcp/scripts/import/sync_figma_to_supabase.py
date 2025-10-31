#!/usr/bin/env python3
"""
Direct Figma to Supabase Sync using MCP Tools
Uses the working Supabase MCP tools to insert components
"""

import os
import sys
import json
import logging
import asyncio
import aiohttp
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FigmaToSupabaseSync:
    """Syncs Figma components directly to Supabase using MCP tools"""
    
    def __init__(self, figma_token: str, project_id: str):
        self.figma_token = figma_token
        self.project_id = project_id
        self.base_url = "https://api.figma.com/v1"
        self.headers = {
            "X-FIGMA-TOKEN": figma_token,
            "Content-Type": "application/json"
        }
        
        # shadcn/ui Design System file
        self.file_key = "JGMQqO02q6wLSyk29RDsgh"
        self.file_name = "shadcn/ui Design System"
    
    async def get_figma_file_data(self) -> Optional[Dict[str, Any]]:
        """Get the complete Figma file data"""
        try:
            url = f"{self.base_url}/files/{self.file_key}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Successfully fetched Figma file: {data.get('name', 'Unknown')}")
                        return data
                    else:
                        logger.error(f"Figma API error {response.status}: {await response.text()}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error fetching Figma file: {e}")
            return None
    
    def extract_components_from_file(self, file_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract all components from the Figma file"""
        components = []
        
        def traverse_node(node: Dict[str, Any], page_name: str = "", depth: int = 0):
            """Recursively traverse nodes to find components"""
            
            node_type = node.get("type", "")
            node_name = node.get("name", "Unnamed")
            
            # Process different node types
            if node_type == "COMPONENT":
                component = self.process_component(node, page_name)
                if component:
                    components.append(component)
                    logger.debug(f"Found component: {component['name']}")
            
            elif node_type == "COMPONENT_SET":
                # Handle component variants
                variant_components = self.process_component_set(node, page_name)
                components.extend(variant_components)
                logger.debug(f"Found component set: {node_name} with {len(variant_components)} variants")
            
            elif node_type == "CANVAS":
                # This is a page
                page_name = node_name
                logger.info(f"Processing page: {page_name}")
            
            # Traverse children
            for child in node.get("children", []):
                traverse_node(child, page_name, depth + 1)
        
        # Start traversal from document
        if file_data.get("document"):
            traverse_node(file_data["document"])
        
        logger.info(f"Extracted {len(components)} total components")
        return components
    
    def process_component(self, node: Dict[str, Any], page_name: str) -> Optional[Dict[str, Any]]:
        """Process a single component node"""
        try:
            name = node.get("name", "Unnamed Component")
            
            # Skip internal/private components
            if name.startswith("_") or "internal" in name.lower():
                return None
            
            # Determine component type from name
            component_type = self.infer_component_type(name)
            
            # Create component record
            component = {
                "figma_id": node.get("id", ""),
                "name": name,
                "description": node.get("description", ""),
                "figma_url": f"https://www.figma.com/file/{self.file_key}?node-id={node.get('id', '').replace(':', '%3A')}",
                "component_type": component_type,
                "tags": self.extract_tags(name, node),
                "props": self.extract_properties(node),
                "figma_node_type": node.get("type", ""),
                "width": node.get("absoluteBoundingBox", {}).get("width"),
                "height": node.get("absoluteBoundingBox", {}).get("height"),
                "status": "active",
                "last_synced": datetime.now(timezone.utc).isoformat(),
                "page_name": page_name,
                "complexity_score": self.calculate_complexity(node),
                "popularity_score": 0
            }
            
            return component
            
        except Exception as e:
            logger.error(f"Error processing component {node.get('name', 'unknown')}: {e}")
            return None
    
    def process_component_set(self, node: Dict[str, Any], page_name: str) -> List[Dict[str, Any]]:
        """Process component set (variants)"""
        components = []
        set_name = node.get("name", "Component Set")
        
        for child in node.get("children", []):
            if child.get("type") == "COMPONENT":
                variant_name = child.get("name", "Variant")
                
                component = {
                    "figma_id": child.get("id", ""),
                    "name": f"{set_name} - {variant_name}",
                    "description": f"Variant of {set_name}",
                    "figma_url": f"https://www.figma.com/file/{self.file_key}?node-id={child.get('id', '').replace(':', '%3A')}",
                    "component_type": self.infer_component_type(set_name),
                    "tags": self.extract_tags(f"{set_name} {variant_name}", child),
                    "props": self.extract_properties(child),
                    "figma_node_type": child.get("type", ""),
                    "width": child.get("absoluteBoundingBox", {}).get("width"),
                    "height": child.get("absoluteBoundingBox", {}).get("height"),
                    "status": "active",
                    "last_synced": datetime.now(timezone.utc).isoformat(),
                    "page_name": page_name,
                    "complexity_score": self.calculate_complexity(child),
                    "popularity_score": 0,
                    "variant_properties": child.get("variantProperties", {})
                }
                
                components.append(component)
        
        return components
    
    def infer_component_type(self, name: str) -> str:
        """Infer component type from name"""
        name_lower = name.lower()
        
        type_mapping = {
            "button": "button",
            "input": "input",
            "card": "card",
            "modal": "modal",
            "dialog": "modal",
            "nav": "navigation",
            "menu": "navigation",
            "table": "data-display",
            "list": "data-display",
            "icon": "icon",
            "badge": "badge",
            "alert": "feedback",
            "toast": "feedback",
            "form": "form",
            "checkbox": "form",
            "radio": "form",
            "select": "form",
            "dropdown": "form",
            "accordion": "layout",
            "tabs": "layout",
            "separator": "layout",
            "avatar": "media",
            "image": "media",
            "progress": "feedback",
            "slider": "form",
            "switch": "form",
            "tooltip": "overlay",
            "popover": "overlay",
            "sheet": "overlay",
            "calendar": "form",
            "date": "form",
            "time": "form",
            "skeleton": "feedback",
            "spinner": "feedback",
            "loading": "feedback"
        }
        
        for keyword, comp_type in type_mapping.items():
            if keyword in name_lower:
                return comp_type
        
        return "component"
    
    def extract_tags(self, name: str, node: Dict[str, Any]) -> List[str]:
        """Extract relevant tags from component"""
        tags = []
        name_lower = name.lower()
        
        # Size tags
        if "large" in name_lower or "lg" in name_lower:
            tags.append("large")
        elif "small" in name_lower or "sm" in name_lower:
            tags.append("small")
        elif "medium" in name_lower or "md" in name_lower:
            tags.append("medium")
        
        # Style tags
        style_keywords = ["outline", "filled", "ghost", "link", "destructive", 
                         "secondary", "primary", "default", "variant"]
        for keyword in style_keywords:
            if keyword in name_lower:
                tags.append(keyword)
        
        # State tags
        state_keywords = ["disabled", "loading", "active", "hover", "focus"]
        for keyword in state_keywords:
            if keyword in name_lower:
                tags.append(keyword)
        
        # Add component type as tag
        tags.append(self.infer_component_type(name))
        
        return list(set(tags))  # Remove duplicates
    
    def extract_properties(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Extract component properties"""
        props = {}
        
        # Basic properties
        if "visible" in node:
            props["visible"] = node["visible"]
        if "opacity" in node:
            props["opacity"] = node["opacity"]
        
        # Layout properties
        layout_props = ["layoutMode", "primaryAxisSizingMode", "counterAxisSizingMode"]
        for prop in layout_props:
            if prop in node:
                props[prop] = node[prop]
        
        # Fills (colors)
        if "fills" in node and node["fills"]:
            props["fills"] = node["fills"][:3]  # Limit to avoid huge data
        
        # Effects
        if "effects" in node and node["effects"]:
            props["effects"] = node["effects"][:3]  # Limit to avoid huge data
        
        return props
    
    def calculate_complexity(self, node: Dict[str, Any]) -> int:
        """Calculate component complexity (1-5)"""
        score = 1
        
        # More children = more complex
        children_count = len(node.get("children", []))
        if children_count > 10:
            score += 2
        elif children_count > 5:
            score += 1
        
        # Has effects or complex fills
        if node.get("effects"):
            score += 1
        if node.get("fills") and len(node.get("fills", [])) > 1:
            score += 1
        
        return min(score, 5)

async def main():
    """Main sync function"""
    print("=== Figma to Supabase Direct Sync ===\n")
    
    # Check environment
    figma_token = os.getenv('FIGMA_PAT') or os.getenv('FIGMA_ACCESS_TOKEN')
    if not figma_token:
        print("❌ Error: No Figma token found!")
        return
    
    project_id = "wsmhiiharnhqupdniwgw"  # Figma Design System project
    
    # Create syncer
    syncer = FigmaToSupabaseSync(figma_token, project_id)
    
    # Get Figma data
    print("🔄 Fetching Figma file data...")
    file_data = await syncer.get_figma_file_data()
    
    if not file_data:
        print("❌ Failed to fetch Figma file data")
        return
    
    # Extract components
    print("🔄 Extracting components...")
    components = syncer.extract_components_from_file(file_data)
    
    print(f"✅ Found {len(components)} components")
    
    # Save component data to file for inspection
    output_file = "extracted_figma_components.json"
    with open(output_file, 'w') as f:
        json.dump(components, f, indent=2, default=str)
    
    print(f"📁 Component data saved to {output_file}")
    
    # Show sample components
    print("\n📋 Sample components:")
    for i, comp in enumerate(components[:10]):
        print(f"  {i+1}. {comp['name']} ({comp['component_type']}) - {len(comp.get('tags', []))} tags")
    
    if len(components) > 10:
        print(f"  ... and {len(components) - 10} more")
    
    print(f"\n✅ Extraction completed! Ready to sync {len(components)} components to database.")

if __name__ == "__main__":
    asyncio.run(main())