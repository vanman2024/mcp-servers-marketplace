#!/usr/bin/env python3
"""
MCP Routing Server for Multi-Agent Orchestration

This server provides tools for coordinating multiple AI agents,
managing sessions, and routing tasks based on agent capabilities.
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastmcp import FastMCP
from pydantic import BaseModel, Field
import aiohttp
import redis.asyncio as redis
from uuid import uuid4

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("routing-mcp")

# Redis client for session state
redis_client = None

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# Agent registry (could be loaded from Supabase)
AGENT_REGISTRY = {
    "claude": {
        "capabilities": ["general", "coding", "architecture", "documentation"],
        "max_concurrent_tasks": 3
    },
    "openai": {
        "capabilities": ["general", "coding", "analysis"],
        "max_concurrent_tasks": 3
    },
    "ui-specialist": {
        "capabilities": ["frontend", "ui", "react", "css"],
        "max_concurrent_tasks": 2
    },
    "backend-specialist": {
        "capabilities": ["backend", "api", "database", "security"],
        "max_concurrent_tasks": 2
    },
    "test-specialist": {
        "capabilities": ["testing", "qa", "automation"],
        "max_concurrent_tasks": 2
    }
}

# Session tracking
active_sessions: Dict[str, Any] = {}

# In-memory storage as fallback when Redis is not available
memory_storage: Dict[str, Any] = {}

class RedisOrMemoryClient:
    """Wrapper that uses Redis if available, otherwise falls back to memory"""
    
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.memory = memory_storage
    
    async def setex(self, key: str, seconds: int, value: str):
        if self.redis:
            return await self.redis.setex(key, seconds, value)
        else:
            self.memory[key] = value
            return True
    
    async def get(self, key: str):
        if self.redis:
            return await self.redis.get(key)
        else:
            return self.memory.get(key)
    
    async def hset(self, key: str, field: str, value: str):
        if self.redis:
            return await self.redis.hset(key, field, value)
        else:
            if key not in self.memory:
                self.memory[key] = {}
            self.memory[key][field] = value
            return True
    
    async def delete(self, key: str):
        if self.redis:
            return await self.redis.delete(key)
        else:
            if key in self.memory:
                del self.memory[key]
            return True

async def init_redis():
    """Initialize Redis connection (optional)"""
    global redis_client
    try:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        real_redis_client = await redis.from_url(redis_url)
        # Test connection
        await real_redis_client.ping()
        logger.info("Redis connection established")
        redis_client = RedisOrMemoryClient(real_redis_client)
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}")
        logger.warning("Running without Redis - session state will not persist")
        redis_client = RedisOrMemoryClient(None)

async def get_supabase_headers():
    """Get headers for Supabase API calls"""
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

# Session Management Tools

@mcp.tool()
async def session_start(
    module_name: str = Field(..., description="Name of the module/feature being worked on"),
    agent_type: str = Field(..., description="Type of agent starting the session"),
    project_id: str = Field(..., description="Project ID from Supabase"),
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context for the session")
) -> Dict[str, Any]:
    """Start a new development session with context tracking"""
    try:
        session_id = str(uuid4())
        
        session_data = {
            "id": session_id,
            "module_name": module_name,
            "agent_type": agent_type,
            "context": context,
            "project_id": project_id,
            "started_at": datetime.utcnow().isoformat(),
            "status": "active",
            "checkpoints": [],
            "handoffs": []
        }
        
        # Store in memory
        active_sessions[session_id] = session_data
        
        # Store in Redis for persistence
        if redis_client:
            await redis_client.setex(
                f"session:{session_id}",
                3600 * 24,  # 24 hour TTL
                json.dumps(session_data)
            )
        
        # Record in Supabase
        if SUPABASE_URL and SUPABASE_KEY:
            async with aiohttp.ClientSession() as session:
                url = f"{SUPABASE_URL}/rest/v1/agent_sessions"
                headers = await get_supabase_headers()
                
                payload = {
                    "session_id": session_id,
                    "module_name": module_name,
                    "agent_type": agent_type,
                    "context": context,
                    "project_id": project_id,
                    "status": "active"
                }
                
                async with session.post(url, json=payload, headers=headers) as resp:
                    if resp.status != 201:
                        logger.warning(f"Failed to record session in Supabase: {await resp.text()}")
        
        return {
            "success": True,
            "session_id": session_id,
            "message": f"Started session for {module_name} with {agent_type}",
            "session": session_data
        }
        
    except Exception as e:
        logger.error(f"Failed to start session: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def session_checkpoint(
    session_id: str = Field(..., description="Session ID to checkpoint"),
    checkpoint_name: str = Field(..., description="Name of the checkpoint"),
    state: Dict[str, Any] = Field(..., description="Current state to save"),
    notes: str = Field("", description="Notes about the checkpoint")
) -> Dict[str, Any]:
    """Create a checkpoint in the current session for recovery"""
    try:
        if session_id not in active_sessions:
            # Try to load from Redis
            if redis_client:
                session_data = await redis_client.get(f"session:{session_id}")
                if session_data:
                    active_sessions[session_id] = json.loads(session_data)
                else:
                    return {"success": False, "error": "Session not found"}
            else:
                return {"success": False, "error": "Session not found"}
        
        checkpoint = {
            "name": checkpoint_name,
            "timestamp": datetime.utcnow().isoformat(),
            "state": state,
            "notes": notes
        }
        
        active_sessions[session_id]["checkpoints"].append(checkpoint)
        
        # Update Redis
        if redis_client:
            await redis_client.setex(
                f"session:{session_id}",
                3600 * 24,
                json.dumps(active_sessions[session_id])
            )
        
        return {
            "success": True,
            "message": f"Checkpoint '{checkpoint_name}' created",
            "checkpoint": checkpoint
        }
        
    except Exception as e:
        logger.error(f"Failed to create checkpoint: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def session_handoff(
    session_id: str = Field(..., description="Session ID to hand off"),
    target_agent: str = Field(..., description="Target agent to hand off to"),
    handoff_notes: str = Field(..., description="Notes for the receiving agent"),
    checkpoint_before_handoff: bool = Field(True, description="Create checkpoint before handoff")
) -> Dict[str, Any]:
    """Prepare session for handoff to another agent"""
    try:
        if session_id not in active_sessions:
            return {"success": False, "error": "Session not found"}
        
        session = active_sessions[session_id]
        
        # Create checkpoint if requested
        if checkpoint_before_handoff:
            await session_checkpoint(
                session_id=session_id,
                checkpoint_name=f"handoff_to_{target_agent}",
                state=session.get("context", {}),
                notes=f"Pre-handoff checkpoint to {target_agent}"
            )
        
        handoff = {
            "from_agent": session["agent_type"],
            "to_agent": target_agent,
            "timestamp": datetime.utcnow().isoformat(),
            "notes": handoff_notes,
            "session_duration": (
                datetime.utcnow() - datetime.fromisoformat(session["started_at"])
            ).total_seconds()
        }
        
        session["handoffs"].append(handoff)
        session["agent_type"] = target_agent
        session["status"] = "handed_off"
        
        # Update Redis
        if redis_client:
            await redis_client.setex(
                f"session:{session_id}",
                3600 * 24,
                json.dumps(session)
            )
        
        # Create handoff record in Supabase
        if SUPABASE_URL and SUPABASE_KEY:
            async with aiohttp.ClientSession() as http_session:
                url = f"{SUPABASE_URL}/rest/v1/agent_handoffs"
                headers = await get_supabase_headers()
                
                payload = {
                    "session_id": session_id,
                    "from_agent": handoff["from_agent"],
                    "to_agent": target_agent,
                    "notes": handoff_notes,
                    "project_id": session.get("project_id")
                }
                
                await http_session.post(url, json=payload, headers=headers)
        
        return {
            "success": True,
            "message": f"Session handed off to {target_agent}",
            "handoff": handoff,
            "session_id": session_id
        }
        
    except Exception as e:
        logger.error(f"Failed to handoff session: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def session_continue(
    session_id: str = Field(..., description="Session ID to continue")
) -> Dict[str, Any]:
    """Continue a previously started or handed-off session"""
    try:
        if session_id not in active_sessions:
            # Try to load from Redis
            if redis_client:
                session_data = await redis_client.get(f"session:{session_id}")
                if session_data:
                    active_sessions[session_id] = json.loads(session_data)
                else:
                    return {"success": False, "error": "Session not found"}
            else:
                return {"success": False, "error": "Session not found"}
        
        session = active_sessions[session_id]
        session["status"] = "active"
        session["continued_at"] = datetime.utcnow().isoformat()
        
        # Get latest checkpoint
        latest_checkpoint = None
        if session["checkpoints"]:
            latest_checkpoint = session["checkpoints"][-1]
        
        return {
            "success": True,
            "message": f"Continuing session for {session['module_name']}",
            "session": session,
            "latest_checkpoint": latest_checkpoint
        }
        
    except Exception as e:
        logger.error(f"Failed to continue session: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# Workflow Orchestration Tools

@mcp.tool()
async def workflow_trigger(
    workflow_name: str = Field(..., description="Name of the workflow to trigger"),
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Workflow parameters"),
    session_id: Optional[str] = Field(None, description="Associated session ID")
) -> Dict[str, Any]:
    """Trigger a predefined workflow"""
    try:
        workflow_id = str(uuid4())
        
        # Define workflow templates
        workflows = {
            "feature_implementation": [
                {"step": "requirements_analysis", "agent": "claude"},
                {"step": "backend_implementation", "agent": "backend-specialist"},
                {"step": "frontend_implementation", "agent": "ui-specialist"},
                {"step": "testing", "agent": "test-specialist"},
                {"step": "documentation", "agent": "claude"}
            ],
            "bug_fix": [
                {"step": "bug_analysis", "agent": "claude"},
                {"step": "fix_implementation", "agent": "backend-specialist"},
                {"step": "testing", "agent": "test-specialist"}
            ],
            "code_review": [
                {"step": "automated_checks", "agent": "claude"},
                {"step": "security_review", "agent": "backend-specialist"},
                {"step": "ui_review", "agent": "ui-specialist"}
            ]
        }
        
        if workflow_name not in workflows:
            return {
                "success": False,
                "error": f"Unknown workflow: {workflow_name}",
                "available_workflows": list(workflows.keys())
            }
        
        workflow_instance = {
            "id": workflow_id,
            "name": workflow_name,
            "parameters": parameters,
            "session_id": session_id,
            "steps": workflows[workflow_name],
            "current_step": 0,
            "status": "running",
            "started_at": datetime.utcnow().isoformat(),
            "results": []
        }
        
        # Store workflow state
        if redis_client:
            await redis_client.setex(
                f"workflow:{workflow_id}",
                3600 * 24,
                json.dumps(workflow_instance)
            )
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "message": f"Started workflow '{workflow_name}'",
            "workflow": workflow_instance
        }
        
    except Exception as e:
        logger.error(f"Failed to trigger workflow: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# Task Routing Tools

@mcp.tool()
async def route_task_to_agent(
    task_id: str = Field(..., description="Task ID to route"),
    task_type: str = Field(..., description="Type of task (e.g., 'frontend', 'backend', 'testing')"),
    agent_selector: str = Field("auto", description="Selection mode: 'auto' or 'manual'"),
    agent_id: Optional[str] = Field(None, description="Specific agent ID for manual selection"),
    complexity: str = Field("medium", description="Task complexity: low, medium, high")
) -> Dict[str, Any]:
    """Route a task to the most appropriate agent"""
    try:
        if agent_selector == "manual" and agent_id:
            selected_agent = agent_id
        else:
            # Auto-select based on task type and agent capabilities
            candidates = []
            for agent, info in AGENT_REGISTRY.items():
                if task_type in info["capabilities"]:
                    candidates.append(agent)
            
            if not candidates:
                # Fallback to general agents
                candidates = ["claude", "openai"]
            
            # Simple load balancing (in production, check actual workload)
            selected_agent = candidates[0]
        
        routing_decision = {
            "task_id": task_id,
            "task_type": task_type,
            "assigned_agent": selected_agent,
            "complexity": complexity,
            "routing_timestamp": datetime.utcnow().isoformat(),
            "routing_reason": f"Best match for {task_type} tasks"
        }
        
        # Record routing decision
        if SUPABASE_URL and SUPABASE_KEY:
            async with aiohttp.ClientSession() as session:
                url = f"{SUPABASE_URL}/rest/v1/task_routing"
                headers = await get_supabase_headers()
                
                await session.post(url, json=routing_decision, headers=headers)
        
        return {
            "success": True,
            "routing_decision": routing_decision,
            "message": f"Task {task_id} routed to {selected_agent}"
        }
        
    except Exception as e:
        logger.error(f"Failed to route task: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def get_agent_workload(
    agent_type: Optional[str] = Field(None, description="Specific agent type to check")
) -> Dict[str, Any]:
    """Check agent availability and current workload"""
    try:
        workload_info = {}
        
        # In production, this would query actual agent status
        # For now, return mock data based on agent registry
        agents_to_check = [agent_type] if agent_type else list(AGENT_REGISTRY.keys())
        
        for agent in agents_to_check:
            if agent in AGENT_REGISTRY:
                workload_info[agent] = {
                    "capabilities": AGENT_REGISTRY[agent]["capabilities"],
                    "max_concurrent_tasks": AGENT_REGISTRY[agent]["max_concurrent_tasks"],
                    "current_tasks": 0,  # Would query actual data
                    "availability": "available",
                    "estimated_wait_time": 0
                }
        
        return {
            "success": True,
            "workload": workload_info,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get agent workload: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# Continuation Management Tools

@mcp.tool()
async def continuation_create(
    session_id: str = Field(..., description="Session ID to create continuation for"),
    title: str = Field(..., description="Title for the continuation"),
    description: str = Field(..., description="Description of work completed and next steps"),
    files_modified: List[str] = Field(default_factory=list, description="List of files modified"),
    dependencies: List[str] = Field(default_factory=list, description="Dependencies or blockers"),
    next_agent_type: Optional[str] = Field(None, description="Suggested agent type for next phase")
) -> Dict[str, Any]:
    """Create a session continuation for handoff or resumption"""
    try:
        if session_id not in active_sessions:
            return {"success": False, "error": "Session not found"}
        
        continuation_id = str(uuid4())
        session = active_sessions[session_id]
        
        continuation = {
            "id": continuation_id,
            "session_id": session_id,
            "title": title,
            "description": description,
            "files_modified": files_modified,
            "dependencies": dependencies,
            "next_agent_type": next_agent_type,
            "created_at": datetime.utcnow().isoformat(),
            "created_by": session["agent_type"],
            "module_name": session["module_name"],
            "project_id": session.get("project_id")
        }
        
        # Store in Redis
        if redis_client:
            await redis_client.setex(
                f"continuation:{continuation_id}",
                3600 * 24 * 7,  # 7 day TTL
                json.dumps(continuation)
            )
        
        # Store in Supabase
        if SUPABASE_URL and SUPABASE_KEY:
            async with aiohttp.ClientSession() as http_session:
                url = f"{SUPABASE_URL}/rest/v1/session_continuations"
                headers = await get_supabase_headers()
                
                await http_session.post(url, json=continuation, headers=headers)
        
        return {
            "success": True,
            "continuation_id": continuation_id,
            "message": f"Created continuation '{title}'",
            "continuation": continuation
        }
        
    except Exception as e:
        logger.error(f"Failed to create continuation: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def continuation_list(
    session_id: Optional[str] = Field(None, description="Filter by session ID"),
    project_id: Optional[str] = Field(None, description="Filter by project ID"),
    limit: int = Field(10, description="Maximum number of continuations to return")
) -> Dict[str, Any]:
    """List session continuations with optional filtering"""
    try:
        continuations = []
        
        if SUPABASE_URL and SUPABASE_KEY:
            async with aiohttp.ClientSession() as session:
                url = f"{SUPABASE_URL}/rest/v1/session_continuations"
                headers = await get_supabase_headers()
                
                # Build query
                params = {"limit": limit}
                if session_id:
                    params["session_id"] = f"eq.{session_id}"
                if project_id:
                    params["project_id"] = f"eq.{project_id}"
                
                async with session.get(url, params=params, headers=headers) as resp:
                    if resp.status == 200:
                        continuations = await resp.json()
        
        return {
            "success": True,
            "continuations": continuations,
            "count": len(continuations)
        }
        
    except Exception as e:
        logger.error(f"Failed to list continuations: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# Branch Management Tools

@mcp.tool()
async def branch_create(
    branch_name: str = Field(..., description="Name for the new branch"),
    base_branch: str = Field("main", description="Base branch to create from"),
    session_id: Optional[str] = Field(None, description="Associated session ID"),
    auto_push: bool = Field(True, description="Automatically push to remote")
) -> Dict[str, Any]:
    """Create and manage a new development branch"""
    try:
        # This would integrate with GitHub MCP for actual branch operations
        branch_info = {
            "name": branch_name,
            "base": base_branch,
            "session_id": session_id,
            "created_at": datetime.utcnow().isoformat(),
            "status": "created"
        }
        
        # Store branch metadata
        if redis_client and session_id:
            await redis_client.hset(
                f"session:{session_id}",
                "branch_name",
                branch_name
            )
        
        return {
            "success": True,
            "message": f"Created branch '{branch_name}' from '{base_branch}'",
            "branch": branch_info
        }
        
    except Exception as e:
        logger.error(f"Failed to create branch: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def branch_pr_create(
    branch_name: str = Field(..., description="Branch to create PR from"),
    title: str = Field(..., description="PR title"),
    body: str = Field(..., description="PR description"),
    session_id: Optional[str] = Field(None, description="Associated session ID"),
    auto_link_issues: bool = Field(True, description="Automatically link related issues")
) -> Dict[str, Any]:
    """Create a pull request with automatic linking and context"""
    try:
        # Gather session context if available
        context = {}
        if session_id and session_id in active_sessions:
            session = active_sessions[session_id]
            context = {
                "module": session["module_name"],
                "started_at": session["started_at"],
                "checkpoints": len(session.get("checkpoints", [])),
                "handoffs": len(session.get("handoffs", []))
            }
        
        pr_info = {
            "branch": branch_name,
            "title": title,
            "body": body,
            "context": context,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # This would integrate with GitHub MCP for actual PR creation
        
        return {
            "success": True,
            "message": f"Created PR '{title}' from branch '{branch_name}'",
            "pr": pr_info
        }
        
    except Exception as e:
        logger.error(f"Failed to create PR: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# Sprint Management Tools

@mcp.tool()
async def sprint_create(
    name: str = Field(..., description="Sprint name"),
    start_date: str = Field(..., description="Sprint start date (ISO format)"),
    end_date: str = Field(..., description="Sprint end date (ISO format)"),
    project_id: str = Field(..., description="Project ID from Supabase"),
    goals: List[str] = Field(default_factory=list, description="Sprint goals")
) -> Dict[str, Any]:
    """Create a new sprint with goals and timeline"""
    try:
        sprint_id = str(uuid4())
        
        sprint = {
            "id": sprint_id,
            "name": name,
            "start_date": start_date,
            "end_date": end_date,
            "project_id": project_id,
            "goals": goals,
            "status": "planning",
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Store in Supabase
        if SUPABASE_URL and SUPABASE_KEY:
            async with aiohttp.ClientSession() as session:
                url = f"{SUPABASE_URL}/rest/v1/sprints"
                headers = await get_supabase_headers()
                
                await session.post(url, json=sprint, headers=headers)
        
        return {
            "success": True,
            "sprint_id": sprint_id,
            "message": f"Created sprint '{name}'",
            "sprint": sprint
        }
        
    except Exception as e:
        logger.error(f"Failed to create sprint: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def sprint_assign_task(
    task_id: str = Field(..., description="Task ID to assign"),
    sprint_id: str = Field(..., description="Sprint ID to assign to"),
    priority: str = Field("medium", description="Task priority in sprint")
) -> Dict[str, Any]:
    """Assign a task to a sprint with priority"""
    try:
        assignment = {
            "task_id": task_id,
            "sprint_id": sprint_id,
            "priority": priority,
            "assigned_at": datetime.utcnow().isoformat()
        }
        
        # Update task in Supabase
        if SUPABASE_URL and SUPABASE_KEY:
            async with aiohttp.ClientSession() as session:
                url = f"{SUPABASE_URL}/rest/v1/tasks"
                headers = await get_supabase_headers()
                
                update_data = {
                    "sprint_id": sprint_id,
                    "sprint_priority": priority
                }
                
                await session.patch(
                    f"{url}?id=eq.{task_id}",
                    json=update_data,
                    headers=headers
                )
        
        return {
            "success": True,
            "message": f"Assigned task {task_id} to sprint {sprint_id}",
            "assignment": assignment
        }
        
    except Exception as e:
        logger.error(f"Failed to assign task to sprint: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# Documentation Workflow Tools

@mcp.tool()
async def docs_workflow_start(
    project_id: str = Field(..., description="Project ID to document"),
    watch_paths: List[str] = Field(default_factory=list, description="Paths to watch for changes"),
    auto_generate: bool = Field(True, description="Automatically generate docs on changes")
) -> Dict[str, Any]:
    """Start automated documentation workflow"""
    try:
        workflow_id = str(uuid4())
        
        docs_workflow = {
            "id": workflow_id,
            "project_id": project_id,
            "watch_paths": watch_paths,
            "auto_generate": auto_generate,
            "status": "running",
            "started_at": datetime.utcnow().isoformat()
        }
        
        # Store workflow state
        if redis_client:
            await redis_client.setex(
                f"docs_workflow:{workflow_id}",
                3600 * 24,
                json.dumps(docs_workflow)
            )
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "message": "Started documentation workflow",
            "workflow": docs_workflow
        }
        
    except Exception as e:
        logger.error(f"Failed to start docs workflow: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# Coordination Tools

@mcp.tool()
async def coordinate_multi_agent_task(
    task_description: str = Field(..., description="Description of the complex task"),
    required_capabilities: List[str] = Field(..., description="List of required capabilities"),
    project_id: str = Field(..., description="Project ID from Supabase")
) -> Dict[str, Any]:
    """Coordinate a complex task requiring multiple agents"""
    try:
        coordination_id = str(uuid4())
        
        # Analyze required capabilities and create sub-tasks
        sub_tasks = []
        for capability in required_capabilities:
            # Find agents with this capability
            capable_agents = [
                agent for agent, info in AGENT_REGISTRY.items()
                if capability in info["capabilities"]
            ]
            
            if capable_agents:
                sub_task = {
                    "id": str(uuid4()),
                    "capability": capability,
                    "assigned_agents": capable_agents,
                    "status": "pending"
                }
                sub_tasks.append(sub_task)
        
        coordination_plan = {
            "id": coordination_id,
            "task_description": task_description,
            "required_capabilities": required_capabilities,
            "sub_tasks": sub_tasks,
            "project_id": project_id,
            "status": "planned",
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Store coordination plan
        if redis_client:
            await redis_client.setex(
                f"coordination:{coordination_id}",
                3600 * 24,
                json.dumps(coordination_plan)
            )
        
        return {
            "success": True,
            "coordination_id": coordination_id,
            "plan": coordination_plan,
            "message": f"Created coordination plan with {len(sub_tasks)} sub-tasks"
        }
        
    except Exception as e:
        logger.error(f"Failed to coordinate multi-agent task: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# Initialize server
def main():
    """Initialize and run the MCP server"""
    # Initialize Redis in a separate event loop
    loop = asyncio.new_event_loop()
    loop.run_until_complete(init_redis())
    loop.close()
    
    # Get port from environment or use default
    port = int(os.getenv('ROUTING_MCP_PORT', '8026'))
    
    logger.info(f"Starting Routing MCP Server on port {port}")
    
    # Run the FastMCP server
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
        path="/"
    )

if __name__ == "__main__":
    main()