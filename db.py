# db.py
from neontology import init_neontology
from neontology.graphengines import Neo4jConfig
from constants import constants

config = Neo4jConfig(
    uri=constants.NEO4J_URI,
    username=constants.NEO4J_USERNAME,
    password=constants.NEO4J_PASSWORD
)


def init_db():
    init_neontology(config)
    print("✅ DB initialization hook called")

def close_db():
    print("🛑 DB shutdown hook called")
