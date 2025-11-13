from fastapi import FastAPI
# from fastmcp import FastMCP
from fastapi_mcp import FastApiMCP
from routes.entity_ops import router as entity_router
from routes.relation_ops import router as relation_router
from db import init_db, close_db
from dotenv import load_dotenv 


load_dotenv()
app = FastAPI(title="Memora MCP Server")


@app.on_event("startup")
def startup_event():
    print("🚀 Starting Memora MCP Server...")
    try:
        init_db()
    except Exception as e:
        print(f"❌ Failed to connect to Neo4j: {e}")

@app.on_event("shutdown")
def shutdown_event():
    close_db()



# @app.get("/add", operation_id="add_two_numbers")
# async def add(a: int, b: int):
#     """Add two numbers and return the sum."""
#     summ = pd.DataFrame({"a": [a], "b": [b], "sum": [a+b]})
#     result = int(summ.loc[0, "sum"])
#     return {"sum": result}


# @mcp.tool()
# def say_hello(name: str) -> str:
#     """A simple tool that greets the user by name."""
#     return f"Hello, {name}!"

app.include_router(entity_router)
app.include_router(relation_router)

mcp = FastApiMCP(app,name="Memora",description="Memora MCP server to store our Intrests and Knowledge")

mcp.mount()
# mcp.mount_sse()


# {
#   "mcpServers": {
#     "memora-mcp": {
#       "command": "wsl",
#       "args": [
#         "-d", "Ubuntu",
#         "-e", "bash",
#         "-c",
#         "cd /home/deepak/projects/Memora  &&  /home/deepak/projects/mcp/bin/mcp-proxy http://127.0.0.1:8000/mcp"
#       ]
#     }
#   }
# }
