from duckduckgo_search import DDGS
from typing import List, Dict

def search_web_for_claim(claim_text: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Searches DuckDuckGo for the given claim and returns the top snippets and URLs.
    """
    results = []
    try:
        # DDGS is a context manager that safely opens and closes the search connection
        with DDGS() as ddgs:
            # We search for the exact claim text to find relevant articles
            raw_results = ddgs.text(claim_text, max_results=max_results)
            
            for r in raw_results:
                results.append({
                    "title": r.get("title", "Unknown Title"),
                    "snippet": r.get("body", "No snippet available."),
                    "url": r.get("href", "")
                })
    except Exception as e:
        print(f"Search failed: {e}")
        
    return results

def format_context_for_llm(search_results: List[Dict[str, str]]) -> str:
    """
    Converts the raw search dictionary into a readable string block for the AI prompt.
    """
    if not search_results:
        return "No external context found."
        
    context_text = "Here is real-time web context to help evaluate the claim:\n\n"
    for i, res in enumerate(search_results, 1):
        context_text += f"Source {i}: {res['title']}\n"
        context_text += f"URL: {res['url']}\n"
        context_text += f"Excerpt: {res['snippet']}\n\n"
        
    return context_text
