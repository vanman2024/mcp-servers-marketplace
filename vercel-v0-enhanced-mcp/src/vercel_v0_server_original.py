#!/usr/bin/env python3
"""
Vercel v0 MCP Server - HTTP Implementation
Provides UI component generation capabilities using Vercel's v0 API

Uses OpenAI SDK with custom base URL for v0 API access
Implemented with FastMCP for HTTP serving
"""

import os
import json
import asyncio
import logging
import re
import subprocess
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

# FastMCP for HTTP serving
from fastmcp import FastMCP

# OpenAI SDK for v0 API
from openai import AsyncOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple rate limiter for API calls"""
    def __init__(self, calls_per_minute: int = 10):
        self.calls_per_minute = calls_per_minute
        self.calls = []
        self.lock = asyncio.Lock()
    
    async def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        async with self.lock:
            now = time.time()
            # Remove calls older than 1 minute
            self.calls = [call_time for call_time in self.calls if now - call_time < 60]
            
            if len(self.calls) >= self.calls_per_minute:
                # Calculate wait time
                oldest_call = self.calls[0]
                wait_time = 60 - (now - oldest_call) + 1
                logger.info(f"Rate limit reached, waiting {wait_time:.1f} seconds")
                await asyncio.sleep(wait_time)
                # Clean up old calls again
                now = time.time()
                self.calls = [call_time for call_time in self.calls if now - call_time < 60]
            
            # Record this call
            self.calls.append(now)


class V0ComponentGenerator:
    """Handles component generation using v0 API"""
    
    def __init__(self, api_key: str, rate_limit: int = 10):
        if not api_key:
            raise ValueError("V0 API key is required")
        if not api_key.startswith(('v0_', 'v1:')):
            logger.warning("API key doesn't match expected v0 format (v0_* or v1:*)")
        
        self.api_key = api_key
        self.rate_limiter = RateLimiter(calls_per_minute=rate_limit)
        self.retry_attempts = 3
        self.retry_delay = 5  # seconds
        
        # v0 uses OpenAI SDK with custom base URL
        try:
            self.client = AsyncOpenAI(
                api_key=api_key,
                base_url='https://api.v0.dev/v1',
                timeout=60.0  # 60 second timeout
            )
        except Exception as e:
            logger.error(f"Failed to initialize v0 client: {e}")
            raise ValueError(f"Failed to initialize v0 API client: {str(e)}")
    
    async def generate_component(
        self, 
        prompt: str, 
        tech_stack: Optional[Dict[str, str]] = None,
        stream: bool = True
    ) -> Dict[str, Any]:
        """Generate a UI component using v0 API"""
        
        # Validate inputs
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        if len(prompt) > 10000:
            raise ValueError("Prompt is too long (max 10000 characters)")
        
        # Default tech stack if not provided
        if not tech_stack:
            tech_stack = {
                "framework": "Next.js 14 App Router",
                "language": "TypeScript",
                "styling": "Tailwind CSS",
                "ui_library": "shadcn/ui",
                "state": "React hooks"
            }
        else:
            # Validate tech stack
            valid_frameworks = ["Next.js 14 App Router", "Next.js 13", "React", "Remix", "Gatsby"]
            valid_languages = ["TypeScript", "JavaScript"]
            valid_styling = ["Tailwind CSS", "CSS Modules", "Styled Components", "Emotion", "CSS"]
            valid_ui_libraries = ["shadcn/ui", "Material-UI", "Chakra UI", "Ant Design", "None"]
            
            framework = tech_stack.get("framework", "Next.js 14 App Router")
            if framework not in valid_frameworks:
                logger.warning(f"Unknown framework: {framework}, using default")
                tech_stack["framework"] = "Next.js 14 App Router"
            
            language = tech_stack.get("language", "TypeScript")
            if language not in valid_languages:
                logger.warning(f"Unknown language: {language}, using TypeScript")
                tech_stack["language"] = "TypeScript"
        
        # Build the system prompt
        system_prompt = """You are v0, an expert at building modern web applications. 
Generate production-ready React/TypeScript components with the specified tech stack.
Always include proper TypeScript types and follow best practices."""
        
        # Build the user prompt with tech stack details
        full_prompt = f"""Create a component with the following specifications:

{prompt}

Tech Stack:
- Framework: {tech_stack.get('framework', 'Next.js 14 App Router')}
- Language: {tech_stack.get('language', 'TypeScript')}
- Styling: {tech_stack.get('styling', 'Tailwind CSS')}
- UI Library: {tech_stack.get('ui_library', 'shadcn/ui')}
- State Management: {tech_stack.get('state', 'React hooks')}

Requirements:
- Follow accessibility best practices
- Make it responsive
- Include proper TypeScript types
- Use modern React patterns
- Include comments explaining complex logic
- IMPORTANT: Generate ONLY the component code, no markdown explanations
- IMPORTANT: Use consistent indentation (2 spaces)
- IMPORTANT: If using external UI libraries, use only the ones specified in the tech stack"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt}
        ]
        
        try:
            if stream:
                return await self._generate_streaming(messages)
            else:
                return await self._generate_regular(messages)
        except Exception as e:
            logger.error(f"v0 generation failed: {e}")
            raise
    
    async def _generate_streaming(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Generate component with streaming and retry logic"""
        for attempt in range(self.retry_attempts):
            try:
                # Apply rate limiting
                await self.rate_limiter.wait_if_needed()
                
                stream = await self.client.chat.completions.create(
                    model='v0-1.5-md',  # Updated to newer model
                    messages=messages,
                    stream=True,
                    max_tokens=4000,
                    temperature=0.7
                )
            
                full_content = ''
                generation_id = ''
                chunk_count = 0
                
                async for chunk in stream:
                    chunk_count += 1
                    if chunk.id:
                        generation_id = chunk.id
                    # Check if choices exist and have content
                    if hasattr(chunk, 'choices') and chunk.choices and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta
                        if hasattr(delta, 'content') and delta.content:
                            full_content += delta.content
                
                logger.info(f"Received {chunk_count} chunks, total content length: {len(full_content)}")
                
                if not full_content:
                    raise ValueError("No content received from v0 API streaming response")
                
                # Parse and validate the generated code
                files = self._parse_generated_code(full_content)
                if not files:
                    logger.warning("No valid code files extracted from v0 response")
                
                return {
                    "content": full_content,
                    "generation_id": generation_id,
                    "files": files,
                    "streaming": True
                }
            except asyncio.TimeoutError:
                if attempt < self.retry_attempts - 1:
                    logger.warning(f"v0 API timeout on attempt {attempt + 1}, retrying...")
                    await asyncio.sleep(self.retry_delay)
                    continue
                logger.error("v0 API request timed out after all retries")
                raise ValueError("v0 API request timed out - please try again")
            except Exception as e:
                if attempt < self.retry_attempts - 1 and "rate" in str(e).lower():
                    logger.warning(f"Rate limit error on attempt {attempt + 1}, retrying after delay...")
                    await asyncio.sleep(self.retry_delay * 2)  # Longer delay for rate limits
                    continue
                elif attempt < self.retry_attempts - 1:
                    logger.warning(f"Generation failed on attempt {attempt + 1}: {e}")
                    await asyncio.sleep(self.retry_delay)
                    continue
                else:
                    logger.error(f"Streaming generation failed after {self.retry_attempts} attempts: {e}")
                    # Fallback to non-streaming
                    logger.info("Falling back to non-streaming generation")
                    return await self._generate_regular(messages)
    
    async def _generate_regular(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Generate component without streaming"""
        try:
            completion = await self.client.chat.completions.create(
                model='v0-1.5-md',  # Updated to newer model
                messages=messages,
                stream=False,
                max_tokens=4000,
                temperature=0.7
            )
            
            # Check if choices exist
            if not completion.choices or len(completion.choices) == 0:
                raise ValueError("No choices returned from v0 API")
            
            if not completion.choices[0].message or not completion.choices[0].message.content:
                raise ValueError("No content in v0 API response")
            
            content = completion.choices[0].message.content
            
            logger.info(f"Non-streaming response length: {len(content)}")
            
            # Parse and validate the generated code
            files = self._parse_generated_code(content)
            if not files:
                logger.warning("No valid code files extracted from v0 response")
            
            return {
                "content": content,
                "generation_id": completion.id,
                "files": files,
                "streaming": False
            }
        except asyncio.TimeoutError:
            logger.error("v0 API request timed out")
            raise ValueError("v0 API request timed out - please try again")
        except Exception as e:
            logger.error(f"Non-streaming generation failed: {e}")
            raise ValueError(f"Failed to generate component: {str(e)}")
    
    def _parse_generated_code(self, code: str) -> List[Dict[str, str]]:
        """Parse generated code to extract multiple files if present"""
        files = []
        
        # Log the raw response for debugging
        logger.info(f"Raw v0 response length: {len(code)} characters")
        logger.debug(f"Raw v0 response first 500 chars: {code[:500]}")
        
        # First, try to extract code from markdown code blocks
        # Updated pattern to handle file markers in code blocks
        # Pattern: ```language file="path/to/file.ext"\ncode\n```
        # Also handle variations like ```tsx file="components/ui/loading-spinner.tsx"
        code_block_with_file_regex = r'```(?:tsx?|jsx?|typescript|javascript|ts|js|css|json)?\s*(?:file=["\'`]([^"\'`]+)["\'`])?\s*\n([\s\S]*?)```'
        matches = re.finditer(code_block_with_file_regex, code, re.MULTILINE)
        
        code_blocks = []
        for match in matches:
            file_path = match.group(1)  # May be None if no file attribute
            code_content = match.group(2)
            
            if file_path:
                # Extract just the filename from the path
                filename = file_path.split('/')[-1]
                files.append({
                    "name": filename,
                    "content": code_content.rstrip('\n'),
                    "path": file_path
                })
                logger.info(f"Found code block with file marker: {file_path}")
            else:
                code_blocks.append(code_content)
        
        # If we found files with paths, return them
        if files:
            logger.info(f"Found {len(files)} files with explicit paths")
            return files
        
        # If we have code blocks without file markers
        if code_blocks:
            logger.info(f"Found {len(code_blocks)} code blocks without file markers")
            extracted_code = '\n\n'.join(code_blocks)
        else:
            logger.info("No code blocks found, checking for raw code")
            # Check if the response contains code without markdown blocks
            # Skip any leading explanation text
            lines = code.split('\n')
            code_start = 0
            for i, line in enumerate(lines):
                # Look for typical code start patterns
                if (line.strip().startswith(('import ', 'export ', 'const ', 'function ', 'class ', '//')) or
                    line.strip() == '' and i > 0 and lines[i-1].strip() != ''):
                    code_start = i
                    break
            
            if code_start > 0:
                extracted_code = '\n'.join(lines[code_start:])
                logger.info(f"Extracted code starting from line {code_start}")
            else:
                extracted_code = code
        
        # Check for multiple file markers in the extracted code
        # Pattern: // File: path/to/file.ext
        file_regex = r'^// File: (.+)$'
        lines = extracted_code.split('\n')
        current_file = None
        current_content = []
        
        for line in lines:
            file_match = re.match(file_regex, line)
            if file_match:
                # Save previous file if exists
                if current_file and current_content:
                    content = '\n'.join(current_content).rstrip('\n')
                    if content:  # Only add if there's actual content
                        files.append({
                            "name": current_file.split('/')[-1],
                            "content": content,
                            "path": current_file
                        })
                # Start new file
                current_file = file_match.group(1).strip()
                current_content = []
                logger.info(f"Found file marker: {current_file}")
            elif current_file is not None:
                current_content.append(line)
        
        # Save the last file
        if current_file and current_content:
            content = '\n'.join(current_content).rstrip('\n')
            if content:
                files.append({
                    "name": current_file.split('/')[-1],
                    "content": content,
                    "path": current_file
                })
        
        # If no file markers found, treat entire code as single component
        if not files and extracted_code.strip():
            # Try to extract component name from code - check multiple patterns
            component_name = 'Component'
            
            # Pattern 1: export default function/const ComponentName
            match1 = re.search(r'export (?:default )?(?:function|const) (\w+)', extracted_code)
            if match1:
                component_name = match1.group(1)
            else:
                # Pattern 2: const ComponentName = React.forwardRef
                match2 = re.search(r'const (\w+) = React\.forwardRef', extracted_code)
                if match2:
                    component_name = match2.group(1)
                else:
                    # Pattern 3: export { ComponentName
                    match3 = re.search(r'export \{ (\w+)', extracted_code)
                    if match3:
                        component_name = match3.group(1)
                    else:
                        # Pattern 4: function ComponentName() or const ComponentName = () =>
                        match4 = re.search(r'(?:function|const) (\w+)\s*(?:\(|=)', extracted_code)
                        if match4:
                            component_name = match4.group(1)
            
            # Clean up any trailing markdown backticks
            cleaned_code = extracted_code.rstrip('\n')
            if cleaned_code.endswith('```'):
                cleaned_code = cleaned_code[:-3].rstrip('\n')
            
            files.append({
                "name": f"{component_name}.tsx",
                "content": cleaned_code,
                "path": f"components/{component_name}.tsx"
            })
            logger.info(f"Created single file: {component_name}.tsx")
        
        return files


class ProjectAnalyzer:
    """Analyzes existing projects to understand dependencies and setup"""
    
    def __init__(self, project_path: str = None):
        self.project_path = Path(project_path) if project_path else Path.cwd()
        
    def analyze_project(self) -> Dict[str, Any]:
        """Analyze the current project structure and dependencies"""
        analysis = {
            "framework": self._detect_framework(),
            "dependencies": self._get_dependencies(),
            "styling": self._detect_styling(),
            "ui_libraries": self._detect_ui_libraries(),
            "typescript": self._has_typescript(),
            "structure": self._analyze_structure(),
            "existing_components": self._find_components()
        }
        return analysis
    
    def _detect_framework(self) -> str:
        """Detect the frontend framework being used"""
        package_json = self.project_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                    
                    if "next" in deps:
                        # Check if it's App Router or Pages Router
                        if (self.project_path / "app").exists():
                            return "Next.js 14 App Router"
                        else:
                            return "Next.js Pages Router"
                    elif "react" in deps:
                        if "vite" in deps:
                            return "React with Vite"
                        else:
                            return "Create React App"
                    elif "vue" in deps:
                        return "Vue.js"
                    elif "svelte" in deps:
                        return "SvelteKit"
            except:
                pass
        return "Unknown"
    
    def _get_dependencies(self) -> Dict[str, str]:
        """Get all project dependencies"""
        package_json = self.project_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    return {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            except:
                pass
        return {}
    
    def _detect_styling(self) -> List[str]:
        """Detect styling frameworks/libraries"""
        deps = self._get_dependencies()
        styling = []
        
        if "tailwindcss" in deps:
            styling.append("Tailwind CSS")
        if "styled-components" in deps:
            styling.append("Styled Components")
        if "@emotion/react" in deps or "@emotion/styled" in deps:
            styling.append("Emotion")
        if "sass" in deps or "node-sass" in deps:
            styling.append("SASS")
        if "postcss" in deps:
            styling.append("PostCSS")
            
        return styling or ["CSS"]
    
    def _detect_ui_libraries(self) -> List[str]:
        """Detect UI component libraries"""
        deps = self._get_dependencies()
        ui_libs = []
        
        if "@radix-ui/react-slot" in deps or "class-variance-authority" in deps:
            ui_libs.append("shadcn/ui")
        if "@mui/material" in deps:
            ui_libs.append("Material-UI")
        if "antd" in deps:
            ui_libs.append("Ant Design")
        if "@chakra-ui/react" in deps:
            ui_libs.append("Chakra UI")
        if "react-bootstrap" in deps:
            ui_libs.append("React Bootstrap")
        if "@mantine/core" in deps:
            ui_libs.append("Mantine")
            
        return ui_libs
    
    def _has_typescript(self) -> bool:
        """Check if project uses TypeScript"""
        deps = self._get_dependencies()
        return "typescript" in deps or (self.project_path / "tsconfig.json").exists()
    
    def _analyze_structure(self) -> Dict[str, Any]:
        """Analyze project structure"""
        structure = {
            "has_components_dir": (self.project_path / "components").exists(),
            "has_pages_dir": (self.project_path / "pages").exists(),
            "has_app_dir": (self.project_path / "app").exists(),
            "has_src_dir": (self.project_path / "src").exists(),
            "has_lib_dir": (self.project_path / "lib").exists(),
            "has_utils_dir": (self.project_path / "utils").exists()
        }
        return structure
    
    def _find_components(self) -> List[str]:
        """Find existing component files"""
        components = []
        
        # Common component directories
        search_dirs = ["components", "src/components", "app/components"]
        
        for dir_name in search_dirs:
            comp_dir = self.project_path / dir_name
            if comp_dir.exists():
                for file in comp_dir.rglob("*.tsx"):
                    components.append(str(file.relative_to(self.project_path)))
                for file in comp_dir.rglob("*.jsx"):
                    components.append(str(file.relative_to(self.project_path)))
                    
        return components[:20]  # Limit to first 20 components
    
    def get_required_dependencies(self, tech_stack: Dict[str, str]) -> Dict[str, str]:
        """Get required dependencies based on tech stack"""
        deps = {}
        
        # Core React/Next.js dependencies
        if "Next.js" in tech_stack.get("framework", ""):
            deps["next"] = "^14.0.0"
            deps["react"] = "^18.0.0"
            deps["react-dom"] = "^18.0.0"
        elif "React" in tech_stack.get("framework", ""):
            deps["react"] = "^18.0.0"
            deps["react-dom"] = "^18.0.0"
            
        # TypeScript
        if tech_stack.get("language") == "TypeScript":
            deps["typescript"] = "^5.0.0"
            deps["@types/react"] = "^18.0.0"
            deps["@types/react-dom"] = "^18.0.0"
            deps["@types/node"] = "^20.0.0"
            
        # Styling
        if "Tailwind" in tech_stack.get("styling", ""):
            deps["tailwindcss"] = "^3.4.0"
            deps["autoprefixer"] = "^10.4.0"
            deps["postcss"] = "^8.4.0"
            
        # UI Libraries
        ui_lib = tech_stack.get("ui_library", "")
        if "shadcn" in ui_lib:
            deps["@radix-ui/react-slot"] = "^1.0.0"
            deps["class-variance-authority"] = "^0.7.0"
            deps["clsx"] = "^2.0.0"
            deps["tailwind-merge"] = "^2.0.0"
            deps["lucide-react"] = "^0.400.0"
        elif "Material-UI" in ui_lib:
            deps["@mui/material"] = "^5.0.0"
            deps["@emotion/react"] = "^11.0.0"
            deps["@emotion/styled"] = "^11.0.0"
        elif "Chakra UI" in ui_lib:
            deps["@chakra-ui/react"] = "^2.0.0"
            deps["@emotion/react"] = "^11.0.0"
            deps["@emotion/styled"] = "^11.0.0"
            deps["framer-motion"] = "^10.0.0"
            
        return deps
    
    def check_missing_dependencies(self, required_deps: Dict[str, str]) -> List[str]:
        """Check which dependencies are missing from package.json"""
        current_deps = self._get_dependencies()
        missing = []
        
        for dep_name, version in required_deps.items():
            if dep_name not in current_deps:
                missing.append(f"{dep_name}@{version}")
                
        return missing
    
    def install_dependencies(self, missing_deps: List[str]) -> Dict[str, Any]:
        """Install missing dependencies using npm/yarn"""
        if not missing_deps:
            return {"success": True, "message": "No dependencies to install"}
            
        package_json = self.project_path / "package.json"
        if not package_json.exists():
            return {"success": False, "error": "No package.json found"}
            
        # Detect package manager
        if (self.project_path / "yarn.lock").exists():
            cmd = ["yarn", "add"] + missing_deps
        elif (self.project_path / "pnpm-lock.yaml").exists():
            cmd = ["pnpm", "add"] + missing_deps
        else:
            cmd = ["npm", "install"] + missing_deps
            
        try:
            result = subprocess.run(
                cmd, 
                cwd=self.project_path, 
                capture_output=True, 
                text=True, 
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "installed": missing_deps,
                    "output": result.stdout
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "attempted": missing_deps
                }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Installation timed out after 5 minutes",
                "attempted": missing_deps
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "attempted": missing_deps
            }
    
    def create_component_files(self, files: List[Dict[str, str]], target_dir: str = None) -> Dict[str, Any]:
        """Create component files in the project with enhanced validation"""
        if not files:
            return {
                "success": False,
                "errors": ["No files provided to create"],
                "created_files": []
            }
        
        # Validate target directory
        if not target_dir:
            # Auto-detect best location
            if (self.project_path / "src" / "components").exists():
                target_dir = "src/components"
            elif (self.project_path / "components").exists():
                target_dir = "components"
            elif (self.project_path / "app" / "components").exists():
                target_dir = "app/components"
            else:
                # Create components directory
                target_dir = "components"
                try:
                    (self.project_path / target_dir).mkdir(exist_ok=True)
                except Exception as e:
                    logger.error(f"Failed to create target directory: {e}")
                    return {
                        "success": False,
                        "errors": [f"Failed to create directory: {str(e)}"],
                        "created_files": []
                    }
        
        created_files = []
        errors = []
        
        for i, file_info in enumerate(files):
            if not isinstance(file_info, dict):
                errors.append({
                    "file": f"file_{i}",
                    "error": "Invalid file info format"
                })
                continue
                
            file_name = file_info.get("name", "Component.tsx")
            content = file_info.get("content", "")
            file_path_from_info = file_info.get("path", None)
            
            # Validate file name
            if not file_name or not isinstance(file_name, str):
                errors.append({
                    "file": f"file_{i}",
                    "error": "Invalid or missing file name"
                })
                continue
            
            # Security: Prevent directory traversal
            if ".." in file_name or ".." in str(file_path_from_info or ""):
                errors.append({
                    "file": file_name,
                    "error": "Invalid file path - directory traversal detected"
                })
                continue
            
            # Ensure proper file extension
            if not file_name.endswith(('.tsx', '.jsx', '.ts', '.js', '.css', '.json')):
                file_name += '.tsx'
            
            # Use the path from file_info if provided, otherwise use target_dir
            if file_path_from_info:
                # Handle paths that might start with / or ./
                clean_path = file_path_from_info.lstrip('./')
                # Additional validation
                if clean_path.startswith('/'):
                    errors.append({
                        "file": file_name,
                        "error": "Absolute paths not allowed"
                    })
                    continue
                file_path = self.project_path / clean_path
            else:
                file_path = self.project_path / target_dir / file_name
            
            try:
                # Create directory if it doesn't exist
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Log content info for debugging
                logger.info(f"Writing file {file_name} with {len(content)} characters")
                logger.debug(f"First 200 chars of content: {content[:200]}")
                
                # Write file with explicit UTF-8 encoding and Unix line endings
                with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
                    # Ensure consistent line endings
                    normalized_content = content.replace('\r\n', '\n').replace('\r', '\n')
                    f.write(normalized_content)
                
                # Verify file was created
                if file_path.exists():
                    created_files.append({
                        "name": file_name,
                        "path": str(file_path.relative_to(self.project_path)),
                        "absolute_path": str(file_path),
                        "size": len(content)
                    })
                    logger.info(f"Successfully created file: {file_path}")
                else:
                    errors.append({
                        "file": file_name,
                        "error": "File was not created (verification failed)"
                    })
                
            except Exception as e:
                logger.error(f"Failed to create file {file_name}: {e}")
                errors.append({
                    "file": file_name,
                    "error": str(e)
                })
        
        return {
            "success": len(errors) == 0,
            "created_files": created_files,
            "errors": errors,
            "target_directory": target_dir
        }


# Initialize FastMCP server
mcp = FastMCP("vercel-v0-original")

# Initialize v0 client - prioritize V0_API_KEY for UI generation
api_key = os.getenv('V0_API_KEY') or os.getenv('VERCEL_TOKEN')
if not api_key:
    raise ValueError("V0_API_KEY or VERCEL_TOKEN environment variable required")

generator = V0ComponentGenerator(api_key)
analyzer = ProjectAnalyzer()

async def setup_project_structure(project_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Set up a basic Next.js + TypeScript + Tailwind + shadcn/ui project structure
    """
    try:
        base_path = Path(project_path) if project_path else Path.cwd()
        created_files = []
        
        # Create package.json if it doesn't exist
        package_json_path = base_path / "package.json"
        if not package_json_path.exists():
            package_json = {
                "name": "v0-generated-project",
                "version": "0.1.0",
                "private": True,
                "scripts": {
                    "dev": "next dev",
                    "build": "next build",
                    "start": "next start",
                    "lint": "next lint"
                },
                "dependencies": {
                    "next": "14.2.3",
                    "react": "^18.3.1",
                    "react-dom": "^18.3.1",
                    "@radix-ui/react-slot": "^1.0.2",
                    "class-variance-authority": "^0.7.0",
                    "clsx": "^2.1.1",
                    "tailwind-merge": "^2.3.0",
                    "lucide-react": "^0.394.0"
                },
                "devDependencies": {
                    "@types/node": "^20.14.0",
                    "@types/react": "^18.3.3",
                    "@types/react-dom": "^18.3.0",
                    "autoprefixer": "^10.4.19",
                    "eslint": "^8.57.0",
                    "eslint-config-next": "14.2.3",
                    "postcss": "^8.4.38",
                    "tailwindcss": "^3.4.4",
                    "typescript": "^5.4.5"
                }
            }
            with open(package_json_path, 'w') as f:
                json.dump(package_json, f, indent=2)
            created_files.append("package.json")
            logger.info("Created package.json")
        
        # Create tsconfig.json if it doesn't exist
        tsconfig_path = base_path / "tsconfig.json"
        if not tsconfig_path.exists():
            tsconfig = {
                "compilerOptions": {
                    "target": "ES2017",
                    "lib": ["dom", "dom.iterable", "esnext"],
                    "allowJs": True,
                    "skipLibCheck": True,
                    "strict": True,
                    "forceConsistentCasingInFileNames": True,
                    "noEmit": True,
                    "esModuleInterop": True,
                    "module": "esnext",
                    "moduleResolution": "bundler",
                    "resolveJsonModule": True,
                    "isolatedModules": True,
                    "jsx": "preserve",
                    "incremental": True,
                    "plugins": [
                        {
                            "name": "next"
                        }
                    ],
                    "paths": {
                        "@/*": ["./*"]
                    }
                },
                "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
                "exclude": ["node_modules"]
            }
            with open(tsconfig_path, 'w') as f:
                json.dump(tsconfig, f, indent=2)
            created_files.append("tsconfig.json")
            logger.info("Created tsconfig.json")
        
        # Create tailwind.config.js if it doesn't exist
        tailwind_config_path = base_path / "tailwind.config.js"
        if not tailwind_config_path.exists():
            tailwind_config = '''/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}'''
            with open(tailwind_config_path, 'w') as f:
                f.write(tailwind_config)
            created_files.append("tailwind.config.js")
            logger.info("Created tailwind.config.js")
        
        # Create postcss.config.js if it doesn't exist
        postcss_config_path = base_path / "postcss.config.js"
        if not postcss_config_path.exists():
            postcss_config = '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
'''
            with open(postcss_config_path, 'w') as f:
                f.write(postcss_config)
            created_files.append("postcss.config.js")
            logger.info("Created postcss.config.js")
        
        # Create components.json for shadcn/ui if it doesn't exist
        components_json_path = base_path / "components.json"
        if not components_json_path.exists():
            components_json = {
                "$schema": "https://ui.shadcn.com/schema.json",
                "style": "default",
                "rsc": True,
                "tsx": True,
                "tailwind": {
                    "config": "tailwind.config.js",
                    "css": "app/globals.css",
                    "baseColor": "slate",
                    "cssVariables": True,
                    "prefix": ""
                },
                "aliases": {
                    "components": "@/components",
                    "utils": "@/lib/utils"
                }
            }
            with open(components_json_path, 'w') as f:
                json.dump(components_json, f, indent=2)
            created_files.append("components.json")
            logger.info("Created components.json")
        
        # Create lib/utils.ts if it doesn't exist
        lib_dir = base_path / "lib"
        lib_dir.mkdir(exist_ok=True)
        utils_path = lib_dir / "utils.ts"
        if not utils_path.exists():
            utils_content = '''import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
'''
            with open(utils_path, 'w') as f:
                f.write(utils_content)
            created_files.append("lib/utils.ts")
            logger.info("Created lib/utils.ts")
        
        # Ensure components directory exists
        components_dir = base_path / "components"
        components_dir.mkdir(exist_ok=True)
        
        return {
            "success": True,
            "created_files": created_files,
            "message": f"Project structure setup completed. Created {len(created_files)} files.",
            "project_path": str(base_path)
        }
        
    except Exception as e:
        logger.error(f"Failed to setup project structure: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# Register tools
@mcp.tool()
async def generate_component(
    prompt: str,
    component_name: Optional[str] = None,
    framework: Optional[str] = None,
    styling: Optional[str] = None,
    ui_library: Optional[str] = None,
    output_format: Optional[str] = "single_file",
    project_path: Optional[str] = None,
    auto_setup: Optional[bool] = True,
    write_to_file: Optional[bool] = False,
    target_directory: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a UI component using Vercel v0 API with intelligent dependency detection
    
    Args:
        prompt: Description of the component to generate
        component_name: Name for the component (optional)
        framework: Frontend framework to use (auto-detected if not provided)
        styling: CSS framework/approach (auto-detected if not provided)
        ui_library: UI component library (auto-detected if not provided)
        output_format: 'single_file' or 'multi_file'
        project_path: Path to analyze for dependencies (defaults to current directory)
        auto_setup: Automatically create missing config files (default: True)
        write_to_file: Whether to write the generated component to files (default: False)
        target_directory: Where to create the component files (auto-detected if not provided)
    
    Returns:
        Generated component code with metadata and project analysis
    """
    # Analyze project if auto-detection is needed
    if project_path:
        project_analyzer = ProjectAnalyzer(project_path)
    else:
        project_analyzer = analyzer
        
    project_analysis = project_analyzer.analyze_project()
    
    # If no framework detected and auto_setup is enabled, create basic project structure
    if auto_setup and project_analysis["framework"] == "Unknown":
        logger.info("No framework detected, setting up basic Next.js + TypeScript + Tailwind project")
        setup_result = await setup_project_structure(project_path)
        if setup_result["success"]:
            # Re-analyze after setup
            project_analysis = project_analyzer.analyze_project()
            logger.info("Project setup completed, re-analyzed project")
    
    # Use detected values or fallback to provided/default values
    tech_stack = {
        "framework": framework or project_analysis["framework"] or "Next.js 14 App Router",
        "language": "TypeScript" if project_analysis["typescript"] else "JavaScript",
        "styling": styling or (project_analysis["styling"][0] if project_analysis["styling"] else "Tailwind CSS"),
        "ui_library": ui_library or (project_analysis["ui_libraries"][0] if project_analysis["ui_libraries"] else "shadcn/ui"),
        "state": "React hooks"
    }
    
    try:
        result = await generator.generate_component(
            prompt=prompt,
            tech_stack=tech_stack,
            stream=True
        )
        
        # Handle file writing if requested
        if write_to_file:
            file_creation_result = project_analyzer.create_component_files(
                result['files'], 
                target_directory
            )
            
            if not file_creation_result["success"]:
                return {
                    "success": False,
                    "error": "Component generated but file creation failed",
                    "file_errors": file_creation_result["errors"],
                    "partial_files": file_creation_result["created_files"]
                }
        
        response = {
            "success": True,
            "generation_id": result['generation_id'],
            "component_name": component_name or "Component",
            "tech_stack_used": tech_stack,
            "project_analysis": project_analysis,
            "auto_detected": {
                "framework": not framework,
                "styling": not styling,
                "ui_library": not ui_library
            }
        }
        
        if write_to_file:
            response["files_created"] = file_creation_result["created_files"]
            response["target_directory"] = file_creation_result["target_directory"]
        
        if output_format == "multi_file":
            # Return structured file data
            response["files"] = result['files']
        else:
            # Return as single file - use extracted code, not raw content
            if result['files'] and len(result['files']) > 0:
                # Use the content from the first extracted file
                response["code"] = result['files'][0]['content']
                response["file_name"] = result['files'][0]['name']
                logger.info(f"Returning extracted code from file: {result['files'][0]['name']}")
            else:
                # Fallback to raw content only if extraction failed
                logger.warning("No files extracted, falling back to raw content")
                response["code"] = result['content']
            
        return response
            
    except Exception as e:
        error_msg = f"Failed to generate component: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }
        
@mcp.tool()
async def analyze_project_dependencies(
    project_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyze a project's dependencies and structure for intelligent v0 generation
    
    Args:
        project_path: Path to the project directory (defaults to current directory)
    
    Returns:
        Detailed analysis of project dependencies, structure, and recommendations
    """
    try:
        if project_path:
            project_analyzer = ProjectAnalyzer(project_path)
        else:
            project_analyzer = analyzer
            
        analysis = project_analyzer.analyze_project()
        
        # Add recommendations based on analysis
        recommendations = []
        
        if not analysis["ui_libraries"]:
            recommendations.append("Consider adding a UI library like shadcn/ui for consistent components")
        
        if "CSS" in analysis["styling"] and len(analysis["styling"]) == 1:
            recommendations.append("Consider adding Tailwind CSS for utility-first styling")
            
        if not analysis["typescript"]:
            recommendations.append("Consider migrating to TypeScript for better type safety")
            
        return {
            "success": True,
            "analysis": analysis,
            "recommendations": recommendations,
            "project_path": str(project_analyzer.project_path)
        }
        
    except Exception as e:
        error_msg = f"Failed to analyze project: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }

@mcp.tool()
async def test_file_creation(
    test_content: str = "// Test component\nexport default function TestComponent() {\n  return <div>Test</div>\n}",
    project_path: Optional[str] = None,
    target_directory: Optional[str] = None
) -> Dict[str, Any]:
    """
    Test file creation functionality
    
    Args:
        test_content: Content to write to test file
        project_path: Path to the project (defaults to current directory)
        target_directory: Where to create the test file (auto-detected if not provided)
    
    Returns:
        Test results
    """
    try:
        if project_path:
            project_analyzer = ProjectAnalyzer(project_path)
        else:
            project_analyzer = analyzer
            
        test_files = [{
            "name": "TestComponent.tsx",
            "content": test_content
        }]
        
        result = project_analyzer.create_component_files(test_files, target_directory)
        
        return {
            "success": True,
            "test_result": result,
            "project_path": str(project_analyzer.project_path)
        }
        
    except Exception as e:
        logger.error(f"File creation test failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def generate_and_create_component(
    prompt: str,
    component_name: Optional[str] = None,
    project_path: Optional[str] = None,
    target_directory: Optional[str] = None
) -> Dict[str, Any]:
    """
    SEMI-AUTONOMOUS: Generate component, check dependencies, create files. Claude Code handles npm install.
    
    Args:
        prompt: Description of the component to generate
        component_name: Name for the component (optional)
        project_path: Path to the project (defaults to current directory)
        auto_install_deps: Whether to automatically install missing dependencies
        target_directory: Where to create the component (auto-detected if not provided)
    
    Returns:
        Complete workflow results including generation, installation, and file creation
    """
    workflow_results = {
        "success": True,
        "steps_completed": [],
        "errors": [],
        "component_name": component_name or "Component"
    }
    
    try:
        # Step 1: Analyze project
        if project_path:
            project_analyzer = ProjectAnalyzer(project_path)
        else:
            project_analyzer = analyzer
            
        analysis = project_analyzer.analyze_project()
        workflow_results["steps_completed"].append("project_analysis")
        workflow_results["project_analysis"] = analysis
        
        # Step 2: Determine tech stack
        tech_stack = {
            "framework": analysis["framework"] or "Next.js 14 App Router",
            "language": "TypeScript" if analysis["typescript"] else "JavaScript",
            "styling": analysis["styling"][0] if analysis["styling"] else "Tailwind CSS",
            "ui_library": analysis["ui_libraries"][0] if analysis["ui_libraries"] else "shadcn/ui",
            "state": "React hooks"
        }
        workflow_results["tech_stack"] = tech_stack
        
        # Step 3: Generate component
        result = await generator.generate_component(
            prompt=prompt,
            tech_stack=tech_stack,
            stream=True
        )
        workflow_results["steps_completed"].append("component_generation")
        workflow_results["generation_id"] = result['generation_id']
        workflow_results["generated_files"] = result['files']
        
        # Step 4: Check dependencies (Claude Code will install them)
        required_deps = project_analyzer.get_required_dependencies(tech_stack)
        missing_deps = project_analyzer.check_missing_dependencies(required_deps)
        
        workflow_results["dependency_analysis"] = {
            "required_dependencies": required_deps,
            "missing_dependencies": missing_deps,
            "needs_installation": len(missing_deps) > 0,
            "install_command": f"npm install {' '.join(missing_deps)}" if missing_deps else None
        }
        
        if missing_deps:
            workflow_results["next_steps"] = [
                f"Run: npm install {' '.join(missing_deps)}",
                "Then the component will be ready to use"
            ]
        else:
            workflow_results["next_steps"] = ["Component is ready to use - all dependencies present"]
        
        # Step 5: Create files
        logger.info(f"Creating files: {len(result['files'])} files to create")
        logger.info(f"Target directory: {target_directory}")
        logger.info(f"Project path: {project_analyzer.project_path}")
        
        file_creation_result = project_analyzer.create_component_files(
            result['files'], 
            target_directory
        )
        workflow_results["steps_completed"].append("file_creation")
        workflow_results["file_creation"] = file_creation_result
        
        logger.info(f"File creation result: {file_creation_result}")
        
        if not file_creation_result["success"]:
            workflow_results["errors"].append("File creation had errors")
            workflow_results["success"] = False
        
        # Final summary
        workflow_results["summary"] = {
            "component_generated": True,
            "files_created": len(file_creation_result.get("created_files", [])),
            "target_directory": file_creation_result.get("target_directory"),
            "dependencies_checked": True,
            "ready_to_use": workflow_results["success"] and len(missing_deps) == 0,
            "requires_npm_install": len(missing_deps) > 0
        }
        
        return workflow_results
        
    except Exception as e:
        error_msg = f"Autonomous workflow failed: {str(e)}"
        logger.error(error_msg)
        workflow_results["success"] = False
        workflow_results["errors"].append(error_msg)
        return workflow_results
        
@mcp.tool()
async def generate_page(
    page_description: str,
    page_name: str,
    include_layout: Optional[bool] = True,
    include_api_route: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Generate a complete Next.js page with v0
    
    Args:
        page_description: Description of the page functionality
        page_name: Name for the page (used for file naming)
        include_layout: Whether to include layout wrapper
        include_api_route: Whether to generate corresponding API route
    
    Returns:
        Generated page code and optional API route
    """
    files = []
    
    # Generate main page component
    page_prompt = f"""Create a Next.js 14 App Router page component for: {page_description}

Page name: {page_name}
Include:
- Proper metadata export
- Loading and error states
- Server/client components as appropriate
- Data fetching if needed
{"- Layout wrapper component" if include_layout else ""}
{"- Corresponding API route structure" if include_api_route else ""}
"""
    
    try:
        result = await generator.generate_component(
            prompt=page_prompt,
            stream=True
        )
        
        # Add page component
        files.append({
            "path": f"app/{page_name}/page.tsx",
            "content": result['content']
        })
        
        # Generate API route if requested
        if include_api_route:
            api_prompt = f"""Create a Next.js 14 API route for the {page_name} page.
This should handle the backend logic for: {page_description}

Include:
- Proper TypeScript types
- Error handling
- Input validation
- CORS headers if needed"""
            
            api_result = await generator.generate_component(
                prompt=api_prompt,
                stream=True
            )
            
            files.append({
                "path": f"app/api/{page_name}/route.ts",
                "content": api_result['content']
            })
        
        return {
            "success": True,
            "files": files,
            "page_name": page_name
        }
        
    except Exception as e:
        error_msg = f"Failed to generate page: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }
        
@mcp.tool()
async def generate_ui_from_data(
    data_structure: str,
    ui_type: str = "table",
    interactions: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate UI component based on data structure
    
    Args:
        data_structure: JSON or description of data structure
        ui_type: Type of UI - 'table', 'cards', 'list', 'chart', 'form'
        interactions: Description of user interactions needed
    
    Returns:
        Generated UI component
    """
    prompt = f"""Create a {ui_type} component to display this data structure:

{data_structure}

UI Type: {ui_type}
{"User Interactions: " + interactions if interactions else "Include basic interactions like sorting, filtering, or selection as appropriate"}

Requirements:
- Handle empty states
- Include loading states
- Make it responsive
- Use proper TypeScript types for the data
- Include sample data for testing"""

    try:
        result = await generator.generate_component(
            prompt=prompt,
            stream=True
        )
        
        return {
            "success": True,
            "code": result['content'],
            "ui_type": ui_type,
            "generation_id": result['generation_id']
        }
        
    except Exception as e:
        error_msg = f"Failed to generate UI from data: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }
        
@mcp.tool()
async def improve_component(
    existing_code: str,
    improvements: str,
    maintain_structure: Optional[bool] = True,
    write_to_file: Optional[bool] = False,
    file_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Improve an existing component using v0
    
    Args:
        existing_code: The current component code
        improvements: Description of improvements needed
        maintain_structure: Whether to keep the same structure
        write_to_file: Whether to write the improved code back to file
        file_path: Path to the file to update (required if write_to_file is True)
    
    Returns:
        Improved component code
    """
    prompt = f"""Improve this existing React component:

```tsx
{existing_code}
```

Improvements needed:
{improvements}

Requirements:
{"- Maintain the existing component structure and API" if maintain_structure else "- Feel free to restructure if it improves the component"}
- Keep all existing functionality
- Improve code quality and performance
- Add better TypeScript types
- Improve accessibility
- Add helpful comments"""

    try:
        result = await generator.generate_component(
            prompt=prompt,
            stream=True
        )
        
        # Write to file if requested
        if write_to_file:
            if not file_path:
                return {
                    "success": False,
                    "error": "file_path is required when write_to_file is True"
                }
            
            try:
                file_full_path = Path.cwd() / file_path
                file_full_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Extract code from result
                code = result['content']
                if result['files']:
                    # Use the first file's content if multiple files
                    code = result['files'][0]['content']
                
                # Write improved code to file
                with open(file_full_path, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(code.replace('\r\n', '\n').replace('\r', '\n'))
                
                return {
                    "success": True,
                    "code": code,
                    "improvements_applied": improvements,
                    "generation_id": result['generation_id'],
                    "file_updated": str(file_path)
                }
            except Exception as write_error:
                return {
                    "success": False,
                    "error": f"Component improved but file update failed: {str(write_error)}",
                    "code": result['content'],
                    "generation_id": result['generation_id']
                }
        
        return {
            "success": True,
            "code": result['content'],
            "improvements_applied": improvements,
            "generation_id": result['generation_id']
        }
        
    except Exception as e:
        error_msg = f"Failed to improve component: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }

@mcp.tool()
async def v0_update_file(
    file_path: str,
    improvements: str,
    maintain_structure: Optional[bool] = True,
    project_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing file in-place using v0 to improve it
    
    Args:
        file_path: Path to the file to update (relative to project_path)
        improvements: Description of improvements needed
        maintain_structure: Whether to keep the same structure
        project_path: Path to the project (defaults to current directory)
    
    Returns:
        Update result with improved code
    """
    try:
        # Read the existing file
        base_path = Path(project_path) if project_path else Path.cwd()
        full_path = base_path / file_path
        
        if not full_path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }
        
        with open(full_path, 'r', encoding='utf-8') as f:
            existing_code = f.read()
        
        # Improve the component
        result = await improve_component(
            existing_code=existing_code,
            improvements=improvements,
            maintain_structure=maintain_structure,
            write_to_file=True,
            file_path=file_path
        )
        
        return result
        
    except Exception as e:
        error_msg = f"Failed to update file: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }
        
@mcp.tool()
async def convert_design_to_code(
    design_description: str,
    design_system: Optional[str] = "shadcn/ui",
    responsive_breakpoints: Optional[str] = "mobile-first"
) -> Dict[str, Any]:
    """
    Convert a design description to code
    
    Args:
        design_description: Detailed description of the design
        design_system: Design system to use
        responsive_breakpoints: Responsive strategy
    
    Returns:
        Component implementing the design
    """
    prompt = f"""Convert this design into a React component:

Design Description:
{design_description}

Design System: {design_system}
Responsive Strategy: {responsive_breakpoints}

Requirements:
- Match the design as closely as possible
- Use the specified design system components
- Ensure full responsiveness
- Include all interactive states (hover, focus, active, disabled)
- Follow accessibility guidelines
- Use semantic HTML"""

    try:
        result = await generator.generate_component(
            prompt=prompt,
            stream=True
        )
        
        return {
            "success": True,
            "code": result['content'],
            "design_system": design_system,
            "generation_id": result['generation_id']
        }
        
    except Exception as e:
        error_msg = f"Failed to convert design: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }

@mcp.tool()
async def v0_create_feature(
    feature_description: str,
    components_needed: List[str],
    api_endpoints: Optional[List[str]] = None,
    project_path: Optional[str] = None,
    create_files: Optional[bool] = True
) -> Dict[str, Any]:
    """
    Create a complete feature with multiple components and optional API routes
    
    Args:
        feature_description: Description of the feature to create
        components_needed: List of component names/descriptions needed
        api_endpoints: Optional list of API endpoints to create
        project_path: Path to the project (defaults to current directory)
        create_files: Whether to create the files (default: True)
    
    Returns:
        Complete feature implementation with all components and APIs
    """
    try:
        # Initialize project analyzer
        project_analyzer = ProjectAnalyzer(project_path) if project_path else analyzer
        project_analysis = project_analyzer.analyze_project()
        
        # Determine tech stack
        tech_stack = {
            "framework": project_analysis["framework"] or "Next.js 14 App Router",
            "language": "TypeScript" if project_analysis["typescript"] else "JavaScript",
            "styling": project_analysis["styling"][0] if project_analysis["styling"] else "Tailwind CSS",
            "ui_library": project_analysis["ui_libraries"][0] if project_analysis["ui_libraries"] else "shadcn/ui",
            "state": "React hooks"
        }
        
        generated_files = []
        
        # Generate each component
        for component_desc in components_needed:
            component_prompt = f"""Create a component for this feature: {feature_description}

Component needed: {component_desc}

Context of other components in this feature:
{', '.join(components_needed)}

Requirements:
- Make sure components can work together
- Use consistent prop types and interfaces
- Export necessary types for other components to use
- Include proper error handling
- Add loading states where appropriate"""

            try:
                result = await generator.generate_component(
                    prompt=component_prompt,
                    tech_stack=tech_stack,
                    stream=True
                )
                
                # Add generated files to list
                generated_files.extend(result['files'])
                
            except Exception as comp_error:
                logger.error(f"Failed to generate component {component_desc}: {comp_error}")
                return {
                    "success": False,
                    "error": f"Failed to generate component {component_desc}: {str(comp_error)}",
                    "partial_files": generated_files
                }
        
        # Generate API endpoints if requested
        if api_endpoints:
            for endpoint_desc in api_endpoints:
                api_prompt = f"""Create a Next.js 14 API route for this feature: {feature_description}

API endpoint needed: {endpoint_desc}

Components using this API:
{', '.join(components_needed)}

Requirements:
- Use App Router route handlers (route.ts)
- Include proper TypeScript types
- Add input validation
- Handle errors gracefully
- Return appropriate status codes
- Include CORS headers if needed
- Add rate limiting comments where appropriate"""

                try:
                    api_result = await generator.generate_component(
                        prompt=api_prompt,
                        stream=True
                    )
                    
                    # Extract endpoint name from description
                    endpoint_name = endpoint_desc.lower().replace(' ', '-')
                    
                    # Add API route file
                    generated_files.append({
                        "name": "route.ts",
                        "content": api_result['content'],
                        "path": f"app/api/{endpoint_name}/route.ts"
                    })
                    
                except Exception as api_error:
                    logger.error(f"Failed to generate API {endpoint_desc}: {api_error}")
        
        # Create files if requested
        if create_files and generated_files:
            file_creation_result = project_analyzer.create_component_files(generated_files)
            
            if not file_creation_result["success"]:
                return {
                    "success": False,
                    "error": "Feature generated but file creation failed",
                    "file_errors": file_creation_result["errors"],
                    "partial_files": file_creation_result["created_files"],
                    "generated_files": generated_files
                }
        
        return {
            "success": True,
            "feature_description": feature_description,
            "components_generated": len([f for f in generated_files if 'component' in f.get('path', '').lower()]),
            "apis_generated": len([f for f in generated_files if 'api' in f.get('path', '').lower()]),
            "files": generated_files,
            "tech_stack_used": tech_stack,
            "files_created": file_creation_result["created_files"] if create_files else None
        }
        
    except Exception as e:
        error_msg = f"Failed to create feature: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }
    
if __name__ == "__main__":
    # Run as HTTP server on specified port
    port = int(os.getenv('V0_MCP_PORT', '8010'))
    logger.info(f"Starting Vercel v0 MCP Server on port {port}")
    # Run with streamable-http transport - serves on both / and /mcp/ paths
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")