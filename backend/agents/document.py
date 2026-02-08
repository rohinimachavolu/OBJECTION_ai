import os
from dotenv import load_dotenv
import requests

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
                    'temperature': 0.2,
                }
            },
            timeout=90
        )
        return response.json()['response']
    except Exception as e:
        print(f"Ollama error: {e}")
        return "Unable to generate document"

def document_generator_agent(query: str, triage_result: dict, action_plan: dict) -> str:
    """
    Generates formal legal documents
    """
    
    category = triage_result.get('category')
    
    # Determine document type
    if category == "employment":
        doc_type = "demand letter for unpaid wages"
    elif category == "housing":
        doc_type = "formal complaint to landlord"
    else:
        doc_type = "formal notice letter"
    
    prompt = f"""Generate a professional {doc_type} based on this situation.

User Situation: {query}
Action Plan Context: {action_plan.get('action_plan', '')}

The document should:
1. Be formally formatted
2. Cite relevant laws
3. State demands clearly
4. Include appropriate tone
5. Have placeholder fields like [YOUR NAME], [DATE], etc.

Generate the complete document now.
"""
    
    return call_ollama(prompt)