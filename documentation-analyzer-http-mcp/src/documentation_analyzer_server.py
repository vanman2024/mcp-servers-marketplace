#!/usr/bin/env python3
"""
Documentation Analyzer HTTP MCP Server

AI-powered documentation analysis and management server with comprehensive tools
for indexing, analyzing, searching, and managing project documentation.

Port: 8036
"""

import os
import logging
import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import re
import ast
import inspect

from fastmcp import FastMCP
from fastmcp.server.context import Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Documentation Analyzer")

# ===================================================================
# CONFIGURATION & INITIALIZATION
# ===================================================================

# Server configuration
ANALYZER_CONFIG = {
    "supported_extensions": [
        ".md", ".rst", ".txt", ".adoc", ".html", ".xml",
        ".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".hpp",
        ".go", ".rs", ".rb", ".php", ".cs", ".swift", ".kt",
        ".yaml", ".yml", ".json", ".toml", ".ini", ".conf"
    ],
    "index_cache_dir": os.path.expanduser("~/.documentation-analyzer/cache"),
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "analysis_models": {
        "summarization": "gpt-3.5-turbo",
        "categorization": "gpt-3.5-turbo",
        "quality_assessment": "gpt-4"
    }
}

# In-memory storage for documentation index
documentation_index = {}
analysis_cache = {}
search_index = defaultdict(set)
relationships = defaultdict(list)

# Helper Functions
def calculate_file_hash(content: str) -> str:
    """Calculate hash of file content for change detection."""
    return hashlib.sha256(content.encode()).hexdigest()

def extract_metadata_from_content(content: str, file_path: str) -> Dict[str, Any]:
    """Extract metadata from file content based on type."""
    metadata = {
        "word_count": len(content.split()),
        "line_count": len(content.splitlines()),
        "has_code_blocks": bool(re.search(r'```[\s\S]*?```', content)),
        "headers": []
    }
    
    # Extract markdown headers
    if file_path.endswith('.md'):
        headers = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        metadata["headers"] = [{"level": len(h[0]), "text": h[1]} for h in headers]
    
    # Extract Python docstrings and classes
    if file_path.endswith('.py'):
        try:
            tree = ast.parse(content)
            metadata["classes"] = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            metadata["functions"] = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        except:
            pass
    
    return metadata

def build_search_tokens(content: str) -> List[str]:
    """Extract search tokens from content."""
    # Simple tokenization - in production, use proper NLP
    tokens = re.findall(r'\b\w+\b', content.lower())
    # Filter out common words (simplified)
    stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 'with', 'to'}
    return [t for t in tokens if len(t) > 2 and t not in stop_words]

# ===================================================================
# STANDALONE TOOLS (simple tools that don't call other tools)
# ===================================================================

@mcp.tool()
async def index_documentation(
    directory: str,
    recursive: bool = True,
    extensions: Optional[List[str]] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Index documentation files in a directory.
    
    Args:
        directory: Path to documentation directory
        recursive: Whether to recursively index subdirectories
        extensions: File extensions to index (uses config defaults if not provided)
        ctx: Context for logging and progress
    
    Returns:
        Index statistics and indexed files
    """
    try:
        if ctx:
            await ctx.info(f"Starting documentation indexing in {directory}")
        
        directory = os.path.expanduser(directory)
        if not os.path.exists(directory):
            return {"success": False, "error": f"Directory not found: {directory}"}
        
        extensions = extensions or ANALYZER_CONFIG["supported_extensions"]
        indexed_files = []
        errors = []
        
        # Walk through directory
        for root, dirs, files in os.walk(directory):
            if not recursive:
                dirs.clear()  # Don't recurse
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, directory)
                    
                    try:
                        # Read file content
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Calculate hash
                        file_hash = calculate_file_hash(content)
                        
                        # Extract metadata
                        metadata = extract_metadata_from_content(content, file_path)
                        
                        # Build search tokens
                        tokens = build_search_tokens(content)
                        
                        # Store in index
                        doc_id = relative_path
                        documentation_index[doc_id] = {
                            "path": file_path,
                            "relative_path": relative_path,
                            "hash": file_hash,
                            "size": len(content),
                            "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                            "metadata": metadata,
                            "indexed_at": datetime.now().isoformat()
                        }
                        
                        # Update search index
                        for token in tokens:
                            search_index[token].add(doc_id)
                        
                        indexed_files.append(relative_path)
                        
                        if ctx and len(indexed_files) % 10 == 0:
                            await ctx.report_progress(len(indexed_files), len(files))
                    
                    except Exception as e:
                        errors.append({"file": relative_path, "error": str(e)})
        
        if ctx:
            await ctx.info(f"Indexed {len(indexed_files)} documentation files")
        
        return {
            "success": True,
            "indexed_count": len(indexed_files),
            "total_size": sum(doc["size"] for doc in documentation_index.values()),
            "errors": errors,
            "index_stats": {
                "total_tokens": len(search_index),
                "avg_tokens_per_doc": sum(len(tokens) for tokens in search_index.values()) / max(len(documentation_index), 1)
            }
        }
        
    except Exception as e:
        logger.error(f"Documentation indexing error: {e}")
        if ctx:
            await ctx.error(f"Indexing failed: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def search_documentation(
    query: str,
    limit: int = 10,
    doc_types: Optional[List[str]] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Search indexed documentation.
    
    Args:
        query: Search query
        limit: Maximum results to return
        doc_types: Filter by document types (extensions)
        ctx: Context for logging
    
    Returns:
        Search results with relevance scores
    """
    try:
        if ctx:
            await ctx.info(f"Searching documentation for: {query}")
        
        # Tokenize query
        query_tokens = build_search_tokens(query.lower())
        
        # Calculate relevance scores
        scores = defaultdict(float)
        for token in query_tokens:
            if token in search_index:
                for doc_id in search_index[token]:
                    scores[doc_id] += 1.0
        
        # Filter by doc types if specified
        if doc_types:
            scores = {
                doc_id: score 
                for doc_id, score in scores.items() 
                if any(documentation_index[doc_id]["relative_path"].endswith(ext) for ext in doc_types)
            }
        
        # Sort by score
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        
        # Build results
        results = []
        for doc_id, score in sorted_results:
            doc = documentation_index[doc_id]
            results.append({
                "path": doc["relative_path"],
                "score": score,
                "size": doc["size"],
                "modified": doc["modified"],
                "metadata": doc["metadata"]
            })
        
        return {
            "success": True,
            "query": query,
            "results_count": len(results),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Documentation search error: {e}")
        if ctx:
            await ctx.error(f"Search failed: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_documentation_stats(
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Get statistics about indexed documentation.
    
    Args:
        ctx: Context for logging
    
    Returns:
        Comprehensive documentation statistics
    """
    try:
        if ctx:
            await ctx.info("Generating documentation statistics")
        
        # Calculate statistics
        stats = {
            "total_documents": len(documentation_index),
            "total_size": sum(doc["size"] for doc in documentation_index.values()),
            "index_size": len(search_index),
            "document_types": defaultdict(int),
            "largest_documents": [],
            "most_recent": [],
            "coverage_by_type": {}
        }
        
        # Group by type
        for doc_id, doc in documentation_index.items():
            ext = os.path.splitext(doc["relative_path"])[1]
            stats["document_types"][ext] += 1
        
        # Find largest documents
        sorted_by_size = sorted(
            documentation_index.items(), 
            key=lambda x: x[1]["size"], 
            reverse=True
        )[:5]
        stats["largest_documents"] = [
            {"path": doc["relative_path"], "size": doc["size"]} 
            for _, doc in sorted_by_size
        ]
        
        # Find most recent
        sorted_by_date = sorted(
            documentation_index.items(), 
            key=lambda x: x[1]["modified"], 
            reverse=True
        )[:5]
        stats["most_recent"] = [
            {"path": doc["relative_path"], "modified": doc["modified"]} 
            for _, doc in sorted_by_date
        ]
        
        return {
            "success": True,
            "stats": stats,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Statistics generation error: {e}")
        if ctx:
            await ctx.error(f"Stats generation failed: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def detect_documentation_changes(
    directory: str,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Detect changes in documentation since last index.
    
    Args:
        directory: Documentation directory to check
        ctx: Context for logging
    
    Returns:
        Changed, new, and deleted files
    """
    try:
        if ctx:
            await ctx.info(f"Detecting documentation changes in {directory}")
        
        directory = os.path.expanduser(directory)
        current_files = {}
        
        # Scan current files
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in ANALYZER_CONFIG["supported_extensions"]):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, directory)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    current_files[relative_path] = calculate_file_hash(content)
        
        # Compare with index
        changes = {
            "new": [],
            "modified": [],
            "deleted": []
        }
        
        # Find new and modified
        for path, hash in current_files.items():
            if path not in documentation_index:
                changes["new"].append(path)
            elif documentation_index[path]["hash"] != hash:
                changes["modified"].append(path)
        
        # Find deleted
        for doc_id in documentation_index:
            if doc_id not in current_files:
                changes["deleted"].append(doc_id)
        
        total_changes = len(changes["new"]) + len(changes["modified"]) + len(changes["deleted"])
        
        if ctx:
            await ctx.info(f"Detected {total_changes} documentation changes")
        
        return {
            "success": True,
            "changes": changes,
            "total_changes": total_changes,
            "checked_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Change detection error: {e}")
        if ctx:
            await ctx.error(f"Change detection failed: {str(e)}")
        return {"success": False, "error": str(e)}

# ===================================================================
# CLASS-BASED TOOLS (complex tools that call other tools)
# ===================================================================

class DocumentationAnalyzer:
    """
    Complex analysis tools that orchestrate multiple operations.
    Uses class-based pattern to avoid FunctionTool errors.
    """
    
    def __init__(self):
        self.analysis_cache = {}
        self.quality_thresholds = {
            "min_word_count": 100,
            "max_typo_ratio": 0.02,
            "min_header_ratio": 0.1,
            "max_complexity": 15
        }
    
    async def analyze_documentation_quality(
        self,
        paths: Optional[List[str]] = None,
        include_suggestions: bool = True,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Analyze documentation quality with AI-powered insights.
        
        Args:
            paths: Specific paths to analyze (all if None)
            include_suggestions: Include improvement suggestions
            ctx: Context for logging and progress
        
        Returns:
            Quality assessment with scores and suggestions
        """
        try:
            if ctx:
                await ctx.info("Starting documentation quality analysis")
            
            # Select documents to analyze
            docs_to_analyze = []
            if paths:
                for path in paths:
                    for doc_id, doc in documentation_index.items():
                        if path in doc["relative_path"]:
                            docs_to_analyze.append((doc_id, doc))
            else:
                docs_to_analyze = list(documentation_index.items())
            
            if not docs_to_analyze:
                return {"success": False, "error": "No documents found to analyze"}
            
            quality_results = []
            total_score = 0
            
            for i, (doc_id, doc) in enumerate(docs_to_analyze):
                if ctx:
                    await ctx.report_progress(i + 1, len(docs_to_analyze))
                
                # Read file content
                with open(doc["path"], 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Calculate quality metrics
                quality_score = await self._calculate_quality_score(content, doc)
                
                # Generate suggestions if requested
                suggestions = []
                if include_suggestions:
                    suggestions = await self._generate_improvement_suggestions(
                        content, quality_score, doc
                    )
                
                quality_results.append({
                    "path": doc["relative_path"],
                    "quality_score": quality_score["overall_score"],
                    "metrics": quality_score["metrics"],
                    "suggestions": suggestions
                })
                
                total_score += quality_score["overall_score"]
            
            average_score = total_score / len(docs_to_analyze)
            
            if ctx:
                await ctx.info(f"Quality analysis complete. Average score: {average_score:.2f}/10")
            
            return {
                "success": True,
                "analyzed_count": len(quality_results),
                "average_score": average_score,
                "results": quality_results,
                "summary": self._generate_quality_summary(quality_results)
            }
            
        except Exception as e:
            logger.error(f"Quality analysis error: {e}")
            if ctx:
                await ctx.error(f"Quality analysis failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _calculate_quality_score(self, content: str, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate quality score based on multiple metrics."""
        metrics = {
            "completeness": 0,
            "clarity": 0,
            "structure": 0,
            "consistency": 0,
            "technical_accuracy": 0
        }
        
        # Completeness check
        word_count = doc["metadata"]["word_count"]
        if word_count >= self.quality_thresholds["min_word_count"]:
            metrics["completeness"] = min(10, word_count / 100)
        else:
            metrics["completeness"] = word_count / self.quality_thresholds["min_word_count"] * 5
        
        # Structure check
        if doc["metadata"].get("headers"):
            header_ratio = len(doc["metadata"]["headers"]) / max(word_count / 100, 1)
            metrics["structure"] = min(10, header_ratio * 10)
        else:
            metrics["structure"] = 3  # Base score for unstructured docs
        
        # Clarity (simplified - in production use NLP)
        avg_sentence_length = word_count / max(content.count('.') + content.count('!') + content.count('?'), 1)
        if 15 <= avg_sentence_length <= 25:
            metrics["clarity"] = 8
        elif 10 <= avg_sentence_length <= 30:
            metrics["clarity"] = 6
        else:
            metrics["clarity"] = 4
        
        # Consistency (check for common patterns)
        metrics["consistency"] = 7  # Base score
        
        # Technical accuracy (simplified)
        metrics["technical_accuracy"] = 7  # Base score
        
        # Calculate overall score
        overall_score = sum(metrics.values()) / len(metrics)
        
        return {
            "overall_score": overall_score,
            "metrics": metrics
        }
    
    async def _generate_improvement_suggestions(
        self, 
        content: str, 
        quality_score: Dict[str, Any], 
        doc: Dict[str, Any]
    ) -> List[str]:
        """Generate improvement suggestions based on quality analysis."""
        suggestions = []
        
        metrics = quality_score["metrics"]
        
        if metrics["completeness"] < 5:
            suggestions.append("Add more detailed content to improve completeness")
        
        if metrics["structure"] < 5:
            suggestions.append("Add section headers to improve document structure")
        
        if metrics["clarity"] < 5:
            suggestions.append("Simplify sentence structure for better readability")
        
        if not doc["metadata"].get("has_code_blocks") and doc["path"].endswith('.md'):
            suggestions.append("Consider adding code examples to illustrate concepts")
        
        return suggestions
    
    def _generate_quality_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of quality analysis results."""
        total_suggestions = sum(len(r["suggestions"]) for r in results)
        
        # Group by score ranges
        score_distribution = {
            "excellent": len([r for r in results if r["quality_score"] >= 8]),
            "good": len([r for r in results if 6 <= r["quality_score"] < 8]),
            "needs_improvement": len([r for r in results if r["quality_score"] < 6])
        }
        
        return {
            "score_distribution": score_distribution,
            "total_suggestions": total_suggestions,
            "top_issues": self._identify_top_issues(results)
        }
    
    def _identify_top_issues(self, results: List[Dict[str, Any]]) -> List[str]:
        """Identify most common issues across documentation."""
        issue_counts = defaultdict(int)
        
        for result in results:
            for suggestion in result["suggestions"]:
                # Simple categorization
                if "completeness" in suggestion.lower():
                    issue_counts["Incomplete documentation"] += 1
                elif "structure" in suggestion.lower():
                    issue_counts["Poor structure"] += 1
                elif "clarity" in suggestion.lower():
                    issue_counts["Clarity issues"] += 1
                elif "example" in suggestion.lower():
                    issue_counts["Lacking examples"] += 1
        
        # Sort by frequency
        return [issue for issue, _ in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:3]]
    
    async def generate_documentation_summary(
        self,
        format: str = "markdown",
        include_toc: bool = True,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive documentation summary.
        
        Args:
            format: Output format (markdown, json, html)
            include_toc: Include table of contents
            ctx: Context for logging
        
        Returns:
            Generated summary in requested format
        """
        try:
            if ctx:
                await ctx.info(f"Generating documentation summary in {format} format")
            
            # Organize documents by structure
            doc_tree = self._build_documentation_tree()
            
            # Generate summary based on format
            if format == "markdown":
                summary = self._generate_markdown_summary(doc_tree, include_toc)
            elif format == "json":
                summary = doc_tree
            elif format == "html":
                summary = self._generate_html_summary(doc_tree, include_toc)
            else:
                return {"success": False, "error": f"Unsupported format: {format}"}
            
            return {
                "success": True,
                "format": format,
                "summary": summary,
                "document_count": len(documentation_index),
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Summary generation error: {e}")
            if ctx:
                await ctx.error(f"Summary generation failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _build_documentation_tree(self) -> Dict[str, Any]:
        """Build hierarchical tree of documentation."""
        tree = {"root": {}, "files": []}
        
        for doc_id, doc in documentation_index.items():
            parts = doc["relative_path"].split(os.sep)
            current = tree["root"]
            
            # Build directory structure
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            
            # Add file
            if "_files" not in current:
                current["_files"] = []
            current["_files"].append({
                "name": parts[-1],
                "path": doc["relative_path"],
                "size": doc["size"],
                "metadata": doc["metadata"]
            })
        
        return tree
    
    def _generate_markdown_summary(self, tree: Dict[str, Any], include_toc: bool) -> str:
        """Generate markdown formatted summary."""
        lines = ["# Documentation Summary\n"]
        
        if include_toc:
            lines.append("## Table of Contents\n")
            lines.extend(self._generate_toc_lines(tree["root"]))
            lines.append("\n---\n")
        
        lines.append("## Documentation Structure\n")
        lines.extend(self._generate_tree_lines(tree["root"]))
        
        return "\n".join(lines)
    
    def _generate_toc_lines(self, node: Dict[str, Any], level: int = 0) -> List[str]:
        """Generate table of contents lines."""
        lines = []
        indent = "  " * level
        
        for key, value in sorted(node.items()):
            if key == "_files":
                continue
            lines.append(f"{indent}- {key}/")
            lines.extend(self._generate_toc_lines(value, level + 1))
        
        return lines
    
    def _generate_tree_lines(self, node: Dict[str, Any], level: int = 0) -> List[str]:
        """Generate tree structure lines."""
        lines = []
        indent = "  " * level
        
        for key, value in sorted(node.items()):
            if key == "_files":
                for file in value:
                    lines.append(f"{indent}- **{file['name']}** ({file['size']} bytes)")
                    if file['metadata'].get('headers'):
                        for header in file['metadata']['headers'][:3]:
                            lines.append(f"{indent}  - {header['text']}")
            else:
                lines.append(f"{indent}### {key}/")
                lines.extend(self._generate_tree_lines(value, level + 1))
        
        return lines
    
    def _generate_html_summary(self, tree: Dict[str, Any], include_toc: bool) -> str:
        """Generate HTML formatted summary."""
        # Simplified HTML generation
        html = ["<html><body><h1>Documentation Summary</h1>"]
        
        if include_toc:
            html.append("<h2>Table of Contents</h2>")
            html.append("<ul>")
            html.extend(self._generate_html_toc(tree["root"]))
            html.append("</ul>")
        
        html.append("<h2>Documentation Structure</h2>")
        html.extend(self._generate_html_tree(tree["root"]))
        
        html.append("</body></html>")
        return "".join(html)
    
    def _generate_html_toc(self, node: Dict[str, Any]) -> List[str]:
        """Generate HTML table of contents."""
        lines = []
        
        for key, value in sorted(node.items()):
            if key == "_files":
                continue
            lines.append(f"<li>{key}/")
            if any(k != "_files" for k in value):
                lines.append("<ul>")
                lines.extend(self._generate_html_toc(value))
                lines.append("</ul>")
            lines.append("</li>")
        
        return lines
    
    def _generate_html_tree(self, node: Dict[str, Any], level: int = 3) -> List[str]:
        """Generate HTML tree structure."""
        lines = []
        
        for key, value in sorted(node.items()):
            if key == "_files":
                lines.append("<ul>")
                for file in value:
                    lines.append(f"<li><strong>{file['name']}</strong> ({file['size']} bytes)</li>")
                lines.append("</ul>")
            else:
                lines.append(f"<h{level}>{key}/</h{level}>")
                lines.extend(self._generate_html_tree(value, min(level + 1, 6)))
        
        return lines

# Create instance and register class methods
analyzer = DocumentationAnalyzer()
mcp.tool(analyzer.analyze_documentation_quality)
mcp.tool(analyzer.generate_documentation_summary)

# ===================================================================
# AI-POWERED TOOLS (placeholder for actual AI integration)
# ===================================================================

@mcp.tool()
async def ai_categorize_documentation(
    paths: Optional[List[str]] = None,
    categories: Optional[List[str]] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    AI-powered documentation categorization.
    
    Args:
        paths: Specific paths to categorize (all if None)
        categories: Custom categories to use
        ctx: Context for logging
    
    Returns:
        Categorization results
    """
    try:
        if ctx:
            await ctx.info("Starting AI-powered categorization")
        
        default_categories = [
            "API Reference",
            "User Guide",
            "Developer Guide",
            "Tutorial",
            "Configuration",
            "Architecture",
            "FAQ",
            "Troubleshooting",
            "Release Notes",
            "Other"
        ]
        
        categories = categories or default_categories
        categorized = defaultdict(list)
        
        # Simulate AI categorization (in production, use actual AI)
        docs_to_categorize = []
        if paths:
            for path in paths:
                for doc_id, doc in documentation_index.items():
                    if path in doc["relative_path"]:
                        docs_to_categorize.append((doc_id, doc))
        else:
            docs_to_categorize = list(documentation_index.items())
        
        for doc_id, doc in docs_to_categorize:
            # Simple rule-based categorization (replace with AI)
            path_lower = doc["relative_path"].lower()
            
            if "api" in path_lower:
                category = "API Reference"
            elif "guide" in path_lower or "tutorial" in path_lower:
                category = "User Guide"
            elif "config" in path_lower:
                category = "Configuration"
            elif "release" in path_lower or "changelog" in path_lower:
                category = "Release Notes"
            elif "faq" in path_lower:
                category = "FAQ"
            else:
                category = "Other"
            
            categorized[category].append({
                "path": doc["relative_path"],
                "confidence": 0.85  # Simulated confidence
            })
        
        return {
            "success": True,
            "categories": dict(categorized),
            "total_categorized": sum(len(docs) for docs in categorized.values()),
            "method": "ai_categorization"
        }
        
    except Exception as e:
        logger.error(f"AI categorization error: {e}")
        if ctx:
            await ctx.error(f"AI categorization failed: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def ai_summarize_documentation(
    path: str,
    max_length: int = 500,
    style: str = "technical",
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Generate AI-powered documentation summary.
    
    Args:
        path: Path to document to summarize
        max_length: Maximum summary length
        style: Summary style (technical, simple, executive)
        ctx: Context for logging
    
    Returns:
        Generated summary
    """
    try:
        if ctx:
            await ctx.info(f"Generating AI summary for {path}")
        
        # Find document
        doc_id = None
        for did, doc in documentation_index.items():
            if path in doc["relative_path"]:
                doc_id = did
                break
        
        if not doc_id:
            return {"success": False, "error": f"Document not found: {path}"}
        
        # Read content
        with open(documentation_index[doc_id]["path"], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simulate AI summarization (in production, use actual AI)
        lines = content.splitlines()
        
        # Extract key sentences (simplified)
        summary_lines = []
        if documentation_index[doc_id]["metadata"].get("headers"):
            # Use headers as structure
            for header in documentation_index[doc_id]["metadata"]["headers"][:3]:
                summary_lines.append(f"- {header['text']}")
        
        # Add first paragraph
        for line in lines:
            if line.strip() and not line.startswith('#'):
                summary_lines.append(line.strip())
                break
        
        summary = "\n".join(summary_lines)[:max_length]
        
        return {
            "success": True,
            "path": documentation_index[doc_id]["relative_path"],
            "summary": summary,
            "style": style,
            "word_count": len(summary.split())
        }
        
    except Exception as e:
        logger.error(f"AI summarization error: {e}")
        if ctx:
            await ctx.error(f"AI summarization failed: {str(e)}")
        return {"success": False, "error": str(e)}

# ===================================================================
# RESOURCES
# ===================================================================

@mcp.resource("docs://index")
def get_documentation_index() -> Dict[str, Any]:
    """Get complete documentation index."""
    return {
        "index": documentation_index,
        "total_documents": len(documentation_index),
        "last_updated": datetime.now().isoformat()
    }

@mcp.resource("docs://stats")
def get_index_statistics() -> Dict[str, Any]:
    """Get current index statistics."""
    return {
        "total_documents": len(documentation_index),
        "total_tokens": len(search_index),
        "document_types": list(set(
            os.path.splitext(doc["relative_path"])[1] 
            for doc in documentation_index.values()
        )),
        "cache_size": len(analysis_cache)
    }

@mcp.resource("docs://search/{query}")
def search_docs_resource(query: str) -> Dict[str, Any]:
    """Search documentation via resource endpoint."""
    # Simplified search for resource
    results = []
    query_lower = query.lower()
    
    for doc_id, doc in documentation_index.items():
        if query_lower in doc["relative_path"].lower():
            results.append({
                "path": doc["relative_path"],
                "size": doc["size"],
                "modified": doc["modified"]
            })
    
    return {
        "query": query,
        "results": results[:10],
        "total_matches": len(results)
    }

@mcp.resource("docs://quality/{path}")
def get_quality_assessment(path: str) -> Dict[str, Any]:
    """Get quality assessment for specific document."""
    # Find document
    doc_id = None
    for did, doc in documentation_index.items():
        if path in doc["relative_path"]:
            doc_id = did
            break
    
    if not doc_id:
        return {"error": f"Document not found: {path}"}
    
    # Return cached or basic assessment
    if doc_id in analysis_cache:
        return analysis_cache[doc_id]
    
    return {
        "path": documentation_index[doc_id]["relative_path"],
        "status": "not_analyzed",
        "message": "Run quality analysis to assess this document"
    }

@mcp.resource("docs://relationships")
def get_documentation_relationships() -> Dict[str, Any]:
    """Get relationships between documents."""
    return {
        "relationships": dict(relationships),
        "total_links": sum(len(rels) for rels in relationships.values())
    }

# ===================================================================
# PROMPTS
# ===================================================================

@mcp.prompt
def analyze_project_documentation(project_path: str) -> str:
    """Generate prompt for comprehensive project documentation analysis."""
    return f"""Analyze the documentation in {project_path} and provide:

1. **Coverage Assessment**: What aspects of the project are well-documented vs gaps
2. **Quality Evaluation**: Rate the documentation quality (clarity, completeness, accuracy)
3. **Organization Review**: How well organized is the documentation structure
4. **Improvement Priorities**: Top 5 specific improvements needed
5. **Best Practices**: Which documentation best practices are followed/missing

Focus on actionable insights that will improve developer experience."""

@mcp.prompt
def generate_documentation_template(doc_type: str, technology: str) -> str:
    """Generate documentation template for specific type and technology."""
    return f"""Create a comprehensive {doc_type} documentation template for a {technology} project.

Include:
- Standard sections for {doc_type}
- Best practices specific to {technology}
- Example content for each section
- Metadata/frontmatter requirements
- Cross-referencing patterns
- Code example formats

Make it ready to use with clear placeholders."""

@mcp.prompt
def documentation_migration_plan(from_format: str, to_format: str, volume: int) -> str:
    """Create migration plan for documentation format conversion."""
    return f"""Design a migration plan to convert {volume} documents from {from_format} to {to_format}.

Address:
- Conversion strategy (bulk vs incremental)
- Content preservation requirements
- Metadata mapping
- Link/reference updates
- Validation approach
- Rollback procedures
- Timeline estimation

Prioritize maintaining documentation availability during migration."""

@mcp.prompt
def api_documentation_review(api_spec_path: str) -> str:
    """Review API documentation completeness and quality."""
    return f"""Review the API documentation at {api_spec_path} for:

1. **Endpoint Coverage**: Are all endpoints documented?
2. **Request/Response Examples**: Quality and completeness
3. **Error Documentation**: Are error cases well documented?
4. **Authentication**: Is auth clearly explained?
5. **Rate Limits**: Are limits and quotas documented?
6. **Versioning**: Is API versioning clear?
7. **SDKs/Code Examples**: Language coverage

Provide specific improvements for each area."""

@mcp.prompt
def create_onboarding_documentation(project_type: str, team_size: str) -> str:
    """Create onboarding documentation structure."""
    return f"""Design onboarding documentation for a {project_type} project with a {team_size} team.

Include:
- Day 1 setup checklist
- Architecture overview
- Development workflow
- Key codebases and their purposes
- Common tasks and how-tos
- Troubleshooting guide
- Team contacts and responsibilities
- Learning path recommendations

Make it progressive from beginner to productive contributor."""

# ===================================================================
# SERVER EXECUTION
# ===================================================================

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv('DOCUMENTATION_ANALYZER_MCP_PORT', '8036'))
    
    # Optional API key for AI features
    api_key = os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        logger.warning("No AI API key found - AI features will be limited")
    
    # Create cache directory
    os.makedirs(ANALYZER_CONFIG["index_cache_dir"], exist_ok=True)
    
    logger.info(f"Starting Documentation Analyzer MCP Server on port {port}")
    logger.info(f"Supported file types: {', '.join(ANALYZER_CONFIG['supported_extensions'])}")
    
    # Run with streamable-http transport for OpenAI Responses API compatibility
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")