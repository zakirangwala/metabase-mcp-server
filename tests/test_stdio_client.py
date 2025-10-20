#!/usr/bin/env python3
"""
Simple stdio MCP client for testing Metabase MCP Server.
"""

import json
import sys
import asyncio
from typing import Dict, Any


class StdioMCPClient:
    def __init__(self):
        self.initialized = False

    def send_message(self, message: Dict[str, Any]) -> None:
        """Send a JSON-RPC message to the server."""
        json_str = json.dumps(message)
        print(json_str, flush=True)

    def read_message(self) -> Dict[str, Any]:
        """Read a JSON-RPC message from the server."""
        try:
            line = sys.stdin.readline().strip()
            if not line:
                return None
            return json.loads(line)
        except (json.JSONDecodeError, EOFError):
            return None

    async def initialize(self) -> Dict[str, Any]:
        """Initialize the MCP session."""
        init_msg = {
            "jsonrpc": "2.0",
            "id": "init",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        self.send_message(init_msg)

        # Read the response
        response = self.read_message()
        if response is None:
            return {"error": {"code": -1, "message": "No response received"}}
        return response

    async def send_initialized(self) -> None:
        """Send the initialized notification."""
        init_msg = {
            "jsonrpc": "2.0",
            "method": "initialized",
            "params": {}
        }
        self.send_message(init_msg)

    async def list_tools(self) -> Dict[str, Any]:
        """List available tools."""
        tools_msg = {
            "jsonrpc": "2.0",
            "id": "tools-list",
            "method": "tools/list",
            "params": {}
        }
        self.send_message(tools_msg)

        # Read the response
        response = self.read_message()
        if response is None:
            return {"error": {"code": -1, "message": "No response received"}}
        return response

    async def call_tool(self, tool_name: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Call a specific tool."""
        call_msg = {
            "jsonrpc": "2.0",
            "id": f"tool-call-{tool_name}",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": params or {}
            }
        }
        self.send_message(call_msg)

        # Read the response
        response = self.read_message()
        if response is None:
            return {"error": {"code": -1, "message": "No response received"}}
        return response


async def test_stdio_connection():
    """Test the MCP server connection via stdio."""
    print("Testing MCP server connection via stdio...", flush=True)

    try:
        client = StdioMCPClient()

        # Step 1: Initialize
        print("1. Initializing session...", flush=True)
        init_result = await client.initialize()
        print(f"Init result: {json.dumps(init_result, indent=2)}", flush=True)

        if init_result is None or "error" in init_result:
            error_msg = init_result.get('error', 'Unknown error') if init_result else 'No response'
            print(f"❌ Initialization failed: {error_msg}", flush=True)
            return False

        # Step 2: Send initialized notification
        print("2. Sending initialized notification...", flush=True)
        await client.send_initialized()

        # Step 3: List tools
        print("3. Listing tools...", flush=True)
        tools_result = await client.list_tools()
        print(f"Tools result: {json.dumps(tools_result, indent=2)}", flush=True)

        if "error" in tools_result:
            print(f"❌ Tools listing failed: {tools_result['error']}", flush=True)
            return False

        if "result" in tools_result:
            tools = tools_result["result"].get("tools", [])
            print(f"✅ Found {len(tools)} tools!", flush=True)
            for tool in tools[:3]:  # Show first 3 tools
                print(f"  - {tool.get('name')}: {tool.get('description', '')[:100]}...", flush=True)
        else:
            print("❌ No tools found in result", flush=True)
            return False

        # Step 4: Test calling a tool
        print("4. Testing tool call (get_metabase_databases)...", flush=True)
        db_result = await client.call_tool("get_metabase_databases")
        print(f"DB result: {json.dumps(db_result, indent=2)}", flush=True)

        if "error" in db_result:
            print(f"❌ Tool call failed: {db_result['error']}", flush=True)
            return False

        if "result" in db_result:
            print("✅ Tool call successful!", flush=True)
            data = db_result["result"].get("data", [])
            print(f"Found {len(data)} databases", flush=True)
        else:
            print("❌ Tool call returned no result", flush=True)
            return False

        return True

    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_stdio_connection())
    if success:
        print("✅ All tests passed!", flush=True)
    else:
        print("❌ Tests failed!", flush=True)
        sys.exit(1)
