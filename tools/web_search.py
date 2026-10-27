import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def web_search(query: str, max_results: int = 3) -> str:
    """Search the web and return a summary of the results."""
    response = client.search(query=query, max_results=max_results)
    results = []

    for r in response["results"]:
        results.append(f"- {r['title']}: {r['content'][:200]}")
    return "\n".join(results) if results else "No results found."
