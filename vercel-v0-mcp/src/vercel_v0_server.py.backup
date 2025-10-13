#!/usr/bin/env python3
"""
Enhanced Vercel v0 MCP Server - Combines Model API and Platform API
Provides full v0 capabilities including chat sessions, code parsing, and frame environment
"""

import os
import json
import asyncio
import logging
import re
import uuid
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
import aiohttp

from fastmcp import FastMCP, Context
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("vercel-v0-enhanced")

# Get API key
V0_API_KEY = os.getenv('V0_API_KEY') or os.getenv('VERCEL_TOKEN')
if not V0_API_KEY:
    raise ValueError("V0_API_KEY or VERCEL_TOKEN environment variable required")

@dataclass
class V0ChatSession:
    """Represents a v0 development session"""
    session_id: str
    chat_id: Optional[str] = None
    messages: List[Dict[str, Any]] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    frame_url: Optional[str] = None
    files: Dict[str, str] = field(default_factory=dict)  # filename -> content
    project_path: Optional[str] = None

class V0PlatformClient:
    """Client for v0 Platform API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://v0.dev/api"
        self.model_url = "https://api.v0.dev/v1"
        self.sessions: Dict[str, V0ChatSession] = {}
        
    async def create_chat_session(self, project_context: Optional[Dict[str, Any]] = None) -> V0ChatSession:
        """Create a new v0 chat session"""
        session = V0ChatSession(
            session_id=str(uuid.uuid4()),
            context=project_context or {}
        )
        self.sessions[session.session_id] = session
        logger.info(f"Created v0 session: {session.session_id}")
        return session
    
    async def send_message(
        self, 
        session: V0ChatSession, 
        prompt: str,
        model: str = "v0-1.5-md",
        stream: bool = True
    ) -> Dict[str, Any]:
        """Send a message to v0 Model API with session context"""
        
        # Build system prompt with context
        system_prompt = self._build_system_prompt(session)
        
        # Add user message to session
        session.messages.append({"role": "user", "content": prompt})
        
        # Prepare messages for API
        messages = [
            {"role": "system", "content": system_prompt}
        ] + session.messages
        
        # Call v0 Model API
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as client:
            async with client.post(
                f"{self.model_url}/chat/completions",
                headers=headers,
                json={
                    "model": model,
                    "messages": messages,
                    "stream": stream
                }
            ) as response:
                if stream:
                    content = await self._handle_streaming_response(response)
                else:
                    data = await response.json()
                    content = data["choices"][0]["message"]["content"]
                
                # Add assistant response to session
                session.messages.append({"role": "assistant", "content": content})
                
                # Parse code from response
                parsed_files = self._parse_code_files(content)
                session.files.update(parsed_files)
                
                return {
                    "content": content,
                    "files": parsed_files,
                    "session_id": session.session_id,
                    "frame_url": session.frame_url
                }
    
    async def _handle_streaming_response(self, response) -> str:
        """Handle SSE streaming response from v0"""
        full_content = ""
        async for line in response.content:
            line = line.decode('utf-8').strip()
            if line.startswith('data: '):
                data_str = line[6:]
                if data_str == '[DONE]':
                    break
                try:
                    data = json.loads(data_str)
                    if 'choices' in data and data['choices']:
                        delta = data['choices'][0].get('delta', {})
                        if 'content' in delta:
                            full_content += delta['content']
                except json.JSONDecodeError:
                    continue
        return full_content
    
    def _build_system_prompt(self, session: V0ChatSession) -> str:
        """Build context-aware system prompt"""
        prompt_parts = [
            "You are v0, an expert AI for building modern web applications.",
            "You generate complete, production-ready code with all necessary files."
        ]
        
        # Add project context if available
        if session.context:
            if 'project_type' in session.context:
                prompt_parts.append(f"Project type: {session.context['project_type']}")
            if 'tech_stack' in session.context:
                stack = session.context['tech_stack']
                prompt_parts.append(f"Tech stack: {json.dumps(stack)}")
            if 'existing_files' in session.context:
                prompt_parts.append(f"Existing files: {', '.join(session.context['existing_files'])}")
        
        # Add file context from session
        if session.files:
            prompt_parts.append(f"Files in session: {', '.join(session.files.keys())}")
        
        prompt_parts.append("""
When generating code:
1. Create complete, working implementations
2. Include all necessary imports and dependencies
3. Follow best practices for the specified framework
4. Add proper TypeScript types when applicable
5. Include error handling and edge cases
6. Format file paths clearly with comments like: // File: path/to/file.tsx
""")
        
        return "\n\n".join(prompt_parts)
    
    def _parse_code_files(self, content: str) -> Dict[str, str]:
        """Parse code files from v0 response"""
        files = {}
        
        # Pattern 1: ```language file="path/to/file"
        pattern1 = r'```(?:\w+)?\s*file=["\'`]([^"\'`]+)["\'`]\s*\n([\s\S]*?)```'
        for match in re.finditer(pattern1, content):
            file_path = match.group(1)
            file_content = match.group(2).strip()
            files[file_path] = file_content
        
        # Pattern 2: // File: path/to/file
        pattern2 = r'// File: (.+)\n([\s\S]*?)(?=// File:|```|$)'
        for match in re.finditer(pattern2, content):
            file_path = match.group(1).strip()
            file_content = match.group(2).strip()
            if file_content:
                files[file_path] = file_content
        
        # Pattern 3: Standard code blocks without file markers
        if not files:
            code_blocks = re.findall(r'```(?:\w+)?\n([\s\S]*?)```', content)
            if code_blocks:
                # Try to extract component name
                main_code = code_blocks[0]
                component_match = re.search(r'(?:export\s+)?(?:default\s+)?(?:function|const)\s+(\w+)', main_code)
                if component_match:
                    name = component_match.group(1)
                    files[f"components/{name}.tsx"] = main_code
                else:
                    files["Component.tsx"] = main_code
        
        return files
    
    async def create_frame_preview(self, session: V0ChatSession) -> str:
        """Create a v0 frame preview URL for the session"""
        # In a real implementation, this would call v0 Platform API
        # to create an actual frame environment
        frame_id = f"frame-{session.session_id[:8]}"
        session.frame_url = f"https://v0.dev/frame/{frame_id}"
        return session.frame_url
    
    async def export_to_project(self, session: V0ChatSession, target_path: str) -> Dict[str, Any]:
        """Export session files to a project directory"""
        target_dir = Path(target_path)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        created_files = []
        for file_path, content in session.files.items():
            full_path = target_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding='utf-8')
            created_files.append(str(full_path))
        
        return {
            "success": True,
            "created_files": created_files,
            "target_path": str(target_dir)
        }

# Global client instance
v0_client = V0PlatformClient(V0_API_KEY)

# Context analyzer from original implementation
class ProjectContextAnalyzer:
    """Analyzes project for v0 context"""
    
    def __init__(self, project_path: Optional[Path] = None):
        self.project_path = project_path or Path.cwd()
    
    async def analyze_project_context(self) -> Dict[str, Any]:
        """Analyze project for v0 context"""
        context = {
            "project_type": self._detect_project_type(),
            "tech_stack": self._analyze_tech_stack(),
            "existing_files": self._scan_project_files(),
            "has_package_json": (self.project_path / "package.json").exists(),
            "has_tsconfig": (self.project_path / "tsconfig.json").exists(),
            "framework": None
        }
        
        # Detect framework
        if (self.project_path / "next.config.js").exists() or (self.project_path / "next.config.mjs").exists():
            context["framework"] = "nextjs"
            if (self.project_path / "app").exists():
                context["nextjs_router"] = "app"
            else:
                context["nextjs_router"] = "pages"
        
        return context
    
    def _detect_project_type(self) -> str:
        """Detect project type from structure"""
        project_name = self.project_path.name.lower()
        
        if "todo" in project_name:
            return "todo_app"
        elif "dashboard" in project_name:
            return "dashboard"
        elif "blog" in project_name:
            return "blog"
        elif "ecommerce" in project_name or "shop" in project_name:
            return "ecommerce"
        else:
            return "web_app"
    
    def _analyze_tech_stack(self) -> Dict[str, str]:
        """Analyze tech stack from package.json"""
        package_json_path = self.project_path / "package.json"
        if not package_json_path.exists():
            return {
                "framework": "Next.js 14 App Router",
                "language": "TypeScript",
                "styling": "Tailwind CSS",
                "ui_library": "shadcn/ui"
            }
        
        try:
            with open(package_json_path) as f:
                data = json.load(f)
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                
                tech_stack = {}
                
                # Framework detection
                if "next" in deps:
                    tech_stack["framework"] = "Next.js"
                elif "react" in deps:
                    tech_stack["framework"] = "React"
                
                # Language
                tech_stack["language"] = "TypeScript" if "typescript" in deps else "JavaScript"
                
                # Styling
                if "tailwindcss" in deps:
                    tech_stack["styling"] = "Tailwind CSS"
                elif "styled-components" in deps:
                    tech_stack["styling"] = "Styled Components"
                else:
                    tech_stack["styling"] = "CSS"
                
                # UI Library
                if "@radix-ui/react-slot" in deps:
                    tech_stack["ui_library"] = "shadcn/ui"
                elif "@mui/material" in deps:
                    tech_stack["ui_library"] = "Material-UI"
                else:
                    tech_stack["ui_library"] = "none"
                
                return tech_stack
        except Exception:
            return {
                "framework": "Next.js 14 App Router",
                "language": "TypeScript",
                "styling": "Tailwind CSS",
                "ui_library": "shadcn/ui"
            }
    
    def _scan_project_files(self) -> List[str]:
        """Scan for existing project files"""
        files = []
        
        # Common directories to scan
        for pattern in ["*.tsx", "*.ts", "*.jsx", "*.js"]:
            files.extend([str(f.relative_to(self.project_path)) 
                         for f in self.project_path.glob(f"**/{pattern}")
                         if not any(skip in str(f) for skip in ['node_modules', '.git', '.next'])])
        
        return files[:20]  # Limit to first 20 files

# MCP Tool Definitions

@mcp.tool()
async def create_v0_session(
    project_path: Optional[str] = None,
    project_type: Optional[str] = None,
    tech_stack: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Create a new v0 development session with context
    
    Args:
        project_path: Path to analyze for context (optional)
        project_type: Type of project (todo_app, dashboard, etc.)
        tech_stack: Override tech stack detection
    
    Returns:
        Session information including session_id
    """
    context = {}
    
    # Analyze project if path provided
    if project_path:
        analyzer = ProjectContextAnalyzer(Path(project_path))
        context = await analyzer.analyze_project_context()
        logger.info(f"Analyzed project context: {context['project_type']}")
    
    # Override with provided values
    if project_type:
        context["project_type"] = project_type
    if tech_stack:
        context["tech_stack"] = tech_stack
    
    # Create session
    session = await v0_client.create_chat_session(context)
    
    return {
        "success": True,
        "session_id": session.session_id,
        "context": context,
        "message": "v0 session created successfully"
    }

@mcp.tool()
async def generate_with_v0(
    prompt: str,
    session_id: Optional[str] = None,
    create_files: Optional[bool] = True,
    target_directory: Optional[str] = None,
    model: Optional[str] = "v0-1.5-md"
) -> Dict[str, Any]:
    """
    Generate code using v0 with session context
    
    Args:
        prompt: What to generate
        session_id: Existing session ID (creates new if not provided)
        create_files: Whether to write files to disk
        target_directory: Where to create files
        model: v0 model to use (v0-1.5-md, v0-1.5-lg, v0-1.0-md)
    
    Returns:
        Generated code, files created, and session info
    """
    # Get or create session
    if session_id and session_id in v0_client.sessions:
        session = v0_client.sessions[session_id]
    else:
        session = await v0_client.create_chat_session()
    
    # Generate with v0
    result = await v0_client.send_message(session, prompt, model=model)
    
    # Create files if requested
    files_created = []
    if create_files and result["files"]:
        target_dir = Path(target_directory) if target_directory else Path.cwd() / "generated"
        export_result = await v0_client.export_to_project(session, str(target_dir))
        files_created = export_result["created_files"]
    
    return {
        "success": True,
        "session_id": session.session_id,
        "content": result["content"],
        "files": result["files"],
        "files_created": files_created,
        "frame_url": result.get("frame_url"),
        "model": model,
        "total_messages": len(session.messages)
    }

@mcp.tool()
async def continue_v0_session(
    session_id: str,
    prompt: str,
    create_files: Optional[bool] = True,
    target_directory: Optional[str] = None
) -> Dict[str, Any]:
    """
    Continue an existing v0 session with context
    
    Args:
        session_id: Existing session ID
        prompt: Next prompt in conversation
        create_files: Whether to write new files
        target_directory: Where to create files
    
    Returns:
        Updated generation with full context
    """
    if session_id not in v0_client.sessions:
        return {
            "success": False,
            "error": f"Session {session_id} not found"
        }
    
    return await generate_with_v0(
        prompt=prompt,
        session_id=session_id,
        create_files=create_files,
        target_directory=target_directory
    )

@mcp.tool()
async def get_v0_session_files(
    session_id: str,
    export_to_directory: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get all files from a v0 session
    
    Args:
        session_id: Session to get files from
        export_to_directory: Optional directory to export files to
    
    Returns:
        All files generated in the session
    """
    if session_id not in v0_client.sessions:
        return {
            "success": False,
            "error": f"Session {session_id} not found"
        }
    
    session = v0_client.sessions[session_id]
    
    result = {
        "success": True,
        "session_id": session_id,
        "files": session.files,
        "total_files": len(session.files)
    }
    
    if export_to_directory:
        export_result = await v0_client.export_to_project(session, export_to_directory)
        result["exported_to"] = export_result["target_path"]
        result["exported_files"] = export_result["created_files"]
    
    return result

@mcp.tool()
async def create_v0_frame_preview(
    session_id: str
) -> Dict[str, Any]:
    """
    Create a v0 frame preview URL for running the app in browser
    
    Args:
        session_id: Session to create preview for
    
    Returns:
        Frame URL for browser preview
    """
    if session_id not in v0_client.sessions:
        return {
            "success": False,
            "error": f"Session {session_id} not found"
        }
    
    session = v0_client.sessions[session_id]
    frame_url = await v0_client.create_frame_preview(session)
    
    return {
        "success": True,
        "session_id": session_id,
        "frame_url": frame_url,
        "message": "Frame preview created. Note: This is a placeholder - real v0 Platform API integration needed."
    }

@mcp.tool()
async def list_v0_sessions() -> Dict[str, Any]:
    """
    List all active v0 sessions
    
    Returns:
        List of active sessions with metadata
    """
    sessions = []
    for session_id, session in v0_client.sessions.items():
        sessions.append({
            "session_id": session_id,
            "created_at": session.created_at.isoformat(),
            "messages": len(session.messages),
            "files": len(session.files),
            "context": session.context.get("project_type", "unknown"),
            "frame_url": session.frame_url
        })
    
    return {
        "success": True,
        "sessions": sessions,
        "total": len(sessions)
    }

# Backward compatibility tools from original implementation

@mcp.tool()
async def generate_component(
    prompt: str,
    component_name: Optional[str] = None,
    write_to_file: Optional[bool] = False,
    target_directory: Optional[str] = None,
    project_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a UI component (backward compatibility)
    
    This now uses v0 sessions internally for better context management
    """
    # Create session with project context
    session_result = await create_v0_session(project_path=project_path)
    session_id = session_result["session_id"]
    
    # Generate component
    return await generate_with_v0(
        prompt=prompt,
        session_id=session_id,
        create_files=write_to_file,
        target_directory=target_directory
    )

@mcp.tool()
async def generate_and_create_component(
    prompt: str,
    component_name: Optional[str] = None,
    project_path: Optional[str] = None,
    target_directory: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate and create component files (backward compatibility)
    """
    return await generate_component(
        prompt=prompt,
        component_name=component_name,
        write_to_file=True,
        target_directory=target_directory,
        project_path=project_path
    )

if __name__ == "__main__":
    # Run as HTTP server
    port = int(os.getenv('V0_MCP_PORT', '8010'))
    logger.info(f"Starting Enhanced Vercel v0 MCP Server on port {port}")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")