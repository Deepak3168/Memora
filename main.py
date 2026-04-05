from fastapi import FastAPI
from routes.auth import auth_router
from db.db_graph import init_db,close_db
from contextlib import asynccontextmanager
from mcp_tools.greet import greet_router
from mcp_tools.category_ops import category_router
import uvicorn
from fastapi_mcp import FastApiMCP
import logging
from mcp_tools.entity_ops import entity_router
from mcp_tools.relation_ops import relation_router
from fastapi.responses import JSONResponse
from db.db_sql import db 
from utils.personal_logs import create_logs_table
from routes.logs import log_router
from fastapi.middleware.cors import CORSMiddleware

# -----------------------------
# Your REST API lifespan
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = init_db()
    yield
    print("REST API shutdown complete.")
    close_db()


FORMAT = '%(levelname)s: %(asctime)-15s: %(filename)s: %(funcName)s: %(module)s: %(message)s'
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG, format=FORMAT)


#cors middleware 
origins = [ "http://localhost",
    "http://localhost:3000",]



create_logs_table(db)

# -----------------------------
# Create main FASTAPI app
# Importantly: use mcp_app.lifespan !!
# -----------------------------
app = FastAPI(
    title="Memora MCP Server/Personal Logger",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allows the defined origins
    allow_credentials=True,         # Allows cookies to be included in cross-origin requests
    allow_methods=["*"],            # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],            # Allows all headers
)

# Include your REST routes
app.include_router(auth_router)
app.include_router(greet_router)
app.include_router(category_router)
app.include_router(entity_router)
app.include_router(relation_router)
app.include_router(log_router)




@app.get("/openapidoc", summary="Return OpenAPI schema for MCP", description="Returns the full OpenAPI JSON used by the server.")
async def get_openapi_schema():
    return JSONResponse(content=app.openapi())
    


# -----------------------------
# Create MCP app and mount it
# -----------------------------
mcp = FastApiMCP(app,exclude_tags=["Authentication"],
                 name="Memora",description="Memora MCP server to store our Intrests and Knowledge",
                 headers = ["API_KEY"]
                 )
mcp.mount()

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, port=8000)
