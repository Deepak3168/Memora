import os 
from pydantic_settings import BaseSettings

class Constants(BaseSettings):
        APP_NAME :str = "Memora"
        VERSION :str= "1.0.0"
        #NEO4J CONFIGURATION
        NEO4J_URI :str = os.environ.get("NEO4J_URI","bolt://localhost:7687")
        NEO4J_USERNAME :str = os.environ.get("NEO4J_USERNAME","neo4j")
        NEO4J_PASSWORD :str = os.environ.get("NEO4J_PASSWORD","Deeak128")

        class Config:
            env_file = ".env"
            from_attributes = True




constants = Constants()
    