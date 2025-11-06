"""
Single Agent Workflow
"""

"""
Hack that is required if you have to run this script
directly from command line 
$ python workflows/single_agent.py
"""
import sys
from pathlib import Path

# Add project root to Python path BEFORE any imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from utils.config import settings
from tools.search_tools import fetch_trending_topics, search_articles
from tools.analysis_tools import analyze_sentiment
from utils.logger import logger
from prompts import research_prompt
import operator

class SingleAgentState(TypedDict):
    """State for single agent workflow."""
    messages: Annotated[List, operator.add]
    task: str
    result: str

def create_single_agent_system():
    """
    Create a simple single-agent research system.
    
    Returns:
        Compiled LangGraph application
    """
    logger.info("Creating single agent system")
    
    # Create the agent with tools
    model = ChatGroq(
        model=settings.DEFAULT_MODEL,
        temperature=0.7,
        groq_api_key=settings.GROQ_API_KEY
    )
    
    agent = create_agent(
        model=model,
        tools=[
            fetch_trending_topics,
            search_articles,
            analyze_sentiment
        ]
    )
    
    # Define the workflow
    def process_task(state: SingleAgentState):
        """Process the task using the agent."""
        logger.info("Single agent processing task")
        
        task = state.get('task', 'Research trending tech topics')
        prompt = research_prompt.format(task=task)
        
        try:
            response = agent.invoke({
                "messages": [{"role": "user", "content": prompt}]
            })
            
            result = response["messages"][-1].content
            
            return {
                "result": result,
                "messages": [{"role": "assistant", "content": result}]
            }
        
        except Exception as e:
            logger.error(f"Single agent error: {str(e)}")
            return {
                "result": f"Error: {str(e)}",
                "messages": [{"role": "assistant", "content": f"Error: {str(e)}"}]
            }
    
    # Build the graph
    workflow = StateGraph(SingleAgentState)
    workflow.add_node("process", process_task)
    workflow.set_entry_point("process")
    workflow.add_edge("process", END)
    
    return workflow.compile()

if __name__ == "__main__":
    # Run the agent
    agent = create_single_agent_system()
    result = agent.invoke({
        "task": "Research trending tech topics",
        "messages": []
    })
    
    print("📊 Research Summary:")
    print(result["result"])  

