#!/usr/bin/env python3
"""
File Generator for Figma-to-Code workflow
Handles direct generation of React/TypeScript files from Figma components
"""

import os
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class FileGenerator:
    """Generates React/TypeScript files directly from Figma component data"""
    
    def __init__(self):
        self.output_base = "generated_components"
    
    def generate_component_file(
        self, 
        component_data: Dict[str, Any], 
        output_directory: str,
        file_format: str = "tsx"
    ) -> Dict[str, Any]:
        """
        Generate a React component file from Figma component data
        
        Args:
            component_data: Normalized component data from Figma
            output_directory: Directory to write files to
            file_format: File format (tsx, jsx, ts, js)
            
        Returns:
            Generation result with file paths and metadata
        """
        try:
            # Ensure output directory exists
            output_path = Path(output_directory)
            output_path.mkdir(parents=True, exist_ok=True)
            
            component_name = component_data.get("name", "UnknownComponent")
            safe_name = self.sanitize_component_name(component_name)
            
            # Generate file content
            file_content = self.generate_tsx_content(component_data, safe_name)
            
            # Write component file
            file_path = output_path / f"{safe_name}.{file_format}"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            # Generate types file if needed
            types_content = self.generate_types_content(component_data, safe_name)
            types_path = output_path / f"{safe_name}.types.ts"
            with open(types_path, 'w', encoding='utf-8') as f:
                f.write(types_content)
            
            # Generate metadata file
            metadata = {
                "figma_component": component_name,
                "generated_name": safe_name,
                "figma_url": component_data.get("figma_url", ""),
                "shadcn_component": component_data.get("shadcn_component", ""),
                "component_type": component_data.get("component_type", ""),
                "design_tokens": component_data.get("design_tokens", {}),
                "generated_at": os.popen("date -Iseconds").read().strip()
            }
            
            metadata_path = output_path / f"{safe_name}.meta.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            return {
                "success": True,
                "component_name": safe_name,
                "files_created": [
                    str(file_path),
                    str(types_path),
                    str(metadata_path)
                ],
                "output_directory": str(output_path)
            }
            
        except Exception as e:
            logger.error(f"Error generating component file: {e}")
            return {
                "success": False,
                "error": str(e),
                "component_name": component_data.get("name", "Unknown")
            }
    
    def sanitize_component_name(self, name: str) -> str:
        """Convert Figma component name to valid React component name"""
        # Remove special characters, convert to PascalCase
        import re
        # Remove non-alphanumeric chars except spaces and slashes
        clean = re.sub(r'[^a-zA-Z0-9\s/]', '', name)
        # Split on spaces or slashes and capitalize each part
        parts = re.split(r'[\s/]+', clean)
        return ''.join(word.capitalize() for word in parts if word)
    
    def generate_tsx_content(self, component_data: Dict[str, Any], component_name: str) -> str:
        """Generate TSX file content for React component"""
        
        shadcn_component = component_data.get("shadcn_component", "div")
        design_tokens = component_data.get("design_tokens", {})
        
        # Basic ShadCN imports based on component type
        imports = self.get_shadcn_imports(shadcn_component)
        
        # Generate props interface
        props_interface = self.generate_props_interface(component_data, component_name)
        
        # Generate component implementation
        component_impl = self.generate_component_implementation(
            component_data, component_name, shadcn_component
        )
        
        return f'''import React from 'react';
{imports}
import {{ cn }} from '@/lib/utils';
import {{ {component_name}Props }} from './{component_name}.types';

{props_interface}

export const {component_name}: React.FC<{component_name}Props> = ({{
  className,
  children,
  ...props
}}) => {{
{component_impl}
}};

export default {component_name};
'''
    
    def generate_types_content(self, component_data: Dict[str, Any], component_name: str) -> str:
        """Generate TypeScript types file"""
        
        return f'''export interface {component_name}Props {{
  className?: string;
  children?: React.ReactNode;
  // Add specific props based on Figma component properties
}}

export interface {component_name}Tokens {{
  // Design tokens from Figma
  {self.format_design_tokens(component_data.get("design_tokens", {}))}
}}
'''
    
    def get_shadcn_imports(self, shadcn_component: str) -> str:
        """Get appropriate ShadCN imports based on component type"""
        import_map = {
            "button": "import { Button } from '@/components/ui/button';",
            "card": "import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';",
            "input": "import { Input } from '@/components/ui/input';",
            "select": "import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';",
            "checkbox": "import { Checkbox } from '@/components/ui/checkbox';",
            "badge": "import { Badge } from '@/components/ui/badge';",
            "avatar": "import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';",
        }
        
        return import_map.get(shadcn_component.lower() if shadcn_component else "", "")
    
    def generate_props_interface(self, component_data: Dict[str, Any], component_name: str) -> str:
        """Generate props interface based on component data"""
        # This could be enhanced to parse actual Figma component properties
        return f"// Props interface defined in {component_name}.types.ts"
    
    def generate_component_implementation(
        self, 
        component_data: Dict[str, Any], 
        component_name: str, 
        shadcn_component: str
    ) -> str:
        """Generate the actual component implementation"""
        
        # Basic implementation - could be enhanced with actual layout parsing
        if shadcn_component == "button":
            return '''  return (
    <Button
      className={cn("", className)}
      {...props}
    >
      {children}
    </Button>
  );'''
        
        elif shadcn_component == "card":
            return '''  return (
    <Card className={cn("", className)} {...props}>
      <CardHeader>
        <CardTitle>{children}</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Component content */}
      </CardContent>
    </Card>
  );'''
        
        else:
            return f'''  return (
    <div className={{cn("", className)}} {{...props}}>
      {{children}}
    </div>
  );'''
    
    def format_design_tokens(self, tokens: Dict[str, Any]) -> str:
        """Format design tokens for TypeScript interface"""
        if not tokens:
            return "// No design tokens available"
        
        formatted = []
        for key, value in tokens.items():
            formatted.append(f"  {key}: '{value}';")
        
        return "\n".join(formatted)
    
    def batch_generate(
        self, 
        components: List[Dict[str, Any]], 
        output_directory: str
    ) -> Dict[str, Any]:
        """Generate multiple components in batch"""
        try:
            results = []
            errors = []
            
            for component in components:
                result = self.generate_component_file(component, output_directory)
                if result["success"]:
                    results.append(result)
                else:
                    errors.append(result)
            
            # Generate index file
            self.generate_index_file(results, output_directory)
            
            return {
                "success": True,
                "generated_count": len(results),
                "error_count": len(errors),
                "results": results,
                "errors": errors,
                "output_directory": output_directory
            }
            
        except Exception as e:
            logger.error(f"Error in batch generation: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_index_file(self, results: List[Dict[str, Any]], output_directory: str):
        """Generate index.ts file for easy imports"""
        try:
            output_path = Path(output_directory)
            index_content = "// Auto-generated component exports\n\n"
            
            for result in results:
                component_name = result["component_name"]
                index_content += f"export {{ {component_name} }} from './{component_name}';\n"
            
            index_path = output_path / "index.ts"
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
                
            logger.info(f"Generated index file: {index_path}")
            
        except Exception as e:
            logger.error(f"Error generating index file: {e}")