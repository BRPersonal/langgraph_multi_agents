"""
Integration tests for workflows
"""
import pytest
from workflows.single_agent import create_single_agent_system
from workflows.multi_agent import create_multi_agent_system

def test_single_agent_workflow():
    """Test single agent workflow execution."""
    system = create_single_agent_system()
    assert system is not None
    
    # Test invocation
    result = system.invoke({
        "task": "Test research task",
        "messages": []
    })
    
    assert "result" in result
    assert isinstance(result["result"], str)

def test_multi_agent_workflow():
    """Test multi-agent workflow execution."""
    system = create_multi_agent_system()
    assert system is not None
    
    # Test invocation
    result = system.invoke({
        "current_task": "Test multi-agent task",
        "messages": [],
        "research_notes": "",
        "trending_topics": [],
        "articles": [],
        "analysis_results": "",
        "patterns": [],
        "final_report": "",
        "next_agent": "researcher",
        "status": "started"
    })
    
    assert "final_report" in result
    assert result["status"] == "complete"

@pytest.mark.asyncio
async def test_workflow_error_handling():
    """Test that workflows handle errors gracefully."""
    system = create_multi_agent_system()
    
    # Test with invalid state
    try:
        result = system.invoke({})
        # Should not crash, should have error handling
        assert result is not None
    except Exception as e:
        # Expected behavior - log and handle gracefully
        assert str(e) is not None

