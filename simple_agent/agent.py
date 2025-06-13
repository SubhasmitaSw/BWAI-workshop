from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

# Root agent is automatically detected by ADK CLI
def get_weather(location: str) -> str:
    """Get the weather for a specific location"""
    return f"The weather in {location} is sunny with a temperature of 45 degrees."

# root agent for ollama with tools
root_agent = LlmAgent(
    model=LiteLlm(model="ollama_chat/gemma3:latest"),
    # model="gemini-2.0-flash-exp",
    name="weather_agent",
    description="You are a weather agent that can get the weather for a specific location.",
    # description="You are a pookie agent that replies in cat lingual as responses to user queries.",
    tools=[get_weather],
)