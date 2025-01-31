from autogen import AssistantAgent, UserProxyAgent
from crewai import Agent
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create shared LLM configuration for CrewAI using GPT-4o
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",  # Changed to GPT-4o
    temperature=0.3
)

def create_data_fetcher():
    return Agent(
        role="Space Data Analyst",
        goal="Fetch space data from NASA APIs",
        backstory="Expert in extracting insights from satellite and rover data.",
        llm=llm,
        verbose=True,
        max_iter=5  # Add safety limit
    )

def create_analytics_agent():
    return Agent(
        role="Data Scientist",
        goal="Analyze space data trends",
        backstory="Specializes in statistical analysis of planetary data.",
        llm=llm,
        verbose=True,
        max_iter=5
    )

# AutoGen Agents with GPT-4o
educator = AssistantAgent(
    name="Educator",
    system_message="Explain space concepts to students using simple analogies.",
    llm_config={
        "config_list": [{
            "model": "gpt-4o",  # Changed to GPT-4o
            "api_key": os.getenv("OPENAI_API_KEY"),
            "max_tokens": 1024,
            "temperature": 0.5
        }],
        "timeout": 60  # Add timeout
    }
)

citizen_agent = UserProxyAgent(
    name="Public",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,  # Add limit
    code_execution_config=False
)

def get_educator():
    return educator

def get_citizen_agent():
    return citizen_agent