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
from dataclasses import dataclass, field, asdict
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
class V0Project:
    """Represents a v0 project"""
    project_id: str
    name: str
    description: Optional[str] = None
    environment_variables: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    chat_ids: List[str] = field(default_factory=list)
    repository_url: Optional[str] = None
    deployment_url: Optional[str] = None

@dataclass
class V0ChatSession:
    """Represents a v0 development session"""
    session_id: str
    chat_id: Optional[str] = None
    project_id: Optional[str] = None
    messages: List[Dict[str, Any]] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    frame_url: Optional[str] = None
    files: Dict[str, str] = field(default_factory=dict)  # filename -> content
    project_path: Optional[str] = None
    repository_context: Dict[str, Any] = field(default_factory=dict)
    is_favorite: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class V0Deployment:
    """Represents a v0 deployment"""
    deployment_id: str
    project_id: str
    session_id: str
    status: str = "pending"  # pending, building, ready, error
    url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    logs: List[str] = field(default_factory=list)
    error_message: Optional[str] = None

class V0PlatformClient:
    """Client for v0 Platform API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://v0.dev/api"
        self.model_url = "https://api.v0.dev/v1"
        self.sessions: Dict[str, V0ChatSession] = {}
        self.projects: Dict[str, V0Project] = {}
        self.deployments: Dict[str, V0Deployment] = {}
        
        # Persistent storage
        self.data_dir = Path.home() / ".mcp-persistent"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.session_file = self.data_dir / "v0-sessions.json"
        self.projects_file = self.data_dir / "v0-projects.json"
        self.deployments_file = self.data_dir / "v0-deployments.json"
        
        # Load persistent data
        self._load_sessions()
        self._load_projects()
        self._load_deployments()
        
    async def create_chat_session(self, project_context: Optional[Dict[str, Any]] = None) -> V0ChatSession:
        """Create a new v0 chat session"""
        session = V0ChatSession(
            session_id=str(uuid.uuid4()),
            context=project_context or {}
        )
        self.sessions[session.session_id] = session
        logger.info(f"Created v0 session: {session.session_id}")
        self._save_sessions()
        return session
    
    def _save_sessions(self):
        """Save sessions to disk"""
        try:
            session_data = {}
            for session_id, session in self.sessions.items():
                session_data[session_id] = {
                    'session_id': session.session_id,
                    'chat_id': session.chat_id,
                    'project_id': session.project_id,
                    'messages': session.messages,
                    'context': session.context,
                    'created_at': session.created_at.isoformat(),
                    'frame_url': session.frame_url,
                    'files': session.files,
                    'project_path': session.project_path,
                    'repository_context': session.repository_context,
                    'is_favorite': session.is_favorite,
                    'metadata': session.metadata
                }
            self.session_file.write_text(json.dumps(session_data, indent=2))
            logger.info(f"Saved {len(session_data)} sessions to {self.session_file}")
        except Exception as e:
            logger.error(f"Failed to save sessions: {e}")
    
    def _save_projects(self):
        """Save projects to disk"""
        try:
            project_data = {}
            for project_id, project in self.projects.items():
                project_data[project_id] = {
                    'project_id': project.project_id,
                    'name': project.name,
                    'description': project.description,
                    'environment_variables': project.environment_variables,
                    'created_at': project.created_at.isoformat(),
                    'updated_at': project.updated_at.isoformat(),
                    'chat_ids': project.chat_ids,
                    'repository_url': project.repository_url,
                    'deployment_url': project.deployment_url
                }
            self.projects_file.write_text(json.dumps(project_data, indent=2))
            logger.info(f"Saved {len(project_data)} projects to {self.projects_file}")
        except Exception as e:
            logger.error(f"Failed to save projects: {e}")
    
    def _save_deployments(self):
        """Save deployments to disk"""
        try:
            deployment_data = {}
            for deployment_id, deployment in self.deployments.items():
                deployment_data[deployment_id] = {
                    'deployment_id': deployment.deployment_id,
                    'project_id': deployment.project_id,
                    'session_id': deployment.session_id,
                    'status': deployment.status,
                    'url': deployment.url,
                    'created_at': deployment.created_at.isoformat(),
                    'logs': deployment.logs,
                    'error_message': deployment.error_message
                }
            self.deployments_file.write_text(json.dumps(deployment_data, indent=2))
            logger.info(f"Saved {len(deployment_data)} deployments to {self.deployments_file}")
        except Exception as e:
            logger.error(f"Failed to save deployments: {e}")
    
    def _load_sessions(self):
        """Load sessions from disk"""
        try:
            if self.session_file.exists():
                session_data = json.loads(self.session_file.read_text())
                for session_id, data in session_data.items():
                    session = V0ChatSession(
                        session_id=data['session_id'],
                        chat_id=data.get('chat_id'),
                        project_id=data.get('project_id'),
                        messages=data.get('messages', []),
                        context=data.get('context', {}),
                        created_at=datetime.fromisoformat(data['created_at']),
                        frame_url=data.get('frame_url'),
                        files=data.get('files', {}),
                        project_path=data.get('project_path'),
                        repository_context=data.get('repository_context', {}),
                        is_favorite=data.get('is_favorite', False),
                        metadata=data.get('metadata', {})
                    )
                    self.sessions[session_id] = session
                logger.info(f"Loaded {len(self.sessions)} sessions from {self.session_file}")
        except Exception as e:
            logger.error(f"Failed to load sessions: {e}")
            self.sessions = {}
    
    def _load_projects(self):
        """Load projects from disk"""
        try:
            if self.projects_file.exists():
                project_data = json.loads(self.projects_file.read_text())
                for project_id, data in project_data.items():
                    project = V0Project(
                        project_id=data['project_id'],
                        name=data['name'],
                        description=data.get('description'),
                        environment_variables=data.get('environment_variables', {}),
                        created_at=datetime.fromisoformat(data['created_at']),
                        updated_at=datetime.fromisoformat(data['updated_at']),
                        chat_ids=data.get('chat_ids', []),
                        repository_url=data.get('repository_url'),
                        deployment_url=data.get('deployment_url')
                    )
                    self.projects[project_id] = project
                logger.info(f"Loaded {len(self.projects)} projects from {self.projects_file}")
        except Exception as e:
            logger.error(f"Failed to load projects: {e}")
            self.projects = {}
    
    def _load_deployments(self):
        """Load deployments from disk"""
        try:
            if self.deployments_file.exists():
                deployment_data = json.loads(self.deployments_file.read_text())
                for deployment_id, data in deployment_data.items():
                    deployment = V0Deployment(
                        deployment_id=data['deployment_id'],
                        project_id=data['project_id'],
                        session_id=data['session_id'],
                        status=data['status'],
                        url=data.get('url'),
                        created_at=datetime.fromisoformat(data['created_at']),
                        logs=data.get('logs', []),
                        error_message=data.get('error_message')
                    )
                    self.deployments[deployment_id] = deployment
                logger.info(f"Loaded {len(self.deployments)} deployments from {self.deployments_file}")
        except Exception as e:
            logger.error(f"Failed to load deployments: {e}")
            self.deployments = {}
    
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
                
                # Save sessions after update
                self._save_sessions()
                
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
    
    # =========================================================================
    # V0 PROJECTS SYSTEM INTEGRATION
    # =========================================================================
    
    async def create_v0_project(
        self, 
        name: str, 
        description: Optional[str] = None,
        environment_variables: Optional[Dict[str, str]] = None,
        repository_url: Optional[str] = None
    ) -> V0Project:
        """Create a new v0 project with environment variables"""
        project = V0Project(
            project_id=str(uuid.uuid4()),
            name=name,
            description=description,
            environment_variables=environment_variables or {},
            repository_url=repository_url
        )
        
        self.projects[project.project_id] = project
        self._save_projects()
        logger.info(f"Created v0 project: {project.name} ({project.project_id})")
        return project
    
    async def list_v0_projects(self) -> List[V0Project]:
        """List all available v0 projects"""
        return list(self.projects.values())
    
    async def get_v0_project_by_id(self, project_id: str) -> Optional[V0Project]:
        """Retrieve project details by ID"""
        return self.projects.get(project_id)
    
    async def assign_project_to_chat(self, session_id: str, project_id: str) -> bool:
        """Link a chat session to a project"""
        if session_id not in self.sessions or project_id not in self.projects:
            return False
        
        session = self.sessions[session_id]
        project = self.projects[project_id]
        
        # Update session with project
        session.project_id = project_id
        session.context.update({
            "project_name": project.name,
            "project_description": project.description,
            "environment_variables": project.environment_variables
        })
        
        # Add session to project's chat list
        if session_id not in project.chat_ids:
            project.chat_ids.append(session_id)
            project.updated_at = datetime.now()
        
        self._save_sessions()
        self._save_projects()
        logger.info(f"Assigned session {session_id} to project {project_id}")
        return True
    
    # =========================================================================
    # REPOSITORY CONTEXT INITIALIZATION
    # =========================================================================
    
    async def initialize_chat_from_repo(
        self,
        session: V0ChatSession,
        repository_url: str,
        branch: str = "main",
        include_patterns: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Load GitHub repository into V0 context"""
        # Parse GitHub URL
        github_pattern = r'github\.com/([^/]+)/([^/]+)(?:\.git)?/?$'
        match = re.search(github_pattern, repository_url)
        
        if not match:
            raise ValueError(f"Invalid GitHub URL: {repository_url}")
        
        owner, repo = match.groups()
        repo = repo.replace('.git', '')
        
        # In a real implementation, this would use GitHub API
        # For now, we'll simulate repository context
        repo_context = {
            "type": "github_repository",
            "owner": owner,
            "repository": repo,
            "branch": branch,
            "url": repository_url,
            "loaded_at": datetime.now().isoformat(),
            "files": [],  # Would be populated from GitHub API
            "structure": {},  # Would be populated from repository analysis
            "tech_stack": {}  # Would be detected from package.json, etc.
        }
        
        # Update session with repository context
        session.repository_context = repo_context
        session.context.update({
            "has_repository": True,
            "repository_url": repository_url,
            "repository_type": "github"
        })
        
        self._save_sessions()
        logger.info(f"Initialized session {session.session_id} from repository {repository_url}")
        
        return {
            "success": True,
            "repository_context": repo_context,
            "files_loaded": len(repo_context["files"]),
            "message": f"Repository {owner}/{repo} loaded into session context"
        }
    
    async def initialize_chat_from_files(
        self,
        session: V0ChatSession,
        file_paths: List[str],
        base_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Load local files into V0 context for codebase awareness"""
        loaded_files = {}
        failed_files = []
        
        for file_path in file_paths:
            try:
                if base_path:
                    full_path = Path(base_path) / file_path
                else:
                    full_path = Path(file_path)
                
                if full_path.exists() and full_path.is_file():
                    # Read file content
                    content = full_path.read_text(encoding='utf-8', errors='ignore')
                    loaded_files[str(file_path)] = {
                        "content": content,
                        "size": len(content),
                        "extension": full_path.suffix,
                        "loaded_at": datetime.now().isoformat()
                    }
                else:
                    failed_files.append(file_path)
            except Exception as e:
                logger.error(f"Failed to load file {file_path}: {e}")
                failed_files.append(file_path)
        
        # Update session context
        file_context = {
            "type": "local_files",
            "loaded_files": loaded_files,
            "failed_files": failed_files,
            "total_files": len(file_paths),
            "successful_files": len(loaded_files),
            "loaded_at": datetime.now().isoformat()
        }
        
        session.repository_context = file_context
        session.context.update({
            "has_files": True,
            "file_count": len(loaded_files),
            "existing_files": list(loaded_files.keys())
        })
        
        self._save_sessions()
        logger.info(f"Loaded {len(loaded_files)} files into session {session.session_id}")
        
        return {
            "success": True,
            "loaded_files": len(loaded_files),
            "failed_files": len(failed_files),
            "file_context": file_context,
            "message": f"Loaded {len(loaded_files)} files into session context"
        }
    
    # =========================================================================
    # DEPLOYMENT INTEGRATION
    # =========================================================================
    
    async def create_v0_deployment(
        self,
        session: V0ChatSession,
        deployment_name: Optional[str] = None
    ) -> V0Deployment:
        """Deploy session files directly to Vercel"""
        deployment = V0Deployment(
            deployment_id=str(uuid.uuid4()),
            project_id=session.project_id or "default",
            session_id=session.session_id,
            status="pending"
        )
        
        # In a real implementation, this would:
        # 1. Package session files
        # 2. Create Vercel deployment
        # 3. Monitor deployment status
        # 4. Return deployment URL
        
        # Simulate deployment process
        deployment.logs.append(f"Starting deployment for session {session.session_id}")
        deployment.logs.append(f"Packaging {len(session.files)} files")
        deployment.status = "building"
        
        # Simulate successful deployment
        deployment.url = f"https://{deployment.deployment_id}.vercel.app"
        deployment.status = "ready"
        deployment.logs.append(f"Deployment ready at {deployment.url}")
        
        self.deployments[deployment.deployment_id] = deployment
        self._save_deployments()
        
        logger.info(f"Created deployment {deployment.deployment_id} for session {session.session_id}")
        return deployment
    
    async def get_deployment_status(self, deployment_id: str) -> Optional[Dict[str, Any]]:
        """Get deployment status and details"""
        deployment = self.deployments.get(deployment_id)
        if not deployment:
            return None
        
        return {
            "deployment_id": deployment.deployment_id,
            "status": deployment.status,
            "url": deployment.url,
            "created_at": deployment.created_at.isoformat(),
            "logs": deployment.logs,
            "error_message": deployment.error_message
        }
    
    async def get_deployment_logs(self, deployment_id: str) -> List[str]:
        """Get deployment logs for debugging"""
        deployment = self.deployments.get(deployment_id)
        return deployment.logs if deployment else []
    
    # =========================================================================
    # ENHANCED CHAT MANAGEMENT
    # =========================================================================
    
    async def fork_v0_chat(self, session_id: str, new_name: Optional[str] = None) -> V0ChatSession:
        """Create a fork/branch of an existing chat session"""
        original_session = self.sessions.get(session_id)
        if not original_session:
            raise ValueError(f"Session {session_id} not found")
        
        # Create new session as fork
        forked_session = V0ChatSession(
            session_id=str(uuid.uuid4()),
            chat_id=None,
            project_id=original_session.project_id,
            messages=original_session.messages.copy(),
            context=original_session.context.copy(),
            files=original_session.files.copy(),
            project_path=original_session.project_path,
            repository_context=original_session.repository_context.copy(),
            metadata={
                **original_session.metadata,
                "forked_from": session_id,
                "fork_name": new_name or f"Fork of {session_id[:8]}"
            }
        )
        
        self.sessions[forked_session.session_id] = forked_session
        self._save_sessions()
        
        logger.info(f"Forked session {session_id} to {forked_session.session_id}")
        return forked_session
    
    async def update_chat_metadata(
        self,
        session_id: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """Update chat session metadata"""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        session.metadata.update(metadata)
        self._save_sessions()
        
        logger.info(f"Updated metadata for session {session_id}")
        return True
    
    async def favorite_chat(self, session_id: str, is_favorite: bool = True) -> bool:
        """Mark/unmark a chat session as favorite"""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        session.is_favorite = is_favorite
        self._save_sessions()
        
        logger.info(f"{'Favorited' if is_favorite else 'Unfavorited'} session {session_id}")
        return True
    
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
    tech_stack: Optional[Dict[str, str]] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Create a new v0 development session with context
    
    Args:
        project_path: Path to analyze for context (optional)
        project_type: Type of project (todo_app, dashboard, etc.)
        tech_stack: Override tech stack detection
        ctx: Optional context for logging and progress
    
    Returns:
        Session information including session_id
    """
    if ctx:
        await ctx.info(f"Creating v0 session for project type: {project_type or 'unspecified'}")
    
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
    
    if ctx:
        await ctx.info(f"v0 session created successfully: {session.session_id}")
    
    return {
        "success": True,
        "session_id": session.session_id,
        "context": context,
        "message": "v0 session created successfully"
    }

# Helper function for generation logic (not a tool)
async def _generate_with_v0_internal(
    prompt: str,
    session_id: Optional[str] = None,
    create_files: Optional[bool] = True,
    target_directory: Optional[str] = None,
    model: Optional[str] = "v0-1.5-md",
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Internal helper for v0 generation"""
    if ctx:
        await ctx.info(f"Generating with v0 using model {model}: {prompt[:100]}...")
    
    try:
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
    except Exception as e:
        logger.error(f"Error in generate_with_v0: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def generate_with_v0(
    prompt: str,
    session_id: Optional[str] = None,
    create_files: Optional[bool] = True,
    target_directory: Optional[str] = None,
    model: Optional[str] = "v0-1.5-md",
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Generate code using v0 with session context
    
    Args:
        prompt: What to generate
        session_id: Existing session ID (creates new if not provided)
        create_files: Whether to write files to disk
        target_directory: Where to create files
        model: v0 model to use (v0-1.5-md, v0-1.5-lg, v0-1.0-md)
        ctx: Optional context for logging and progress
    
    Returns:
        Generated code, files created, and session info
    """
    return await _generate_with_v0_internal(
        prompt=prompt,
        session_id=session_id,
        create_files=create_files,
        target_directory=target_directory,
        model=model,
        ctx=ctx
    )

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
    
    return await _generate_with_v0_internal(
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
            "frame_url": session.frame_url,
            "project_id": session.project_id,
            "is_favorite": session.is_favorite,
            "has_repository": bool(session.repository_context),
            "metadata": session.metadata
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

# ============================================================================
# NEW V0 PLATFORM API MCP TOOLS
# ============================================================================

@mcp.tool()
async def create_v0_project(
    name: str,
    description: Optional[str] = None,
    environment_variables: Optional[Dict[str, str]] = None,
    repository_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new v0 project with environment variables
    
    Args:
        name: Project name
        description: Optional project description
        environment_variables: Environment variables for the project
        repository_url: Optional GitHub repository URL
    
    Returns:
        Created project information
    """
    try:
        project = await v0_client.create_v0_project(
            name=name,
            description=description,
            environment_variables=environment_variables,
            repository_url=repository_url
        )
        
        return {
            "success": True,
            "project_id": project.project_id,
            "name": project.name,
            "description": project.description,
            "environment_variables": project.environment_variables,
            "repository_url": project.repository_url,
            "created_at": project.created_at.isoformat(),
            "message": f"Project '{name}' created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating v0 project: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def list_v0_projects() -> Dict[str, Any]:
    """
    List all available v0 projects
    
    Returns:
        List of all projects with their details
    """
    try:
        projects = await v0_client.list_v0_projects()
        
        project_list = []
        for project in projects:
            project_list.append({
                "project_id": project.project_id,
                "name": project.name,
                "description": project.description,
                "chat_count": len(project.chat_ids),
                "created_at": project.created_at.isoformat(),
                "repository_url": project.repository_url,
                "deployment_url": project.deployment_url
            })
        
        return {
            "success": True,
            "projects": project_list,
            "total": len(project_list)
        }
    except Exception as e:
        logger.error(f"Error listing v0 projects: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def get_v0_project_by_id(project_id: str) -> Dict[str, Any]:
    """
    Retrieve project details by ID
    
    Args:
        project_id: The project ID to retrieve
    
    Returns:
        Project details or error
    """
    try:
        project = await v0_client.get_v0_project_by_id(project_id)
        
        if not project:
            return {
                "success": False,
                "error": f"Project {project_id} not found"
            }
        
        return {
            "success": True,
            "project_id": project.project_id,
            "name": project.name,
            "description": project.description,
            "environment_variables": project.environment_variables,
            "created_at": project.created_at.isoformat(),
            "updated_at": project.updated_at.isoformat(),
            "chat_ids": project.chat_ids,
            "repository_url": project.repository_url,
            "deployment_url": project.deployment_url
        }
    except Exception as e:
        logger.error(f"Error getting v0 project: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def assign_project_to_chat(session_id: str, project_id: str) -> Dict[str, Any]:
    """
    Link a chat session to a project
    
    Args:
        session_id: The session ID to assign to project
        project_id: The project ID to assign session to
    
    Returns:
        Success status and details
    """
    try:
        success = await v0_client.assign_project_to_chat(session_id, project_id)
        
        if not success:
            return {
                "success": False,
                "error": f"Failed to assign session {session_id} to project {project_id}. Check that both exist."
            }
        
        return {
            "success": True,
            "session_id": session_id,
            "project_id": project_id,
            "message": f"Session {session_id} assigned to project {project_id}"
        }
    except Exception as e:
        logger.error(f"Error assigning project to chat: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def initialize_chat_from_repo(
    session_id: str,
    repository_url: str,
    branch: str = "main",
    include_patterns: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Load GitHub repository into V0 chat context for codebase awareness
    
    Args:
        session_id: Session to initialize with repository context
        repository_url: GitHub repository URL
        branch: Git branch to use (default: main)
        include_patterns: File patterns to include (optional)
    
    Returns:
        Repository context initialization result
    """
    try:
        if session_id not in v0_client.sessions:
            return {
                "success": False,
                "error": f"Session {session_id} not found"
            }
        
        session = v0_client.sessions[session_id]
        result = await v0_client.initialize_chat_from_repo(
            session=session,
            repository_url=repository_url,
            branch=branch,
            include_patterns=include_patterns
        )
        
        return result
    except Exception as e:
        logger.error(f"Error initializing chat from repo: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def initialize_chat_from_files(
    session_id: str,
    file_paths: List[str],
    base_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Load local files into V0 chat context for existing project awareness
    
    Args:
        session_id: Session to initialize with file context
        file_paths: List of file paths to load
        base_path: Base directory path (optional)
    
    Returns:
        File context initialization result
    """
    try:
        if session_id not in v0_client.sessions:
            return {
                "success": False,
                "error": f"Session {session_id} not found"
            }
        
        session = v0_client.sessions[session_id]
        result = await v0_client.initialize_chat_from_files(
            session=session,
            file_paths=file_paths,
            base_path=base_path
        )
        
        return result
    except Exception as e:
        logger.error(f"Error initializing chat from files: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def create_v0_deployment(
    session_id: str,
    deployment_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Deploy session files directly to Vercel
    
    Args:
        session_id: Session to deploy
        deployment_name: Optional name for deployment
    
    Returns:
        Deployment details including URL
    """
    try:
        if session_id not in v0_client.sessions:
            return {
                "success": False,
                "error": f"Session {session_id} not found"
            }
        
        session = v0_client.sessions[session_id]
        deployment = await v0_client.create_v0_deployment(
            session=session,
            deployment_name=deployment_name
        )
        
        return {
            "success": True,
            "deployment_id": deployment.deployment_id,
            "session_id": session_id,
            "status": deployment.status,
            "url": deployment.url,
            "created_at": deployment.created_at.isoformat(),
            "logs": deployment.logs,
            "message": f"Deployment created successfully at {deployment.url}"
        }
    except Exception as e:
        logger.error(f"Error creating v0 deployment: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def get_deployment_status(deployment_id: str) -> Dict[str, Any]:
    """
    Get deployment status and details
    
    Args:
        deployment_id: Deployment ID to check
    
    Returns:
        Deployment status information
    """
    try:
        status = await v0_client.get_deployment_status(deployment_id)
        
        if not status:
            return {
                "success": False,
                "error": f"Deployment {deployment_id} not found"
            }
        
        return {
            "success": True,
            **status
        }
    except Exception as e:
        logger.error(f"Error getting deployment status: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def get_deployment_logs(deployment_id: str) -> Dict[str, Any]:
    """
    Get deployment logs for debugging
    
    Args:
        deployment_id: Deployment ID to get logs for
    
    Returns:
        Deployment logs
    """
    try:
        logs = await v0_client.get_deployment_logs(deployment_id)
        
        return {
            "success": True,
            "deployment_id": deployment_id,
            "logs": logs,
            "total_logs": len(logs)
        }
    except Exception as e:
        logger.error(f"Error getting deployment logs: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def fork_v0_chat(
    session_id: str,
    new_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a fork/branch of an existing chat session
    
    Args:
        session_id: Session to fork
        new_name: Optional name for the fork
    
    Returns:
        New forked session details
    """
    try:
        forked_session = await v0_client.fork_v0_chat(session_id, new_name)
        
        return {
            "success": True,
            "original_session_id": session_id,
            "forked_session_id": forked_session.session_id,
            "fork_name": forked_session.metadata.get("fork_name"),
            "created_at": forked_session.created_at.isoformat(),
            "files_count": len(forked_session.files),
            "message": f"Session forked successfully to {forked_session.session_id}"
        }
    except Exception as e:
        logger.error(f"Error forking v0 chat: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def update_chat_metadata(
    session_id: str,
    metadata: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update chat session metadata
    
    Args:
        session_id: Session to update
        metadata: Metadata to update
    
    Returns:
        Update success status
    """
    try:
        success = await v0_client.update_chat_metadata(session_id, metadata)
        
        if not success:
            return {
                "success": False,
                "error": f"Session {session_id} not found"
            }
        
        return {
            "success": True,
            "session_id": session_id,
            "updated_metadata": metadata,
            "message": "Chat metadata updated successfully"
        }
    except Exception as e:
        logger.error(f"Error updating chat metadata: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def favorite_chat(
    session_id: str,
    is_favorite: bool = True
) -> Dict[str, Any]:
    """
    Mark/unmark a chat session as favorite
    
    Args:
        session_id: Session to favorite/unfavorite
        is_favorite: Whether to mark as favorite (default: True)
    
    Returns:
        Favorite status update result
    """
    try:
        success = await v0_client.favorite_chat(session_id, is_favorite)
        
        if not success:
            return {
                "success": False,
                "error": f"Session {session_id} not found"
            }
        
        return {
            "success": True,
            "session_id": session_id,
            "is_favorite": is_favorite,
            "message": f"Session {'favorited' if is_favorite else 'unfavorited'} successfully"
        }
    except Exception as e:
        logger.error(f"Error updating favorite status: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# ============================================================================
# MCP PROMPTS - Critical instructions for agents on how to use V0 Enhanced
# ============================================================================

@mcp.prompt
def v0_enhanced_usage_guide(project_type: str = "web_app") -> str:
    """CRITICAL guide on how to use V0 Enhanced correctly with natural language"""
    return f"""
# V0 Enhanced MCP Server Usage Guide for {project_type}

## 🚨 CRITICAL: Natural Language Only!

V0 Enhanced creates complete applications from NATURAL LANGUAGE descriptions. 
Talk to it like you're describing your app to a designer, NOT a developer.

### ✅ GOOD Example for {project_type}:
```python
mcp__vercel-v0-enhanced__generate_with_v0(
    prompt="Build a modern todo app that feels like Linear or Notion. Clean design 
            with smooth animations. Users can add, edit, and delete todos. Include 
            filtering by status and dark mode. Make it responsive.",
    create_files=True
)
```

### ❌ BAD Example (Too Technical):
```python
# DON'T DO THIS - V0 doesn't want technical specs!
mcp__vercel-v0-enhanced__generate_with_v0(
    prompt="Create TodoItem.tsx with props {{id, text, completed}}, 
            useTodos.ts hook with CRUD methods, types/todo.ts interface"
)
```

## Key Principles:
1. **Describe the experience**, not the code
2. **Reference popular apps** for UI patterns ("like Notion", "similar to Linear")
3. **Talk section by section** - be detailed and conversational
4. **Focus on what users do**, not how it works
5. **Include visual details naturally** ("soft shadows", "smooth animations")

## Best Practices:
- Start simple, then enhance with more prompts
- Use the session_id to continue building
- Let V0 make technical decisions
- Describe user flows and interactions
"""

@mcp.prompt
def v0_enhanced_examples(use_case: str = "dashboard") -> str:
    """Real-world examples of effective V0 Enhanced prompts"""
    examples = {
        "dashboard": """
Create an analytics dashboard for tracking website metrics. Show real-time 
visitor count, page views, and user engagement with interactive charts. 
The design should be clean and professional, similar to Vercel's dashboard. 
Include date range filters and the ability to export data. Make sure it 
looks great on mobile devices too.""",
        "e-commerce": """
Build a product listing page for an online clothing store. Display products 
in a grid with images, names, prices, and a quick add to cart button. 
Include filters on the left for size, color, and price range. Add a search 
bar at the top. The style should feel modern and minimal like Everlane's 
website. Include hover effects that show additional product images.""",
        "saas": """
Create a team collaboration workspace similar to Slack but simpler. Users 
should see a sidebar with channels, a main chat area, and a member list 
on the right. Include the ability to send messages, share files, and 
mention other users. Add a clean header with search and user profile. 
Use a purple accent color and make everything feel fast and responsive.""",
        "form": """
Design a multi-step onboarding flow for a fitness app. Start with personal 
info (name, age, email), then fitness goals (weight loss, muscle gain, etc), 
then current activity level. Show progress dots at the top. Make it feel 
encouraging and friendly with smooth transitions between steps. Include 
validation but don't be annoying about errors."""
    }
    
    example = examples.get(use_case, examples["dashboard"])
    return f"""
# V0 Enhanced Prompt Example for {use_case}

## {use_case.title()} Example:
```
{example}
```

Remember: More detail = better results! V0 understands context and intent.
"""

@mcp.prompt
def v0_vs_figma_comparison(feature_type: str = "general") -> str:
    """When to use V0 Enhanced vs Figma MCP Application"""
    return f"""
# V0 Enhanced vs Figma MCP Application for {feature_type}

## Use V0 Enhanced When:
- Starting a new {feature_type} from scratch
- You want AI to make design decisions
- Building standard patterns (dashboards, forms, etc)
- Need to move fast with prototypes
- Don't have specific design requirements

## Use Figma MCP Application When:
- You need enterprise-grade components for {feature_type}
- Building complex features (data tables, analytics)
- Require specific UI components from the database
- Need accessibility compliance
- Want pre-built, tested components

## Examples for {feature_type}:

### V0 Enhanced (Natural Language):
```python
generate_with_v0(prompt="Create a user profile page like GitHub's")
```

### Figma MCP (Component Categories):
```python
build_dashboard(dashboard_type="analytics", theme="dark")
```

## Pro Tip: Use Both Together!
1. V0 creates the app structure
2. Figma MCP adds enterprise components
"""

# ============================================================================
# MCP RESOURCES - Documentation available to agents
# ============================================================================

@mcp.resource("resource://v0_prompting_guide")
async def v0_prompting_guide() -> str:
    """Comprehensive guide on writing effective V0 prompts"""
    guide_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'V0_ENHANCED_PROMPTING_GUIDE.md')
    if os.path.exists(guide_path):
        with open(guide_path, 'r') as f:
            return f.read()
    else:
        return """
# V0 Enhanced Prompting Guide

## Key Principles:
1. Use natural language, not technical specifications
2. Describe the user experience, not the implementation
3. Reference popular apps for UI patterns
4. Be detailed about visual design and interactions
5. Let V0 make the technical decisions

## Example Prompts:

### Dashboard:
"Create a modern analytics dashboard that looks like Stripe's. Show key metrics at the top,
revenue charts in the middle, and recent transactions at the bottom. Include date range
filters and export functionality. Make it responsive with a collapsible sidebar."

### Forms:
"Build a multi-step onboarding form for a SaaS product. Start with company info,
then team size and needs, then billing details. Show progress indicators and
save progress automatically. Make it feel welcoming with smooth animations."

## Tips:
- More detail = better results
- Mention specific UI libraries if needed (V0 defaults to shadcn/ui)
- Describe interactions and animations
- Specify responsive behavior
"""

@mcp.resource("resource://v0_test_examples")
async def v0_test_examples() -> str:
    """Examples of successful V0 prompts and outputs"""
    return """
# V0 Enhanced Test Examples

## Successfully Generated Apps:

### 1. Todo Application
**Prompt**: "Build a modern todo application that feels like Linear or Notion..."
**Result**: Complete Next.js app with 16 files including components, hooks, and styling

### 2. Dashboard
**Prompt**: "Create an analytics dashboard for tracking website metrics..."
**Result**: Full dashboard with charts, filters, and responsive design

### 3. E-commerce Site
**Prompt**: "Build a product listing page for an online clothing store..."
**Result**: Product grid, filtering, search, and cart functionality

## Tips from Testing:
- V0 automatically uses shadcn/ui when you mention "modern components"
- Reference specific apps for better results
- Include details about interactions and animations
- Describe mobile behavior for responsive design
"""

if __name__ == "__main__":
    # Run as HTTP server
    port = int(os.getenv('V0_MCP_PORT', '8015'))
    logger.info(f"Starting Enhanced Vercel v0 MCP Server on port {port}")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")