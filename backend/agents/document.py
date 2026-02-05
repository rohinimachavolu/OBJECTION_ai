from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

def document_generator_agent(query: str, triage_result: dict, action_plan: dict) -> str:
    """
    Generates formal legal documents
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
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
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.2,
    )
    
    return chat_completion.choices[0].message.content