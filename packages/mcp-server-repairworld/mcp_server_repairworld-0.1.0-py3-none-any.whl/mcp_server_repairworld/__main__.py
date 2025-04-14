from .server import mcp
import argparse
from . import config

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
