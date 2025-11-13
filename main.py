from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from routes.entity_ops import router as entity_router
from routes.relation_ops import router as relation_router
from db import init_db, close_db
import os 
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    print("App shutdown complete.")



app = FastAPI(lifespan=lifespan,title="Memora MCP Server")




app.include_router(entity_router)
app.include_router(relation_router)

mcp = FastApiMCP(app,name="Memora",description="Memora MCP server to store our Intrests and Knowledge")
mcp.mount()
