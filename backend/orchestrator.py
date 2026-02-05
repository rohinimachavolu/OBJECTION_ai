from typing import TypedDict
from agents.triage import triage_agent
from agents.rights import rights_explainer_agent
from agents.actions import action_strategist_agent
from agents.document import document_generator_agent
from agents.resources import resource_connector_agent
from agents.news import news_monitor_agent  # NEW IMPORT

class LegalAssistantState(TypedDict):
    query: str
    location: str
    triage: dict
    rights: dict
    actions: dict
    document: str
    resources: dict
    news: dict  # NEW FIELD

def run_legal_assistant(query: str, location: str) -> dict:
    """
    Orchestrates all agents to process legal query
    """
    print("🔍 Step 1: Triaging legal issue...")
    triage_result = triage_agent(query, location)
    
    print("📜 Step 2: Explaining your rights...")
    rights_result = rights_explainer_agent(query, triage_result)
    
    print("🎯 Step 3: Creating action plan...")
    actions_result = action_strategist_agent(query, rights_result, triage_result)
    
    print("📄 Step 4: Generating document...")
    document = document_generator_agent(query, triage_result, actions_result)
    
    print("🤝 Step 5: Finding resources...")
    resources_result = resource_connector_agent(triage_result)
    
    print("📰 Step 6: Fetching recent news...")  # NEW STEP
    news_result = news_monitor_agent(triage_result)
    
    return {
        "triage": triage_result,
        "rights": rights_result,
        "actions": actions_result,
        "document": document,
        "resources": resources_result,
        "news": news_result  # NEW RESULT
    }

# Test
if __name__ == "__main__":
    result = run_legal_assistant(
        "My boss hasn't paid me overtime for 3 months. I work 50 hours/week as a server.",
        "Boston, MA"
    )
    
    print("\n" + "="*50)
    print("TRIAGE:", result['triage'])
    print("\n" + "="*50)
    print("RIGHTS:", result['rights']['explanation'][:300])
    print("\n" + "="*50)
    print("NEWS:", len(result['news']['articles']), "articles found")