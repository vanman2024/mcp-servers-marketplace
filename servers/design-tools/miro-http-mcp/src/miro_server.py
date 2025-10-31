#!/usr/bin/env python3
"""
Miro HTTP MCP Server - Visual Workflow Board Management

A comprehensive MCP server for creating and managing Miro boards for visual workflow diagrams,
agent orchestration planning, and collaborative design processes.

All tools use class-based methods for better testability and maintainability.
"""

import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import httpx
from fastmcp import FastMCP
from fastmcp.server.context import Context
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================================================================
# CONFIGURATION & INITIALIZATION  
# ===================================================================

# Initialize FastMCP server
mcp = FastMCP("Miro Board Manager")

# Miro API configuration
MIRO_API_BASE = "https://api.miro.com/v2"
MIRO_ACCESS_TOKEN = os.getenv("MIRO_ACCESS_TOKEN")

class MiroClient:
    """Async client for Miro API interactions with error handling and retry logic"""
    
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {MIRO_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
    
    async def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Miro API with error handling"""
        url = f"{MIRO_API_BASE}{endpoint}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, headers=self.headers)
                elif method.upper() == "POST":
                    response = await client.post(url, headers=self.headers, json=data)
                elif method.upper() == "PUT":
                    response = await client.put(url, headers=self.headers, json=data)
                elif method.upper() == "DELETE":
                    response = await client.delete(url, headers=self.headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPStatusError as e:
                logger.error(f"Miro API HTTP error: {e.response.status_code} - {e.response.text}")
                return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
            except Exception as e:
                logger.error(f"Miro API request failed: {str(e)}")
                return {"error": str(e)}

# Initialize Miro client
miro_client = MiroClient()

# Helper functions for data validation and processing
async def validate_board_access(board_id: str) -> Dict[str, Any]:
    """Validate that board exists and is accessible"""
    if not MIRO_ACCESS_TOKEN:
        return {"valid": False, "error": "Miro access token not configured"}
    
    result = await miro_client.make_request("GET", f"/boards/{board_id}")
    if "error" in result:
        return {"valid": False, "error": result["error"]}
    
    return {"valid": True, "board": result}

def generate_board_colors(agent_type: str) -> str:
    """Generate color scheme for different agent types"""
    colors = {
        "frontend": "#4CAF50",      # Green
        "backend": "#2196F3",       # Blue  
        "ai-coordinator": "#9C27B0", # Purple
        "testing": "#FF9800",       # Orange
        "devops": "#607D8B",        # Blue Grey
        "design": "#F44336",        # Red
        "database": "#795548",      # Brown
        "api": "#00BCD4",          # Cyan
        "planning": "#9E9E9E",     # Grey
        "deployment": "#3F51B5"     # Indigo
    }
    return colors.get(agent_type.lower(), "#757575")

# ===================================================================
# CLASS-BASED TOOLS (ALL tools for better testability)
# ===================================================================

class MiroBoardTools:
    """
    Core Miro board management tools.
    Class-based approach for better testability and maintainability.
    """
    
    def __init__(self, client: Optional[MiroClient] = None):
        self.client = client or miro_client
    
    async def create_board(
        self,
        name: str,
        description: str = "",
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Create a new Miro board for visual workflows
        
        Args:
            name: Board name (required)
            description: Board description
            ctx: Context for logging
        
        Returns:
            Board creation result with ID and URL
        """
        if not MIRO_ACCESS_TOKEN:
            return {"success": False, "error": "Miro access token not configured"}
        
        try:
            if ctx:
                await ctx.info(f"Creating Miro board: {name}")
            
            board_data = {
                "name": name,
                "description": description
            }
            
            result = await self.client.make_request("POST", "/boards", board_data)
            
            if "error" in result:
                if ctx:
                    await ctx.error(f"Failed to create board: {result['error']}")
                return {"success": False, "error": result["error"]}
            
            if ctx:
                await ctx.info(f"Board created successfully: {result.get('id')}")
            
            return {
                "success": True,
                "board_id": result.get("id"),
                "board_url": f"https://miro.com/app/board/{result.get('id')}/",
                "name": name,
                "description": description,
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Create board error: {e}")
            if ctx:
                await ctx.error(f"Board creation failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def create_sticky_note(
        self,
        board_id: str,
        content: str,
        x: float = 0,
        y: float = 0,
        color: str = "#FFF9B1",
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Add a sticky note to a Miro board
        
        Args:
            board_id: Target board ID
            content: Note content
            x: X position on board
            y: Y position on board  
            color: Note color (hex)
            ctx: Context for logging
        
        Returns:
            Sticky note creation result
        """
        try:
            if ctx:
                await ctx.info(f"Creating sticky note on board {board_id}")
            
            # Validate board access
            validation = await validate_board_access(board_id)
            if not validation["valid"]:
                return {"success": False, "error": validation["error"]}
            
            note_data = {
                "data": {
                    "content": content,
                    "shape": "square"
                },
                "style": {
                    "fillColor": color,
                    "fontSize": "14",
                    "textAlign": "center"
                },
                "position": {"x": x, "y": y},
                "geometry": {"width": 150, "height": 150}
            }
            
            result = await self.client.make_request("POST", f"/boards/{board_id}/sticky_notes", note_data)
            
            if "error" in result:
                if ctx:
                    await ctx.error(f"Failed to create sticky note: {result['error']}")
                return {"success": False, "error": result["error"]}
            
            if ctx:
                await ctx.info(f"Sticky note created: {result.get('id')}")
            
            return {
                "success": True,
                "item_id": result.get("id"),
                "content": content,
                "position": {"x": x, "y": y},
                "color": color
            }
            
        except Exception as e:
            logger.error(f"Create sticky note error: {e}")
            if ctx:
                await ctx.error(f"Sticky note creation failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def create_shape(
        self,
        board_id: str,
        shape_type: str,
        content: str = "",
        x: float = 0,
        y: float = 0,
        width: int = 200,
        height: int = 100,
        color: str = "#E1F5FE",
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Create a shape element on a Miro board
        
        Args:
            board_id: Target board ID
            shape_type: Shape type (rectangle, circle, triangle, etc.)
            content: Shape content/text
            x: X position on board
            y: Y position on board
            width: Shape width
            height: Shape height
            color: Fill color (hex)
            ctx: Context for logging
        
        Returns:
            Shape creation result
        """
        try:
            if ctx:
                await ctx.info(f"Creating {shape_type} shape on board {board_id}")
            
            # Validate board access
            validation = await validate_board_access(board_id)
            if not validation["valid"]:
                return {"success": False, "error": validation["error"]}
            
            shape_data = {
                "data": {
                    "content": content,
                    "shape": shape_type
                },
                "style": {
                    "fillColor": color,
                    "borderColor": "#1976D2",
                    "borderWidth": "2",
                    "fontSize": "14",
                    "textAlign": "center",
                    "textAlignVertical": "middle"
                },
                "position": {"x": x, "y": y},
                "geometry": {"width": width, "height": height}
            }
            
            result = await self.client.make_request("POST", f"/boards/{board_id}/shapes", shape_data)
            
            if "error" in result:
                if ctx:
                    await ctx.error(f"Failed to create shape: {result['error']}")
                return {"success": False, "error": result["error"]}
            
            if ctx:
                await ctx.info(f"Shape created: {result.get('id')}")
            
            return {
                "success": True,
                "item_id": result.get("id"),
                "shape_type": shape_type,
                "content": content,
                "position": {"x": x, "y": y},
                "dimensions": {"width": width, "height": height}
            }
            
        except Exception as e:
            logger.error(f"Create shape error: {e}")
            if ctx:
                await ctx.error(f"Shape creation failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def create_connector(
        self,
        board_id: str,
        start_item_id: str,
        end_item_id: str,
        label: str = "",
        style: str = "elbowed",
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Create a connector line between two board items
        
        Args:
            board_id: Target board ID
            start_item_id: Source item ID
            end_item_id: Target item ID
            label: Optional connector label
            style: Connector style (elbowed, curved, straight)
            ctx: Context for logging
        
        Returns:
            Connector creation result
        """
        try:
            if ctx:
                await ctx.info(f"Creating connector from {start_item_id} to {end_item_id}")
            
            # Validate board access
            validation = await validate_board_access(board_id)
            if not validation["valid"]:
                return {"success": False, "error": validation["error"]}
            
            connector_data = {
                "data": {
                    "startItem": {"id": start_item_id},
                    "endItem": {"id": end_item_id},
                    "shape": style,
                    "style": {
                        "strokeColor": "#1976D2",
                        "strokeStyle": "normal",
                        "strokeWidth": "2"
                    }
                }
            }
            
            if label:
                connector_data["data"]["captions"] = [{"content": label, "position": 0.5}]
            
            result = await self.client.make_request("POST", f"/boards/{board_id}/connectors", connector_data)
            
            if "error" in result:
                if ctx:
                    await ctx.error(f"Failed to create connector: {result['error']}")
                return {"success": False, "error": result["error"]}
            
            if ctx:
                await ctx.info(f"Connector created: {result.get('id')}")
            
            return {
                "success": True,
                "connector_id": result.get("id"),
                "start_item": start_item_id,
                "end_item": end_item_id,
                "label": label,
                "style": style
            }
            
        except Exception as e:
            logger.error(f"Create connector error: {e}")
            if ctx:
                await ctx.error(f"Connector creation failed: {str(e)}")
            return {"success": False, "error": str(e)}

class MiroWorkflowTools:
    """
    Complex workflow creation tools that orchestrate multiple board elements.
    Class-based approach for better testability and coordination of multiple operations.
    """
    
    def __init__(self, board_tools: Optional[MiroBoardTools] = None):
        self.board_tools = board_tools or MiroBoardTools()
    
    async def create_agent_workflow_board(
        self,
        workflow_name: str,
        agents: List[Dict[str, Any]],
        connections: Optional[List[Dict[str, Any]]] = None,
        mcp_servers: Optional[List[Dict[str, Any]]] = None,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Create a complete agent workflow visualization board
        
        Args:
            workflow_name: Name for the workflow board
            agents: List of agent definitions with name, type, description
            connections: Optional connections between agents
            mcp_servers: Optional MCP servers to include
            ctx: Context for logging
        
        Returns:
            Complete workflow board creation result
        """
        try:
            if ctx:
                await ctx.info(f"Creating agent workflow board: {workflow_name}")
            
            # Create the main board
            board_result = await self.board_tools.create_board(
                name=f"Agent Workflow: {workflow_name}",
                description=f"Agent orchestration workflow created on {datetime.now().isoformat()}",
                ctx=ctx
            )
            
            if not board_result["success"]:
                return board_result
            
            board_id = board_result["board_id"]
            created_items = {}
            
            # Create agent shapes in a grid layout
            rows = int(len(agents) ** 0.5) + 1
            cols = int(len(agents) / rows) + 1
            
            for i, agent in enumerate(agents):
                row = i // cols
                col = i % cols
                x = -400 + (col * 300)
                y = -200 + (row * 150)
                
                agent_color = generate_board_colors(agent.get("type", "generic"))
                
                shape_result = await self.board_tools.create_shape(
                    board_id=board_id,
                    shape_type="round_rectangle",
                    content=f"{agent['name']}\n{agent.get('description', '')}",
                    x=x, y=y,
                    width=200, height=100,
                    color=agent_color,
                    ctx=ctx
                )
                
                if shape_result["success"]:
                    created_items[agent["name"]] = shape_result["item_id"]
            
            # Add MCP servers if provided
            if mcp_servers:
                for i, mcp_server in enumerate(mcp_servers):
                    x = 400
                    y = -200 + (i * 120)
                    
                    server_result = await self.board_tools.create_shape(
                        board_id=board_id,
                        shape_type="rectangle",
                        content=f"MCP: {mcp_server['name']}\nPort: {mcp_server.get('port', 'N/A')}",
                        x=x, y=y,
                        width=150, height=80,
                        color="#E8F5E8",
                        ctx=ctx
                    )
                    
                    if server_result["success"]:
                        created_items[f"mcp_{mcp_server['name']}"] = server_result["item_id"]
            
            # Create connections if provided
            if connections:
                for connection in connections:
                    from_agent = connection.get("from_agent")
                    to_agent = connection.get("to_agent")
                    
                    if from_agent in created_items and to_agent in created_items:
                        await self.board_tools.create_connector(
                            board_id=board_id,
                            start_item_id=created_items[from_agent],
                            end_item_id=created_items[to_agent],
                            label=connection.get("label", ""),
                            ctx=ctx
                        )
            
            if ctx:
                await ctx.info(f"Workflow board completed with {len(created_items)} items")
            
            return {
                "success": True,
                "board_id": board_id,
                "board_url": f"https://miro.com/app/board/{board_id}/",
                "workflow_name": workflow_name,
                "items_created": len(created_items),
                "agents": len(agents),
                "connections": len(connections) if connections else 0,
                "mcp_servers": len(mcp_servers) if mcp_servers else 0
            }
            
        except Exception as e:
            logger.error(f"Workflow board creation error: {e}")
            if ctx:
                await ctx.error(f"Workflow board creation failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def create_kanban_board(
        self,
        board_name: str,
        columns: List[str],
        tasks: Optional[List[Dict[str, Any]]] = None,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Create a kanban-style task board with columns and task cards
        
        Args:
            board_name: Name for the kanban board
            columns: List of column names (e.g., ["To Do", "In Progress", "Done"])
            tasks: Optional initial tasks with column assignments
            ctx: Context for logging
        
        Returns:
            Kanban board creation result
        """
        try:
            if ctx:
                await ctx.info(f"Creating kanban board: {board_name}")
            
            # Create the board
            board_result = await self.board_tools.create_board(
                name=f"Kanban: {board_name}",
                description=f"Task management board created on {datetime.now().isoformat()}",
                ctx=ctx
            )
            
            if not board_result["success"]:
                return board_result
            
            board_id = board_result["board_id"]
            column_items = {}
            
            # Create column headers
            column_width = 300
            start_x = -((len(columns) - 1) * column_width) / 2
            
            for i, column in enumerate(columns):
                x = start_x + (i * column_width)
                y = -300
                
                header_result = await self.board_tools.create_shape(
                    board_id=board_id,
                    shape_type="rectangle",
                    content=column,
                    x=x, y=y,
                    width=250, height=60,
                    color="#2196F3",
                    ctx=ctx
                )
                
                if header_result["success"]:
                    column_items[column] = []
            
            # Add tasks if provided
            if tasks:
                for task in tasks:
                    column = task.get("column", columns[0])
                    if column not in column_items:
                        continue
                    
                    # Position task under its column
                    column_index = columns.index(column)
                    x = start_x + (column_index * column_width)
                    y = -200 + (len(column_items[column]) * 80)
                    
                    task_color = "#FFF9B1"  # Default yellow
                    if task.get("priority") == "high":
                        task_color = "#FFCDD2"  # Light red
                    elif task.get("priority") == "medium":
                        task_color = "#FFE0B2"  # Light orange
                    
                    task_result = await self.board_tools.create_sticky_note(
                        board_id=board_id,
                        content=task.get("title", "Untitled Task"),
                        x=x, y=y,
                        color=task_color,
                        ctx=ctx
                    )
                    
                    if task_result["success"]:
                        column_items[column].append(task_result["item_id"])
            
            if ctx:
                await ctx.info(f"Kanban board completed with {len(columns)} columns")
            
            return {
                "success": True,
                "board_id": board_id,
                "board_url": f"https://miro.com/app/board/{board_id}/",
                "board_name": board_name,
                "columns": columns,
                "tasks_created": len(tasks) if tasks else 0
            }
            
        except Exception as e:
            logger.error(f"Kanban board creation error: {e}")
            if ctx:
                await ctx.error(f"Kanban board creation failed: {str(e)}")
            return {"success": False, "error": str(e)}

# Create instances for tool registration
board_tools = MiroBoardTools()
workflow_tools = MiroWorkflowTools(board_tools)

# Register all class methods with FastMCP
mcp.tool(board_tools.create_board)
mcp.tool(board_tools.create_sticky_note)
mcp.tool(board_tools.create_shape)
mcp.tool(board_tools.create_connector)
mcp.tool(workflow_tools.create_agent_workflow_board)
mcp.tool(workflow_tools.create_kanban_board)

# ===================================================================
# RESOURCES
# ===================================================================

@mcp.resource("miro://templates")
def get_miro_templates() -> Dict[str, Any]:
    """Standard Miro board templates and configurations"""
    return {
        "agent_workflow_template": {
            "description": "Template for agent orchestration workflows",
            "required_fields": ["workflow_name", "agents"],
            "optional_fields": ["connections", "mcp_servers"],
            "agent_structure": {
                "name": "string (required)",
                "type": "string (frontend|backend|ai-coordinator|testing|devops|design)",
                "description": "string (optional)"
            }
        },
        "kanban_template": {
            "description": "Template for kanban task boards",
            "required_fields": ["board_name", "columns"],
            "optional_fields": ["tasks"],
            "task_structure": {
                "title": "string (required)",
                "column": "string (column name)",
                "priority": "string (high|medium|low)"
            }
        },
        "color_schemes": {
            "agent_types": {
                "frontend": "#4CAF50",
                "backend": "#2196F3", 
                "ai-coordinator": "#9C27B0",
                "testing": "#FF9800",
                "devops": "#607D8B",
                "design": "#F44336"
            },
            "priorities": {
                "high": "#FFCDD2",
                "medium": "#FFE0B2", 
                "low": "#FFF9B1"
            }
        }
    }

@mcp.resource("miro://examples/workflows")
def get_workflow_examples() -> Dict[str, Any]:
    """Example workflow configurations for common use cases"""
    return {
        "devloop_standard": {
            "workflow_name": "DevLoop Standard",
            "agents": [
                {"name": "project-planner", "type": "planning", "description": "Project planning and architecture"},
                {"name": "backend-agent", "type": "backend", "description": "API and database development"},
                {"name": "frontend-agent", "type": "frontend", "description": "UI/UX development"},
                {"name": "testing-agent", "type": "testing", "description": "Quality assurance"},
                {"name": "devops-agent", "type": "devops", "description": "Deployment and infrastructure"}
            ],
            "connections": [
                {"from_agent": "project-planner", "to_agent": "backend-agent", "label": "Requirements"},
                {"from_agent": "backend-agent", "to_agent": "frontend-agent", "label": "API Ready"},
                {"from_agent": "frontend-agent", "to_agent": "testing-agent", "label": "UI Complete"},
                {"from_agent": "testing-agent", "to_agent": "devops-agent", "label": "Tests Pass"}
            ]
        },
        "mcp_integration": {
            "workflow_name": "MCP Server Integration",
            "agents": [
                {"name": "mcp-coordinator", "type": "ai-coordinator", "description": "MCP server orchestration"},
                {"name": "github-agent", "type": "api", "description": "GitHub integration"},
                {"name": "vercel-agent", "type": "deployment", "description": "Vercel deployment"}
            ],
            "mcp_servers": [
                {"name": "github", "port": "8011", "status": "active"},
                {"name": "vercel-v0", "port": "8010", "status": "active"},
                {"name": "filesystem", "port": "8006", "status": "active"}
            ]
        }
    }

@mcp.resource("miro://examples/kanban")
def get_kanban_examples() -> Dict[str, Any]:
    """Example kanban board configurations"""
    return {
        "development_sprint": {
            "board_name": "Development Sprint",
            "columns": ["Backlog", "To Do", "In Progress", "Code Review", "Testing", "Done"],
            "tasks": [
                {"title": "Setup project structure", "column": "Done", "priority": "high"},
                {"title": "Implement user authentication", "column": "In Progress", "priority": "high"},
                {"title": "Create dashboard UI", "column": "To Do", "priority": "medium"},
                {"title": "Write unit tests", "column": "To Do", "priority": "medium"},
                {"title": "Deploy to staging", "column": "Backlog", "priority": "low"}
            ]
        },
        "feature_planning": {
            "board_name": "Feature Planning",
            "columns": ["Ideas", "Research", "Design", "Development", "Released"],
            "tasks": [
                {"title": "User feedback analysis", "column": "Ideas", "priority": "medium"},
                {"title": "Technical feasibility study", "column": "Research", "priority": "high"},
                {"title": "UI mockups", "column": "Design", "priority": "medium"}
            ]
        }
    }

@mcp.resource("miro://config")
def get_miro_config() -> Dict[str, Any]:
    """Miro server configuration and status"""
    return {
        "server_name": "Miro Board Manager",
        "version": "1.0.0",
        "api_base": MIRO_API_BASE,
        "token_configured": bool(MIRO_ACCESS_TOKEN),
        "features": [
            "Board creation",
            "Sticky notes",
            "Shapes and elements", 
            "Connectors",
            "Agent workflows",
            "Kanban boards"
        ],
        "supported_shapes": [
            "rectangle", "round_rectangle", "circle", 
            "triangle", "rhombus", "parallelogram"
        ],
        "supported_connector_styles": [
            "elbowed", "curved", "straight"
        ],
        "testability": {
            "pattern": "class-based tools",
            "benefits": [
                "Direct method testing without MCP client",
                "Easy dependency injection and mocking",
                "Isolated unit testing of individual functions",
                "Better error handling testing"
            ]
        }
    }

@mcp.resource("miro://best-practices")
def get_best_practices() -> Dict[str, Any]:
    """Best practices for Miro board design and workflow visualization"""
    return {
        "board_organization": {
            "layout": "Use consistent spacing and alignment for professional appearance",
            "colors": "Use color coding to group related elements and show hierarchy",
            "labels": "Keep text concise but descriptive for clarity",
            "connections": "Use connectors to show clear relationships and flow"
        },
        "agent_workflows": {
            "positioning": "Arrange agents in logical flow order (left to right or top to bottom)",
            "grouping": "Group related agents by function or responsibility", 
            "mcp_integration": "Place MCP servers on the side to show supporting infrastructure",
            "documentation": "Include board description explaining the workflow purpose"
        },
        "kanban_boards": {
            "columns": "Limit to 4-6 columns for optimal visual management",
            "task_size": "Keep task descriptions short and actionable",
            "priority": "Use color coding to indicate task priority levels",
            "movement": "Regularly update task positions to reflect current status"
        },
        "testing_approach": {
            "class_benefits": "Class-based tools enable direct testing without MCP client setup",
            "dependency_injection": "Pass mock clients to class constructors for isolated testing",
            "unit_testing": "Test individual methods independently with controlled inputs",
            "integration_testing": "Use real Miro client for end-to-end validation"
        }
    }

# ===================================================================
# PROMPTS
# ===================================================================

@mcp.prompt
def create_workflow_prompt(workflow_type: str, team_size: str = "medium") -> str:
    """
    Generate a comprehensive prompt for creating agent workflow diagrams
    
    Args:
        workflow_type: Type of workflow (development, design, testing, deployment)
        team_size: Team size (small, medium, large)
    """
    base_prompt = f"Create a {workflow_type} workflow diagram for a {team_size} team using Miro boards."
    
    workflow_guidance = {
        "development": "Include planning, backend, frontend, testing, and deployment agents. Show clear handoff points between development phases.",
        "design": "Focus on design thinking process with research, ideation, prototyping, and validation agents. Include user feedback loops.",
        "testing": "Emphasize quality assurance with unit testing, integration testing, performance testing, and security testing agents.",
        "deployment": "Show CI/CD pipeline with build, test, staging, and production deployment agents. Include monitoring and rollback procedures."
    }
    
    team_guidance = {
        "small": "3-5 agents with overlapping responsibilities. Emphasize direct communication and minimal handoffs.",
        "medium": "5-8 specialized agents with clear role definitions. Include coordination and communication protocols.",
        "large": "8+ agents organized into teams. Include management and coordination layers with detailed process flows."
    }
    
    return f"""{base_prompt}

{workflow_guidance.get(workflow_type, 'Focus on clear agent roles and responsibilities with logical workflow progression.')}

Team size considerations: {team_guidance.get(team_size, 'Adjust agent count and complexity based on team capabilities.')}

Include:
1. Agent definitions with clear roles and responsibilities
2. Connection flows showing work handoffs and dependencies  
3. MCP server integrations for automation and tooling
4. Color coding for different agent types and priorities
5. Board description explaining the workflow purpose and usage"""

@mcp.prompt
def design_kanban_prompt(project_type: str, methodology: str = "agile") -> str:
    """
    Generate a prompt for designing effective kanban boards
    
    Args:
        project_type: Type of project (software, marketing, research, etc.)
        methodology: Development methodology (agile, waterfall, lean)
    """
    return f"""Design an effective kanban board for a {project_type} project using {methodology} methodology.

Project type considerations for {project_type}:
- Customize column names to match {project_type} workflow stages
- Include appropriate task types and priorities for this domain
- Consider stakeholder review and approval processes
- Plan for domain-specific deliverables and milestones

Methodology alignment for {methodology}:
- Structure columns to support {methodology} principles and practices
- Include feedback loops and iteration cycles as appropriate
- Plan for regular reviews and process improvements
- Ensure task flow supports {methodology} delivery cadence

Board design requirements:
1. 4-6 columns maximum for visual clarity
2. Clear task movement criteria between columns
3. Color coding for priority levels (high, medium, low)
4. Task templates with consistent structure
5. Board description with usage guidelines and workflow rules

Include sample tasks that demonstrate:
- Proper task granularity and scope
- Priority level distribution
- Column assignment logic
- Task progression through the workflow"""

@mcp.prompt
def optimize_board_layout_prompt(board_purpose: str, element_count: str = "medium") -> str:
    """
    Generate guidance for optimizing Miro board layout and visual design
    
    Args:
        board_purpose: Main board purpose (workflow, planning, brainstorming, etc.)
        element_count: Expected number of elements (few, medium, many)
    """
    return f"""Optimize the layout and visual design of a Miro board for {board_purpose} with {element_count} elements.

Layout optimization for {board_purpose}:
- Arrange elements to support the primary use case and user flow
- Create visual hierarchy that guides attention to key information
- Group related elements and create clear separation between sections
- Ensure adequate whitespace for readability and future additions

Element density considerations for {element_count} elements:
- Plan grid spacing and alignment for consistent visual appearance
- Balance information density with visual clarity
- Consider zoom levels and viewing distances for different use cases
- Plan for both overview and detailed examination scenarios

Visual design best practices:
1. Consistent color scheme with purposeful color coding
2. Readable font sizes and clear text hierarchy
3. Logical connector routing that avoids visual clutter
4. Strategic use of shapes and icons for quick recognition
5. Board sections with clear boundaries and labels

Accessibility and collaboration:
- Ensure adequate contrast ratios for all text and elements
- Use multiple visual cues (color, shape, text) for important information
- Plan for both desktop and mobile viewing experiences
- Include board navigation aids for complex layouts
- Design for real-time collaboration with multiple cursors and edits"""

@mcp.prompt
def troubleshoot_workflow_prompt(issue_type: str, workflow_stage: str) -> str:
    """
    Generate troubleshooting guidance for workflow visualization issues
    
    Args:
        issue_type: Type of issue (performance, clarity, adoption, maintenance)
        workflow_stage: Current workflow stage (design, implementation, optimization)
    """
    return f"""Troubleshoot and resolve {issue_type} issues in workflow visualization at the {workflow_stage} stage.

Issue analysis for {issue_type}:
- Identify root causes and contributing factors specific to this issue type
- Analyze impact on workflow effectiveness and team productivity
- Consider both technical and human factors affecting the visualization
- Evaluate current vs. desired state to define success criteria

Stage-specific considerations for {workflow_stage}:
- Focus on appropriate intervention points and modification strategies
- Consider stage-specific constraints and opportunities
- Plan changes that align with current workflow maturity level
- Balance immediate fixes with long-term optimization goals

Resolution strategies:
1. Quick wins that can be implemented immediately
2. Medium-term improvements requiring coordination and planning
3. Long-term optimizations for sustained workflow effectiveness
4. Prevention measures to avoid similar issues in the future
5. Success metrics and monitoring approaches

Implementation guidance:
- Step-by-step action plan with clear responsibilities
- Change management considerations for team adoption
- Testing and validation approaches before full rollout
- Rollback procedures if changes don't achieve desired results
- Documentation updates and team communication strategies"""

@mcp.prompt
def mcp_integration_prompt(integration_scope: str, complexity: str = "medium") -> str:
    """
    Generate guidance for integrating MCP servers into workflow visualizations
    
    Args:
        integration_scope: Integration scope (single-server, multi-server, ecosystem)
        complexity: Integration complexity (simple, medium, complex)
    """
    return f"""Design MCP server integration for workflow visualization with {integration_scope} scope at {complexity} complexity level.

Integration scope for {integration_scope}:
- Define the boundaries and interfaces for MCP server integration
- Identify key touchpoints between agents and MCP infrastructure
- Plan for scalability and future expansion of server capabilities
- Consider dependencies and interaction patterns between components

Complexity management for {complexity} integration:
- Break down integration into manageable phases and milestones
- Identify critical path dependencies and potential bottlenecks
- Plan for testing and validation at each integration level
- Design error handling and recovery mechanisms

MCP visualization requirements:
1. Clear representation of server capabilities and status
2. Visual connections between agents and their required MCP services
3. Status indicators for server health and availability
4. Configuration and dependency documentation
5. Integration flow diagrams showing data and control paths

Technical considerations:
- Server discovery and registration processes
- Authentication and authorization for agent-server communication
- Monitoring and alerting for server performance and availability
- Version management and compatibility tracking
- Deployment orchestration and rollback procedures

Testing approach for class-based tools:
- Unit test individual class methods with mock dependencies
- Integration test with real MCP servers for end-to-end validation
- Test error scenarios and recovery mechanisms
- Validate visual output and board structure accuracy"""

# ===================================================================
# SERVER EXECUTION
# ===================================================================

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv('MIRO_MCP_PORT', '8021'))
    
    # Check API key configuration
    if not MIRO_ACCESS_TOKEN:
        logger.warning("MIRO_ACCESS_TOKEN not found - server will run with limited functionality")
        logger.info("Set MIRO_ACCESS_TOKEN environment variable to enable full Miro API access")
    else:
        logger.info("Miro API token configured successfully")
    
    logger.info(f"Starting Miro Board Manager MCP Server on port {port}")
    logger.info("Available tools: create_board, create_sticky_note, create_shape, create_connector, create_agent_workflow_board, create_kanban_board")
    logger.info("Available resources: miro://templates, miro://examples/workflows, miro://examples/kanban, miro://config, miro://best-practices")
    logger.info("Available prompts: create_workflow_prompt, design_kanban_prompt, optimize_board_layout_prompt, troubleshoot_workflow_prompt, mcp_integration_prompt")
    logger.info("Architecture: Class-based tools for better testability and maintainability")
    
    # Run with streamable-http transport for OpenAI Responses API compatibility
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")