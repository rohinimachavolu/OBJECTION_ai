from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from orchestrator import run_legal_assistant

app = FastAPI(title="OBJECTION.ai API")

# CORS - Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    location: str

@app.post("/query")
async def handle_query(request: QueryRequest):
    """Main endpoint for legal queries"""
    result = run_legal_assistant(request.query, request.location)
    return result

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "OBJECTION.ai"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)