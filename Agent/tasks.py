from crewai import Task
import requests
import os
from dotenv import load_dotenv
from Agent.agents import create_analytics_agent, create_data_fetcher

load_dotenv()

# NASA API Key (from .env)
NASA_KEY = os.getenv("NASA_API_KEY")

data_fetcher = create_data_fetcher()
analytics_agent = create_analytics_agent()

def fetch_mars_weather():
    return Task(
        description="Fetch latest Mars weather from NASA InSight API.",
        agent=data_fetcher,
        expected_output="JSON data with temperature, wind speed, and season.",
        async_execution=True,
        action=lambda: requests.get(
            f"https://api.nasa.gov/insight_weather/?api_key={NASA_KEY}&feedtype=json&ver=1.0"
        ).json()
    )

def analyze_data_task():
    return Task(
        description="Analyze Mars weather data for trends.",
        agent=analytics_agent,
        expected_output="Bullet points highlighting key patterns.",
        context=[fetch_mars_weather()]
    )