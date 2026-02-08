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
                    'temperature': 0.3,
                }
            },
            timeout=60
        )
        return response.json()['response']
    except Exception as e:
        print(f"Ollama error: {e}")
        return "Unable to generate action plan"

def action_strategist_agent(query: str, rights_info: dict, triage_result: dict) -> dict:
    """
    Provides step-by-step action plan
    """
    
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
    
    action_plan = call_ollama(prompt)
    
    return {
        "action_plan": action_plan
    }