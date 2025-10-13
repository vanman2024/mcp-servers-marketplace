#!/usr/bin/env python3
"""
Docker HTTP MCP Server
Container management and orchestration tools for DevLoop3 autonomous workflows.
Based on the QuantGeekDev/docker-mcp pattern with FastMCP HTTP transport.
"""

import os
import json
import subprocess
from typing import Any, Dict, List, Optional, Union
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Docker HTTP Server")

async def run_docker_command(cmd: List[str]) -> Dict[str, Any]:
    """Execute docker command and return structured result"""
    try:
        result = subprocess.run(
            ["docker"] + cmd, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
            "command": " ".join(["docker"] + cmd)
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Command timed out after 30 seconds",
            "command": " ".join(["docker"] + cmd)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "command": " ".join(["docker"] + cmd)
        }

@mcp.tool()
async def docker_list_containers(all: bool = False, filters: Optional[str] = None) -> Dict[str, Any]:
    """List Docker containers"""
    try:
        cmd = ["ps", "--format", "json"]
        if all:
            cmd.append("--all")
        if filters:
            cmd.extend(["--filter", filters])
            
        result = await run_docker_command(cmd)
        
        if result["success"] and result["stdout"]:
            # Parse JSON output
            containers = []
            for line in result["stdout"].split('\n'):
                if line.strip():
                    containers.append(json.loads(line))
            result["containers"] = containers
            result["count"] = len(containers)
        else:
            result["containers"] = []
            result["count"] = 0
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_run_container(
    image: str,
    name: Optional[str] = None,
    ports: Optional[List[str]] = None,
    volumes: Optional[List[str]] = None,
    environment: Optional[List[str]] = None,
    detach: bool = True,
    remove: bool = False,
    interactive: bool = False,
    tty: bool = False,
    additional_args: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Run a new Docker container"""
    try:
        cmd = ["run"]
        
        if detach:
            cmd.append("-d")
        if remove:
            cmd.append("--rm")
        if interactive:
            cmd.append("-i")
        if tty:
            cmd.append("-t")
        if name:
            cmd.extend(["--name", name])
            
        if ports:
            for port in ports:
                cmd.extend(["-p", port])
                
        if volumes:
            for volume in volumes:
                cmd.extend(["-v", volume])
                
        if environment:
            for env in environment:
                cmd.extend(["-e", env])
                
        if additional_args:
            cmd.extend(additional_args)
            
        cmd.append(image)
        
        result = await run_docker_command(cmd)
        
        if result["success"]:
            result["container_id"] = result["stdout"]
            result["message"] = f"Container started successfully"
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_stop_container(container: str, timeout: int = 10) -> Dict[str, Any]:
    """Stop a running Docker container"""
    try:
        cmd = ["stop", "--time", str(timeout), container]
        result = await run_docker_command(cmd)
        
        if result["success"]:
            result["message"] = f"Container {container} stopped successfully"
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_start_container(container: str) -> Dict[str, Any]:
    """Start a stopped Docker container"""
    try:
        cmd = ["start", container]
        result = await run_docker_command(cmd)
        
        if result["success"]:
            result["message"] = f"Container {container} started successfully"
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_restart_container(container: str, timeout: int = 10) -> Dict[str, Any]:
    """Restart a Docker container"""
    try:
        cmd = ["restart", "--time", str(timeout), container]
        result = await run_docker_command(cmd)
        
        if result["success"]:
            result["message"] = f"Container {container} restarted successfully"
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_remove_container(container: str, force: bool = False, volumes: bool = False) -> Dict[str, Any]:
    """Remove a Docker container"""
    try:
        cmd = ["rm"]
        if force:
            cmd.append("--force")
        if volumes:
            cmd.append("--volumes")
        cmd.append(container)
        
        result = await run_docker_command(cmd)
        
        if result["success"]:
            result["message"] = f"Container {container} removed successfully"
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_exec_command(
    container: str, 
    command: List[str], 
    interactive: bool = False,
    tty: bool = False,
    user: Optional[str] = None,
    workdir: Optional[str] = None
) -> Dict[str, Any]:
    """Execute a command in a running container"""
    try:
        cmd = ["exec"]
        if interactive:
            cmd.append("-i")
        if tty:
            cmd.append("-t")
        if user:
            cmd.extend(["--user", user])
        if workdir:
            cmd.extend(["--workdir", workdir])
            
        cmd.append(container)
        cmd.extend(command)
        
        result = await run_docker_command(cmd)
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_logs(
    container: str, 
    follow: bool = False,
    tail: Optional[int] = None,
    since: Optional[str] = None,
    timestamps: bool = False
) -> Dict[str, Any]:
    """Get logs from a Docker container"""
    try:
        cmd = ["logs"]
        if follow:
            cmd.append("--follow")
        if tail:
            cmd.extend(["--tail", str(tail)])
        if since:
            cmd.extend(["--since", since])
        if timestamps:
            cmd.append("--timestamps")
        cmd.append(container)
        
        result = await run_docker_command(cmd)
        
        if result["success"]:
            result["logs"] = result["stdout"]
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_inspect_container(container: str) -> Dict[str, Any]:
    """Get detailed information about a container"""
    try:
        cmd = ["inspect", container]
        result = await run_docker_command(cmd)
        
        if result["success"] and result["stdout"]:
            result["container_info"] = json.loads(result["stdout"])[0]
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_list_images(all: bool = False, filters: Optional[str] = None) -> Dict[str, Any]:
    """List Docker images"""
    try:
        cmd = ["images", "--format", "json"]
        if all:
            cmd.append("--all")
        if filters:
            cmd.extend(["--filter", filters])
            
        result = await run_docker_command(cmd)
        
        if result["success"] and result["stdout"]:
            images = []
            for line in result["stdout"].split('\n'):
                if line.strip():
                    images.append(json.loads(line))
            result["images"] = images
            result["count"] = len(images)
        else:
            result["images"] = []
            result["count"] = 0
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_pull_image(image: str, platform: Optional[str] = None) -> Dict[str, Any]:
    """Pull a Docker image from registry"""
    try:
        cmd = ["pull"]
        if platform:
            cmd.extend(["--platform", platform])
        cmd.append(image)
        
        result = await run_docker_command(cmd)
        
        if result["success"]:
            result["message"] = f"Image {image} pulled successfully"
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_remove_image(image: str, force: bool = False, no_prune: bool = False) -> Dict[str, Any]:
    """Remove a Docker image"""
    try:
        cmd = ["rmi"]
        if force:
            cmd.append("--force")
        if no_prune:
            cmd.append("--no-prune")
        cmd.append(image)
        
        result = await run_docker_command(cmd)
        
        if result["success"]:
            result["message"] = f"Image {image} removed successfully"
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_build_image(
    path: str,
    tag: Optional[str] = None,
    dockerfile: Optional[str] = None,
    build_args: Optional[List[str]] = None,
    no_cache: bool = False
) -> Dict[str, Any]:
    """Build a Docker image from Dockerfile"""
    try:
        cmd = ["build"]
        if tag:
            cmd.extend(["-t", tag])
        if dockerfile:
            cmd.extend(["-f", dockerfile])
        if build_args:
            for arg in build_args:
                cmd.extend(["--build-arg", arg])
        if no_cache:
            cmd.append("--no-cache")
        cmd.append(path)
        
        result = await run_docker_command(cmd)
        
        if result["success"]:
            result["message"] = f"Image built successfully"
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_system_info() -> Dict[str, Any]:
    """Get Docker system information"""
    try:
        cmd = ["system", "info", "--format", "json"]
        result = await run_docker_command(cmd)
        
        if result["success"] and result["stdout"]:
            result["system_info"] = json.loads(result["stdout"])
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_system_prune(
    all: bool = False,
    volumes: bool = False,
    force: bool = False
) -> Dict[str, Any]:
    """Clean up Docker system (remove unused data)"""
    try:
        cmd = ["system", "prune"]
        if all:
            cmd.append("--all")
        if volumes:
            cmd.append("--volumes")
        if force:
            cmd.append("--force")
            
        result = await run_docker_command(cmd)
        
        if result["success"]:
            result["message"] = "System cleanup completed"
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_compose_up(
    file: Optional[str] = None,
    detach: bool = True,
    build: bool = False,
    services: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Start services using docker-compose"""
    try:
        cmd = ["compose"]
        if file:
            cmd.extend(["-f", file])
        cmd.append("up")
        if detach:
            cmd.append("-d")
        if build:
            cmd.append("--build")
        if services:
            cmd.extend(services)
            
        result = await run_docker_command(cmd)
        
        if result["success"]:
            result["message"] = "Docker Compose services started"
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_compose_down(
    file: Optional[str] = None,
    volumes: bool = False,
    remove_orphans: bool = False
) -> Dict[str, Any]:
    """Stop and remove docker-compose services"""
    try:
        cmd = ["compose"]
        if file:
            cmd.extend(["-f", file])
        cmd.append("down")
        if volumes:
            cmd.append("--volumes")
        if remove_orphans:
            cmd.append("--remove-orphans")
            
        result = await run_docker_command(cmd)
        
        if result["success"]:
            result["message"] = "Docker Compose services stopped"
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_network_list() -> Dict[str, Any]:
    """List Docker networks"""
    try:
        cmd = ["network", "ls", "--format", "json"]
        result = await run_docker_command(cmd)
        
        if result["success"] and result["stdout"]:
            networks = []
            for line in result["stdout"].split('\n'):
                if line.strip():
                    networks.append(json.loads(line))
            result["networks"] = networks
            result["count"] = len(networks)
        else:
            result["networks"] = []
            result["count"] = 0
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def docker_volume_list() -> Dict[str, Any]:
    """List Docker volumes"""
    try:
        cmd = ["volume", "ls", "--format", "json"]
        result = await run_docker_command(cmd)
        
        if result["success"] and result["stdout"]:
            volumes = []
            for line in result["stdout"].split('\n'):
                if line.strip():
                    volumes.append(json.loads(line))
            result["volumes"] = volumes
            result["count"] = len(volumes)
        else:
            result["volumes"] = []
            result["count"] = 0
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Get port from environment variable
    port = int(os.getenv('DOCKER_MCP_PORT', '8020'))
    
    print(f"Docker server initializing...")
    print(f"Starting Docker HTTP MCP Server on port {port}")
    print("Container management and orchestration tools")
    
    # Run the server
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")