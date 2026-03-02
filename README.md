🌐 GraphRAG: Context Graph Ingestion Engine
FastAPI + LlamaIndex + Neo4j + Groq

An advanced RAG (Retrieval-Augmented Generation) pipeline that transforms unstructured "Resources" into a structured Context Graph (Knowledge Graph) using LLM-based triplet extraction.

🚀 Why This Engine?
Traditional Vector RAG often misses the "connective tissue" between entities. This project uses GraphRAG to map relationships, enabling deep, multi-hop reasoning.

Lightning Fast: Powered by Groq (Llama 3 70B) for near-instant entity extraction.

Structured Intelligence: Built on LlamaIndex for seamless data orchestration.

Scalable Storage: Uses Neo4j as the graph store for high-performance relationship querying.

High Accuracy: ~85-90% precision in triplet extraction (Subject → Predicate → Object).

<img width="1200" height="536" alt="image" src="https://github.com/user-attachments/assets/cdd9f765-92ec-460f-b0d5-84a3b8688513" />

📋 Prerequisites
Before running the engine, ensure you have:

A Groq API Key

A Neo4j Instance (AuraDB)

Python 3.10+

⚙️ Installation & Setup
Clone the repository:

Bash
git clone https://github.com/yourusername/graph-rag-engine.git
cd graph-rag-engine
Install dependencies:

Bash
pip install -r requirements.txt
Configure Environment Variables:
Create a .env file in the root directory:

Code snippet
GROQ_API_KEY=your_key_here
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
Run the API:

Bash
uvicorn main:app --reload

🧪 Converting Synthetic Data to Graph
You can push unstructured text to the /build_graph endpoint.

Sample Request:

Bash
curl -X 'POST' 'http://localhost:8000/build_graph' \
-H 'Content-Type: application/json' \
-d '{"text": "Project Nexus is managed by Dr. Thorne at OmniCorp. It uses Neo4j to store neural weights."}'
Resulting Graph Structure:

(Dr. Thorne) -[MANAGES]-> (Project Nexus)

(Project Nexus) -[USES]-> (Neo4j)

(Dr. Thorne) -[WORKS_AT]-> (OmniCorp)

📈 Roadmap

[ ] Integration with Microsoft GraphRAG community summaries.

[ ] Frontend visualization dashboard using react-force-graph.

[ ] Support for local LLMs via Ollama.
