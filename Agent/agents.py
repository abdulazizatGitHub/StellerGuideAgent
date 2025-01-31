from crewai import Agent
from autogen import AssistantAgent, UserProxyAgent
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# CrewAI Agents
def create_data_fetcher():
    return Agent(
        role="Space Data Analyst",
        goal="Fetch space data from NASA APIs",
        backstory="Expert in extracting insights from satellite and rover data.",
        verbose=True
    )

def create_analytics_agent():
    return Agent(
        role="Data Scientist",
        goal="Analyze space data trends",
        backstory="Specializes in statistical analysis of planetary data.",
        verbose=True
    )

# AutoGen Agents (Education and Public Interaction)
educator = AssistantAgent(
    name="Educator",
    system_message="Explain space concepts to students using simple analogies.",
    llm_config={
        "config_list": [{
            "model": "gpt-3.5-turbo",
            "api_key": os.getenv("OPENAI_API_KEY")  # Add API key here
        }]
    }
)

citizen_agent = UserProxyAgent(
    name="Public",
    human_input_mode="NEVER",
    code_execution_config=False
)

def get_educator():
    return educator

def get_citizen_agent():
    return citizen_agent