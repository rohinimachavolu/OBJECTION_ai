# ⚖️ OBJECTION.ai
source venv/bin/activate
Ollama : ollama serve
frontend : streamlit run frontend/app.py
backend : python backend/main.py   
**Your Constitutional Copilot for Legal Rights**

OBJECTION.ai is an AI-powered legal assistant that helps everyday people understand their legal rights, navigate complex situations, and access free resources - without needing expensive lawyers.

Built for **JusticeHack Hackathon** 🏆

---

## 🎯 Problem We're Solving

Millions of people face legal issues daily but can't afford lawyers ($300+/hour). They struggle with:
- Not knowing if something is legally actionable
- Understanding complex legal jargon
- Finding the right resources and agencies
- Distinguishing urgent situations from routine ones
- Navigating federal vs state vs local laws

**OBJECTION.ai democratizes legal knowledge** by providing free, AI-powered guidance for everyday legal situations.

---

## ✨ Key Features

### 1. **Multi-Agent AI System**
- **Triage Agent**: Classifies legal issues and assesses urgency
- **Rights Explainer**: Cites actual constitutional and statutory rights
- **Action Strategist**: Provides step-by-step guidance
- **Document Generator**: Creates demand letters, complaints, forms
- **Resource Connector**: Finds free legal aid and agencies
- **News Monitor**: Shows recent developments related to your issue

### 2. **360° Legal Coverage**
- Immigration & visa issues
- Employment & labor disputes
- Housing & tenant rights
- Criminal justice & police encounters
- Consumer protection
- Family law matters

### 3. **Smart Emergency Detection**
- **Active Violence** → Immediate 911 alert
- **Mental Health Crisis** → 988 Lifeline resources
- **Past Threats** → Legal escalation paths
- **Normal Issues** → Step-by-step guidance

### 4. **RAG-Powered Legal Research**
- Searches actual legal documents (Constitution, federal/state laws)
- Cites specific statutes and regulations
- Jurisdiction-aware (applies your state/local laws)
- Reduces AI hallucination with grounded sources

### 5. **Real-Time News Integration**
- Pulls recent news related to your legal issue
- Examples: ICE enforcement trends, wage theft cases, tenant victories
- Helps you understand local patterns and developments

---

## 🏗️ Project Structure

```
objection-ai/
├── backend/                      # FastAPI backend server
│   ├── agents/                   # AI agent modules
│   │   ├── triage.py            # Classifies legal issues, detects emergencies
│   │   ├── rights.py            # Explains constitutional & statutory rights
│   │   ├── actions.py           # Provides action plans and scripts
│   │   ├── document.py          # Generates legal documents
│   │   ├── resources.py         # Finds legal aid and agencies
│   │   └── news.py              # Fetches recent news articles
│   │
│   ├── data/                     # Training data and resources
│   │   ├── legal_corpus/        # Legal documents for RAG
│   │   │   ├── flsa_overtime.txt           # Fair Labor Standards Act
│   │   │   ├── fourth_amendment.txt        # Search & seizure rights
│   │   │   └── ma_tenant_rights.txt        # State housing laws
│   │   └── resources.json                   # Legal aid database
│   │
│   ├── main.py                   # FastAPI application entry point
│   ├── orchestrator.py           # Coordinates all agents (workflow)
│   └── rag.py                    # RAG engine with ChromaDB
│
├── frontend/                     # Streamlit user interface
│   └── app.py                    # Main UI with tabs and alerts
│
├── .env                          # API keys (not committed to git)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 📚 Data Sources & Training

### **Legal Corpus (RAG Knowledge Base)**

OBJECTION.ai does **NOT use traditional machine learning training**. Instead, it uses **Retrieval-Augmented Generation (RAG)** to ground responses in real legal documents:

#### **What We Use:**
1. **Federal Laws**
   - U.S. Constitution (Amendments 1, 4, 5, 14)
   - Fair Labor Standards Act (FLSA) - overtime, minimum wage
   - Fair Housing Act - tenant rights, discrimination
   - Title VII - employment discrimination
   - Americans with Disabilities Act (ADA)

2. **State Laws** (Currently: Massachusetts, expandable to all 50 states)
   - State-specific tenant rights (habitability, eviction rules)
   - State labor laws (wage theft, overtime exemptions)
   - State criminal procedure codes

3. **Legal Resources Database**
   - Free legal aid organizations (by state)
   - Government agencies (contact info, filing procedures)
   - Crisis hotlines (988, domestic violence, immigration)
   - Eligibility requirements for free services

#### **Data Format:**
Each legal document includes:
- **Citation**: Official reference (e.g., "29 USC §207")
- **Jurisdiction**: Federal, state, or local
- **Category**: Employment, housing, immigration, etc.
- **Legal Text**: Full statute or regulation
- **Plain English**: Simplified explanation for non-lawyers

#### **How RAG Works:**
1. User asks a question
2. System searches vector database for relevant laws
3. Retrieves top 2-3 most relevant legal documents
4. AI generates response grounded in those specific laws
5. Every claim is cited with source (no hallucination)

#### **Data Collection Process:**
- Federal laws: Downloaded from [Congress.gov](https://www.congress.gov/) (public domain)
- State laws: Scraped from state legislature websites
- Simplified versions: Based on ACLU "Know Your Rights" guides, Nolo.com legal guides
- Resources: Manually curated from government websites, legal aid directories

---

## 🤖 AI Models Used

### **Language Model: Groq (Llama 3.3 70B)**
- **Why Groq?** Free API with generous limits (14,400 requests/day)
- **Why Llama 3.3?** Strong reasoning, fast inference, good at structured outputs
- **Temperature Settings:**
  - Triage: 0.1 (precise classification)
  - Rights/Actions: 0.3 (balanced accuracy and readability)
  - Documents: 0.2 (formal, consistent formatting)

### **Vector Database: ChromaDB**
- Stores legal document embeddings
- Fast semantic search (cosine similarity)
- Local deployment (no external dependencies)

### **News API: NewsAPI**
- Free tier: 100 requests/day
- Pulls real-time news articles
- Filters by relevance, date, and jurisdiction

---

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.9 or higher
- pip (Python package manager)
- Terminal/Command Prompt

### **Step 1: Clone Repository**
```bash
git clone https://github.com/your-username/objection-ai.git
cd objection-ai
```

### **Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 3: Get Free API Keys**

#### **Groq API (Required)**
1. Go to: https://console.groq.com/
2. Sign up (free)
3. Create API key
4. Copy the key

#### **NewsAPI (Optional but Recommended)**
1. Go to: https://newsapi.org/register
2. Sign up (free)
3. Copy the API key

### **Step 4: Configure Environment Variables**

Create a `.env` file in the root directory:

```bash
touch .env
```

Add your API keys:

```
GROQ_API_KEY=your_groq_api_key_here
NEWS_API_KEY=your_newsapi_key_here
```

### **Step 5: Initialize RAG Database**

Test that legal documents load properly:

```bash
python backend/rag.py
```

You should see:
```
✅ Loaded 3 legal documents into RAG
🔍 Test Search Results:
[Legal document snippets...]
```

### **Step 6: Start the Backend**

```bash
python backend/main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Keep this terminal open!**

### **Step 7: Start the Frontend**

Open a **new terminal window**:

```bash
streamlit run frontend/app.py
```

Your browser should automatically open to: `http://localhost:8501`

---

## 🎮 How to Use

### **Quick Start**

1. **Select a Demo Scenario** (sidebar)
   - "Unpaid overtime wages"
   - "Landlord won't fix mold"
   - "ICE encounter as immigrant"
   - "Domestic violence emergency"

2. **Or Enter Custom Query**
   - Be specific: dates, amounts, what happened
   - Include your location

3. **Click "Get Legal Guidance"**
   - Wait 30-60 seconds (AI is analyzing)

4. **Review Results in Tabs:**
   - 📜 **Your Rights**: Constitutional & legal protections
   - 🎯 **Action Plan**: Step-by-step guidance
   - 📄 **Document**: Generated demand letter/complaint
   - 🤝 **Resources**: Free legal aid contacts
   - 📰 **Recent News**: Related developments

### **Example Queries**

**Good ✅:**
```
"My boss hasn't paid me overtime for 3 months. I work 50 hours/week 
as a server in Boston. They only pay regular hourly rate."
```

**Too Vague ❌:**
```
"I have a problem with my boss"
```

**Good ✅:**
```
"My landlord won't fix black mold in my bathroom. I sent written 
notice 3 weeks ago. The lease says they're responsible for repairs."
```

**Too Vague ❌:**
```
"My apartment has issues"
```

---

## 🔧 Configuration & Customization

### **Add More Legal Documents**

1. Create a new `.txt` file in `backend/data/legal_corpus/`
2. Format:
   ```
   [Title] - [Topic]
   Citation: [Official Reference]
   Jurisdiction: [Federal/State/Local]
   Category: [employment/housing/immigration/etc.]

   [Full legal text or key excerpts]

   Plain English: [Simplified explanation]
   ```

3. Restart backend to load new documents

### **Add More Resources**

Edit `backend/data/resources.json`:

```json
{
  "employment": {
    "california": [
      {
        "name": "California Labor Commissioner",
        "phone": "1-844-522-6734",
        "website": "https://www.dir.ca.gov/dlse/",
        "services": ["Wage claims", "Workplace safety"]
      }
    ]
  }
}
```

### **Adjust AI Behavior**

Edit agent prompt templates in `backend/agents/*.py`:

```python
prompt = f"""You are a legal expert...
[Modify instructions here]
"""
```

---

## 🏛️ Legal Architecture Decisions

### **Why Multi-Agent System?**
- **Separation of Concerns**: Each agent has one job (triage, rights, actions)
- **Parallel Processing**: Multiple agents can work simultaneously
- **Easier Debugging**: Isolate issues to specific agents
- **Scalability**: Add new agents (e.g., case law search) without breaking existing ones

### **Why RAG Instead of Fine-Tuning?**
- **Accuracy**: Grounded in actual legal sources (no hallucination)
- **Transparency**: Every claim is cited with source
- **Updatability**: Add new laws by dropping files (no retraining)
- **Cost**: Fine-tuning LLMs is expensive; RAG uses free vector DB

### **Why Groq (Not OpenAI/Claude)?**
- **Cost**: 100% free tier (14,400 requests/day)
- **Speed**: Groq's LPU architecture is extremely fast
- **Quality**: Llama 3.3 70B rivals GPT-4 for structured tasks

### **Why Streamlit (Not React)?**
- **Speed**: Build functional UI in hours, not days
- **Focus**: Hackathon priorities → AI logic over frontend polish
- **Deployment**: One-click deploy to Streamlit Cloud

---

## 🚨 Safety & Disclaimers

### **What OBJECTION.ai IS:**
- ✅ Legal information tool
- ✅ Educational resource
- ✅ Guidance for self-help
- ✅ Resource directory

### **What OBJECTION.ai IS NOT:**
- ❌ Legal advice (only lawyers can provide that)
- ❌ Substitute for a licensed attorney
- ❌ Guaranteed to be 100% accurate
- ❌ Responsible for legal outcomes

### **Emergency Detection:**
- **Active violence** → Always directs to 911
- **Mental health crisis** → 988 Suicide Lifeline
- **Past threats** → Legal escalation paths

### **User Privacy:**
- No conversation data stored long-term
- API calls are encrypted (HTTPS)
- No personally identifiable information logged

---

## 🐛 Troubleshooting

### **Backend won't start**
```bash
# Check if port 8000 is already in use
lsof -i :8000

# Kill the process
kill -9 <PID>

# Try again
python backend/main.py
```

### **Frontend shows "Connection Error"**
- Make sure backend is running (`python backend/main.py`)
- Check backend logs for errors
- Verify you see "Uvicorn running on http://0.0.0.0:8000"

### **RAG shows "No documents found"**
```bash
# Verify files exist
ls backend/data/legal_corpus/

# Should show: flsa_overtime.txt, fourth_amendment.txt, ma_tenant_rights.txt

# Test RAG manually
python backend/rag.py
```

### **News tab shows no articles**
- Check if `NEWS_API_KEY` is in `.env`
- Verify API key at: https://newsapi.org/account
- NewsAPI free tier: 100 requests/day (may be rate limited)

### **Groq API errors**
- Check if `GROQ_API_KEY` is in `.env`
- Verify key at: https://console.groq.com/keys
- Free tier: 14,400 requests/day

---

## 📈 Future Enhancements

### **Phase 2 (Post-Hackathon):**
- [ ] Add all 50 states' legal corpuses
- [ ] Case law search (recent court decisions)
- [ ] Multi-language support (Spanish, Chinese, etc.)
- [ ] User accounts (save documents, track cases)
- [ ] Integration with court filing systems
- [ ] Mobile app (iOS/Android)

### **Phase 3 (Production):**
- [ ] Lawyer marketplace (connect with pro bono attorneys)
- [ ] Community forums (peer support)
- [ ] AI-powered document review
- [ ] Automated court form filling
- [ ] Legal deadline tracking

---

## 🤝 Contributing

We welcome contributions! Areas we need help:

1. **Legal Corpus Expansion**: Add more states' laws
2. **Resource Database**: Curate legal aid by state
3. **UI/UX Improvements**: Better mobile experience
4. **Testing**: Edge cases, error handling
5. **Documentation**: Tutorials, video guides

**How to contribute:**
```bash
# Fork the repo
# Create a feature branch
git checkout -b feature/add-california-laws

# Make changes
# Commit and push
git push origin feature/add-california-laws

# Open a Pull Request
```

---

## 📄 License

This project is licensed under the **MIT License** - see LICENSE file for details.

**Legal Disclaimer:** This software provides legal information, not legal advice. For serious legal matters, consult a licensed attorney.

---

## 👥 Team

**Built by:** [Your Name / Team Name]
**Hackathon:** JusticeHack 2026
**Contact:** your-email@example.com

---

## 🙏 Acknowledgments

- **Groq**: Free AI inference (Llama 3.3)
- **NewsAPI**: Real-time news data
- **ChromaDB**: Vector database
- **Streamlit**: Rapid UI development
- **ACLU**: "Know Your Rights" resources
- **Legal Aid Organizations**: Resource directories

---

## 📊 Tech Stack Summary

| Component | Technology | Why? |
|-----------|-----------|------|
| **Frontend** | Streamlit | Fast prototyping, built-in components |
| **Backend** | FastAPI | Async support, automatic API docs |
| **AI Model** | Groq (Llama 3.3 70B) | Free, fast, high quality |
| **Vector DB** | ChromaDB | Simple, local, no setup |
| **Orchestration** | LangGraph | Multi-agent workflows |
| **News** | NewsAPI | Real-time articles |
| **Deployment** | Railway/Render | Easy hosting |

---

## 📞 Support

**Issues?** Open a GitHub issue: https://github.com/your-username/objection-ai/issues

**Questions?** Email: your-email@example.com

**Demo Video:** [Link to hackathon demo]

---

**⚖️ Justice should be accessible to everyone, not just those who can afford it.**

**OBJECTION.ai - Because your rights matter.**

