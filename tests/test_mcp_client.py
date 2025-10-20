#!/usr/bin/env python3
"""
Simple MCP client test script for Metabase MCP Server.
This script demonstrates how to properly connect to the streamable-http MCP server.
"""

import asyncio
import json
import aiohttp
from typing import Dict, Any


class MCPClient:
    def __init__(self, server_url: str = "http://127.0.0.1:3200/mcp"):
        self.server_url = server_url
        self.session_id: str = None
        self.http_session: aiohttp.ClientSession = None

    async def __aenter__(self):
        self.http_session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.http_session:
            await self.http_session.close()

    async def initialize_session(self) -> Dict[str, Any]:
        """Initialize a session with the MCP server."""
        payload = {
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

        async with self.http_session.post(
            self.server_url,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
        ) as response:
            # Handle Server-Sent Events response
            if response.content_type == "text/event-stream":
                # Read the SSE response
                text_content = await response.text()
                print(f"SSE Response: {text_content}")
                print(f"All response headers: {dict(response.headers)}")

                # Parse SSE data (basic parsing)
                lines = text_content.strip().split('\n')
                data_lines = [line for line in lines if line.startswith('data: ')]
                if data_lines:
                    try:
                        result = json.loads(data_lines[0][6:])  # Remove 'data: ' prefix
                        print(f"Parsed SSE data: {json.dumps(result, indent=2)}")

                        # Extract session ID from response headers or cookies
                        if 'mcp-session-id' in response.headers:
                            self.session_id = response.headers['mcp-session-id']
                            print(f"Extracted session ID from mcp-session-id header: {self.session_id}")
                        elif 'X-Session-ID' in response.headers:
                            self.session_id = response.headers['X-Session-ID']
                            print(f"Extracted session ID from header: {self.session_id}")
                        elif 'Set-Cookie' in response.headers:
                            cookie_header = response.headers['Set-Cookie']
                            print(f"Cookie header: {cookie_header}")
                            # Parse session ID from cookie if present
                            if 'session_id=' in cookie_header:
                                self.session_id = cookie_header.split('session_id=')[1].split(';')[0]
                                print(f"Extracted session ID: {self.session_id}")
                            else:
                                # Try to extract from any cookie that might contain session info
                                import re
                                session_match = re.search(r'session[_-]?id=([^;\s]+)', cookie_header)
                                if session_match:
                                    self.session_id = session_match.group(1)
                                    print(f"Extracted session ID from cookie regex: {self.session_id}")

                        return result
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse SSE data: {e}")
                        return {"error": "Failed to parse SSE response"}
                else:
                    return {"error": "No data in SSE response"}
            else:
                # Fallback to JSON parsing
                result = await response.json()
                print(f"JSON response: {json.dumps(result, indent=2)}")

                # Extract session ID if present in JSON response
                if 'sessionId' in result:
                    self.session_id = result['sessionId']
                    print(f"Extracted session ID from JSON: {self.session_id}")

                return result

    async def send_initialized(self) -> Dict[str, Any]:
        """Send the initialized notification (required by MCP protocol)."""
        payload = {
            "jsonrpc": "2.0",
            "method": "initialized",
            "params": {}
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }

        if self.session_id:
            headers["mcp-session-id"] = self.session_id
            self.http_session.cookie_jar.update_cookies({"mcp-session-id": self.session_id})

        async with self.http_session.post(
            self.server_url,
            json=payload,
            headers=headers
        ) as response:
            # Handle Server-Sent Events response
            if response.content_type == "text/event-stream":
                text_content = await response.text()
                print(f"Initialized SSE Response: {text_content}")

                lines = text_content.strip().split('\n')
                data_lines = [line for line in lines if line.startswith('data: ')]
                if data_lines:
                    try:
                        result = json.loads(data_lines[0][6:])
                        print(f"Initialized response: {json.dumps(result, indent=2)}")
                        return result
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse initialized SSE data: {e}")
                        return {"error": "Failed to parse SSE response"}
                else:
                    return {"result": "Initialized notification sent"}
            else:
                result = await response.json()
                print(f"Initialized JSON response: {json.dumps(result, indent=2)}")
                return result

    async def list_tools(self) -> Dict[str, Any]:
        """List available tools from the MCP server."""
        payload = {
            "jsonrpc": "2.0",
            "id": "tools-list",
            "method": "tools/list"
            # No params for tools/list according to some MCP implementations
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }

        # Add session ID if available
        if self.session_id:
            headers["mcp-session-id"] = self.session_id
            # Also add as cookie for session persistence
            self.http_session.cookie_jar.update_cookies({"mcp-session-id": self.session_id})

        async with self.http_session.post(
            self.server_url,
            json=payload,
            headers=headers
        ) as response:
            # Handle Server-Sent Events response
            if response.content_type == "text/event-stream":
                text_content = await response.text()
                print(f"SSE Response: {text_content}")

                lines = text_content.strip().split('\n')
                data_lines = [line for line in lines if line.startswith('data: ')]
                if data_lines:
                    try:
                        result = json.loads(data_lines[0][6:])
                        print(f"Parsed SSE data: {json.dumps(result, indent=2)}")
                        return result
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse SSE data: {e}")
                        return {"error": "Failed to parse SSE response"}
                else:
                    return {"error": "No data in SSE response"}
            else:
                result = await response.json()
                print(f"JSON response: {json.dumps(result, indent=2)}")
                return result

    async def call_tool(self, tool_name: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Call a specific tool."""
        payload = {
            "jsonrpc": "2.0",
            "id": f"tool-call-{tool_name}",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": params or {}
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }

        if self.session_id:
            headers["mcp-session-id"] = self.session_id
            # Also add as cookie for session persistence
            self.http_session.cookie_jar.update_cookies({"mcp-session-id": self.session_id})

        async with self.http_session.post(
            self.server_url,
            json=payload,
            headers=headers
        ) as response:
            # Handle Server-Sent Events response
            if response.content_type == "text/event-stream":
                text_content = await response.text()
                print(f"SSE Response: {text_content}")

                lines = text_content.strip().split('\n')
                data_lines = [line for line in lines if line.startswith('data: ')]
                if data_lines:
                    try:
                        result = json.loads(data_lines[0][6:])
                        print(f"Parsed SSE data: {json.dumps(result, indent=2)}")
                        return result
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse SSE data: {e}")
                        return {"error": "Failed to parse SSE response"}
                else:
                    return {"error": "No data in SSE response"}
            else:
                result = await response.json()
                print(f"JSON response: {json.dumps(result, indent=2)}")
                return result


async def test_mcp_connection():
    """Test the MCP server connection."""
    print("Testing MCP server connection...")

    try:
        async with MCPClient() as client:
            # Step 1: Initialize session
            print("\n1. Initializing session...")
            init_result = await client.initialize_session()

            # Step 2: Send initialized notification (required by MCP protocol)
            print("\n2. Sending initialized notification...")
            await client.send_initialized()

            # Step 3: List available tools
            print("\n3. Listing tools...")
            tools_result = await client.list_tools()

            if tools_result.get("result"):
                tools = tools_result["result"].get("tools", [])
                print(f"Found {len(tools)} available tools")
                for tool in tools[:3]:  # Show first 3 tools
                    print(f"  - {tool.get('name')}: {tool.get('description', '')[:100]}...")
            else:
                print(f"Error listing tools: {tools_result}")

            # Step 4: Test a simple tool call (get databases)
            print("\n4. Testing tool call (get_metabase_databases)...")
            db_result = await client.call_tool("get_metabase_databases")
            if db_result.get("result"):
                print("✅ Successfully connected to Metabase database!")
                print(f"Found databases: {len(db_result['result'].get('data', []))}")
            else:
                print(f"Error calling tool: {db_result}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = asyncio.run(test_mcp_connection())
    if success:
        print("\n✅ MCP server test completed successfully!")
    else:
        print("\n❌ MCP server test failed!")
