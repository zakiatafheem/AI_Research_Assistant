import streamlit as st
import os

from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import initialize_agent, AgentType

# Streamlit page settings
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖"
)

# API Keys from Hugging Face Secrets
groq_api_key = os.getenv("GROQ_API_KEY")

# Title
st.title("🤖 AI Research Assistant")
st.write("Research any topic using Agentic AI")

# Load LLM
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

# Tavily Search Tool
search_tool = TavilySearchResults(max_results=3)

# Agent
agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# User Input
query = st.text_input(
    "Enter your research topic",
    placeholder="Example: Latest trends in Generative AI"
)

# Button
if st.button("Research"):

    if query:

        prompt = f"""
        Research the following topic and provide:

        - Key Points
        - Important Trends
        - Real-world Applications
        - Challenges
        - Short Summary

        Format response in bullet points with headings.

        Topic: {query}
        """

        with st.spinner("Researching..."):

            try:
                result = agent.run(prompt)

                st.subheader("📌 Research Results")
                st.markdown(result)

            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.warning("Please enter a topic.")