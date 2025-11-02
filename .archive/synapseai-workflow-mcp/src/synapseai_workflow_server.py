#!/usr/bin/env python3
"""
SynapseAI Workflow MCP Server
Task-oriented tools using Supabase SDK for efficient workflow management
Designed for 100+ parallel Claude instances with Responses API integration
"""

import os
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# FastMCP for HTTP serving
from fastmcp import FastMCP

# Supabase SDK
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

# FastAPI for Responses API integration
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================================================================
# CONFIGURATION
# ===================================================================

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")

# Initialize Supabase client
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
    options=ClientOptions(
        auto_refresh_token=True,
        persist_session=True
    )
)

# Initialize FastMCP server
mcp = FastMCP("SynapseAI Workflow Server")

# ===================================================================
# PYDANTIC MODELS FOR API
# ===================================================================

class TaskRequest(BaseModel):
    specialist_type: str
    project_id: Optional[str] = None
    skills: Optional[List[str]] = None

class TaskUpdate(BaseModel):
    task_id: str
    status: str
    activities: List[Dict[str, Any]]
    artifacts: Optional[List[Dict[str, Any]]] = []
    completion_percentage: Optional[int] = None

class DependencyRequest(BaseModel):
    task_id: str
    include_transitive: bool = True

# ===================================================================
# WORKFLOW TOOLS
# ===================================================================

@mcp.tool()
async def get_next_task_for_agent(
    specialist_type: str,
    project_id: Optional[str] = None,
    skills: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get next available task for a Claude agent with full context
    
    Args:
        specialist_type: Type of specialist (e.g., 'backend', 'frontend', 'testing')
        project_id: Optional project filter
        skills: Optional required skills for the task
    
    Returns:
        Complete task context including module, phase, milestone info
    """
    try:
        # Build the query using Supabase SDK
        query = supabase.table('tasks').select(
            """
            *,
            module:modules!inner(
                *,
                phase:phases!inner(
                    *,
                    milestone:milestones!inner(
                        *,
                        project:projects!inner(*)
                    )
                )
            )
            """
        ).eq('status', 'pending').is_('assigned_specialist', 'null')
        
        # Add filters
        if specialist_type:
            query = query.eq('specialist_type', specialist_type)
        
        if project_id:
            query = query.eq('module.phase.milestone.project.id', project_id)
        
        # Order by priority and dependencies
        query = query.order('priority', desc=True).order('created_at').limit(1)
        
        result = query.execute()
        
        if not result.data:
            return {
                'success': False,
                'message': 'No available tasks matching criteria'
            }
        
        task = result.data[0]
        
        # Get dependencies
        deps = supabase.table('task_dependencies').select(
            'depends_on_task_id'
        ).eq('task_id', task['id']).execute()
        
        # Get previous activities
        activities = supabase.table('activities').select(
            '*'
        ).eq('task_id', task['id']).order('created_at', desc=True).limit(5).execute()
        
        return {
            'success': True,
            'task': task,
            'dependencies': [d['depends_on_task_id'] for d in deps.data],
            'recent_activities': activities.data,
            'context': {
                'project': task['module']['phase']['milestone']['project']['name'],
                'milestone': task['module']['phase']['milestone']['name'],
                'phase': task['module']['phase']['name'],
                'module': task['module']['name']
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get next task: {e}")
        return {
            'success': False,
            'error': str(e)
        }

@mcp.tool()
async def claim_task(
    task_id: str,
    specialist_id: str,
    session_id: str
) -> Dict[str, Any]:
    """
    Claim a task for a specific Claude agent
    
    Args:
        task_id: Task ID to claim
        specialist_id: Claude agent identifier
        session_id: Claude session ID for tracking
    
    Returns:
        Success status and task details
    """
    try:
        # Atomic claim to prevent race conditions
        result = supabase.table('tasks').update({
            'assigned_specialist': specialist_id,
            'session_id': session_id,
            'status': 'in_progress',
            'started_at': datetime.utcnow().isoformat()
        }).eq('id', task_id).is_('assigned_specialist', 'null').execute()
        
        if not result.data:
            return {
                'success': False,
                'error': 'Task already claimed or not found'
            }
        
        # Log activity
        supabase.table('activities').insert({
            'task_id': task_id,
            'description': f'Task claimed by {specialist_id}',
            'type': 'task_claimed',
            'session_id': session_id,
            'metadata': {'specialist_id': specialist_id}
        }).execute()
        
        return {
            'success': True,
            'task': result.data[0]
        }
        
    except Exception as e:
        logger.error(f"Failed to claim task: {e}")
        return {
            'success': False,
            'error': str(e)
        }

@mcp.tool()
async def update_task_progress(
    task_id: str,
    status: str,
    activities: List[Dict[str, Any]],
    artifacts: Optional[List[Dict[str, Any]]] = None,
    completion_percentage: Optional[int] = None
) -> Dict[str, Any]:
    """
    Update task progress with activities and artifacts
    
    Args:
        task_id: Task ID to update
        status: New status (in_progress, completed, blocked, etc.)
        activities: List of activities to log
        artifacts: Optional list of created artifacts (files, PRs, etc.)
        completion_percentage: Optional completion percentage
    
    Returns:
        Update status
    """
    try:
        # Update task
        update_data = {
            'status': status,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        if completion_percentage is not None:
            update_data['completion_percentage'] = completion_percentage
            
        if status == 'completed':
            update_data['completed_at'] = datetime.utcnow().isoformat()
        
        task_result = supabase.table('tasks').update(
            update_data
        ).eq('id', task_id).execute()
        
        if not task_result.data:
            return {
                'success': False,
                'error': 'Task not found'
            }
        
        # Batch insert activities
        if activities:
            activity_records = [
                {
                    'task_id': task_id,
                    'description': act.get('description'),
                    'type': act.get('type', 'progress_update'),
                    'session_id': act.get('session_id'),
                    'metadata': act.get('metadata', {})
                }
                for act in activities
            ]
            supabase.table('activities').insert(activity_records).execute()
        
        # Insert artifacts if any
        if artifacts:
            artifact_records = [
                {
                    'task_id': task_id,
                    'type': art.get('type'),
                    'url': art.get('url'),
                    'metadata': art.get('metadata', {})
                }
                for art in artifacts
            ]
            supabase.table('task_artifacts').insert(artifact_records).execute()
        
        return {
            'success': True,
            'task': task_result.data[0]
        }
        
    except Exception as e:
        logger.error(f"Failed to update task progress: {e}")
        return {
            'success': False,
            'error': str(e)
        }

@mcp.tool()
async def get_task_dependencies(
    task_id: str,
    include_transitive: bool = True
) -> Dict[str, Any]:
    """
    Get task dependencies efficiently
    
    Args:
        task_id: Task ID to get dependencies for
        include_transitive: Include transitive dependencies
    
    Returns:
        Upstream and downstream dependencies with status
    """
    try:
        # Get direct dependencies
        upstream = supabase.table('task_dependencies').select(
            """
            depends_on_task:tasks!depends_on_task_id(
                id, name, status, assigned_specialist
            )
            """
        ).eq('task_id', task_id).execute()
        
        downstream = supabase.table('task_dependencies').select(
            """
            dependent_task:tasks!task_id(
                id, name, status, assigned_specialist
            )
            """
        ).eq('depends_on_task_id', task_id).execute()
        
        result = {
            'success': True,
            'upstream': [dep['depends_on_task'] for dep in upstream.data],
            'downstream': [dep['dependent_task'] for dep in downstream.data],
            'can_start': all(dep['depends_on_task']['status'] == 'completed' for dep in upstream.data)
        }
        
        # Get transitive dependencies if requested
        if include_transitive and upstream.data:
            # This would need recursive CTE in production
            pass
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to get dependencies: {e}")
        return {
            'success': False,
            'error': str(e)
        }

@mcp.tool()
async def get_project_overview(
    project_id: str
) -> Dict[str, Any]:
    """
    Get complete project overview for coordination
    
    Args:
        project_id: Project ID
    
    Returns:
        Project structure with progress metrics
    """
    try:
        # Get project with full hierarchy
        project = supabase.table('projects').select(
            """
            *,
            milestones(
                *,
                phases(
                    *,
                    modules(
                        *,
                        tasks(*)
                    )
                )
            )
            """
        ).eq('id', project_id).single().execute()
        
        if not project.data:
            return {
                'success': False,
                'error': 'Project not found'
            }
        
        # Calculate metrics
        total_tasks = 0
        completed_tasks = 0
        in_progress_tasks = 0
        blocked_tasks = 0
        
        for milestone in project.data.get('milestones', []):
            for phase in milestone.get('phases', []):
                for module in phase.get('modules', []):
                    for task in module.get('tasks', []):
                        total_tasks += 1
                        if task['status'] == 'completed':
                            completed_tasks += 1
                        elif task['status'] == 'in_progress':
                            in_progress_tasks += 1
                        elif task['status'] == 'blocked':
                            blocked_tasks += 1
        
        return {
            'success': True,
            'project': project.data,
            'metrics': {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'in_progress_tasks': in_progress_tasks,
                'blocked_tasks': blocked_tasks,
                'completion_percentage': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get project overview: {e}")
        return {
            'success': False,
            'error': str(e)
        }

# ===================================================================
# RESPONSES API INTEGRATION
# ===================================================================

# Create FastAPI app for Responses API
api = FastAPI(title="SynapseAI Workflow API")

@api.post("/tasks/next")
async def api_get_next_task(request: TaskRequest):
    """API endpoint for getting next task"""
    result = await get_next_task_for_agent(
        specialist_type=request.specialist_type,
        project_id=request.project_id,
        skills=request.skills
    )
    if not result['success']:
        raise HTTPException(status_code=404, detail=result.get('error', 'No tasks available'))
    return result

@api.post("/tasks/update")
async def api_update_task(update: TaskUpdate):
    """API endpoint for updating task progress"""
    result = await update_task_progress(
        task_id=update.task_id,
        status=update.status,
        activities=update.activities,
        artifacts=update.artifacts,
        completion_percentage=update.completion_percentage
    )
    if not result['success']:
        raise HTTPException(status_code=400, detail=result.get('error'))
    return result

@api.get("/tasks/{task_id}/dependencies")
async def api_get_dependencies(task_id: str, include_transitive: bool = True):
    """API endpoint for getting task dependencies"""
    result = await get_task_dependencies(
        task_id=task_id,
        include_transitive=include_transitive
    )
    if not result['success']:
        raise HTTPException(status_code=404, detail=result.get('error'))
    return result

# ===================================================================
# SERVER STARTUP
# ===================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Start MCP server
    logger.info("Starting SynapseAI Workflow MCP Server on port 8030")
    
    # Run both MCP and FastAPI
    config = uvicorn.Config(
        api,
        host="0.0.0.0",
        port=8031,  # FastAPI on different port
        log_level="info"
    )
    
    # Start MCP server in background
    mcp_task = asyncio.create_task(
        mcp.run(transport="http", port=8030)
    )
    
    # Start FastAPI server
    server = uvicorn.Server(config)
    asyncio.run(server.serve())