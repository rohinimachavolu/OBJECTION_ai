import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="OBJECTION.ai",
    page_icon="⚖️",
    layout="wide"
)

# Custom CSS for blinking emergency alert
st.markdown("""
<style>
@keyframes blink {
    0%, 49% { opacity: 1; }
    50%, 100% { opacity: 0.3; }
}

.emergency-alert {
    background: linear-gradient(135deg, #ff0000 0%, #cc0000 100%);
    color: white;
    padding: 25px;
    border-radius: 10px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    border: 4px solid #ffffff;
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
    animation: blink 1s infinite;
}

.emergency-icon {
    font-size: 48px;
    margin-bottom: 10px;
}

.emergency-text {
    margin-top: 10px;
    font-size: 18px;
    font-weight: normal;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("⚖️ OBJECTION.ai")
st.subheader("Your Constitutional Copilot for Legal Rights")

# Sidebar
with st.sidebar:
    st.header("📍 Your Location")
    location = st.text_input("City, State", value="Boston, MA")
    
    st.markdown("---")
    st.header("🎯 Quick Scenarios")
    scenario = st.selectbox("Try a demo:", [
        "Custom Query",
        "Unpaid overtime wages",
        "Landlord won't fix mold",
        "ICE encounter as immigrant",
        "Domestic violence emergency"
    ])
    
    st.markdown("---")
    st.info("💡 **Tip:** Be specific about dates, amounts, and what happened.")

# Predefined scenarios
SCENARIOS = {
    "Unpaid overtime wages": "My boss hasn't paid me overtime for the last 3 months. I work 50 hours per week as a server at a restaurant in Boston. They only pay me regular hourly rate.",
    "Landlord won't fix mold": "There's black mold growing in my bathroom and bedroom. I told my landlord 3 weeks ago in writing but they haven't fixed it. The lease says they're responsible for repairs.",
    "ICE encounter as immigrant": "I'm an international student on F-1 visa. I'm worried about ICE enforcement in my area. What are my rights if approached by immigration officers?",
    "Domestic violence emergency": "My partner physically attacked me and is threatening me. I'm scared and don't know what to do. I need help immediately."
}

# Main query input
if scenario != "Custom Query":
    query = SCENARIOS[scenario]
    st.info(f"**Demo Scenario:** {query}")
    user_query = query
else:
    user_query = st.text_area(
        "Describe your legal situation:",
        height=150,
        placeholder="Example: My landlord is trying to evict me without proper notice..."
    )

# Submit button
if st.button("🔍 Get Legal Guidance", type="primary", use_container_width=True):
    if not user_query:
        st.error("Please enter a query or select a demo scenario!")
    else:
        with st.spinner("⚖️ Analyzing your situation... This may take 30-60 seconds..."):
            try:
                # Call backend
                response = requests.post(
                    "http://localhost:8000/query",
                    json={"query": user_query, "location": location},
                    timeout=120
                )
                result = response.json()
                
                # Check urgency for emergency alert
                triage = result.get('triage', {})
                urgency = triage.get('urgency', 'medium').lower()
                requires_lawyer = triage.get('requires_lawyer', False)
                
                # Display results in tabs
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "📜 Your Rights",
                    "🎯 Action Plan",
                    "📄 Document",
                    "🤝 Resources",
                    "📰 Recent News"
                ])
                
                with tab1:
                    # Get triage info
                    triage = result.get('triage', {})
                    urgency = triage.get('urgency', 'medium').lower()
                    situation_type = triage.get('situation_type', 'legal_dispute')
                    
                    # DIFFERENT ALERTS BASED ON SITUATION TYPE
                    
                    # 1. ACTIVE VIOLENCE - Show 911
                    if situation_type == 'active_violence':
                        st.markdown("""
                        <div class="emergency-alert">
                            <div class="emergency-icon">🚨</div>
                            <div>EMERGENCY - CALL 911 IMMEDIATELY</div>
                            <div class="emergency-text">
                                If you are in immediate physical danger, call 911 now.<br>
                                Get to a safe location if possible.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.error("**Emergency Contacts:**")
                        st.markdown("🚨 **Police/Fire/Medical:** 911")
                        st.markdown("---")
                    
                    # 2. MENTAL HEALTH CRISIS - Show 988 and crisis resources
                    elif situation_type == 'mental_health_crisis':
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); 
                                    color: white; padding: 25px; border-radius: 10px; 
                                    text-align: center; margin-bottom: 20px; border: 3px solid #ffffff;">
                            <div style="font-size: 36px; margin-bottom: 10px;">💜</div>
                            <div style="font-size: 22px; font-weight: bold;">YOU ARE NOT ALONE - HELP IS AVAILABLE</div>
                            <div style="margin-top: 15px; font-size: 16px;">
                                If you're thinking about suicide or need someone to talk to right now
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info("📞 **988 Suicide & Crisis Lifeline**\n\nCall or text **988** anytime, 24/7\n\nFree, confidential support")
                        with col2:
                            st.info("💬 **Crisis Text Line**\n\nText **HOME** to **741741**\n\nTrained crisis counselors available")
                        
                        st.warning("💡 **Also consider:** If your roommate's behavior is creating an unsafe living situation, you may have legal options (restraining order, breaking lease, etc.). See the Action Plan tab.")
                        st.markdown("---")
                    
                    # 3. PAST VIOLENCE/THREATS - Show warning but not emergency
                    elif situation_type == 'past_violence' or urgency == 'high':
                        st.warning("⚠️ **HIGH PRIORITY SITUATION**")
                        st.markdown("""
                        This situation requires prompt attention. Consider:
                        - Filing a police report (non-emergency: 311 or local police non-emergency number)
                        - Consulting with a lawyer about protective orders
                        - Contacting a domestic violence hotline for guidance: **1-800-799-7233**
                        """)
                        st.markdown("---")
                    
                    st.subheader("Your Legal Rights")
                    
                    # Triage metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Category", triage.get('category', 'N/A').title())
                    with col2:
                        urgency_display = urgency.title()
                        urgency_color = {
                            'low': '🟢',
                            'medium': '🟡', 
                            'high': '🟠',
                            'critical': '🔴'
                        }.get(urgency, '⚪')
                        st.metric("Urgency", f"{urgency_color} {urgency_display}")
                    with col3:
                        requires_lawyer = triage.get('requires_lawyer', False)
                        needs_lawyer = "Yes ⚠️" if requires_lawyer else "Not Required"
                        st.metric("Need Lawyer?", needs_lawyer)
                    
                    st.markdown("---")
                    
                    # Rights explanation
                    rights = result.get('rights', {})
                    st.markdown(rights.get('explanation', 'No rights information available'))
                    
                    # Sources
                    if 'sources' in rights:
                        with st.expander("📚 Legal Sources"):
                            for source in rights['sources']:
                                st.code(source.get('source', 'Unknown'))
                
                with tab2:
                    st.subheader("What You Should Do Next")
                    actions = result.get('actions', {})
                    st.markdown(actions.get('action_plan', 'No action plan available'))
                
                with tab3:
                    st.subheader("Generated Legal Document")
                    document = result.get('document', 'No document generated')
                    st.text_area("Document Content", document, height=400)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Document",
                        data=document,
                        file_name="legal_document.txt",
                        mime="text/plain"
                    )
                
                with tab4:
                    st.subheader("Free Legal Resources")
                    resources = result.get('resources', {}).get('resources', [])
                    
                    if resources:
                        for resource in resources:
                            with st.container():
                                st.markdown(f"### {resource.get('name', 'Unknown')}")
                                if 'phone' in resource:
                                    st.markdown(f"📞 **Phone:** {resource['phone']}")
                                if 'website' in resource:
                                    st.markdown(f"🌐 **Website:** {resource['website']}")
                                if 'services' in resource:
                                    st.markdown(f"**Services:** {', '.join(resource['services'])}")
                                if 'eligibility' in resource:
                                    st.info(f"ℹ️ {resource['eligibility']}")
                                st.markdown("---")
                    else:
                        st.warning("No specific resources found for your location/category.")
                        st.info("💡 Try contacting your state's Attorney General office or local legal aid society.")
                
                with tab5:
                    st.subheader("📰 Recent News & Developments")
                    
                    news_data = result.get('news', {})
                    articles = news_data.get('articles', [])
                    query_used = news_data.get('query_used', '')
                    
                    if query_used:
                        st.caption(f"🔍 Search: {query_used}")
                    
                    if articles:
                        st.success(f"Found {len(articles)} recent articles related to your issue")
                        
                        for i, article in enumerate(articles, 1):
                            with st.container():
                                col1, col2 = st.columns([3, 1])
                                
                                with col1:
                                    # Article title as link
                                    if article.get('url'):
                                        st.markdown(f"### [{article.get('title', 'No title')}]({article['url']})")
                                    else:
                                        st.markdown(f"### {article.get('title', 'No title')}")
                                    
                                    # Description
                                    if article.get('description'):
                                        st.write(article['description'])
                                    
                                    # Metadata
                                    meta_parts = []
                                    if article.get('source'):
                                        meta_parts.append(f"**Source:** {article['source']}")
                                    if article.get('published_at'):
                                        try:
                                            date_obj = datetime.fromisoformat(article['published_at'].replace('Z', '+00:00'))
                                            date_str = date_obj.strftime('%B %d, %Y')
                                            meta_parts.append(f"**Date:** {date_str}")
                                        except:
                                            pass
                                    
                                    if meta_parts:
                                        st.caption(" | ".join(meta_parts))
                                
                                with col2:
                                    # Display image if available
                                    if article.get('image_url'):
                                        try:
                                            st.image(article['image_url'], width=150)
                                        except:
                                            pass
                                
                                st.markdown("---")
                        
                        # Relevance disclaimer
                        st.info("💡 **Note:** These articles are related to your issue but may not directly apply to your specific situation. Use them for general awareness.")
                        
                    else:
                        st.warning("No recent news articles found for this topic.")
                        st.info(f"💡 Try searching Google News for: **{triage.get('category', 'legal')} news {location}**")
                
                # Success message
                st.success("✅ Analysis complete! Review all tabs for comprehensive guidance.")
                
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The backend might be processing. Try again in a moment.")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Make sure the backend server is running: `python backend/main.py`")

# Footer
st.markdown("---")
st.caption("⚠️ **Disclaimer:** This is legal information, not legal advice. For serious legal matters, consult a licensed attorney.")