"""
Unit tests for agents
"""
import pytest
from agents.research_agents import ResearchAgent, DataCollectorAgent
from agents.analysis_agents import AnalystAgent
from agents.writing_agents import WriterAgent

@pytest.fixture
def mock_state():
    """Create mock state for testing."""
    return {
        "current_task": "Test task",
        "research_notes": "Test research notes",
        "trending_topics": ["AI", "ML", "LangGraph"],
        "articles": [],
        "analysis_results": "",
        "final_report": ""
    }

def test_research_agent_initialization():
    """Test that research agent initializes correctly."""
    agent = ResearchAgent()
    assert agent.name == "Researcher"
    assert agent.model is not None

def test_researcher_execute(mock_state):
    """Test research agent execution."""
    agent = ResearchAgent()
    result = agent.execute(mock_state)
    
    assert "research_notes" in result
    assert "next_agent" in result
    assert result["next_agent"] == "collector"

def test_analyst_execute(mock_state):
    """Test analyst agent execution."""
    agent = AnalystAgent()
    result = agent.execute(mock_state)
    
    assert "analysis_results" in result
    assert "next_agent" in result

def test_writer_execute(mock_state):
    """Test writer agent execution."""
    mock_state["analysis_results"] = "Test analysis"
    agent = WriterAgent()
    result = agent.execute(mock_state)
    
    assert "final_report" in result
    assert result["next_agent"] == "END"

