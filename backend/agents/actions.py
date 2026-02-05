from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

def action_strategist_agent(query: str, rights_info: dict, triage_result: dict) -> dict:
    """
    Provides step-by-step action plan
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""You are a legal action strategist. Based on this situation, provide a clear action plan.

User Situation: {query}
Their Rights: {rights_info.get('explanation', 'See rights explanation')}
Category: {triage_result.get('category')}

Provide:
1. Immediate actions (numbered list, 3-5 steps)
2. A professional script/template for communication
3. Timeline (how long they have to act)
4. Escalation path (what to do if initial steps fail)

Be specific and actionable.
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
        "action_plan": chat_completion.choices[0].message.content
    }