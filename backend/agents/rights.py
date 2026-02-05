from groq import Groq
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag import LegalRAG

load_dotenv()

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
    
    # Generate explanation
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
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
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.3,
    )
    
    return {
        "explanation": chat_completion.choices[0].message.content,
        "sources": rag_results['metadatas']
    }

# Test
if __name__ == "__main__":
    test_triage = {
        "category": "employment",
        "jurisdiction": {"state": "Massachusetts"},
        "key_issues": ["overtime", "unpaid wages"]
    }
    
    result = rights_explainer_agent(
        "My boss hasn't paid me overtime",
        test_triage
    )
    print(result['explanation'])