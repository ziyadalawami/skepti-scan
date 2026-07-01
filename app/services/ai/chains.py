import json
from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.services.ai.prompts import EVALUATION_PROMPT
from app.services.ai.retriever import search_web_for_claim, format_context_for_llm

llm = ChatOpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    model="openai/gpt-oss-20b",
    temperature=0.0
)

evaluation_chain = EVALUATION_PROMPT | llm

def evaluate_claim(claim_text: str) -> dict:
    """Runs the full RAG pipeline: Search -> Format -> Evaluate."""
    
    # 1. Retrieve real-time data from the web
    print(f"Searching web for: {claim_text}")
    search_results = search_web_for_claim(claim_text, max_results=3)
    
    # 2. Format the data into a readable string
    context_text = format_context_for_llm(search_results)
    
    # 3. Pass BOTH the claim and the context to the LLM
    print("Evaluating claim with retrieved context...")
    response = evaluation_chain.invoke({
        "claim_text": claim_text,
        "context": context_text
    })
    
    try:
        raw_content = response.content.strip()
        if raw_content.startswith("```json"):
            raw_content = raw_content[7:-3].strip()
        elif raw_content.startswith("```"):
            raw_content = raw_content[3:-3].strip()
            
        result = json.loads(raw_content)
        
        # Add the retrieved URLs to our final JSON so the database saves them!
        result["sources"] = [res["url"] for res in search_results]
        
        return result
        
    except json.JSONDecodeError as e:
        return {
            "status": "inconclusive",
            "confidence": 0.0,
            "justification": f"System failed to parse AI evaluation. Error: {str(e)}",
            "sources": []
        }
