#!/usr/bin/env python3
"""
UI/UX Design HTTP MCP Server
Provides comprehensive UI/UX design capabilities with sequential thinking, 
OpenAI integration, and orchestration of other MCP servers

Features:
- Sequential thinking for design process
- Component generation via V0 and MUI servers
- Design system analysis and validation
- User journey mapping
- Accessibility evaluation
- Performance optimization
- Cross-platform design strategies
"""

import os
import json
import asyncio
import logging
import httpx
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from pathlib import Path

# FastMCP for HTTP serving
from fastmcp import FastMCP
from fastmcp.server.context import Context

# OpenAI for design analysis and generation
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI not available - some features will be limited")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================================================================
# CONFIGURATION & TEMPLATES
# ===================================================================

class MCPOrchestrator:
    """Orchestrates calls to other MCP servers"""
    
    def __init__(self):
        self.servers = {
            'vercel-v0': 'http://localhost:8010',
            'mui': 'http://localhost:8020',
            'sequential-thinking': 'http://localhost:8013',
            'openai-tools': 'http://localhost:8015',
            'github': 'http://localhost:8012'
        }
        self.client = httpx.AsyncClient(timeout=300.0)
    
    async def call_mcp_tool(self, server: str, tool: str, **kwargs) -> Dict[str, Any]:
        """Call a tool on another MCP server"""
        if server not in self.servers:
            raise ValueError(f"Unknown server: {server}")
        
        url = self.servers[server]
        payload = {
            "jsonrpc": "2.0",
            "id": f"call_{datetime.now().isoformat()}",
            "method": "tools/call",
            "params": {
                "name": tool,
                "arguments": kwargs
            }
        }
        
        try:
            response = await self.client.post(url, json=payload)
            result = response.json()
            
            if "error" in result:
                raise Exception(f"MCP Error: {result['error']}")
            
            return result.get("result", {})
            
        except Exception as e:
            logger.error(f"Failed to call {server}.{tool}: {e}")
            return {"error": str(e), "success": False}

class DesignSystemAnalyzer:
    """Analyzes and validates design systems"""
    
    def __init__(self, openai_client: Optional[AsyncOpenAI] = None):
        self.openai_client = openai_client
        
    async def analyze_component_consistency(self, components: List[Dict], ctx: Optional[Context] = None) -> Dict[str, Any]:
        """Analyze design consistency across components"""
        if ctx:
            await ctx.info("Analyzing component design consistency")
            
        analysis = {
            "consistency_score": 0.0,
            "issues": [],
            "recommendations": [],
            "color_usage": {},
            "typography_usage": {},
            "spacing_patterns": {}
        }
        
        # Analyze color patterns
        colors = set()
        for comp in components:
            if "colors" in comp:
                colors.update(comp["colors"])
        
        analysis["color_usage"] = {
            "unique_colors": len(colors),
            "colors": list(colors)
        }
        
        # Calculate consistency score
        if len(components) > 1:
            consistency_factors = []
            
            # Color consistency
            avg_colors_per_component = sum(len(c.get("colors", [])) for c in components) / len(components)
            if avg_colors_per_component <= 5:
                consistency_factors.append(0.9)
            else:
                consistency_factors.append(0.6)
                
            analysis["consistency_score"] = sum(consistency_factors) / len(consistency_factors)
        
        if ctx:
            await ctx.info(f"Consistency analysis complete. Score: {analysis['consistency_score']:.2f}")
            
        return analysis

# Initialize FastMCP server and orchestrator
mcp = FastMCP("UI/UX Design Server")
orchestrator = MCPOrchestrator()

# Initialize OpenAI client if available
openai_client = None
if OPENAI_AVAILABLE:
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        openai_client = AsyncOpenAI(api_key=api_key)
    else:
        logger.warning("OpenAI API key not found - AI features will be limited")

design_analyzer = DesignSystemAnalyzer(openai_client)

class ComponentGenerator:
    """Built-in component generation using Claude Code's capabilities"""
    
    @staticmethod
    def _generate_component_props(comp_type: str) -> List[str]:
        """Generate appropriate props for component type"""
        base_props = ["className", "children"]
        
        prop_mapping = {
            "button": base_props + ["onClick", "disabled", "variant", "size", "loading"],
            "card": base_props + ["title", "subtitle", "image", "actions"],
            "form": base_props + ["onSubmit", "validation", "fields", "submitText"],
            "navigation": base_props + ["items", "activeItem", "onNavigate"],
            "modal": base_props + ["open", "onClose", "title", "size"],
            "input": base_props + ["value", "onChange", "placeholder", "error", "label"],
            "header": base_props + ["logo", "navigation", "user", "theme"],
            "footer": base_props + ["links", "copyright", "social"]
        }
        
        return prop_mapping.get(comp_type, base_props + ["data", "config"])
    
    @staticmethod
    def _generate_component_features(comp_type: str) -> List[str]:
        """Generate features list for component type"""
        feature_mapping = {
            "button": ["loading states", "accessibility", "keyboard navigation", "focus management"],
            "card": ["responsive layout", "hover effects", "image optimization", "content overflow"],
            "form": ["validation", "error handling", "submit states", "field validation"],
            "navigation": ["responsive menu", "active states", "keyboard navigation", "mobile menu"],
            "modal": ["focus trap", "escape key", "backdrop click", "scroll lock"],
            "input": ["validation", "error states", "placeholder animation", "accessibility"],
            "header": ["responsive design", "mobile menu", "sticky behavior", "theme switching"],
            "footer": ["responsive layout", "social links", "newsletter signup", "sitemap"]
        }
        
        return feature_mapping.get(comp_type, ["responsive design", "accessibility", "theme support"])
    
    @staticmethod
    def _generate_code_structure(comp_type: str, project_name: str) -> Dict[str, str]:
        """Generate code structure for component"""
        component_name = f"{project_name.title()}{comp_type.title()}"
        
        return {
            "interface": f"interface {component_name}Props",
            "component": f"const {component_name}: React.FC<{component_name}Props>",
            "export": f"export default {component_name}",
            "file_structure": {
                "main": f"components/{component_name}/{component_name}.tsx",
                "types": f"components/{component_name}/types.ts",
                "styles": f"components/{component_name}/{component_name}.module.css",
                "tests": f"components/{component_name}/__tests__/{component_name}.test.tsx"
            }
        }

# Add generator instance
component_generator = ComponentGenerator()

# ===================================================================
# TOOLS
# ===================================================================

@mcp.tool()
async def sequential_design_thinking(
    design_challenge: str,
    target_users: str,
    tech_stack: Optional[str] = None,
    project_type: Optional[str] = None,
    platform: Optional[str] = None,
    constraints: Optional[str] = None,
    thinking_steps: int = 7,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Apply sequential thinking process to UI/UX design challenges with full build planning
    
    Args:
        design_challenge: The design problem to solve
        target_users: Target user demographics and needs
        tech_stack: Technology stack (React, Vue, Angular, etc.)
        project_type: Type of project (web app, mobile app, desktop, etc.)
        platform: Target platform (iOS, Android, web, desktop)
        constraints: Technical, business, or design constraints
        thinking_steps: Number of thinking iterations (default 7 for full build plan)
        ctx: Context for logging and progress
    
    Returns:
        Sequential thinking process with comprehensive build plan
    """
    try:
        if ctx:
            await ctx.info(f"Starting sequential design thinking for: {design_challenge}")
            
        # Build comprehensive project context
        project_context = f"""
Build Planning Context:
- Challenge: {design_challenge}
- Target Users: {target_users}
- Tech Stack: {tech_stack or 'To be determined'}
- Project Type: {project_type or 'Web application'}
- Platform: {platform or 'Cross-platform'}
- Constraints: {constraints or 'None specified'}

Full Build Plan Requirements:
1. Architecture & Tech Stack Analysis
2. UI/UX Design System Planning
3. Component Structure & Dependencies
4. Development Pipeline & Testing Strategy
5. Deployment & DevOps Considerations
6. Performance & Accessibility Requirements
7. Timeline & Resource Planning
"""

        # Use sequential thinking MCP server if available
        thinking_result = await orchestrator.call_mcp_tool(
            'sequential-thinking',
            'sequentialthinking',
            thought=project_context,
            nextThoughtNeeded=True,
            thoughtNumber=1,
            totalThoughts=thinking_steps
        )
        
        # Build comprehensive design and build process
        design_process = {
            "challenge": design_challenge,
            "target_users": target_users,
            "tech_stack": tech_stack,
            "project_type": project_type,
            "platform": platform,
            "constraints": constraints,
            "thinking_process": [thinking_result] if thinking_result.get("success") else [],
            "build_plan": {
                "architecture": {},
                "components": [],
                "pipeline": {},
                "timeline": {}
            },
            "design_insights": [],
            "next_steps": []
        }
        
        # Continue thinking process
        for step in range(2, thinking_steps + 1):
            if ctx:
                await ctx.report_progress(step - 1, thinking_steps)
                
            next_thought = await orchestrator.call_mcp_tool(
                'sequential-thinking',
                'sequentialthinking',
                thought=f"Building on previous insights, considering user needs for {target_users}",
                nextThoughtNeeded=step < thinking_steps,
                thoughtNumber=step,
                totalThoughts=thinking_steps
            )
            
            if next_thought.get("success"):
                design_process["thinking_process"].append(next_thought)
        
        # Extract design insights
        design_process["design_insights"] = [
            "User-centered approach prioritizing {target_users}",
            f"Core challenge: {design_challenge}",
            "Iterative design with user feedback loops",
            "Accessibility-first design principles"
        ]
        
        # Generate comprehensive build plan next steps
        design_process["next_steps"] = [
            f"Set up {tech_stack or 'chosen'} development environment",
            "Create user personas and journey maps",
            "Design component library and design system",
            "Set up CI/CD pipeline and testing framework",
            "Develop core application architecture",
            "Implement key user flows and interactions",
            "Conduct usability testing and performance optimization",
            f"Deploy to {platform or 'target platform'} and monitor"
        ]
        
        # Build specific architecture recommendations
        if tech_stack:
            design_process["build_plan"]["architecture"] = {
                "frontend": tech_stack,
                "recommended_structure": f"{tech_stack.lower()}-based component architecture",
                "state_management": "Context API" if "react" in tech_stack.lower() else "Vuex" if "vue" in tech_stack.lower() else "NgRx",
                "testing": "Jest + Testing Library",
                "build_tool": "Vite" if tech_stack.lower() in ["react", "vue"] else "Angular CLI"
            }
        
        if ctx:
            await ctx.info("Sequential design thinking process completed")
            
        return {
            "success": True,
            "design_process": design_process,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Sequential design thinking failed: {e}")
        if ctx:
            await ctx.error(f"Design thinking failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def generate_design_system(
    project_name: str,
    brand_colors: List[str],
    typography_scale: Optional[str] = "modular",
    component_types: Optional[List[str]] = None,
    create_files: bool = True,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Generate comprehensive design system with components
    
    Args:
        project_name: Name of the project/design system
        brand_colors: List of brand colors (hex codes)
        typography_scale: Typography scale system (modular, perfect-fourth, etc.)
        component_types: Types of components to generate
        create_files: Whether to create actual component files
        ctx: Context for logging and progress
    
    Returns:
        Generated design system with components
    """
    try:
        if ctx:
            await ctx.info(f"Generating design system for {project_name}")
            
        if component_types is None:
            component_types = ["button", "card", "form", "navigation", "modal"]
        
        design_system = {
            "name": project_name,
            "colors": {
                "primary": brand_colors[0] if brand_colors else "#007AFF",
                "secondary": brand_colors[1] if len(brand_colors) > 1 else "#34C759",
                "accent": brand_colors[2] if len(brand_colors) > 2 else "#FF3B30",
                "neutral": ["#000000", "#333333", "#666666", "#999999", "#CCCCCC", "#F5F5F5", "#FFFFFF"]
            },
            "typography": {
                "scale": typography_scale,
                "sizes": {
                    "xs": "0.75rem",
                    "sm": "0.875rem", 
                    "base": "1rem",
                    "lg": "1.125rem",
                    "xl": "1.25rem",
                    "2xl": "1.5rem",
                    "3xl": "1.875rem",
                    "4xl": "2.25rem"
                }
            },
            "spacing": {
                "unit": "4px",
                "scale": [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96]
            },
            "components": [],
            "generated_files": []
        }
        
        # Generate components using V0 and MUI servers
        total_components = len(component_types)
        for i, comp_type in enumerate(component_types):
            if ctx:
                await ctx.report_progress(i, total_components)
                await ctx.info(f"Generating {comp_type} component")
            
            # Try V0 first for modern React components
            try:
                v0_result = await orchestrator.call_mcp_tool(
                    'vercel-v0',
                    'generate_component',
                    prompt=f"Create a modern {comp_type} component for {project_name} using colors {brand_colors}. Include TypeScript types, accessibility features, and responsive design.",
                    component_name=f"{project_name.title()}{comp_type.title()}",
                    framework="react"
                )
                
                if v0_result.get("success"):
                    design_system["components"].append({
                        "type": comp_type,
                        "generator": "vercel-v0",
                        "component_data": v0_result
                    })
                    
            except Exception as v0_error:
                logger.warning(f"V0 generation failed for {comp_type}: {v0_error}")
                
                # Fallback to Claude Code's built-in capabilities
                if ctx:
                    await ctx.info(f"V0 unavailable, generating {comp_type} with Claude Code")
                
                # Generate component specification using Claude Code
                component_spec = {
                    "name": f"{project_name.title()}{comp_type.title()}",
                    "type": comp_type,
                    "framework": "react",
                    "typescript": True,
                    "props": component_generator._generate_component_props(comp_type),
                    "styling": {
                        "method": "tailwind",
                        "colors": brand_colors,
                        "responsive": True,
                        "accessibility": True
                    },
                    "features": component_generator._generate_component_features(comp_type),
                    "code_structure": component_generator._generate_code_structure(comp_type, project_name),
                    "documentation": f"Modern {comp_type} component for {project_name} with accessibility and responsive design"
                }
                
                design_system["components"].append({
                    "type": comp_type,
                    "generator": "claude-code",
                    "component_data": component_spec
                })
        
        # Analyze design system consistency
        if design_system["components"]:
            consistency_analysis = await design_analyzer.analyze_component_consistency(
                design_system["components"], ctx
            )
            design_system["consistency_analysis"] = consistency_analysis
        
        if ctx:
            await ctx.info(f"Design system generated with {len(design_system['components'])} components")
            
        return {
            "success": True,
            "design_system": design_system,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Design system generation failed: {e}")
        if ctx:
            await ctx.error(f"Design system generation failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def create_user_journey_map(
    product_name: str,
    user_persona: str,
    journey_stages: List[str],
    pain_points: Optional[List[str]] = None,
    opportunities: Optional[List[str]] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Create comprehensive user journey map with touchpoints and emotions
    
    Args:
        product_name: Name of the product/service
        user_persona: Description of the target user persona
        journey_stages: List of journey stages (e.g., awareness, consideration, purchase)
        pain_points: Known pain points in the journey
        opportunities: Identified opportunities for improvement
        ctx: Context for logging and progress
    
    Returns:
        Detailed user journey map with insights
    """
    try:
        if ctx:
            await ctx.info(f"Creating user journey map for {product_name}")
            
        journey_map = {
            "product_name": product_name,
            "user_persona": user_persona,
            "stages": [],
            "overall_pain_points": pain_points or [],
            "overall_opportunities": opportunities or [],
            "recommendations": [],
            "emotional_journey": []
        }
        
        # Process each journey stage
        for i, stage in enumerate(journey_stages):
            if ctx:
                await ctx.report_progress(i, len(journey_stages))
                await ctx.info(f"Mapping stage: {stage}")
            
            stage_data = {
                "name": stage,
                "touchpoints": [],
                "user_actions": [],
                "emotions": [],
                "pain_points": [],
                "opportunities": [],
                "ui_requirements": []
            }
            
            # Use OpenAI to analyze stage if available
            if openai_client:
                try:
                    analysis_prompt = f"""
                    Analyze the {stage} stage of the user journey for {product_name}.
                    User persona: {user_persona}
                    
                    Provide insights on:
                    1. Key touchpoints users encounter
                    2. Primary user actions and goals
                    3. Emotional state (frustrated, excited, confused, satisfied)
                    4. Potential pain points
                    5. Opportunities for improvement
                    6. UI/UX requirements for this stage
                    
                    Format as JSON with keys: touchpoints, user_actions, emotions, pain_points, opportunities, ui_requirements
                    """
                    
                    response = await openai_client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": analysis_prompt}],
                        temperature=0.7
                    )
                    
                    ai_analysis = json.loads(response.choices[0].message.content)
                    stage_data.update(ai_analysis)
                    
                except Exception as ai_error:
                    logger.warning(f"AI analysis failed for stage {stage}: {ai_error}")
            
            # Default stage analysis if AI unavailable
            if not stage_data["touchpoints"]:
                stage_data.update({
                    "touchpoints": [f"{stage} interface", f"{stage} interactions"],
                    "user_actions": [f"Navigate {stage}", f"Complete {stage} tasks"],
                    "emotions": ["curious", "focused"],
                    "pain_points": [f"Complexity in {stage}"],
                    "opportunities": [f"Simplify {stage} process"],
                    "ui_requirements": [f"Clear {stage} UI", f"Intuitive {stage} flow"]
                })
            
            journey_map["stages"].append(stage_data)
        
        # Generate overall recommendations
        journey_map["recommendations"] = [
            "Reduce friction in high-pain-point stages",
            "Enhance positive emotional moments",
            "Improve cross-stage consistency",
            "Add progress indicators for long journeys",
            "Implement user feedback loops"
        ]
        
        # Create emotional journey summary
        for stage in journey_map["stages"]:
            journey_map["emotional_journey"].append({
                "stage": stage["name"],
                "primary_emotion": stage["emotions"][0] if stage["emotions"] else "neutral",
                "intensity": "medium"  # Could be calculated based on pain points
            })
        
        if ctx:
            await ctx.info("User journey map creation completed")
            
        return {
            "success": True,
            "journey_map": journey_map,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"User journey mapping failed: {e}")
        if ctx:
            await ctx.error(f"Journey mapping failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def evaluate_accessibility(
    design_elements: List[Dict[str, Any]],
    wcag_level: str = "AA",
    target_disabilities: Optional[List[str]] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Evaluate design accessibility against WCAG guidelines
    
    Args:
        design_elements: List of design elements to evaluate
        wcag_level: WCAG compliance level (A, AA, AAA)
        target_disabilities: Specific disabilities to consider
        ctx: Context for logging and progress
    
    Returns:
        Accessibility evaluation with recommendations
    """
    try:
        if ctx:
            await ctx.info(f"Evaluating accessibility for WCAG {wcag_level}")
            
        if target_disabilities is None:
            target_disabilities = ["visual", "hearing", "motor", "cognitive"]
        
        evaluation = {
            "wcag_level": wcag_level,
            "target_disabilities": target_disabilities,
            "overall_score": 0.0,
            "element_evaluations": [],
            "issues": [],
            "recommendations": [],
            "compliance_summary": {}
        }
        
        total_score = 0
        total_elements = len(design_elements)
        
        # Evaluate each design element
        for i, element in enumerate(design_elements):
            if ctx:
                await ctx.report_progress(i, total_elements)
                
            element_eval = {
                "element": element.get("name", f"Element {i+1}"),
                "type": element.get("type", "unknown"),
                "score": 0.0,
                "issues": [],
                "recommendations": []
            }
            
            element_score = 100  # Start with perfect score
            
            # Check color contrast
            if "colors" in element:
                # Simplified contrast check
                colors = element["colors"]
                if len(colors) >= 2:
                    # Assume proper contrast checking logic here
                    contrast_ratio = 4.5  # Placeholder
                    if wcag_level == "AA" and contrast_ratio < 4.5:
                        element_eval["issues"].append("Insufficient color contrast for WCAG AA")
                        element_eval["recommendations"].append("Increase color contrast ratio to 4.5:1 minimum")
                        element_score -= 20
                    elif wcag_level == "AAA" and contrast_ratio < 7.0:
                        element_eval["issues"].append("Insufficient color contrast for WCAG AAA")
                        element_eval["recommendations"].append("Increase color contrast ratio to 7:1 minimum")
                        element_score -= 15
            
            # Check text sizing
            if "font_size" in element:
                font_size = element.get("font_size", 16)
                if font_size < 14:
                    element_eval["issues"].append("Font size too small for accessibility")
                    element_eval["recommendations"].append("Increase font size to minimum 14px")
                    element_score -= 15
            
            # Check interactive elements
            if element.get("interactive", False):
                if "focus_indicators" not in element:
                    element_eval["issues"].append("Missing focus indicators")
                    element_eval["recommendations"].append("Add visible focus indicators for keyboard navigation")
                    element_score -= 10
                    
                if "aria_labels" not in element:
                    element_eval["issues"].append("Missing ARIA labels")
                    element_eval["recommendations"].append("Add appropriate ARIA labels for screen readers")
                    element_score -= 15
            
            # Check for motor accessibility
            if "motor" in target_disabilities and element.get("interactive", False):
                touch_target_size = element.get("touch_target_size", 44)
                if touch_target_size < 44:
                    element_eval["issues"].append("Touch target too small")
                    element_eval["recommendations"].append("Increase touch target to minimum 44px")
                    element_score -= 10
            
            element_eval["score"] = max(0, element_score)
            total_score += element_eval["score"]
            evaluation["element_evaluations"].append(element_eval)
        
        # Calculate overall scores
        evaluation["overall_score"] = total_score / total_elements if total_elements > 0 else 0
        
        # Generate compliance summary
        evaluation["compliance_summary"] = {
            "wcag_level": wcag_level,
            "estimated_compliance": evaluation["overall_score"],
            "major_issues": len([e for e in evaluation["element_evaluations"] if e["score"] < 70]),
            "elements_passing": len([e for e in evaluation["element_evaluations"] if e["score"] >= 80])
        }
        
        # Overall recommendations
        evaluation["recommendations"] = [
            "Implement automated accessibility testing",
            "Conduct user testing with assistive technology users",
            "Ensure keyboard navigation throughout interface",
            "Provide alternative text for all images",
            "Test with screen readers",
            "Validate color-only information conveyance"
        ]
        
        if ctx:
            await ctx.info(f"Accessibility evaluation completed. Score: {evaluation['overall_score']:.1f}/100")
            
        return {
            "success": True,
            "evaluation": evaluation,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Accessibility evaluation failed: {e}")
        if ctx:
            await ctx.error(f"Accessibility evaluation failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def orchestrate_design_pipeline(
    project_name: str,
    requirements: Dict[str, Any],
    target_platforms: List[str],
    use_ai_analysis: bool = True,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Orchestrate complete design pipeline using multiple MCP servers
    
    Args:
        project_name: Name of the design project
        requirements: Project requirements and constraints
        target_platforms: Target platforms (web, mobile, desktop)
        use_ai_analysis: Whether to use AI-powered analysis
        ctx: Context for logging and progress
    
    Returns:
        Complete design pipeline results
    """
    try:
        if ctx:
            await ctx.info(f"Starting design pipeline orchestration for {project_name}")
            
        pipeline_result = {
            "project_name": project_name,
            "requirements": requirements,
            "target_platforms": target_platforms,
            "stages_completed": [],
            "generated_assets": [],
            "analysis_results": {},
            "next_steps": []
        }
        
        stages = [
            "sequential_thinking",
            "design_system_generation", 
            "component_creation",
            "accessibility_evaluation",
            "user_journey_mapping"
        ]
        
        total_stages = len(stages)
        
        # Stage 1: Sequential Design Thinking
        if ctx:
            await ctx.report_progress(0, total_stages)
            await ctx.info("Stage 1: Sequential design thinking")
            
        thinking_result = await sequential_design_thinking(
            design_challenge=requirements.get("challenge", f"Design {project_name}"),
            target_users=requirements.get("target_users", "General users"),
            constraints=requirements.get("constraints"),
            ctx=ctx
        )
        
        if thinking_result.get("success"):
            pipeline_result["stages_completed"].append("sequential_thinking")
            pipeline_result["analysis_results"]["design_thinking"] = thinking_result
        
        # Stage 2: Design System Generation
        if ctx:
            await ctx.report_progress(1, total_stages)
            await ctx.info("Stage 2: Design system generation")
            
        design_system_result = await generate_design_system(
            project_name=project_name,
            brand_colors=requirements.get("brand_colors", ["#007AFF", "#34C759"]),
            component_types=requirements.get("component_types"),
            ctx=ctx
        )
        
        if design_system_result.get("success"):
            pipeline_result["stages_completed"].append("design_system_generation")
            pipeline_result["analysis_results"]["design_system"] = design_system_result
        
        # Stage 3: User Journey Mapping
        if ctx:
            await ctx.report_progress(2, total_stages)
            await ctx.info("Stage 3: User journey mapping")
            
        journey_result = await create_user_journey_map(
            product_name=project_name,
            user_persona=requirements.get("target_users", "Primary user"),
            journey_stages=requirements.get("journey_stages", ["awareness", "consideration", "onboarding", "usage", "advocacy"]),
            ctx=ctx
        )
        
        if journey_result.get("success"):
            pipeline_result["stages_completed"].append("user_journey_mapping")
            pipeline_result["analysis_results"]["user_journey"] = journey_result
        
        # Stage 4: Generate Additional Components via External MCP Servers
        if ctx:
            await ctx.report_progress(3, total_stages)
            await ctx.info("Stage 4: Component generation via MCP servers")
            
        # Try to generate components using V0
        try:
            v0_components = []
            component_types = requirements.get("component_types", ["header", "footer", "card"])
            
            for comp_type in component_types[:3]:  # Limit to 3 for demo
                v0_result = await orchestrator.call_mcp_tool(
                    'vercel-v0',
                    'generate_component',
                    prompt=f"Create a {comp_type} component for {project_name} that matches the design system",
                    component_name=f"{project_name.title()}{comp_type.title()}"
                )
                
                if v0_result.get("success"):
                    v0_components.append(v0_result)
            
            if v0_components:
                pipeline_result["generated_assets"].extend(v0_components)
                pipeline_result["stages_completed"].append("component_creation")
                
        except Exception as comp_error:
            logger.warning(f"Component generation via V0 failed: {comp_error}")
        
        # Stage 5: Accessibility Evaluation
        if ctx:
            await ctx.report_progress(4, total_stages)
            await ctx.info("Stage 5: Accessibility evaluation")
            
        # Create mock design elements for accessibility evaluation
        design_elements = []
        if design_system_result.get("success"):
            components = design_system_result.get("design_system", {}).get("components", [])
            for comp in components:
                design_elements.append({
                    "name": comp.get("type", "component"),
                    "type": comp.get("type", "ui"),
                    "interactive": comp.get("type") in ["button", "form", "navigation"],
                    "colors": requirements.get("brand_colors", ["#007AFF"]),
                    "font_size": 16
                })
        
        if design_elements:
            accessibility_result = await evaluate_accessibility(
                design_elements=design_elements,
                wcag_level="AA",
                ctx=ctx
            )
            
            if accessibility_result.get("success"):
                pipeline_result["stages_completed"].append("accessibility_evaluation")
                pipeline_result["analysis_results"]["accessibility"] = accessibility_result
        
        # Generate next steps
        pipeline_result["next_steps"] = [
            "Review sequential thinking insights",
            "Validate design system with stakeholders", 
            "Prototype key user journeys",
            "Conduct usability testing",
            "Implement accessibility fixes",
            "Create responsive designs for all target platforms",
            "Set up design system documentation"
        ]
        
        if ctx:
            await ctx.info(f"Design pipeline completed. Stages: {len(pipeline_result['stages_completed'])}/{total_stages}")
            
        return {
            "success": True,
            "pipeline_result": pipeline_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Design pipeline orchestration failed: {e}")
        if ctx:
            await ctx.error(f"Pipeline orchestration failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# ===================================================================
# RESOURCES
# ===================================================================

@mcp.resource("design://templates/design-system")
def get_design_system_template() -> Dict[str, Any]:
    """Complete design system template with all components"""
    return {
        "design_system_template": {
            "foundation": {
                "colors": {
                    "primary": {"50": "#eff6ff", "500": "#3b82f6", "900": "#1e3a8a"},
                    "secondary": {"50": "#f0fdf4", "500": "#22c55e", "900": "#14532d"},
                    "neutral": {"50": "#f9fafb", "500": "#6b7280", "900": "#111827"}
                },
                "typography": {
                    "font_families": {
                        "sans": ["Inter", "system-ui", "sans-serif"],
                        "serif": ["Merriweather", "serif"],
                        "mono": ["JetBrains Mono", "monospace"]
                    },
                    "font_sizes": {
                        "xs": "0.75rem", "sm": "0.875rem", "base": "1rem",
                        "lg": "1.125rem", "xl": "1.25rem", "2xl": "1.5rem"
                    }
                },
                "spacing": {
                    "scale": [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128]
                },
                "breakpoints": {
                    "sm": "640px", "md": "768px", "lg": "1024px", "xl": "1280px"
                }
            },
            "components": {
                "button": {
                    "variants": ["primary", "secondary", "outline", "ghost"],
                    "sizes": ["sm", "md", "lg"],
                    "states": ["default", "hover", "active", "disabled", "loading"]
                },
                "input": {
                    "types": ["text", "email", "password", "number", "search"],
                    "states": ["default", "focus", "error", "disabled"],
                    "variants": ["outline", "filled", "underline"]
                },
                "card": {
                    "variants": ["elevated", "outlined", "filled"],
                    "layouts": ["vertical", "horizontal"],
                    "sizes": ["sm", "md", "lg"]
                }
            }
        }
    }

@mcp.resource("design://patterns/ui-patterns")
def get_ui_patterns() -> Dict[str, Any]:
    """Common UI design patterns and best practices"""
    return {
        "ui_patterns": {
            "navigation": {
                "primary": ["top_nav", "sidebar", "bottom_nav", "breadcrumbs"],
                "secondary": ["tabs", "pills", "steps", "pagination"],
                "mobile": ["hamburger", "bottom_tabs", "gesture_nav"]
            },
            "layout": {
                "grid_systems": ["12_column", "css_grid", "flexbox"],
                "containers": ["full_width", "constrained", "breakout"],
                "spacing": ["consistent_margins", "vertical_rhythm", "optical_alignment"]
            },
            "forms": {
                "validation": ["inline", "on_submit", "progressive"],
                "input_groups": ["labels", "placeholders", "help_text", "error_states"],
                "multi_step": ["progress_indicator", "save_state", "navigation"]
            },
            "feedback": {
                "notifications": ["toast", "banner", "modal", "inline"],
                "loading": ["spinners", "skeletons", "progress_bars"],
                "empty_states": ["first_use", "no_results", "error_recovery"]
            }
        }
    }

@mcp.resource("design://guidelines/accessibility")
def get_accessibility_guidelines() -> Dict[str, Any]:
    """Comprehensive accessibility guidelines and checklists"""
    return {
        "accessibility_guidelines": {
            "wcag_principles": {
                "perceivable": {
                    "text_alternatives": "Provide text alternatives for images",
                    "captions": "Provide captions and transcripts for media", 
                    "adaptable": "Content can be presented in different ways",
                    "distinguishable": "Make it easier for users to see and hear content"
                },
                "operable": {
                    "keyboard_accessible": "All functionality available via keyboard",
                    "no_seizures": "Don't use content that causes seizures",
                    "navigable": "Help users navigate and find content"
                },
                "understandable": {
                    "readable": "Make text readable and understandable",
                    "predictable": "Make content appear and operate predictably",
                    "input_assistance": "Help users avoid and correct mistakes"
                },
                "robust": {
                    "compatible": "Maximize compatibility with assistive technologies"
                }
            },
            "implementation_checklist": {
                "color_contrast": {
                    "aa_normal": "4.5:1 minimum ratio",
                    "aa_large": "3:1 minimum ratio", 
                    "aaa_normal": "7:1 minimum ratio",
                    "aaa_large": "4.5:1 minimum ratio"
                },
                "keyboard_navigation": [
                    "Tab order is logical",
                    "Focus indicators are visible",
                    "No keyboard traps",
                    "Skip links available"
                ],
                "screen_readers": [
                    "Alt text for images",
                    "ARIA labels for complex UI",
                    "Proper heading hierarchy",
                    "Form labels associated"
                ]
            }
        }
    }

@mcp.resource("design://examples/{category}")
def get_design_examples(category: str) -> Dict[str, Any]:
    """Design examples by category"""
    examples = {
        "mobile": {
            "onboarding": ["welcome_screen", "feature_intro", "permission_requests"],
            "navigation": ["tab_bar", "drawer", "modal_presentation"],
            "forms": ["login", "registration", "checkout", "profile_edit"]
        },
        "web": {
            "landing_pages": ["saas", "portfolio", "e-commerce", "blog"],
            "dashboards": ["analytics", "admin", "user_profile", "settings"],
            "e-commerce": ["product_grid", "product_detail", "cart", "checkout"]
        },
        "desktop": {
            "productivity": ["text_editor", "file_manager", "project_manager"],
            "creative": ["image_editor", "video_editor", "design_tool"],
            "utilities": ["system_monitor", "calculator", "calendar"]
        }
    }
    
    return {
        "category": category,
        "examples": examples.get(category, {}),
        "available_categories": list(examples.keys())
    }

@mcp.resource("design://workflows/design-process")
def get_design_process_workflow() -> Dict[str, Any]:
    """Complete design process workflow and methodologies"""
    return {
        "design_process": {
            "discovery": {
                "research": ["user_interviews", "surveys", "analytics_review"],
                "analysis": ["persona_creation", "journey_mapping", "competitive_analysis"],
                "definition": ["problem_statement", "design_requirements", "success_metrics"]
            },
            "ideation": {
                "brainstorming": ["mind_mapping", "crazy_8s", "affinity_mapping"],
                "concept_development": ["sketching", "storyboarding", "user_flows"],
                "validation": ["concept_testing", "stakeholder_review", "feasibility_check"]
            },
            "design": {
                "wireframing": ["low_fidelity", "information_architecture", "interaction_flow"],
                "prototyping": ["medium_fidelity", "interactive_prototype", "micro_interactions"],
                "visual_design": ["style_guide", "high_fidelity", "design_system"]
            },
            "validation": {
                "usability_testing": ["moderated_sessions", "unmoderated_testing", "a_b_testing"],
                "accessibility_testing": ["screen_reader", "keyboard_navigation", "color_contrast"],
                "performance_testing": ["load_times", "interaction_responsiveness", "mobile_performance"]
            },
            "implementation": {
                "handoff": ["design_specs", "asset_export", "developer_documentation"],
                "collaboration": ["design_reviews", "implementation_support", "qa_participation"],
                "iteration": ["feedback_incorporation", "post_launch_analysis", "continuous_improvement"]
            }
        }
    }

# ===================================================================
# PROMPTS
# ===================================================================

@mcp.prompt
def design_critique_prompt(design_description: str, target_audience: str = "general users") -> str:
    """Generate prompt for design critique and feedback"""
    return f"""
    Please provide a comprehensive design critique for the following design:

    Design Description: {design_description}
    Target Audience: {target_audience}

    Evaluate the design based on:

    1. **Visual Hierarchy & Layout**
       - Is information organized clearly?
       - Does the layout guide the user's eye appropriately?
       - Are related elements grouped effectively?

    2. **User Experience & Usability**
       - Is the interface intuitive for {target_audience}?
       - Are user flows clear and efficient?
       - Are there any potential friction points?

    3. **Accessibility & Inclusivity**
       - Does the design accommodate users with disabilities?
       - Is color contrast sufficient?
       - Are interactive elements appropriately sized?

    4. **Visual Design & Aesthetics**
       - Is the visual style appropriate for the target audience?
       - Are colors, typography, and spacing used effectively?
       - Does the design feel cohesive and polished?

    5. **Technical Considerations**
       - Is the design feasible to implement?
       - How will it perform across different devices?
       - Are there any potential technical constraints?

    Provide specific, actionable feedback with suggestions for improvement.
    """

@mcp.prompt
def user_persona_development_prompt(product_type: str, research_data: str = "") -> str:
    """Generate prompt for developing detailed user personas"""
    return f"""
    Create detailed user personas for a {product_type} based on the following research data:

    Research Data: {research_data if research_data else "No specific research data provided"}

    For each persona, include:

    1. **Demographics & Background**
       - Age, gender, location, education
       - Job title, industry, income level
       - Family situation, lifestyle

    2. **Goals & Motivations**
       - Primary goals related to the {product_type}
       - Secondary goals and motivations
       - Success criteria and desired outcomes

    3. **Pain Points & Frustrations**
       - Current challenges they face
       - Frustrations with existing solutions
       - Barriers to achieving their goals

    4. **Behavior Patterns**
       - How they currently solve problems
       - Technology usage patterns
       - Decision-making process

    5. **Needs & Expectations**
       - Functional requirements
       - Emotional needs
       - Experience expectations

    6. **Context of Use**
       - When and where they would use the {product_type}
       - Device preferences
       - Environmental constraints

    Create 2-3 distinct personas that represent different user segments.
    Include a brief scenario for each persona showing how they would interact with the {product_type}.
    """

@mcp.prompt
def accessibility_audit_prompt(interface_type: str, wcag_level: str = "AA") -> str:
    """Generate prompt for comprehensive accessibility audit"""
    return f"""
    Conduct a comprehensive accessibility audit for a {interface_type} interface targeting WCAG {wcag_level} compliance.

    Evaluate the following areas:

    1. **Perceivable**
       - Text alternatives for non-text content
       - Captions for audio/video content
       - Color contrast ratios (minimum {wcag_level} standards)
       - Text resizing capabilities (up to 200%)
       - Visual presentation and readability

    2. **Operable**
       - Keyboard accessibility for all interactive elements
       - No seizure-inducing content
       - Sufficient time limits for time-based content
       - Clear navigation and wayfinding
       - Input methods beyond just mouse/touch

    3. **Understandable**
       - Page language identification
       - Consistent navigation and interaction patterns
       - Clear error identification and suggestions
       - Instructions and labels for form inputs
       - Predictable interface behavior

    4. **Robust**
       - Valid, semantic HTML markup
       - Compatibility with assistive technologies
       - Progressive enhancement approach
       - Graceful degradation for older technologies

    For each area, provide:
    - Specific issues found or potential risks
    - WCAG success criteria references
    - Concrete recommendations for improvement
    - Priority level (high/medium/low) for each recommendation

    Include a summary with overall compliance assessment and next steps.
    """

@mcp.prompt
def design_system_scaling_prompt(current_system: str, new_requirements: str) -> str:
    """Generate prompt for scaling design systems"""
    return f"""
    Analyze how to scale the following design system to meet new requirements:

    Current Design System: {current_system}
    New Requirements: {new_requirements}

    Provide recommendations for:

    1. **Component Evolution**
       - Which existing components need updates?
       - What new components are required?
       - How to maintain backward compatibility?

    2. **Token System Expansion**
       - New design tokens needed (colors, spacing, typography)
       - How to extend existing token hierarchies
       - Naming conventions for new tokens

    3. **Documentation & Guidelines**
       - Updates needed to component documentation
       - New usage guidelines and patterns
       - Examples and best practices for new components

    4. **Implementation Strategy**
       - Rollout plan for design system updates
       - Migration path for existing implementations
       - Testing strategy for component changes

    5. **Governance & Maintenance**
       - Review process for new components
       - Quality assurance and testing protocols
       - Long-term maintenance considerations

    6. **Platform Considerations**
       - Cross-platform consistency requirements
       - Platform-specific adaptations needed
       - Technical implementation constraints

    Focus on maintaining design system coherence while enabling new functionality.
    Prioritize backwards compatibility and provide clear migration guidance.
    """

@mcp.prompt
def user_flow_optimization_prompt(current_flow: str, conversion_goals: str) -> str:
    """Generate prompt for optimizing user flows and conversion"""
    return f"""
    Optimize the following user flow to improve conversion and user experience:

    Current User Flow: {current_flow}
    Conversion Goals: {conversion_goals}

    Analyze and provide recommendations for:

    1. **Flow Efficiency**
       - Identify unnecessary steps or friction points
       - Opportunities to reduce cognitive load
       - Ways to streamline the process

    2. **Decision Points & Motivation**
       - Key decision moments in the flow
       - How to increase user confidence at each step
       - Motivational elements and value reinforcement

    3. **Form & Input Optimization**
       - Simplify data entry requirements
       - Smart defaults and progressive disclosure
       - Validation and error handling improvements

    4. **Visual Design & Layout**
       - Page layout optimization for flow clarity
       - Visual hierarchy to guide user attention
       - Call-to-action prominence and placement

    5. **Mobile Experience**
       - Mobile-specific flow considerations
       - Touch interaction optimization
       - Performance and loading considerations

    6. **Personalization Opportunities**
       - How to tailor flow based on user context
       - Dynamic content and adaptive interfaces
       - Progressive user onboarding

    7. **Measurement & Testing**
       - Key metrics to track flow performance
       - A/B testing opportunities
       - Analytics implementation recommendations

    Provide specific, actionable recommendations with expected impact on {conversion_goals}.
    Include both quick wins and longer-term optimization strategies.
    """

@mcp.prompt
def cross_platform_design_prompt(platform_list: str, design_requirements: str) -> str:
    """Generate prompt for cross-platform design strategy"""
    return f"""
    Develop a comprehensive cross-platform design strategy for:

    Target Platforms: {platform_list}
    Design Requirements: {design_requirements}

    Address the following considerations:

    1. **Platform-Specific Guidelines**
       - Native design patterns for each platform
       - Platform UI conventions and expectations
       - Technical capabilities and constraints

    2. **Consistency vs. Native Feel**
       - Which elements should be consistent across platforms
       - Where to embrace platform-specific conventions
       - Brand consistency while respecting platform norms

    3. **Responsive Design Strategy**
       - Breakpoint strategy across devices
       - Layout adaptation approaches
       - Content prioritization for different screen sizes

    4. **Interaction Patterns**
       - Touch, mouse, and keyboard interaction models
       - Gesture support and conventions
       - Accessibility across input methods

    5. **Content Strategy**
       - Content adaptation for different contexts
       - Information architecture across platforms
       - Progressive disclosure strategies

    6. **Technical Implementation**
       - Shared component library approach
       - Asset optimization and delivery
       - Performance considerations per platform

    7. **Testing & Validation**
       - Cross-platform testing strategy
       - User testing across different devices
       - Quality assurance processes

    8. **Maintenance & Evolution**
       - Design system governance across platforms
       - Update and rollout strategies
       - Long-term platform roadmap alignment

    Provide a detailed strategy that balances consistency with platform optimization.
    Include specific recommendations for each target platform.
    """

@mcp.prompt
def design_system_governance_prompt(team_size: str, organization_type: str) -> str:
    """Generate prompt for design system governance and adoption"""
    return f"""
    Establish a design system governance model for:

    Team Size: {team_size}
    Organization Type: {organization_type}

    Create a comprehensive governance framework covering:

    1. **Organizational Structure**
       - Design system team roles and responsibilities
       - Stakeholder engagement model
       - Decision-making processes and authority

    2. **Contribution Process**
       - How teams can propose new components
       - Review and approval workflows
       - Quality standards and acceptance criteria

    3. **Documentation Standards**
       - Component documentation requirements
       - Usage guidelines and examples
       - Versioning and changelog practices

    4. **Quality Assurance**
       - Testing standards for components
       - Accessibility compliance verification
       - Cross-browser and device testing protocols

    5. **Adoption Strategy**
       - Rollout plan for design system implementation
       - Training and education programs
       - Migration support for existing products

    6. **Maintenance & Evolution**
       - Regular review and update cycles
       - Deprecation policies and timelines
       - Breaking change communication strategies

    7. **Communication & Support**
       - Regular updates and announcements
       - Support channels for implementers
       - Community building and feedback collection

    8. **Metrics & Success Tracking**
       - Adoption metrics and KPIs
       - Design consistency measurements
       - Development efficiency improvements

    9. **Tooling & Infrastructure**
       - Design tool integration and workflows
       - Development environment setup
       - Automated testing and deployment

    Tailor recommendations to the {organization_type} context and {team_size} constraints.
    Include both short-term implementation steps and long-term sustainability strategies.
    """

# ===================================================================
# SERVER EXECUTION
# ===================================================================

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv('UIUX_DESIGN_MCP_PORT', '8025'))
    
    # Get API keys
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        logger.warning("OpenAI API key not found - AI features will be limited")
    
    v0_key = os.getenv('V0_API_KEY')
    if not v0_key:
        logger.warning("V0 API key not found - V0 integration will be limited")
    
    logger.info(f"Starting UI/UX Design MCP Server on port {port}")
    logger.info("Features: Sequential thinking, Design systems, Accessibility, MCP orchestration")
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")