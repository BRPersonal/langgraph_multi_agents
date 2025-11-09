"""
Multi-Agent Workflow
"""

"""
Hack that is required if you have to run this script
directly from command line 
"""
import sys
from pathlib import Path

# Add project root to Python path BEFORE any imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from typing import TypedDict, Annotated, List, Literal
from langgraph.graph import StateGraph, END
from agents.research_agents import ResearchAgent, DataCollectorAgent
from agents.analysis_agents import AnalystAgent
from agents.writing_agents import WriterAgent
from utils.logger import logger
import operator


class MultiAgentState(TypedDict):
    """Shared state across all agents."""
    messages: Annotated[List, operator.add]
    current_task: str
    research_notes: str
    trending_topics: List[str]
    articles: List[dict]
    analysis_results: str
    patterns: List[str]
    final_report: str
    next_agent: str
    status: str

def create_multi_agent_system():
    """
    Create a hierarchical multi-agent research system.
    
    Returns:
        Compiled LangGraph application
    """
    logger.info("Creating multi-agent system")
    
    # Initialize all agents
    researcher = ResearchAgent()
    collector = DataCollectorAgent()
    analyst = AnalystAgent()
    writer = WriterAgent()
    
    # Define workflow nodes
    def research_node(state: MultiAgentState):
        """Research team gathers trending topics."""
        logger.info("Executing research node")
        result = researcher.execute(state)
        result["status"] = "research_complete"
        return result
    
    def collect_node(state: MultiAgentState):
        """Data collection team gathers detailed information."""
        logger.info("Executing collection node")
        result = collector.execute(state)
        result["status"] = "collection_complete"
        return result
    
    def analyze_node(state: MultiAgentState):
        """Analysis team processes findings."""
        logger.info("Executing analysis node")
        result = analyst.execute(state)
        result["status"] = "analysis_complete"
        return result
    
    def write_node(state: MultiAgentState):
        """Writing team creates final report."""
        logger.info("Executing writing node")
        result = writer.execute(state)
        result["status"] = "complete"
        return result
    
    # Routing logic
    def route_next(state: MultiAgentState) -> Literal["collect", "analyze", "write", "end"]:
        """Determine next agent based on state."""
        next_agent = state.get("next_agent", "end")
        
        routing = {
            "collector": "collect",
            "analyst": "analyze",
            "writer": "write",
            "END": "end"
        }
        
        return routing.get(next_agent, "end")
    
    # Build the workflow graph
    workflow = StateGraph(MultiAgentState)
    
    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("collect", collect_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("write", write_node)
    
    # Set entry point
    workflow.set_entry_point("research")
    
    # Add edges with routing
    workflow.add_conditional_edges(
        "research",
        route_next,
        {
            "collect": "collect",
            "analyze": "analyze",
            "write": "write",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "collect",
        route_next,
        {
            "analyze": "analyze",
            "write": "write",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "analyze",
        route_next,
        {
            "write": "write",
            "end": END
        }
    )
    
    workflow.add_edge("write", END)
    
    return workflow.compile()

