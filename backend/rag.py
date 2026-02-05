import chromadb
from chromadb.utils import embedding_functions
import os
from pathlib import Path

class LegalRAG:
    def __init__(self):
        # Initialize Chroma client
        self.client = chromadb.Client()
        
        # Create collection
        self.collection = self.client.get_or_create_collection(
            name="legal_corpus",
            embedding_function=embedding_functions.DefaultEmbeddingFunction()
        )
        
        # Load legal documents
        self.load_corpus()
    
    def load_corpus(self):
        """Load legal documents from data/legal_corpus folder"""
        corpus_path = Path("backend/data/legal_corpus")
        
        documents = []
        metadatas = []
        ids = []
        
        for file_path in corpus_path.glob("*.txt"):
            with open(file_path, 'r') as f:
                content = f.read()
                documents.append(content)
                metadatas.append({"source": file_path.name})
                ids.append(file_path.stem)
        
        if documents:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ Loaded {len(documents)} legal documents into RAG")
        else:
            print("⚠️ No documents found in legal_corpus folder")
    
    def search(self, query: str, n_results: int = 3):
        """Search for relevant legal information"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return {
            "documents": results['documents'][0],
            "metadatas": results['metadatas'][0]
        }

# Test the RAG
if __name__ == "__main__":
    rag = LegalRAG()
    results = rag.search("overtime pay")
    print("\n🔍 Test Search Results:")
    for doc in results['documents']:
        print(f"\n{doc[:200]}...")