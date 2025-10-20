#!/usr/bin/env python3
"""
Simple synchronous stdio test for Metabase MCP Server.
"""

import json
import sys
import time


def send_message(message):
    """Send a JSON-RPC message to the server."""
    json_str = json.dumps(message)
    print(json_str, flush=True)


def read_response():
    """Read a response from the server."""
    try:
        line = sys.stdin.readline().strip()
        if line:
            return json.loads(line)
    except (json.JSONDecodeError, EOFError):
        pass
    return None


def test_stdio_connection():
    """Test the MCP server connection via stdio."""
    print("Testing MCP server connection via stdio...", flush=True)

    # Step 1: Initialize
    print("1. Sending initialize...", flush=True)
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
    send_message(init_msg)

    # Read initialization response
    init_response = read_response()
    print(f"Init response: {json.dumps(init_response, indent=2)}", flush=True)

    if not init_response or "error" in init_response:
        print("❌ Initialization failed", flush=True)
        return False

    # Step 2: Send initialized notification
    print("2. Sending initialized...", flush=True)
    initialized_msg = {
        "jsonrpc": "2.0",
        "method": "initialized",
        "params": {}
    }
    send_message(initialized_msg)

    # Step 3: List tools
    print("3. Listing tools...", flush=True)
    tools_msg = {
        "jsonrpc": "2.0",
        "id": "tools-list",
        "method": "tools/list",
        "params": {}
    }
    send_message(tools_msg)

    # Read tools response
    tools_response = read_response()
    print(f"Tools response: {json.dumps(tools_response, indent=2)}", flush=True)

    if not tools_response or "error" in tools_response:
        print("❌ Tools listing failed", flush=True)
        return False

    # Check if we got tools
    if "result" in tools_response:
        tools = tools_response["result"].get("tools", [])
        print(f"✅ Found {len(tools)} tools!", flush=True)
        for tool in tools[:3]:
            print(f"  - {tool.get('name')}: {tool.get('description', '')[:100]}...", flush=True)
    else:
        print("❌ No tools in response", flush=True)
        return False

    # Step 4: Call a tool
    print("4. Calling get_metabase_databases...", flush=True)
    call_msg = {
        "jsonrpc": "2.0",
        "id": "tool-call",
        "method": "tools/call",
        "params": {
            "name": "get_metabase_databases",
            "arguments": {}
        }
    }
    send_message(call_msg)

    # Read tool call response
    call_response = read_response()
    print(f"Call response: {json.dumps(call_response, indent=2)}", flush=True)

    if not call_response or "error" in call_response:
        print("❌ Tool call failed", flush=True)
        return False

    if "result" in call_response:
        data = call_response["result"].get("data", [])
        print(f"✅ Tool call successful! Found {len(data)} databases", flush=True)
        return True
    else:
        print("❌ Tool call returned no result", flush=True)
        return False


if __name__ == "__main__":
    success = test_stdio_connection()
    if success:
        print("✅ All tests passed!", flush=True)
    else:
        print("❌ Tests failed!", flush=True)
        sys.exit(1)
