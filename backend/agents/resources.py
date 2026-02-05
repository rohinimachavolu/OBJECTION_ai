import json
from pathlib import Path

def resource_connector_agent(triage_result: dict) -> dict:
    """
    Finds relevant legal resources based on category and location
    """
    category = triage_result.get('category', 'general')
    state = triage_result.get('jurisdiction', {}).get('state', '').lower()
    
    # Load resources
    resources_path = Path("backend/data/resources.json")
    with open(resources_path, 'r') as f:
        all_resources = json.load(f)
    
    # Get category resources
    category_resources = all_resources.get(category, {})
    
    # Combine federal and state resources
    resources = []
    resources.extend(category_resources.get('federal', []))
    resources.extend(category_resources.get(state, []))
    
    return {
        "resources": resources,
        "category": category
    }

# Test
if __name__ == "__main__":
    test_triage = {
        "category": "employment",
        "jurisdiction": {"state": "massachusetts"}
    }
    
    result = resource_connector_agent(test_triage)
    print(json.dumps(result, indent=2))