import os
from google.adk.agents.llm_agent import Agent
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

# ----------------------------
# SEARCH TOOL
# ----------------------------
def web_search(query: str) -> dict:
    """Search the internet and return top results."""
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv("SERPAPI_KEY")
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    data = []
    if "organic_results" in results:
        for r in results["organic_results"][:5]:
            data.append({
                "title": r.get("title"),
                "snippet": r.get("snippet"),
                "link": r.get("link")
            })

    return {
        "status": "success",
        "query": query,
        "results": data
    }


# ----------------------------
# ROOT AGENT (MAIN LOGIC)
# ----------------------------
root_agent = Agent(
    model="gemini-2.0-flash-thinking-exp",
    name="content_writer_agent",
    description="An AI agent that writes LinkedIn posts and blogs using real-time web search data.",
    instruction=(
        "You are a professional content writer AI. "
        "When the user asks for a LinkedIn post, blog, or trend analysis, "
        "FIRST use the 'web_search' tool to gather fresh information from the internet. "
        "Then write a high-quality, structured output using insights from search results."
    ),
    tools=[web_search],
)

