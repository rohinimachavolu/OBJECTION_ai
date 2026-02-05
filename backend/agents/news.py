import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

load_dotenv()

def news_monitor_agent(triage_result: dict) -> dict:
    """
    Fetches recent news related to the legal issue
    """
    category = triage_result.get('category', 'legal')
    jurisdiction = triage_result.get('jurisdiction', {})
    state = jurisdiction.get('state', '')
    city = jurisdiction.get('city', '')
    key_issues = triage_result.get('key_issues', [])
    
    # Build better search queries
    search_queries = build_search_query(category, state, city, key_issues)
    
    # Fetch news from NewsAPI
    all_articles = []
    
    for query in search_queries[:3]:  # Try top 3 queries
        articles = fetch_news(query)
        all_articles.extend(articles)
        
        if len(all_articles) >= 8:  # Get at least 8 articles
            break
    
    # Remove duplicates
    unique_articles = []
    seen_titles = set()
    
    for article in all_articles:
        title = article['title'].lower()
        # Skip if duplicate or generic
        if title not in seen_titles and len(title) > 20:
            unique_articles.append(article)
            seen_titles.add(title)
            
        if len(unique_articles) >= 10:
            break
    
    return {
        "articles": unique_articles,
        "query_used": search_queries[0] if search_queries else "legal news",
        "category": category
    }

def build_search_query(category: str, state: str, city: str, key_issues: list) -> list:
    """
    Build highly targeted search queries based on category
    """
    queries = []
    
    # Make state/city lowercase for better matching
    state = state.lower()
    city = city.lower()
    
    # Category-specific PRECISE keywords
    category_keywords = {
        "immigration": [
            f"ICE arrest {state} {city}",
            f"immigration enforcement {state}",
            f"ICE raid {city}",
            "deportation united states",
            f"visa enforcement {state}",
            "immigration detention center"
        ],
        "employment": [
            f"wage theft {state}",
            f"labor law violation {city}",
            f"unpaid overtime lawsuit {state}",
            "department of labor enforcement",
            f"worker rights {state}",
            "employment discrimination lawsuit"
        ],
        "housing": [
            f"eviction {city} {state}",
            f"landlord lawsuit {state}",
            f"tenant rights violation {city}",
            "housing discrimination",
            f"rent control {city}",
            f"illegal eviction {state}"
        ],
        "criminal": [
            f"police misconduct {city}",
            f"wrongful arrest {state}",
            f"police shooting {city}",
            "civil rights lawsuit police",
            f"excessive force {state}",
            "criminal justice reform"
        ],
        "consumer": [
            f"consumer fraud {state}",
            f"ftc lawsuit {city}",
            "consumer protection enforcement",
            f"class action lawsuit {state}",
            "consumer rights violation"
        ],
        "family": [
            f"family court {state}",
            f"custody case {city}",
            "divorce law changes",
            f"child support {state}"
        ]
    }
    
    # Get category-specific queries
    if category in category_keywords:
        queries.extend(category_keywords[category])
    
    # Add key issue-based queries (very specific)
    if key_issues:
        for issue in key_issues[:2]:
            queries.append(f'"{issue}" {state}')  # Use quotes for exact match
            queries.append(f'{issue} lawsuit {state}')
    
    return queries

def fetch_news(query: str, days_back: int = 60) -> list:
    """
    Fetch news from NewsAPI with better filtering
    """
    api_key = os.getenv("NEWS_API_KEY")
    
    if not api_key:
        return get_fallback_news(query)
    
    # Calculate date range - go back further for better results
    to_date = datetime.now()
    from_date = to_date - timedelta(days=days_back)
    
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": from_date.strftime("%Y-%m-%d"),
        "to": to_date.strftime("%Y-%m-%d"),
        "language": "en",
        "sortBy": "relevancy",  # Changed from publishedAt to relevancy
        "apiKey": api_key,
        "pageSize": 10  # Get more results
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('status') == 'ok':
            articles = []
            for article in data.get('articles', []):
                # Filter out bad results
                title = article.get('title', '')
                description = article.get('description', '')
                
                # Skip removed/deleted articles
                if '[Removed]' in title or not description:
                    continue
                
                # Skip articles from irrelevant sources
                source_name = article.get('source', {}).get('name', '')
                if source_name in ['Google News', 'Yahoo']:
                    continue
                
                articles.append({
                    "title": title,
                    "description": description,
                    "url": article.get('url', ''),
                    "source": source_name,
                    "published_at": article.get('publishedAt', ''),
                    "image_url": article.get('urlToImage', '')
                })
            return articles
        else:
            print(f"NewsAPI error: {data.get('message', 'Unknown error')}")
            return get_fallback_news(query)
            
    except Exception as e:
        print(f"Error fetching news: {e}")
        return get_fallback_news(query)

def get_fallback_news(query: str) -> list:
    """
    Fallback: Generate helpful search suggestions when API fails
    """
    category = query.split()[0].title()
    
    return [
        {
            "title": f"Search for Recent {category} News",
            "description": f"No API key configured or rate limit reached. Click to search Google News for the latest {category.lower()} developments.",
            "url": f"https://www.google.com/search?q={query.replace(' ', '+')}+news&tbm=nws",
            "source": "Search Suggestion",
            "published_at": datetime.now().isoformat(),
            "image_url": ""
        }
    ]

# Test
if __name__ == "__main__":
    # Test immigration
    print("Testing IMMIGRATION news...")
    test_triage = {
        "category": "immigration",
        "jurisdiction": {"state": "Massachusetts", "city": "Boston"},
        "key_issues": ["ICE enforcement", "deportation"]
    }
    
    result = news_monitor_agent(test_triage)
    
    print(f"\nFound {len(result['articles'])} articles")
    print(f"Query used: {result['query_used']}\n")
    
    for i, article in enumerate(result['articles'][:5], 1):
        print(f"{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   URL: {article['url'][:50]}...")
        print()