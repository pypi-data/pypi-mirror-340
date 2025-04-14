import argparse
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from . import config

import logging

# Set global logging level (for all loggers)
# change this if you want the API call logs.
logging.basicConfig(level=logging.WARNING)

#print(sys.argv)

config.API_BASE = None
config.CUSTOMER_API_KEY = None
config.HEADERS = None

# Init FastMCP server
mcp = FastMCP("repair-tools")

async def call_backend(method: str, endpoint: str, params=None, json=None) -> dict[str, Any] | str:
    url = f"{config.API_BASE}/{endpoint}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=config.HEADERS,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Error contacting backend: {str(e)}"

@mcp.tool()
async def create_repair_request(serial_number: str, description: str) -> str:
    """Create a new repair request (only for customers)."""
    payload = {
        "device_serial_number": serial_number,
        "description": description
    }
    params = {"api_key": config.CUSTOMER_API_KEY}
    result = await call_backend("POST", "repair_requests", params=params, json=payload)

    if isinstance(result, str):
        return result
    return "Repair request submitted successfully."

@mcp.tool()
async def view_all_requests() -> str:
    """Fetch all repair requests."""
    params = {"api_key": config.CUSTOMER_API_KEY}
    result = await call_backend("GET", "repair_requests", params=params)

    if isinstance(result, str):
        return result
    if not result:
        return "No repair requests found."

    output = []
    for req in result:
        output.append(f"ID: {req['request_id']} | Device: {req['device_serial_number']} | Desc: {req['description']} | User: {req['username']} | Status: {req['status']}")
    return "\n".join(output)

@mcp.tool()
async def view_request_by_id(request_id: int) -> str:
    """View details of a specific repair request."""
    params = {
        "api_key": config.CUSTOMER_API_KEY,
        "request_id": request_id
    }
    result = await call_backend("GET", "repair_requests", params=params)

    if isinstance(result, str):
        return result
    if not result:
        return f"No request found with ID {request_id}"

    req = result[0]
    return f"ID: {req['request_id']}\nDevice: {req['device_serial_number']}\nDesc: {req['description']}\nUser: {req['username']}\nStatus: {req['status']}"

# mostly required for - mcp dev server.py command
# gets called only when you connect from the inspector
if __name__ == "__main__":
    print("Running the server!")
    # Parse command-line arguments with defaults
    parser = argparse.ArgumentParser(description="MCP server for repair app")
    parser.add_argument(
        "--api-base",
        type=str,
        default="http://localhost:5000/api",
        help="Base URL of the repair API (default: http://localhost:5000/api)"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default="cust123456",
        help="API key for authentication (default: test-api-key)"
    )
    args = parser.parse_args()
    # Use parsed arguments
    config.API_BASE = args.api_base.rstrip("/")
    config.CUSTOMER_API_KEY = args.api_key
    config.HEADERS = {
        "Accept": "application/json"
    }

    mcp.run(transport="stdio")
