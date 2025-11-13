🧠 Memora MCP Server

Memora MCP Server is a lightweight backend built using FastAPI and Neo4j that acts as a memory engine — capable of storing entities and relationships representing personal interests, skills, and experiences as a Knowledge Graph.
This project demonstrates how MCP (Model Context Protocol) can be used to give LLMs persistent memory and reasoning over structured context.

🚀 Features

Entity and relationship creation with Neo4j

REST API built with FastAPI

Integration-ready MCP endpoint for LLM clients (like Claude)

Designed as a base for building personalized AI memory or contextual intelligence systems

⚙️ Setup
1. Clone the repository
git clone https://github.com/<your-username>/memora-mcp-server.git
cd memora-mcp-server

2. Create a virtual environment

Use venv to keep dependencies simple and isolated:

python -m venv mcp
source mcp/bin/activate   # (Linux/Mac)
mcp\Scripts\activate      # (Windows)

3. Install dependencies
pip install -r requirements.txt

4. Run the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


Your API will now be available at:
👉 http://127.0.0.1:8000/docs

🗄️ Neo4j Setup
1. Install Neo4j
sudo apt install neo4j -y

2. Set up Neo4j password

After installation, open the Neo4j console:

sudo neo4j console


Then visit http://localhost:7474
 and set your new password.

3. Start Neo4j service
sudo systemctl start neo4j
sudo systemctl enable neo4j

4. Create .env file

Create a .env file as mentioned in constants.py, for example:

NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here

🧩 MCP Server Integration (Claude)

You can connect this backend to Claude Desktop as an MCP Server.

Steps:

Open Claude → Settings → Developers → Edit Config

Copy the JSON config from
mcpconfig.json

Restart Claude

On Windows: close it from Task Manager

On Mac/Linux: simply restart the app

You should now see Memora MCP Server listed in Claude’s connected MCP tools.

💬 Example Prompt for Claude

Try this inside Claude after connecting the MCP server:

“From now, create entities and relationships based on my interests, skills, and knowledge.
Build a knowledge graph that reflects my personality, expertise, and learning history.”

Claude will then begin creating entities (representing your interests, skills, etc.) and relationships (showing how they connect), gradually forming a personal knowledge graph.

🔮 Potential Use Cases

Personalized AI assistants that remember your context

Context-driven recommendations and ads

Graph-to-vector embeddings for LLM fine-tuning

Building a long-term AI memory system

🧱 Project Structure
📦 memora-mcp-server
├── main.py                 # FastAPI entry point
├── routes/
│   ├── entity_ops.py       # Entity creation & listing routes
│   └── relation_ops.py     # Relationship endpoints
├── models/
│   └── entity_node.py      # EntityNode definition
├── db/
│   └── init.py             # Neo4j connection setup
├── constants.py            # Env and configuration constants
├── claude_desktop_config.json # MCP config for Claude
└── requirements.txt

🧠 Concept Overview

Every time you interact with the MCP server, new entities (like “Deepak”, “Backend Developer”, “Python”) and relationships (like Deepak → skilled_in → Python) are stored in Neo4j.
Over time, this forms a graph representation of your memory and interests — a foundational step toward a Memory Engine that can later:

Generate embeddings

Train fine-tuned models

Enable contextual recall for future prompts

🧑‍💻 Author

Deepak Ootala
Passionate about backend development, data engineering, and building intelligent systems that evolve with user context.
