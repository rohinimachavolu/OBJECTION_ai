import os
from dotenv import load_dotenv
import sys
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag import LegalRAG

load_dotenv()

def call_ollama(prompt: str, model: str = "llama3.1:8b") -> str:
    """
    Call local Ollama instance
    """
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': 0.3,
                }
            },
            timeout=60
        )
        return response.json()['response']
    except Exception as e:
        print(f"Ollama error: {e}")
        return "Unable to generate response"

def rights_explainer_agent(query: str, triage_result: dict) -> dict:
    """
    Explains legal rights based on relevant laws
    """
    # Search for relevant laws
    rag = LegalRAG()
    category = triage_result.get("category", "general")
    search_query = f"{category} {' '.join(triage_result.get('key_issues', []))}"
    
    rag_results = rag.search(search_query, n_results=2)
    legal_context = "\n\n".join(rag_results['documents'])
    
    prompt = f"""You are a legal rights expert. Explain the user's rights based on these laws.

User Situation: {query}
Category: {category}
Location: {triage_result.get('jurisdiction', {}).get('state', 'Unknown')}

Relevant Laws:
{legal_context}

Provide:
1. Constitutional rights (if applicable)
2. Federal law protections
3. State law protections
4. Plain English explanation

Be clear, concise, and cite specific laws.
"""
    
    explanation = call_ollama(prompt)
    
    return {
        "explanation": explanation,
        "sources": rag_results['metadatas']
    }