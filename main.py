from fastapi import FastAPI
from routes.auth import auth_router
from db import init_db,close_db
from contextlib import asynccontextmanager
from mcp_tools.greet import greet_router
import uvicorn
from fastapi_mcp import FastApiMCP
import logging

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






# -----------------------------
# Create main FASTAPI app
# Importantly: use mcp_app.lifespan !!
# -----------------------------
app = FastAPI(
    title="Memora MCP Server",
    lifespan=lifespan,
)



# Include your REST routes
app.include_router(auth_router)
app.include_router(greet_router)




# -----------------------------
# Create MCP app and mount it
# -----------------------------
mcp = FastApiMCP(app,exclude_tags=["Authentication"],name="Memora",description="Memora MCP server to store our Intrests and Knowledge")
mcp.mount()


# Run the server
if __name__ == "__main__":
    uvicorn.run(app, port=8000)
