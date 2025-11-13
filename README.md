# langgraph_multi_agents
Multi agent system using LangGraph and LangChain
original source: https://github.com/MahendraMedapati27/langchain_Multi_Agent_System.git

Create project
$ cd ~/poc/python
$ git clone git@github.com-personal:BRPersonal/langgraph_multi_agents.git
$ cd langgraph_multi_agents
$ uv init
$ vi pyproject.toml
set 3.13 for requires-python = ">=3.13"

Pin the python version before adding dependences
$ uv python pin 3.13

Install dependencies
$ uv add langgraph==1.0.2

# Install LLM integrations (choose your provider)
$ uv add langchain-openai  # For OpenAI models
$ uv add langchain-anthropic  # For Claude
$ uv add langchain-google-genai  # For Gemini
$ uv add langchain-groq  # For Groq (Llama models)

Install langgraph command line interface(cli) for development
$ uv add "langgraph-cli[inmem]"

add pydantic dependencies
uv add pydantic pydantic-settings

add langchain
uv add langchain
uv add pytest
uv add pytest-asyncio

Run all thests
python -m pytest -vv 


uv run streamlit run app.py --server.port 8501 --server.address localhost


