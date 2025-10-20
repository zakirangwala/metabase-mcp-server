#!/usr/bin/env python3
"""
Complete MCP stdio test that follows the proper protocol sequence.
"""

import json
import sys
import time
import subprocess
import threading
import queue


def run_server():
    """Run the MCP server in a separate process."""
    return subprocess.Popen(
        ['python', 'src/metabase_mcp_server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )


def send_message(process, message):
    """Send a JSON-RPC message to the server process."""
    json_str = json.dumps(message) + '\n'
    process.stdin.write(json_str)
    process.stdin.flush()
    print(f"Sent: {json_str.strip()}")


def read_response(process):
    """Read a response from the server process."""
    try:
        line = process.stdout.readline().strip()
        if line:
            response = json.loads(line)
            print(f"Received: {line}")
            return response
    except (json.JSONDecodeError, EOFError):
        pass
    return None


def test_complete_mcp_protocol():
    """Test the complete MCP protocol sequence."""
    print("🚀 Starting complete MCP protocol test...", flush=True)

    # Start the server
    server_process = run_server()

    try:
        # Step 1: Send initialize
        print("1️⃣ Sending initialize...", flush=True)
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
        send_message(server_process, init_msg)

        # Read initialization response
        init_response = read_response(server_process)
        if not init_response or "error" in init_response:
            print("❌ Initialization failed", flush=True)
            return False

        print("✅ Initialize response received", flush=True)

        # Step 2: Send initialized notification
        print("2️⃣ Sending initialized notification...", flush=True)
        initialized_msg = {
            "jsonrpc": "2.0",
            "method": "initialized",
            "params": {}
        }
        send_message(server_process, initialized_msg)

        # Give the server a moment to process
        time.sleep(0.1)

        # Step 3: List tools
        print("3️⃣ Listing tools...", flush=True)
        tools_msg = {
            "jsonrpc": "2.0",
            "id": "tools-list",
            "method": "tools/list",
            "params": {}
        }
        send_message(server_process, tools_msg)

        # Read tools response
        tools_response = read_response(server_process)
        if not tools_response or "error" in tools_response:
            print("❌ Tools listing failed", flush=True)
            return False

        # Check if we got tools
        if "result" in tools_response:
            tools = tools_response["result"].get("tools", [])
            print(f"✅ Found {len(tools)} tools!", flush=True)
            for tool in tools[:5]:  # Show first 5 tools
                print(f"  - {tool.get('name')}: {tool.get('description', '')[:80]}...", flush=True)
        else:
            print("❌ No tools in response", flush=True)
            return False

        # Step 4: Call a tool
        print("4️⃣ Calling get_metabase_databases...", flush=True)
        call_msg = {
            "jsonrpc": "2.0",
            "id": "tool-call",
            "method": "tools/call",
            "params": {
                "name": "get_metabase_databases",
                "arguments": {}
            }
        }
        send_message(server_process, call_msg)

        # Read tool call response
        call_response = read_response(server_process)
        if not call_response or "error" in call_response:
            print("❌ Tool call failed", flush=True)
            return False

        if "result" in call_response:
            data = call_response["result"].get("data", [])
            print(f"✅ Tool call successful! Found {len(data)} databases", flush=True)

            # Show some database info
            for db in data[:3]:
                print(f"  📊 {db.get('name', 'Unknown')} (ID: {db.get('id', 'Unknown')})", flush=True)

            return True
        else:
            print("❌ Tool call returned no result", flush=True)
            return False

    finally:
        # Clean up
        server_process.terminate()
        server_process.wait()


if __name__ == "__main__":
    success = test_complete_mcp_protocol()
    if success:
        print("🎉 All tests passed! Your Metabase MCP server is working perfectly!", flush=True)
    else:
        print("💥 Tests failed!", flush=True)
        sys.exit(1)
