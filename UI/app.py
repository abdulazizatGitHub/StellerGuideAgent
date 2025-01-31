import streamlit as st
from Agent.agents import create_data_fetcher, create_analytics_agent, get_educator, get_citizen_agent
from Agent.tasks import fetch_mars_weather, analyze_data_task
from crewai import Crew
import agentops
from openai import OpenAI
import os

educator = get_educator()
citizen_agent = get_citizen_agent()

# Initialize AgentOps (for monitoring)
agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"))

# Setup OpenAI (for images)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🚀 StellarGuide: Your Space Assistant")

# User Input
query = st.text_input("Ask about space:", "What's happening on Mars today?")

if st.button("Search"):
    # Crew Setup
    data_fetcher = create_data_fetcher()
    analytics_agent = create_analytics_agent()
    
    # To this:
    crew = Crew(
        agents=[data_fetcher, analytics_agent],
        tasks=[fetch_mars_weather(), analyze_data_task()],
        verbose=True  # ✅ Correct boolean value
    )
    
    # Execute Tasks
    result = crew.kickoff()
    
    # Display Results
    st.subheader("Latest Mars Weather")
    st.json(result)
    
    # Educator Explanation
    st.subheader("Explanation for Students")
    citizen_agent.initiate_chat(educator, message=f"Explain this to a 10-year-old: {result}")
    st.write(educator.last_message()["content"])
    
    # Generate Image
    image_prompt = f"Friendly cartoon of Mars with weather: {result}"
    response = client.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        size="1024x1024"
    )
    st.image(response.data[0].url, caption="AI-Generated Mars Scene")