from dotenv import dotenv_values
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("resy-mcp")

RESY_API_KEY = dotenv_values(".env").get("RESY_API_KEY", None)

@mcp.tool()
async def get_reservation_details():
    if RESY_API_KEY is None:
        raise ValueError("RESY_API_KEY not set in .env file.")

    return "Success"
