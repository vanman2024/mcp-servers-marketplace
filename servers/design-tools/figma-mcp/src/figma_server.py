#!/usr/bin/env python3
"""
Figma MCP Server - HTTP Implementation (Streamlined)
Direct Figma-to-Code workflow with ShadCN components and file generation

Provides tools for:
- Direct generation of React/TypeScript files from Figma designs
- Mapping Figma components to ShadCN UI library
- Batch processing of multiple components
- File-based component generation with metadata
- Real-time validation of Figma API access
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timezone
import asyncio
from urllib.parse import urlparse

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Debug mode from environment
DEBUG = os.getenv('FIGMA_DEBUG', '').lower() in ('true', '1', 'yes')
if DEBUG:
    logging.getLogger().setLevel(logging.DEBUG)
    logger.debug("Debug mode enabled")

logger.info("=== Figma MCP Server Starting ===")
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

# Import our modules
from figma_client import FigmaClient
from design_normalizer import DesignNormalizer
from component_mapper import ShadcnComponentMapper
from file_generator import FileGenerator

# Initialize FastMCP server
mcp = FastMCP("figma-design")

# Environment variable checking with detailed logging
logger.info("Checking environment variables...")

# Check for Figma token
figma_pat = os.getenv('FIGMA_PAT')
figma_access_token = os.getenv('FIGMA_ACCESS_TOKEN')

if figma_pat:
    logger.info("✓ FIGMA_PAT detected (length: %d)", len(figma_pat))
    # Mask the token for security
    masked_token = figma_pat[:10] + "..." + figma_pat[-4:] if len(figma_pat) > 14 else "***"
    logger.debug("FIGMA_PAT format check: %s", masked_token)
else:
    logger.warning("✗ FIGMA_PAT not found")

if figma_access_token:
    logger.info("✓ FIGMA_ACCESS_TOKEN detected (length: %d)", len(figma_access_token))
    masked_token = figma_access_token[:10] + "..." + figma_access_token[-4:] if len(figma_access_token) > 14 else "***"
    logger.debug("FIGMA_ACCESS_TOKEN format check: %s", masked_token)
else:
    logger.warning("✗ FIGMA_ACCESS_TOKEN not found")

# Get configuration from environment
FIGMA_TOKEN = figma_pat or figma_access_token

# Enhanced validation with detailed error messages
if not FIGMA_TOKEN:
    error_msg = """
    ERROR: Figma authentication token not found!
    
    Please set one of the following environment variables:
    - FIGMA_PAT (Personal Access Token)
    - FIGMA_ACCESS_TOKEN
    
    To get a Figma PAT:
    1. Go to https://www.figma.com/developers/access-tokens
    2. Generate a new token with 'File content' scope
    3. Set it as: export FIGMA_PAT="your-token-here"
    
    Example:
    export FIGMA_PAT="figd_AbCdEfGhIjKlMnOpQrStUvWxYz"
    """
    logger.error(error_msg)
    raise ValueError(error_msg)

# Validate Figma token format (basic check)
if len(FIGMA_TOKEN) < 20:
    logger.warning("Figma token seems too short (length: %d). Tokens are typically 40+ characters.", len(FIGMA_TOKEN))

# Check if token starts with expected prefixes
if not FIGMA_TOKEN.startswith(('figd_', 'figp_', 'fig-')):
    logger.warning("Figma token may have incorrect format. Expected prefixes: 'figd_', 'figp_', or 'fig-'")
    logger.info("Token starts with: '%s...'", FIGMA_TOKEN[:5] if len(FIGMA_TOKEN) > 5 else FIGMA_TOKEN)

logger.info("Figma authentication configured successfully!")

# Initialize clients
figma_client = FigmaClient(FIGMA_TOKEN)
normalizer = DesignNormalizer()
component_mapper = ShadcnComponentMapper()
file_generator = FileGenerator()

# Helper functions
def extract_file_key(file_url_or_key: str) -> str:
    """Extract Figma file key from URL or return key as-is"""
    if file_url_or_key.startswith("http"):
        # Parse Figma URL: https://www.figma.com/file/{key}/{name} or https://www.figma.com/design/{key}/{name}
        parsed = urlparse(file_url_or_key)
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) >= 2 and path_parts[0] in ["file", "design"]:
            return path_parts[1]
        raise ValueError(f"Invalid Figma URL format. Expected /file/ or /design/ but got: {parsed.path}")
    return file_url_or_key

# MCP Tools

@mcp.tool()
async def validate_figma_access(
    file_url: str
) -> Dict[str, Any]:
    """
    Validate Figma API access and get basic file information (fast validation)
    
    Args:
        file_url: Figma file URL or file key
        
    Returns:
        Access validation and file information
    """
    try:
        file_key = extract_file_key(file_url)
        
        # Test Figma API access with just file info (fast)
        file_info = await figma_client.get_file_info(file_key)
        
        return {
            "status": "success",
            "access": "valid",
            "file_info": {
                "name": file_info.get("name", "Unknown"),
                "key": file_key,
                "url": f"https://www.figma.com/design/{file_key}",
                "last_modified": file_info.get("lastModified"),
                "version": file_info.get("version", "Unknown")
            },
            "message": f"✅ Successfully accessed Figma file: {file_info.get('name', 'Unknown')}"
        }
        
    except Exception as e:
        logger.error(f"Error validating Figma access: {str(e)}")
        return {
            "status": "error",
            "access": "invalid",
            "error": str(e),
            "message": "❌ Failed to access Figma file - check URL and API token"
        }


@mcp.tool()
async def preview_figma_components(
    file_url: str,
    component_filter: Optional[str] = None,
    max_results: int = 20
) -> Dict[str, Any]:
    """
    Preview components from a Figma file without generating files (fast preview)
    
    Args:
        file_url: Figma file URL or file key
        component_filter: Optional filter for component names (e.g. "Button", "Card")
        max_results: Maximum number of components to return (default 20 for speed)
        
    Returns:
        List of components with metadata for preview
    """
    try:
        file_key = extract_file_key(file_url)
        
        # Get file info first (fast)
        file_info = await figma_client.get_file_info(file_key)
        
        # Get components from Figma (this is the slow part)
        figma_data = await figma_client.get_file_components(file_key)
        components = figma_data.get("components", {})
        
        component_list = []
        processed_count = 0
        total_components = len(components)
        
        # Process components with early exit for speed
        for node_id, component_data in components.items():
            # Stop if we hit the max results limit
            if processed_count >= max_results:
                break
                
            try:
                component_name = component_data.get("name", "")
                
                # Apply filter if provided
                if component_filter and component_filter.lower() not in component_name.lower():
                    continue
                
                # Simple mapping without complex processing
                component_list.append({
                    "name": component_name,
                    "node_id": node_id,
                    "figma_url": f"https://www.figma.com/design/{file_key}?node-id={node_id}",
                    "description": component_data.get("description", "")
                })
                processed_count += 1
                
            except Exception as e:
                logger.warning(f"Error processing component {node_id}: {str(e)}")
        
        filter_message = f" matching '{component_filter}'" if component_filter else ""
        limit_message = f" (showing first {max_results})" if processed_count >= max_results else ""
        
        return {
            "status": "success",
            "file_info": {
                "name": file_info.get("name", "Unknown"),
                "key": file_key,
                "total_components": total_components,
                "filtered_components": processed_count
            },
            "components": component_list,
            "message": f"✅ Found {processed_count} components{filter_message}{limit_message}"
        }
        
    except Exception as e:
        logger.error(f"Error previewing components: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "message": f"❌ Failed to preview components: {str(e)}"
        }


@mcp.tool()
async def generate_component_from_figma(
    file_url: str,
    component_name: str,
    output_directory: str = "generated_components"
) -> Dict[str, Any]:
    """
    Generate React component files directly from Figma component
    
    Args:
        file_url: Figma file URL or file key
        component_name: Specific component name to generate
        output_directory: Directory to write generated files
        
    Returns:
        Generation result with created files
    """
    try:
        file_key = extract_file_key(file_url)
        
        # Get components from Figma
        figma_data = await figma_client.get_file_components(file_key)
        components = figma_data.get("components", {})
        
        # Find the specific component
        target_component = None
        target_node_id = None
        
        for node_id, component_data in components.items():
            if component_data.get("name", "").lower() == component_name.lower():
                target_component = component_data
                target_node_id = node_id
                break
        
        if not target_component:
            return {
                "status": "error",
                "error": f"Component '{component_name}' not found in Figma file"
            }
        
        # Get full node data
        node_data = await figma_client.get_node_data(file_key, target_node_id)
        
        # Normalize the component data
        normalized = normalizer.normalize_component(node_data)
        
        # Map to ShadCN component
        shadcn_mapping = component_mapper.map_component(normalized)
        
        # Extract design tokens
        design_tokens = normalizer.extract_design_tokens(node_data)
        
        # Prepare component data for file generation
        component_data = {
            "name": component_name,
            "node_id": target_node_id,
            "component_type": shadcn_mapping["type"],
            "shadcn_component": shadcn_mapping["component"],
            "json_layout": normalized,
            "design_tokens": design_tokens,
            "figma_url": f"https://www.figma.com/file/{file_key}?node-id={target_node_id}"
        }
        
        # Generate files
        result = file_generator.generate_component_file(component_data, output_directory)
        
        if result["success"]:
            return {
                "status": "success",
                "component": result["component_name"],
                "files_created": result["files_created"],
                "output_directory": result["output_directory"],
                "message": f"Successfully generated component '{component_name}'"
            }
        else:
            return {
                "status": "error",
                "error": result["error"]
            }
        
    except Exception as e:
        logger.error(f"Error generating component: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
async def batch_generate_components(
    file_url: str,
    component_filter: Optional[str] = None,
    output_directory: str = "generated_components",
    max_components: int = 10
) -> Dict[str, Any]:
    """
    Generate multiple React components from a Figma file
    
    Args:
        file_url: Figma file URL or file key
        component_filter: Optional filter for component names (e.g. "Button", "Card")
        output_directory: Directory to write generated files
        max_components: Maximum number of components to generate
        
    Returns:
        Batch generation results with file list
    """
    try:
        file_key = extract_file_key(file_url)
        
        # Get file info
        file_info = await figma_client.get_file_info(file_key)
        
        # Get components from Figma
        figma_data = await figma_client.get_file_components(file_key)
        components = figma_data.get("components", {})
        
        # Process components
        component_data_list = []
        processed_count = 0
        
        for node_id, component_data in components.items():
            if processed_count >= max_components:
                break
                
            try:
                component_name = component_data.get("name", "")
                
                # Apply filter if provided
                if component_filter and component_filter.lower() not in component_name.lower():
                    continue
                
                # Get full node data
                node_data = await figma_client.get_node_data(file_key, node_id)
                
                # Normalize the component data
                normalized = normalizer.normalize_component(node_data)
                
                # Map to ShadCN component
                shadcn_mapping = component_mapper.map_component(normalized)
                
                # Extract design tokens
                design_tokens = normalizer.extract_design_tokens(node_data)
                
                # Prepare component data
                comp_data = {
                    "name": component_name,
                    "node_id": node_id,
                    "component_type": shadcn_mapping["type"],
                    "shadcn_component": shadcn_mapping["component"],
                    "json_layout": normalized,
                    "design_tokens": design_tokens,
                    "figma_url": f"https://www.figma.com/file/{file_key}?node-id={node_id}"
                }
                
                component_data_list.append(comp_data)
                processed_count += 1
                
            except Exception as e:
                logger.warning(f"Error processing component {node_id}: {str(e)}")
        
        # Generate all components
        batch_result = file_generator.batch_generate(component_data_list, output_directory)
        
        if batch_result["success"]:
            return {
                "status": "success",
                "file_info": {
                    "name": file_info.get("name", "Unknown"),
                    "key": file_key
                },
                "generated_count": batch_result["generated_count"],
                "error_count": batch_result["error_count"],
                "output_directory": batch_result["output_directory"],
                "results": batch_result["results"],
                "errors": batch_result.get("errors", []),
                "message": f"Generated {batch_result['generated_count']} components successfully"
            }
        else:
            return {
                "status": "error",
                "error": batch_result["error"]
            }
        
    except Exception as e:
        logger.error(f"Error in batch generation: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }


# ===================================================================
# RESOURCES - Design System Guidelines and Best Practices
# ===================================================================

@mcp.resource("figma://design-system/principles")
def design_system_principles() -> str:
    """Core design system principles for consistent component usage"""
    return """
# Design System Principles

## Component Selection Strategy
- **Analyze first**: Review available components before building
- **Reuse over recreate**: Always use existing components when possible
- **Consistency over creativity**: Maintain design system integrity
- **Progressive enhancement**: Start with base components, customize minimally

## Component Usage Guidelines
- Use the same Button component across the entire application
- Apply consistent spacing using design tokens
- Maintain typography hierarchy from the design system
- Colors should come from the defined palette only
- Never create custom components that duplicate existing ones

## Decision Framework
1. Check if component exists in Figma library first
2. Use exact component if available
3. Use closest variant and customize via props only
4. Document any new patterns for future standardization
"""

@mcp.resource("figma://component-catalog/best-practices")
def component_best_practices() -> str:
    """Best practices for working with Figma component catalog"""
    return """
# Component Catalog Best Practices

## Selection Process
1. **Preview first**: Use preview_figma_components to browse options
2. **Filter smart**: Use component_filter to find relevant components
3. **Generate selectively**: Only pull in components you'll actually use
4. **Document decisions**: Record why certain components were chosen

## Naming Conventions
- Use semantic naming: primary-button, secondary-button
- Follow BEM methodology where applicable
- Maintain consistent naming across variants
- Group related components logically

## File Organization
```
components/
├── ui/
│   ├── Button/         # All button variants
│   ├── Card/           # All card variants
│   └── Input/          # All input variants
└── composite/          # App-specific combinations
```

## Quality Standards
- All components must include TypeScript types
- Props should follow ShadCN conventions
- Accessibility attributes required
- Responsive design built-in
"""

@mcp.resource("figma://development/workflow")
def development_workflow() -> str:
    """Recommended development workflow using Figma components"""
    return """
# Figma-to-Code Development Workflow

## Phase 1: Analysis & Planning
1. Analyze application requirements
2. Preview available Figma components
3. Map app features to design system components
4. Create component selection plan

## Phase 2: Component Generation
1. Generate only needed components (typically 10-20, not all 979)
2. Organize in logical folder structure
3. Validate generated code quality
4. Test component integration

## Phase 3: Application Development
1. Import and use generated components
2. Apply consistent theming via CSS variables
3. Customize through props, not direct CSS modification
4. Build composite components from base components

## Phase 4: Maintenance
1. Monitor for design system updates
2. Re-generate components when Figma updates
3. Maintain consistency across application
4. Document custom patterns

## Example Component Usage
```typescript
// ✅ Correct - Consistent usage
<Button variant="primary" size="lg">Main Action</Button>
<Button variant="secondary" size="md">Secondary Action</Button>

// ❌ Incorrect - Creating custom buttons
<CustomButton customStyle={{...}}>Don't do this</CustomButton>
```
"""

# ===================================================================
# PROMPTS - AI Guidance for Design System Usage
# ===================================================================

@mcp.prompt
def analyze_component_needs(app_description: str) -> str:
    """
    Analyze application requirements and recommend component selection
    
    Args:
        app_description: Description of the application being built
    """
    return f"""
You are a Design System Architect analyzing component needs for: {app_description}

Your task is to:
1. Identify the core UI patterns needed for this application
2. Map requirements to available Figma components
3. Recommend a minimal, focused component library
4. Ensure design consistency and reusability

Guidelines:
- Prefer fewer, reusable components over many specific ones
- Consider all user interaction patterns
- Think about responsive design needs
- Plan for accessibility requirements
- Optimize for developer experience

Provide a structured analysis with:
- Required component types
- Recommended Figma components to generate
- Usage patterns and conventions
- Potential customization needs
"""

@mcp.prompt
def component_selection_guide() -> str:
    """Guide for selecting the right components from the Figma library"""
    return """
You are a Component Selection Expert helping choose the optimal components from a 979-component Figma design library.

Your expertise:
- Understanding design system hierarchies
- Identifying reusable patterns
- Avoiding component proliferation
- Maintaining design consistency

Selection criteria:
1. **Frequency of use**: Prioritize components used multiple times
2. **Base vs variants**: Start with base components, add variants as needed
3. **Composition**: Choose components that work well together
4. **Scalability**: Select components that adapt to different contexts
5. **Accessibility**: Ensure components meet WCAG standards

Process:
1. Preview available components first
2. Identify 10-15 core components maximum
3. Generate only what's immediately needed
4. Plan for progressive enhancement
5. Document selection rationale

Remember: A focused, consistent component library is more valuable than a comprehensive but overwhelming one.
"""

@mcp.prompt
def design_system_consistency(component_type: str, usage_context: str) -> str:
    """
    Ensure consistent usage of design system components
    
    Args:
        component_type: Type of component being used (Button, Card, etc.)
        usage_context: Where/how the component will be used
    """
    return f"""
You are a Design System Consistency Guardian ensuring proper usage of {component_type} components in: {usage_context}

Your role:
- Enforce design system rules and patterns
- Prevent design inconsistencies
- Guide proper component implementation
- Maintain visual and behavioral consistency

For {component_type} components, ensure:
1. **Visual consistency**: Same styling patterns across all instances
2. **Behavioral consistency**: Same interaction patterns everywhere
3. **Semantic consistency**: Same meanings for same visual treatments
4. **Responsive consistency**: Same breakpoint behaviors
5. **Accessibility consistency**: Same ARIA patterns and keyboard navigation

Implementation checklist:
- Use exact same component, customize via props only
- Apply consistent spacing using design tokens
- Maintain typography hierarchy
- Use defined color palette only
- Follow established interaction patterns
- Implement proper accessibility attributes

Context: {usage_context}
Expected outcome: Seamless, consistent user experience across the entire application.
"""

# ===================================================================
# TOOLS - Existing tool definitions continue below
# ===================================================================

# Health check endpoint
@mcp.tool()
async def health_check() -> Dict[str, Any]:
    """
    Check health status of Figma MCP server with detailed diagnostics
    
    Returns:
        Comprehensive health status including:
        - Server status
        - Figma API connectivity
        - Configuration validation
        - Error details if any
    """
    status = {
        "server": "healthy",
        "version": "2.0.0-streamlined",
        "architecture": "direct-api-to-file",
        "environment": {
            "debug_mode": DEBUG,
            "python_version": sys.version.split()[0],
            "port": int(os.getenv("FIGMA_MCP_PORT", "8031"))
        },
        "figma_api": {
            "status": "unknown",
            "token_format": "unknown",
            "user": None,
            "error": None
        },
        "file_system": {
            "status": "unknown",
            "write_permissions": False,
            "error": None
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    # Validate Figma token format
    if FIGMA_TOKEN:
        token_prefix = FIGMA_TOKEN[:5] if len(FIGMA_TOKEN) > 5 else FIGMA_TOKEN
        if FIGMA_TOKEN.startswith(('figd_', 'figp_')):
            status["figma_api"]["token_format"] = "valid"
        else:
            status["figma_api"]["token_format"] = f"unusual (starts with '{token_prefix}')"
    
    # Check Figma API connectivity
    try:
        logger.debug("Testing Figma API connection...")
        user = await figma_client.get_current_user()
        status["figma_api"]["status"] = "connected"
        status["figma_api"]["user"] = {
            "email": user.get("email", "Unknown"),
            "handle": user.get("handle", "Unknown"),
            "id": user.get("id", "Unknown")
        }
        logger.info("Figma API connection successful")
    except Exception as e:
        error_msg = str(e)
        status["figma_api"]["status"] = "error"
        status["figma_api"]["error"] = error_msg
        
        # Provide helpful error context
        if "401" in error_msg or "unauthorized" in error_msg.lower():
            status["figma_api"]["error_hint"] = "Invalid or expired token. Please check your FIGMA_PAT or FIGMA_ACCESS_TOKEN"
        elif "403" in error_msg or "forbidden" in error_msg.lower():
            status["figma_api"]["error_hint"] = "Token lacks required permissions. Ensure it has 'File content' scope"
        elif "network" in error_msg.lower() or "connection" in error_msg.lower():
            status["figma_api"]["error_hint"] = "Network connectivity issue. Check internet connection"
        else:
            status["figma_api"]["error_hint"] = "Unexpected error. Check logs for details"
        
        logger.error("Figma API connection failed: %s", error_msg)
    
    # Check file system write permissions
    try:
        import tempfile
        test_dir = "health_check_test"
        os.makedirs(test_dir, exist_ok=True)
        test_file = os.path.join(test_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        os.rmdir(test_dir)
        
        status["file_system"]["status"] = "writable"
        status["file_system"]["write_permissions"] = True
        logger.debug("File system write permissions confirmed")
    except Exception as e:
        error_msg = str(e)
        status["file_system"]["status"] = "error"
        status["file_system"]["error"] = error_msg
        status["file_system"]["error_hint"] = "Cannot write files. Check directory permissions"
        logger.error("File system write test failed: %s", error_msg)
    
    # Overall health assessment
    if status["figma_api"]["status"] == "connected" and status["file_system"]["status"] == "writable":
        status["overall_status"] = "healthy"
        status["message"] = "All systems operational - ready for direct file generation"
    elif status["figma_api"]["status"] == "connected":
        status["overall_status"] = "degraded"
        status["message"] = "Figma API connected but file system issues detected"
    else:
        status["overall_status"] = "unhealthy"
        status["message"] = "Critical services are down"
    
    return status


if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv("FIGMA_MCP_PORT", "8031"))
    
    logger.info(f"Starting Figma MCP server on port {port}")
    logger.info("Available tools:")
    try:
        tools = mcp._list_tools()
        for tool in tools:
            logger.info(f"  - {tool.name}: {tool.description}")
    except Exception as e:
        logger.info(f"Could not list tools: {e}")
        logger.info("Server starting anyway...")
    
    # Run with streamable-http transport for proper MCP compatibility
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)