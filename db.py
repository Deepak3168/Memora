# db.py
from neontology import init_neontology
from neontology.graphengines import Neo4jConfig

# Neo4j configuration
config = Neo4jConfig(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="Deepak128"
)

# Initialize Neo4j driver globally
init_neontology(config)
print("✅ Neo4j initialized with neontology")

def init_db():
    """Dummy function for FastAPI startup hook"""
    print("✅ DB initialization hook called")

def close_db():
    """Dummy function for FastAPI shutdown hook"""
    print("🛑 DB shutdown hook called")
