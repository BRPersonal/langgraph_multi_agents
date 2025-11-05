from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from utils.config import settings

# Define a simple tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # In production, call a real weather API
    return f"The weather in {city} is sunny, 72°F"

def get_time(timezone: str = "UTC") -> str:
    """Get current time in specified timezone."""
    from datetime import datetime
    return f"Current time: {datetime.now().strftime('%H:%M:%S')}"
    
# Create the agent
model = ChatOpenAI(model="gpt-4", temperature=0)
agent = create_agent(
    model=model,
    tools=[get_weather, get_time]
)
# Run it!
response = agent.invoke({
    "messages": [{"role": "user", "content": "What's the weather in NYC?"}]
})
print(response["messages"][-1].content)