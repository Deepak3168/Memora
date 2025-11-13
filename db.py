# db.py
from neontology import init_neontology
from neontology.graphengines import Neo4jConfig
from constants import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

# Neo4j configuration
config = Neo4jConfig(
    uri=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD
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
