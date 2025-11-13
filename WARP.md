# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Multi-agent research system built with LangGraph 1.0 and LangChain. The system coordinates specialized AI agents (Research, Data Collection, Analysis, Writing) to gather trending topics, analyze information, and generate intelligence reports.

Original source: https://github.com/MahendraMedapati27/langchain_Multi_Agent_System.git

## Development Commands

### Environment Setup
```bash
# Pin Python version before adding dependencies
uv python pin 3.13

# Install all dependencies (defined in pyproject.toml)
uv sync
```

### Testing
```bash
# Run all tests with verbose output
python -m pytest -vv

# Run specific test file
python -m pytest tests/test_agents.py -vv

# Run specific test function
python -m pytest tests/test_agents.py::test_research_agent_initialization -vv

# Run with asyncio support
python -m pytest -vv --asyncio-mode=auto
```

### Running the Application
```bash
# Start Streamlit web interface (main application)
uv run streamlit run app.py --server.port 8501 --server.address localhost

# Run single agent workflow directly
python workflows/single_agent.py

# Run multi-agent workflow directly
python workflows/multi_agent.py
```

### LangGraph CLI (for development)
```bash
# The langgraph-cli[inmem] package is installed for local development
# Use it to test and debug graph workflows
```

## Architecture

### State Management
- **MultiAgentState**: Shared state across all agents in the multi-agent workflow, including messages, research notes, trending topics, articles, analysis results, patterns, and routing information
- **SingleAgentState**: Simpler state for the single-agent workflow with messages, task, and result
- State uses `TypedDict` with `Annotated` fields and operators (like `operator.add`) for list accumulation

### Agent Hierarchy (Multi-Agent System)
1. **ResearchAgent** (`agents/research_agents.py`): Entry point - gathers trending topics using search tools
2. **DataCollectorAgent** (`agents/research_agents.py`): Collects detailed articles for each trending topic
3. **AnalystAgent** (`agents/analysis_agents.py`): Analyzes patterns and generates insights from collected data
4. **WriterAgent** (`agents/writing_agents.py`): Creates final executive report from analysis

All agents inherit from **BaseAgent** (`agents/base.py`) which provides:
- Model initialization (Groq with Llama or Google Gemini)
- Common `execute()` and `invoke()` interfaces
- Error handling and logging

### Workflow Patterns
- **Multi-agent workflow** (`workflows/multi_agent.py`): Uses StateGraph with conditional edges. Each agent decides the next agent via `next_agent` field in state. Routing logic in `route_next()` function.
- **Single-agent workflow** (`workflows/single_agent.py`): Uses LangGraph's `create_react_agent` with tools. Simpler linear flow through one processing node.

### Tools Architecture
- All tools decorated with `@tool` from `langchain_core.tools`
- Tools in `tools/search_tools.py`: `fetch_trending_topics()`, `search_articles()` (uses `@retry_with_backoff` decorator)
- Tools in `tools/analysis_tools.py`: `analyze_sentiment()`, `detect_patterns()`
- Currently use simulated data - production would integrate real APIs (Google Trends, Serper, etc.)

### Configuration
- Environment variables loaded via `pydantic-settings` in `utils/config.py`
- Requires `.env` file with: `GROQ_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `DEFAULT_MODEL`, `FAST_MODEL`
- Singleton `settings` instance exported from config module
- Config automatically sets environment variables for downstream libraries

### Path Resolution Hack
Both workflow files include a path resolution pattern at the top:
```python
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
```
This allows running workflow scripts directly from command line. When importing these modules, this runs but is harmless.

## Key Dependencies

- **langgraph==1.0.2**: State machine and workflow orchestration
- **langchain**: Base LLM abstractions and tools
- **langchain-groq**: Groq LLM integration (primary, free & fast)
- **langchain-google-genai**: Google Gemini integration (alternative)
- **langchain-openai** & **langchain-anthropic**: Additional LLM options
- **pydantic-settings**: Environment configuration management
- **streamlit**: Web UI framework
- **pytest** & **pytest-asyncio**: Testing

## Environment Variables Required

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
DEFAULT_MODEL=llama-3.3-70b-versatile
FAST_MODEL=gemini-2.0-flash-exp
```

## Agent Execution Flow (Multi-Agent)

1. User submits task via Streamlit UI
2. ResearchAgent fetches trending topics → sets `next_agent="collector"`
3. DataCollectorAgent gathers articles → sets `next_agent="analyst"`
4. AnalystAgent processes and analyzes → sets `next_agent="writer"`
5. WriterAgent generates final report → sets `next_agent="END"`
6. Conditional routing in graph checks `next_agent` field to determine flow

## Testing Patterns

- Tests use `@pytest.fixture` for mock state objects
- Agent initialization tests verify agent name and model setup
- Execution tests verify output structure (presence of expected keys, routing decisions)
- Mock state includes all required MultiAgentState fields
