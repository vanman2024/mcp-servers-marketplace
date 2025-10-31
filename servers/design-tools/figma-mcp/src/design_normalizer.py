"""
Design Normalizer
Converts Figma node data to normalized component format
"""

import logging
from typing import Dict, Any, List, Optional, Union
import json

logger = logging.getLogger(__name__)


class DesignNormalizer:
    """Normalizes Figma design data to a standard format"""
    
    def normalize_component(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Figma node to normalized component structure"""
        try:
            normalized = {
                "type": node.get("type", "UNKNOWN"),
                "name": node.get("name", ""),
                "id": node.get("id", ""),
                "visible": node.get("visible", True),
                "locked": node.get("locked", False),
                "opacity": node.get("opacity", 1.0),
                "blendMode": node.get("blendMode", "NORMAL"),
                "figma_data": node  # Preserve original for reference
            }
            
            # Process based on node type
            node_type = node.get("type", "")
            
            if node_type in ["FRAME", "COMPONENT", "COMPONENT_SET", "INSTANCE"]:
                normalized.update(self._normalize_frame(node))
            elif node_type == "TEXT":
                normalized.update(self._normalize_text(node))
            elif node_type in ["RECTANGLE", "ELLIPSE", "POLYGON", "STAR", "LINE"]:
                normalized.update(self._normalize_shape(node))
            elif node_type == "VECTOR":
                normalized.update(self._normalize_vector(node))
            elif node_type == "GROUP":
                normalized.update(self._normalize_group(node))
            
            # Process children if present
            if "children" in node:
                normalized["children"] = [
                    self.normalize_component(child) for child in node.get("children", [])
                ]
            
            return normalized
            
        except Exception as e:
            logger.error(f"Error normalizing component: {str(e)}")
            return {"type": "ERROR", "error": str(e), "original": node}
    
    def _normalize_frame(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize frame/component nodes"""
        frame_data = {
            "layout": self._extract_layout(node),
            "constraints": self._extract_constraints(node),
            "background": self._extract_fills(node.get("fills", [])),
            "border": self._extract_strokes(node),
            "effects": self._extract_effects(node.get("effects", [])),
            "cornerRadius": self._extract_corner_radius(node),
            "padding": self._extract_padding(node),
            "spacing": node.get("itemSpacing", 0),
            "clipsContent": node.get("clipsContent", False)
        }
        
        # Extract auto-layout properties
        if node.get("layoutMode"):
            frame_data["autoLayout"] = {
                "mode": node.get("layoutMode"),
                "direction": "horizontal" if node.get("layoutMode") == "HORIZONTAL" else "vertical",
                "justify": self._map_alignment(node.get("primaryAxisAlignItems", "MIN")),
                "align": self._map_alignment(node.get("counterAxisAlignItems", "MIN")),
                "spacing": node.get("itemSpacing", 0),
                "padding": {
                    "top": node.get("paddingTop", 0),
                    "right": node.get("paddingRight", 0),
                    "bottom": node.get("paddingBottom", 0),
                    "left": node.get("paddingLeft", 0)
                },
                "wrap": node.get("layoutWrap", "NO_WRAP") == "WRAP"
            }
        
        return frame_data
    
    def _normalize_text(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize text nodes"""
        style = node.get("style", {})
        
        return {
            "text": node.get("characters", ""),
            "textStyle": {
                "fontFamily": style.get("fontFamily", "Inter"),
                "fontSize": style.get("fontSize", 14),
                "fontWeight": style.get("fontWeight", 400),
                "letterSpacing": style.get("letterSpacing", 0),
                "lineHeight": style.get("lineHeightPx", style.get("fontSize", 14) * 1.5),
                "textAlign": self._map_text_align(style.get("textAlignHorizontal", "LEFT")),
                "textDecoration": style.get("textDecoration", "NONE"),
                "textCase": style.get("textCase", "ORIGINAL"),
                "fills": self._extract_fills(style.get("fills", []))
            },
            "constraints": self._extract_constraints(node),
            "effects": self._extract_effects(node.get("effects", []))
        }
    
    def _normalize_shape(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize shape nodes"""
        return {
            "shapeType": node.get("type"),
            "fills": self._extract_fills(node.get("fills", [])),
            "strokes": self._extract_strokes(node),
            "effects": self._extract_effects(node.get("effects", [])),
            "constraints": self._extract_constraints(node),
            "cornerRadius": self._extract_corner_radius(node)
        }
    
    def _normalize_vector(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize vector/SVG nodes"""
        return {
            "vectorData": node.get("vectorData", {}),
            "fills": self._extract_fills(node.get("fills", [])),
            "strokes": self._extract_strokes(node),
            "effects": self._extract_effects(node.get("effects", [])),
            "constraints": self._extract_constraints(node)
        }
    
    def _normalize_group(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize group nodes"""
        return {
            "constraints": self._extract_constraints(node),
            "effects": self._extract_effects(node.get("effects", []))
        }
    
    def _extract_layout(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Extract layout properties"""
        bounds = node.get("absoluteBoundingBox", {})
        return {
            "x": bounds.get("x", 0),
            "y": bounds.get("y", 0),
            "width": bounds.get("width", 0),
            "height": bounds.get("height", 0),
            "rotation": node.get("rotation", 0)
        }
    
    def _extract_constraints(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Extract constraint properties"""
        constraints = node.get("constraints", {})
        return {
            "horizontal": constraints.get("horizontal", "LEFT"),
            "vertical": constraints.get("vertical", "TOP")
        }
    
    def _extract_fills(self, fills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract and normalize fill properties"""
        normalized_fills = []
        
        for fill in fills:
            if not fill.get("visible", True):
                continue
                
            normalized_fill = {
                "type": fill.get("type", "SOLID"),
                "opacity": fill.get("opacity", 1.0),
                "blendMode": fill.get("blendMode", "NORMAL")
            }
            
            if fill.get("type") == "SOLID":
                color = fill.get("color", {})
                normalized_fill["color"] = self._rgba_to_hex(color)
            elif fill.get("type") in ["GRADIENT_LINEAR", "GRADIENT_RADIAL", "GRADIENT_ANGULAR"]:
                normalized_fill["gradient"] = self._extract_gradient(fill)
            elif fill.get("type") == "IMAGE":
                normalized_fill["imageRef"] = fill.get("imageRef")
            
            normalized_fills.append(normalized_fill)
        
        return normalized_fills
    
    def _extract_strokes(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Extract stroke properties"""
        strokes = node.get("strokes", [])
        if not strokes:
            return None
            
        stroke = strokes[0]  # Use first stroke
        return {
            "color": self._rgba_to_hex(stroke.get("color", {})),
            "weight": node.get("strokeWeight", 1),
            "style": node.get("strokeDashes", []) and "dashed" or "solid",
            "align": node.get("strokeAlign", "INSIDE"),
            "cap": node.get("strokeCap", "NONE"),
            "join": node.get("strokeJoin", "MITER")
        }
    
    def _extract_effects(self, effects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract effect properties"""
        normalized_effects = []
        
        for effect in effects:
            if not effect.get("visible", True):
                continue
                
            normalized_effect = {
                "type": effect.get("type"),
                "radius": effect.get("radius", 0),
                "offset": {
                    "x": effect.get("offset", {}).get("x", 0),
                    "y": effect.get("offset", {}).get("y", 0)
                },
                "spread": effect.get("spread", 0)
            }
            
            if "color" in effect:
                normalized_effect["color"] = self._rgba_to_hex(effect["color"])
            
            normalized_effects.append(normalized_effect)
        
        return normalized_effects
    
    def _extract_corner_radius(self, node: Dict[str, Any]) -> Union[float, Dict[str, float]]:
        """Extract corner radius"""
        if "cornerRadius" in node:
            return node["cornerRadius"]
        elif "rectangleCornerRadii" in node:
            radii = node["rectangleCornerRadii"]
            return {
                "topLeft": radii[0],
                "topRight": radii[1],
                "bottomRight": radii[2],
                "bottomLeft": radii[3]
            }
        return 0
    
    def _extract_padding(self, node: Dict[str, Any]) -> Dict[str, float]:
        """Extract padding values"""
        return {
            "top": node.get("paddingTop", 0),
            "right": node.get("paddingRight", 0),
            "bottom": node.get("paddingBottom", 0),
            "left": node.get("paddingLeft", 0)
        }
    
    def _extract_gradient(self, fill: Dict[str, Any]) -> Dict[str, Any]:
        """Extract gradient information"""
        gradient = {
            "type": fill.get("type"),
            "stops": []
        }
        
        for stop in fill.get("gradientStops", []):
            gradient["stops"].append({
                "position": stop.get("position", 0),
                "color": self._rgba_to_hex(stop.get("color", {}))
            })
        
        # Extract transform if available
        if "gradientHandlePositions" in fill:
            gradient["handles"] = fill["gradientHandlePositions"]
        
        return gradient
    
    def _rgba_to_hex(self, color: Dict[str, float]) -> str:
        """Convert RGBA color to hex"""
        r = int(color.get("r", 0) * 255)
        g = int(color.get("g", 0) * 255)
        b = int(color.get("b", 0) * 255)
        a = color.get("a", 1.0)
        
        if a < 1.0:
            return f"#{r:02x}{g:02x}{b:02x}{int(a * 255):02x}"
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _map_alignment(self, figma_align: str) -> str:
        """Map Figma alignment to CSS-like values"""
        mapping = {
            "MIN": "start",
            "CENTER": "center",
            "MAX": "end",
            "SPACE_BETWEEN": "space-between",
            "SPACE_AROUND": "space-around",
            "SPACE_EVENLY": "space-evenly"
        }
        return mapping.get(figma_align, "start")
    
    def _map_text_align(self, figma_align: str) -> str:
        """Map Figma text alignment to CSS values"""
        mapping = {
            "LEFT": "left",
            "CENTER": "center",
            "RIGHT": "right",
            "JUSTIFIED": "justify"
        }
        return mapping.get(figma_align, "left")
    
    def extract_design_tokens(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Extract design tokens from component"""
        tokens = {
            "colors": {},
            "spacing": {},
            "typography": {},
            "effects": {}
        }
        
        # Extract colors from fills
        if "fills" in node:
            for i, fill in enumerate(node.get("fills", [])):
                if fill.get("type") == "SOLID" and fill.get("visible", True):
                    color = self._rgba_to_hex(fill.get("color", {}))
                    tokens["colors"][f"fill-{i}"] = color
        
        # Extract colors from strokes
        if "strokes" in node:
            for i, stroke in enumerate(node.get("strokes", [])):
                if stroke.get("visible", True):
                    color = self._rgba_to_hex(stroke.get("color", {}))
                    tokens["colors"][f"stroke-{i}"] = color
        
        # Extract spacing
        if node.get("layoutMode"):
            tokens["spacing"]["itemSpacing"] = node.get("itemSpacing", 0)
            tokens["spacing"]["paddingTop"] = node.get("paddingTop", 0)
            tokens["spacing"]["paddingRight"] = node.get("paddingRight", 0)
            tokens["spacing"]["paddingBottom"] = node.get("paddingBottom", 0)
            tokens["spacing"]["paddingLeft"] = node.get("paddingLeft", 0)
        
        # Extract typography for text nodes
        if node.get("type") == "TEXT" and "style" in node:
            style = node["style"]
            tokens["typography"] = {
                "fontFamily": style.get("fontFamily", "Inter"),
                "fontSize": style.get("fontSize", 14),
                "fontWeight": style.get("fontWeight", 400),
                "lineHeight": style.get("lineHeightPx", 21),
                "letterSpacing": style.get("letterSpacing", 0)
            }
        
        # Extract effects
        for i, effect in enumerate(node.get("effects", [])):
            if effect.get("visible", True):
                effect_token = {
                    "type": effect.get("type"),
                    "radius": effect.get("radius", 0)
                }
                if "color" in effect:
                    effect_token["color"] = self._rgba_to_hex(effect["color"])
                if "offset" in effect:
                    effect_token["offsetX"] = effect["offset"].get("x", 0)
                    effect_token["offsetY"] = effect["offset"].get("y", 0)
                
                tokens["effects"][f"effect-{i}"] = effect_token
        
        return tokens