#!/usr/bin/env python3
"""
Figma Components Sync Script
Pulls all components from Figma's free component library and syncs them to our database
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

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database_integration import FigmaDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FigmaComponentSyncer:
    """Syncs Figma components to database"""
    
    def __init__(self, figma_token: str):
        self.figma_token = figma_token
        self.base_url = "https://api.figma.com/v1"
        self.headers = {
            "X-FIGMA-TOKEN": figma_token,
            "Content-Type": "application/json"
        }
        self.database = FigmaDatabase()
        
        # Known Figma community files with free components
        self.component_files = [
            {
                "name": "shadcn/ui Design System (Community)",
                "file_key": "JGMQqO02q6wLSyk29RDsgh",
                "description": "Complete shadcn/ui design system components from Figma community",
                "url": "https://www.figma.com/design/JGMQqO02q6wLSyk29RDsgh/-shadcn-ui---Design-System--Community---Copy-"
            },
            # Add more known component libraries here
        ]
    
    async def sync_all_components(self) -> Dict[str, Any]:
        """Main sync function - pulls all components from known files"""
        if not self.database.is_connected():
            logger.error("Database not connected. Check SUPABASE_SERVICE_KEY environment variable.")
            return {"success": False, "error": "Database not connected"}
        
        logger.info("Starting Figma component sync...")
        
        total_stats = {
            "files_processed": 0,
            "components_found": 0,
            "components_synced": 0,
            "errors": 0
        }
        
        async with aiohttp.ClientSession() as session:
            for file_info in self.component_files:
                try:
                    logger.info(f"Processing file: {file_info['name']}")
                    
                    # Get file data
                    file_data = await self.get_file_data(session, file_info['file_key'])
                    if not file_data:
                        logger.error(f"Failed to get file data for {file_info['name']}")
                        total_stats["errors"] += 1
                        continue
                    
                    # Extract components
                    components = self.extract_components(file_data, file_info)
                    logger.info(f"Found {len(components)} components in {file_info['name']}")
                    
                    total_stats["files_processed"] += 1
                    total_stats["components_found"] += len(components)
                    
                    # Sync to database
                    sync_stats = await self.database.sync_from_figma(components)
                    total_stats["components_synced"] += sync_stats.get("added", 0) + sync_stats.get("updated", 0)
                    
                    logger.info(f"Synced {sync_stats.get('added', 0)} new and {sync_stats.get('updated', 0)} updated components")
                    
                except Exception as e:
                    logger.error(f"Error processing file {file_info['name']}: {e}")
                    total_stats["errors"] += 1
        
        logger.info(f"Sync completed. Stats: {total_stats}")
        return {"success": True, "stats": total_stats}
    
    async def get_file_data(self, session: aiohttp.ClientSession, file_key: str) -> Optional[Dict[str, Any]]:
        """Get file data from Figma API"""
        try:
            url = f"{self.base_url}/files/{file_key}"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                elif response.status == 404:
                    logger.warning(f"File {file_key} not found or not accessible")
                    return None
                else:
                    logger.error(f"API error {response.status}: {await response.text()}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching file {file_key}: {e}")
            return None
    
    def extract_components(self, file_data: Dict[str, Any], file_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract component data from Figma file response"""
        components = []
        
        def traverse_node(node: Dict[str, Any], parent_path: str = ""):
            """Recursively traverse file nodes to find components"""
            
            # Check if this node is a component
            if node.get("type") == "COMPONENT":
                component = self.process_component_node(node, file_info, parent_path)
                if component:
                    components.append(component)
            
            # Check if this node is a component set (variants)
            elif node.get("type") == "COMPONENT_SET":
                component_set = self.process_component_set(node, file_info, parent_path)
                if component_set:
                    components.extend(component_set)
            
            # Traverse children
            for child in node.get("children", []):
                child_path = f"{parent_path}/{node.get('name', '')}" if parent_path else node.get('name', '')
                traverse_node(child, child_path)
        
        # Start traversal from document root
        if file_data.get("document"):
            traverse_node(file_data["document"])
        
        return components
    
    def process_component_node(self, node: Dict[str, Any], file_info: Dict[str, Any], parent_path: str) -> Optional[Dict[str, Any]]:
        """Process a single component node"""
        try:
            name = node.get("name", "Unnamed Component")
            
            # Skip if name indicates it's not a public component
            if any(skip in name.lower() for skip in ["_", "test", "example", "demo"]):
                return None
            
            # Extract component data
            component = {
                "id": node.get("id"),
                "name": name,
                "description": node.get("description", ""),
                "type": node.get("type"),
                "file_key": file_info["file_key"],
                "figma_url": f"https://www.figma.com/file/{file_info['file_key']}?node-id={node.get('id', '').replace(':', '%3A')}",
                "parent_path": parent_path,
                "absoluteBoundingBox": node.get("absoluteBoundingBox", {}),
                "properties": self.extract_component_properties(node),
                "styles": self.extract_styles(node),
                "constraints": node.get("constraints", {}),
                "layoutMode": node.get("layoutMode"),
                "itemSpacing": node.get("itemSpacing"),
                "fills": node.get("fills", []),
                "strokes": node.get("strokes", []),
                "effects": node.get("effects", []),
                "children_count": len(node.get("children", [])),
                "extracted_at": datetime.now(timezone.utc).isoformat()
            }
            
            return component
            
        except Exception as e:
            logger.error(f"Error processing component {node.get('name', 'unknown')}: {e}")
            return None
    
    def process_component_set(self, node: Dict[str, Any], file_info: Dict[str, Any], parent_path: str) -> List[Dict[str, Any]]:
        """Process a component set (variants)"""
        components = []
        
        try:
            base_name = node.get("name", "Component Set")
            
            # Process each variant in the component set
            for child in node.get("children", []):
                if child.get("type") == "COMPONENT":
                    variant_name = child.get("name", "Variant")
                    
                    component = {
                        "id": child.get("id"),
                        "name": f"{base_name} - {variant_name}",
                        "description": f"Variant of {base_name}: {child.get('description', '')}",
                        "type": child.get("type"),
                        "file_key": file_info["file_key"],
                        "figma_url": f"https://www.figma.com/file/{file_info['file_key']}?node-id={child.get('id', '').replace(':', '%3A')}",
                        "parent_path": f"{parent_path}/{base_name}",
                        "variant_of": node.get("id"),
                        "variant_properties": child.get("variantProperties", {}),
                        "absoluteBoundingBox": child.get("absoluteBoundingBox", {}),
                        "properties": self.extract_component_properties(child),
                        "styles": self.extract_styles(child),
                        "constraints": child.get("constraints", {}),
                        "fills": child.get("fills", []),
                        "strokes": child.get("strokes", []),
                        "effects": child.get("effects", []),
                        "children_count": len(child.get("children", [])),
                        "extracted_at": datetime.now(timezone.utc).isoformat()
                    }
                    
                    components.append(component)
            
        except Exception as e:
            logger.error(f"Error processing component set {node.get('name', 'unknown')}: {e}")
        
        return components
    
    def extract_component_properties(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant properties from component node"""
        properties = {}
        
        # Basic properties
        if "visible" in node:
            properties["visible"] = node["visible"]
        if "locked" in node:
            properties["locked"] = node["locked"]
        if "opacity" in node:
            properties["opacity"] = node["opacity"]
        if "blendMode" in node:
            properties["blendMode"] = node["blendMode"]
        
        # Layout properties
        layout_props = ["layoutMode", "primaryAxisSizingMode", "counterAxisSizingMode", 
                       "primaryAxisAlignItems", "counterAxisAlignItems", "itemSpacing"]
        for prop in layout_props:
            if prop in node:
                properties[prop] = node[prop]
        
        # Text properties (if it's a text node or contains text)
        if node.get("type") == "TEXT":
            text_props = ["characters", "style", "characterStyleOverrides", "styleOverrideTable"]
            for prop in text_props:
                if prop in node:
                    properties[prop] = node[prop]
        
        return properties
    
    def extract_styles(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Extract style information from node"""
        styles = {}
        
        # Extract fills (colors, gradients)
        if "fills" in node and node["fills"]:
            styles["fills"] = []
            for fill in node["fills"]:
                if fill.get("type") == "SOLID":
                    color = fill.get("color", {})
                    styles["fills"].append({
                        "type": "solid",
                        "color": {
                            "r": color.get("r", 0),
                            "g": color.get("g", 0),
                            "b": color.get("b", 0),
                            "a": color.get("a", 1)
                        },
                        "opacity": fill.get("opacity", 1)
                    })
        
        # Extract strokes (borders)
        if "strokes" in node and node["strokes"]:
            styles["strokes"] = []
            for stroke in node["strokes"]:
                if stroke.get("type") == "SOLID":
                    color = stroke.get("color", {})
                    styles["strokes"].append({
                        "type": "solid",
                        "color": {
                            "r": color.get("r", 0),
                            "g": color.get("g", 0),
                            "b": color.get("b", 0),
                            "a": color.get("a", 1)
                        }
                    })
        
        # Extract effects (shadows, blurs)
        if "effects" in node and node["effects"]:
            styles["effects"] = []
            for effect in node["effects"]:
                styles["effects"].append({
                    "type": effect.get("type"),
                    "visible": effect.get("visible", True),
                    "radius": effect.get("radius"),
                    "color": effect.get("color"),
                    "offset": effect.get("offset")
                })
        
        return styles

async def main():
    """Main sync script"""
    print("=== Figma Component Sync Script ===\n")
    
    # Check for Figma token
    figma_token = os.getenv('FIGMA_PAT') or os.getenv('FIGMA_ACCESS_TOKEN')
    if not figma_token:
        print("❌ Error: No Figma token found!")
        print("Set FIGMA_PAT or FIGMA_ACCESS_TOKEN environment variable")
        print("Get a token from: https://www.figma.com/developers/access-tokens")
        return
    
    print(f"✅ Figma token found (length: {len(figma_token)})")
    
    # Check database connection
    database = FigmaDatabase()
    if not database.is_connected():
        print("❌ Error: Database not connected!")
        print("Set SUPABASE_SERVICE_KEY environment variable")
        return
    
    print("✅ Database connected")
    
    # Create syncer and run
    syncer = FigmaComponentSyncer(figma_token)
    
    print("\n🔄 Starting component sync...")
    result = await syncer.sync_all_components()
    
    if result.get("success"):
        stats = result.get("stats", {})
        print(f"\n✅ Sync completed successfully!")
        print(f"   Files processed: {stats.get('files_processed', 0)}")
        print(f"   Components found: {stats.get('components_found', 0)}")
        print(f"   Components synced: {stats.get('components_synced', 0)}")
        print(f"   Errors: {stats.get('errors', 0)}")
    else:
        print(f"\n❌ Sync failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    asyncio.run(main())