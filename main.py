import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_index.core import Document, KnowledgeGraphIndex, StorageContext, Settings
from llama_index.graph_stores.neo4j import Neo4jGraphStore
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# NEW IMPORTS FOR EXISTING GRAPH RETRIEVAL
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import KnowledgeGraphRAGRetriever

# 1. Load the environment variables
load_dotenv()

print("\n--- CONNECTION CHECK ---")
print("URI Loaded:", os.getenv("NEO4J_URI"))
print("Username Loaded:", os.getenv("NEO4J_USERNAME"))
print("------------------------\n")

app = FastAPI(title="LlamaIndex Knowledge Graph API")

# 2. Configure LlamaIndex to use the NEW Groq model and local embeddings
Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
Settings.embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")
Settings.chunk_size = 512

# 3. Define the data formats for our endpoints
class ResourceData(BaseModel):
    text: str

class QueryData(BaseModel):
    question: str

# --- ENDPOINT 1: Build the Graph (Ingestion) ---
@app.post("/build_graph")
async def build_graph(data: ResourceData):
    try:
        # Connect to Neo4j database 
        graph_store = Neo4jGraphStore(
            username=os.getenv("NEO4J_USERNAME"),
            password=os.getenv("NEO4J_PASSWORD"),
            url=os.getenv("NEO4J_URI"),
            database=os.getenv("NEO4J_USERNAME"),
            refresh_schema=False
        )
        storage_context = StorageContext.from_defaults(graph_store=graph_store)

        # Convert the text into a Document
        doc = Document(text=data.text)

        # Groq processes the text, extracts triplets, and pushes them to Neo4j
        index = KnowledgeGraphIndex.from_documents(
            [doc],
            storage_context=storage_context,
            max_triplets_per_chunk=10,
            include_embeddings=False
        )

        return {"status": "success", "message": "Knowledge Graph built successfully!"}
    
    except Exception as e:
        print(f"Error occurred during build: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- ENDPOINT 2: Query the Graph (Retrieval) ---
@app.post("/query_graph")
async def query_graph(data: QueryData):
    try:
        # 1. Connect to the existing Neo4j database 
        graph_store = Neo4jGraphStore(
            username=os.getenv("NEO4J_USERNAME"),
            password=os.getenv("NEO4J_PASSWORD"),
            url=os.getenv("NEO4J_URI"),
            database=os.getenv("NEO4J_USERNAME"),
            refresh_schema=False
        )
        storage_context = StorageContext.from_defaults(graph_store=graph_store)

        # 2. Use the KnowledgeGraphRAGRetriever designed for existing Graph Databases
        retriever = KnowledgeGraphRAGRetriever(
            storage_context=storage_context,
            verbose=True
        )

        # 3. Attach the retriever to a Query Engine
        query_engine = RetrieverQueryEngine.from_args(retriever)

        # 4. Ask the question and get the answer from Groq
        response = query_engine.query(data.question)

        return {
            "status": "success", 
            "question": data.question, 
            "answer": str(response)
        }
    
    except Exception as e:
        print(f"Error occurred during query: {e}")
        raise HTTPException(status_code=500, detail=str(e))
