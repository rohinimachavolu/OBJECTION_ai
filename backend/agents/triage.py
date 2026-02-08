import os
from dotenv import load_dotenv
import json
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
                    'temperature': 0.1,
                }
            },
            timeout=60
        )
        return response.json()['response']
    except Exception as e:
        print(f"Ollama error: {e}")
        return "{}"

def triage_agent(query: str, location: str) -> dict:
    """
    Classifies the legal issue and determines jurisdiction
    """
    
    prompt = f"""You are a legal triage specialist. Analyze this situation and respond ONLY with valid JSON.

User Query: {query}
User Location: {location}

IMPORTANT - Distinguish between:
1. CRITICAL (call 911): Active physical violence, weapons, someone attacking you RIGHT NOW
2. HIGH: Serious situation needing help soon (abuse, threats, severe issues) but not immediate 911 emergency
3. MEDIUM: Legal issue that should be addressed
4. LOW: Minor issue, can self-resolve

Examples:
- "My partner is hitting me right now" → CRITICAL
- "My partner threatened me with a gun yesterday" → HIGH
- "I feel depressed because of my roommate's abuse" → HIGH (mental health crisis, not 911)
- "My boss yelled at me" → MEDIUM

Classify into ONE category:
- immigration
- housing
- employment
- criminal
- consumer
- family

Respond with this exact JSON structure:
{{
  "category": "housing",
  "jurisdiction": {{
    "state": "Massachusetts",
    "city": "Boston"
  }},
  "urgency": "high",
  "requires_lawyer": false,
  "key_issues": ["emotional abuse", "roommate dispute"],
  "situation_type": "mental_health_crisis"
}}

situation_type can be:
- "active_violence" (happening RIGHT NOW, call 911)
- "mental_health_crisis" (suicidal thoughts, severe depression - need crisis hotline)
- "past_violence" (threats/violence occurred but not happening now)
- "legal_dispute" (normal legal issue)
"""
    
    response_text = call_ollama(prompt)
    
    # Parse response
    try:
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        json_str = response_text[start:end]
        result = json.loads(json_str)
        
        # Smart classification based on context
        query_lower = query.lower()
        
        # Mental health indicators (NOT 911, but crisis hotline)
        mental_health_keywords = ['depressed', 'depression', 'suicidal', 'kill myself', 'want to die', 'end it all', 'no reason to live']
        
        # Active violence indicators (911 NOW)
        active_violence_keywords = ['attacking me', 'hitting me', 'has a gun', 'right now', 'currently', 'is hurting']
        
        # Check for mental health crisis
        if any(keyword in query_lower for keyword in mental_health_keywords):
            result['situation_type'] = 'mental_health_crisis'
            result['urgency'] = 'high'
        
        # Check for active violence
        elif any(keyword in query_lower for keyword in active_violence_keywords):
            result['situation_type'] = 'active_violence'
            result['urgency'] = 'critical'
        
        else:
            result['situation_type'] = result.get('situation_type', 'legal_dispute')
        
        return result
    except Exception as e:
        print(f"Triage error: {e}")
        return {
            "category": "general",
            "jurisdiction": {"state": location.split(",")[-1].strip()},
            "urgency": "medium",
            "requires_lawyer": False,
            "key_issues": [],
            "situation_type": "legal_dispute"
        }

# Test
if __name__ == "__main__":
    result = triage_agent(
        "My boss hasn't paid me overtime for the last 3 months",
        "Boston, MA"
    )
    print(json.dumps(result, indent=2))