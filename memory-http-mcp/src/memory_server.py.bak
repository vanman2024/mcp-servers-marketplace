#!/usr/bin/env python3
"""
Memory MCP Server - HTTP Implementation
Knowledge graph system for persistent information storage

Converted from official MCP TypeScript stdio server to FastMCP HTTP server
Based on: https://github.com/modelcontextprotocol/servers/blob/main/src/memory/index.ts
"""

import os
import json
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from threading import Lock

# FastMCP for HTTP serving
from fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Entity:
    """Represents a node in the knowledge graph"""
    def __init__(self, name: str, entity_type: str, observations: List[str] = None):
        self.name = name
        self.entity_type = entity_type
        self.observations = observations or []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "entityType": self.entity_type,
            "observations": self.observations
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Entity':
        return cls(
            name=data["name"],
            entity_type=data["entityType"],
            observations=data.get("observations", [])
        )


class Relation:
    """Represents an edge in the knowledge graph"""
    def __init__(self, from_entity: str, to_entity: str, relation_type: str):
        self.from_entity = from_entity
        self.to_entity = to_entity
        self.relation_type = relation_type
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "from": self.from_entity,
            "to": self.to_entity,
            "relationType": self.relation_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Relation':
        return cls(
            from_entity=data["from"],
            to_entity=data["to"],
            relation_type=data["relationType"]
        )


class KnowledgeGraph:
    """Main knowledge graph storage and operations"""
    
    def __init__(self, graph_path: str = None):
        """Initialize knowledge graph with optional persistent storage"""
        self.graph_path = Path(graph_path) if graph_path else Path.home() / ".mcp-memory-graph.json"
        self.entities: Dict[str, Entity] = {}
        self.relations: List[Relation] = []
        self._lock = Lock()
        
        # Load existing graph if available
        self._load_graph()
        logger.info(f"Knowledge graph initialized with {len(self.entities)} entities and {len(self.relations)} relations")
    
    def _load_graph(self):
        """Load graph from persistent storage"""
        if self.graph_path.exists():
            try:
                with open(self.graph_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load entities
                for entity_data in data.get("entities", []):
                    entity = Entity.from_dict(entity_data)
                    self.entities[entity.name] = entity
                
                # Load relations
                for relation_data in data.get("relations", []):
                    relation = Relation.from_dict(relation_data)
                    self.relations.append(relation)
                
                logger.info(f"Loaded knowledge graph from {self.graph_path}")
            except Exception as e:
                logger.error(f"Error loading graph: {e}")
    
    def _save_graph(self):
        """Save graph to persistent storage"""
        try:
            data = {
                "entities": [entity.to_dict() for entity in self.entities.values()],
                "relations": [relation.to_dict() for relation in self.relations],
                "lastModified": datetime.utcnow().isoformat()
            }
            
            # Ensure directory exists
            self.graph_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write atomically
            temp_path = self.graph_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            temp_path.replace(self.graph_path)
            logger.info(f"Saved knowledge graph to {self.graph_path}")
            
        except Exception as e:
            logger.error(f"Error saving graph: {e}")
            raise
    
    async def create_entities(self, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple new entities in the knowledge graph"""
        with self._lock:
            created = []
            errors = []
            
            for entity_data in entities:
                name = entity_data.get("name")
                entity_type = entity_data.get("entityType")
                observations = entity_data.get("observations", [])
                
                if not name or not entity_type:
                    errors.append({"entity": entity_data, "error": "Missing name or entityType"})
                    continue
                
                if name in self.entities:
                    errors.append({"entity": name, "error": "Entity already exists"})
                    continue
                
                entity = Entity(name, entity_type, observations)
                self.entities[name] = entity
                created.append(name)
            
            if created:
                self._save_graph()
            
            return {
                "success": len(errors) == 0,
                "created": created,
                "errors": errors,
                "totalEntities": len(self.entities)
            }
    
    async def create_relations(self, relations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple new relations between entities"""
        with self._lock:
            created = []
            errors = []
            
            for relation_data in relations:
                from_entity = relation_data.get("from")
                to_entity = relation_data.get("to")
                relation_type = relation_data.get("relationType")
                
                if not all([from_entity, to_entity, relation_type]):
                    errors.append({"relation": relation_data, "error": "Missing required fields"})
                    continue
                
                if from_entity not in self.entities:
                    errors.append({"relation": relation_data, "error": f"Entity '{from_entity}' not found"})
                    continue
                
                if to_entity not in self.entities:
                    errors.append({"relation": relation_data, "error": f"Entity '{to_entity}' not found"})
                    continue
                
                # Check if relation already exists
                exists = any(
                    r.from_entity == from_entity and 
                    r.to_entity == to_entity and 
                    r.relation_type == relation_type 
                    for r in self.relations
                )
                
                if exists:
                    errors.append({"relation": relation_data, "error": "Relation already exists"})
                    continue
                
                relation = Relation(from_entity, to_entity, relation_type)
                self.relations.append(relation)
                created.append(relation.to_dict())
            
            if created:
                self._save_graph()
            
            return {
                "success": len(errors) == 0,
                "created": created,
                "errors": errors,
                "totalRelations": len(self.relations)
            }
    
    async def add_observations(self, observations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Add observations to existing entities"""
        with self._lock:
            updated = []
            errors = []
            
            for obs_data in observations:
                entity_name = obs_data.get("entityName")
                contents = obs_data.get("contents", [])
                
                if not entity_name:
                    errors.append({"observation": obs_data, "error": "Missing entityName"})
                    continue
                
                if entity_name not in self.entities:
                    errors.append({"observation": obs_data, "error": f"Entity '{entity_name}' not found"})
                    continue
                
                entity = self.entities[entity_name]
                new_observations = [obs for obs in contents if obs not in entity.observations]
                entity.observations.extend(new_observations)
                
                if new_observations:
                    updated.append({
                        "entity": entity_name,
                        "addedObservations": len(new_observations)
                    })
            
            if updated:
                self._save_graph()
            
            return {
                "success": len(errors) == 0,
                "updated": updated,
                "errors": errors
            }
    
    async def delete_entities(self, entity_names: List[str]) -> Dict[str, Any]:
        """Delete entities and their associated relations"""
        with self._lock:
            deleted = []
            errors = []
            deleted_relations = 0
            
            for name in entity_names:
                if name not in self.entities:
                    errors.append({"entity": name, "error": "Entity not found"})
                    continue
                
                # Delete entity
                del self.entities[name]
                deleted.append(name)
                
                # Delete associated relations
                original_count = len(self.relations)
                self.relations = [
                    r for r in self.relations 
                    if r.from_entity != name and r.to_entity != name
                ]
                deleted_relations += original_count - len(self.relations)
            
            if deleted:
                self._save_graph()
            
            return {
                "success": len(errors) == 0,
                "deletedEntities": deleted,
                "deletedRelations": deleted_relations,
                "errors": errors,
                "remainingEntities": len(self.entities)
            }
    
    async def delete_observations(self, deletions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Delete specific observations from entities"""
        with self._lock:
            updated = []
            errors = []
            
            for deletion in deletions:
                entity_name = deletion.get("entityName")
                observations_to_delete = deletion.get("observations", [])
                
                if not entity_name:
                    errors.append({"deletion": deletion, "error": "Missing entityName"})
                    continue
                
                if entity_name not in self.entities:
                    errors.append({"deletion": deletion, "error": f"Entity '{entity_name}' not found"})
                    continue
                
                entity = self.entities[entity_name]
                original_count = len(entity.observations)
                entity.observations = [
                    obs for obs in entity.observations 
                    if obs not in observations_to_delete
                ]
                
                deleted_count = original_count - len(entity.observations)
                if deleted_count > 0:
                    updated.append({
                        "entity": entity_name,
                        "deletedObservations": deleted_count
                    })
            
            if updated:
                self._save_graph()
            
            return {
                "success": len(errors) == 0,
                "updated": updated,
                "errors": errors
            }
    
    async def delete_relations(self, relations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Delete specific relations from the graph"""
        with self._lock:
            deleted = []
            errors = []
            
            for relation_data in relations:
                from_entity = relation_data.get("from")
                to_entity = relation_data.get("to")
                relation_type = relation_data.get("relationType")
                
                if not all([from_entity, to_entity, relation_type]):
                    errors.append({"relation": relation_data, "error": "Missing required fields"})
                    continue
                
                # Find and remove matching relations
                original_count = len(self.relations)
                self.relations = [
                    r for r in self.relations
                    if not (r.from_entity == from_entity and 
                           r.to_entity == to_entity and 
                           r.relation_type == relation_type)
                ]
                
                if len(self.relations) < original_count:
                    deleted.append(relation_data)
                else:
                    errors.append({"relation": relation_data, "error": "Relation not found"})
            
            if deleted:
                self._save_graph()
            
            return {
                "success": len(errors) == 0,
                "deleted": deleted,
                "errors": errors,
                "remainingRelations": len(self.relations)
            }
    
    async def read_graph(self) -> Dict[str, Any]:
        """Read the entire knowledge graph"""
        with self._lock:
            return {
                "entities": [entity.to_dict() for entity in self.entities.values()],
                "relations": [relation.to_dict() for relation in self.relations],
                "metadata": {
                    "totalEntities": len(self.entities),
                    "totalRelations": len(self.relations),
                    "graphPath": str(self.graph_path)
                }
            }
    
    async def search_nodes(self, query: str) -> List[Dict[str, Any]]:
        """Search for nodes matching a query"""
        query_lower = query.lower()
        results = []
        
        with self._lock:
            for entity in self.entities.values():
                # Search in name
                if query_lower in entity.name.lower():
                    results.append({
                        "entity": entity.to_dict(),
                        "matchedField": "name",
                        "relevance": 1.0
                    })
                    continue
                
                # Search in type
                if query_lower in entity.entity_type.lower():
                    results.append({
                        "entity": entity.to_dict(),
                        "matchedField": "entityType",
                        "relevance": 0.8
                    })
                    continue
                
                # Search in observations
                for i, obs in enumerate(entity.observations):
                    if query_lower in obs.lower():
                        results.append({
                            "entity": entity.to_dict(),
                            "matchedField": f"observation[{i}]",
                            "relevance": 0.6
                        })
                        break
        
        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results
    
    async def open_nodes(self, names: List[str]) -> List[Dict[str, Any]]:
        """Open specific nodes by name"""
        results = []
        
        with self._lock:
            for name in names:
                if name in self.entities:
                    entity = self.entities[name]
                    
                    # Get related entities
                    outgoing = [
                        {"to": r.to_entity, "type": r.relation_type}
                        for r in self.relations if r.from_entity == name
                    ]
                    incoming = [
                        {"from": r.from_entity, "type": r.relation_type}
                        for r in self.relations if r.to_entity == name
                    ]
                    
                    results.append({
                        "entity": entity.to_dict(),
                        "relations": {
                            "outgoing": outgoing,
                            "incoming": incoming
                        }
                    })
                else:
                    results.append({
                        "error": f"Entity '{name}' not found"
                    })
        
        return results


# Initialize FastMCP server
mcp = FastMCP("memory")

# Get graph file path from environment or use default
graph_path = os.getenv('MEMORY_GRAPH_PATH')
knowledge_graph = KnowledgeGraph(graph_path)

# Register tools
@mcp.tool()
async def create_entities(entities: List[Dict[str, Any]], ctx: Optional[Context] = None) -> Dict[str, Any]:
    """
    Create multiple new entities in the knowledge graph.
    
    Args:
        entities: List of entities, each with:
            - name: Unique name for the entity
            - entityType: Type of the entity (e.g., 'person', 'place', 'concept')
            - observations: List of observation strings
        ctx: Optional context for logging and progress
    
    Returns:
        Result with created entities and any errors
    """
    if ctx:
        await ctx.info(f"Creating {len(entities)} entities in knowledge graph")
    
    try:
        result = await knowledge_graph.create_entities(entities)
        if ctx:
            successful = sum(1 for e in result.get('entities', []) if e.get('success'))
            await ctx.info(f"Successfully created {successful}/{len(entities)} entities")
        return result
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to create entities: {str(e)}")
        raise

@mcp.tool()
async def create_relations(relations: List[Dict[str, Any]], ctx: Optional[Context] = None) -> Dict[str, Any]:
    """
    Create multiple new relations between entities.
    
    Args:
        relations: List of relations, each with:
            - from: Name of the source entity
            - to: Name of the target entity
            - relationType: Type of the relation (e.g., 'knows', 'located_in')
        ctx: Optional context for logging and progress
    
    Returns:
        Result with created relations and any errors
    """
    if ctx:
        await ctx.info(f"Creating {len(relations)} relations in knowledge graph")
    
    try:
        result = await knowledge_graph.create_relations(relations)
        if ctx:
            successful = sum(1 for r in result.get('relations', []) if r.get('success'))
            await ctx.info(f"Successfully created {successful}/{len(relations)} relations")
        return result
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to create relations: {str(e)}")
        raise

@mcp.tool()
async def add_observations(observations: List[Dict[str, Any]], ctx: Optional[Context] = None) -> Dict[str, Any]:
    """
    Add new observations to existing entities.
    
    Args:
        observations: List of observation sets, each with:
            - entityName: Name of the entity to add observations to
            - contents: List of observation strings to add
        ctx: Optional context for logging and progress
    
    Returns:
        Result with updated entities and any errors
    """
    if ctx:
        total_obs = sum(len(obs.get('contents', [])) for obs in observations)
        await ctx.info(f"Adding {total_obs} observations to {len(observations)} entities")
    
    try:
        result = await knowledge_graph.add_observations(observations)
        if ctx:
            await ctx.info(f"Successfully added observations to entities")
        return result
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to add observations: {str(e)}")
        raise

@mcp.tool()
async def delete_entities(entity_names: List[str], ctx: Optional[Context] = None) -> Dict[str, Any]:
    """
    Delete multiple entities and their associated relations.
    
    Args:
        entity_names: List of entity names to delete
        ctx: Optional context for logging and progress
    
    Returns:
        Result with deleted entities, relations, and any errors
    """
    if ctx:
        await ctx.info(f"Deleting {len(entity_names)} entities from knowledge graph")
    
    try:
        result = await knowledge_graph.delete_entities(entity_names)
        if ctx:
            deleted = result.get('deleted_entities', 0)
            await ctx.info(f"Successfully deleted {deleted} entities")
        return result
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to delete entities: {str(e)}")
        raise

@mcp.tool()
async def delete_observations(deletions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Delete specific observations from entities.
    
    Args:
        deletions: List of deletion requests, each with:
            - entityName: Name of the entity
            - observations: List of observations to delete
    
    Returns:
        Result with updated entities and any errors
    """
    return await knowledge_graph.delete_observations(deletions)

@mcp.tool()
async def delete_relations(relations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Delete multiple relations from the knowledge graph.
    
    Args:
        relations: List of relations to delete, each with from, to, and relationType
    
    Returns:
        Result with deleted relations and any errors
    """
    return await knowledge_graph.delete_relations(relations)

@mcp.tool()
async def read_graph() -> Dict[str, Any]:
    """
    Read the entire knowledge graph.
    
    Returns:
        Complete graph with all entities, relations, and metadata
    """
    return await knowledge_graph.read_graph()

@mcp.tool()
async def search_nodes(query: str) -> List[Dict[str, Any]]:
    """
    Search for nodes in the knowledge graph based on a query.
    
    Args:
        query: Search query to match against names, types, and observations
    
    Returns:
        List of matching entities with relevance scores
    """
    return await knowledge_graph.search_nodes(query)

@mcp.tool()
async def open_nodes(names: List[str]) -> List[Dict[str, Any]]:
    """
    Open specific nodes by their names to see details and relations.
    
    Args:
        names: List of entity names to retrieve
    
    Returns:
        List of entities with their incoming and outgoing relations
    """
    return await knowledge_graph.open_nodes(names)

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv('MEMORY_MCP_PORT', '8002'))
    
    logger.info(f"Starting Memory MCP Server on port {port}")
    logger.info(f"Graph file: {knowledge_graph.graph_path}")
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")