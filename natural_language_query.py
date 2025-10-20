#!/usr/bin/env python3
"""
Natural Language Query Interface for Metabase MCP Server

This script demonstrates how to connect to your Metabase MCP server
and make natural language queries to your database.
"""

import asyncio
import json
import aiohttp
from typing import Dict, Any, List


class MetabaseMCPClient:
    """Client for interacting with Metabase MCP Server."""

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

    async def initialize(self) -> Dict[str, Any]:
        """Initialize the MCP session."""
        payload = {
            "jsonrpc": "2.0",
            "id": "init",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "metabase-query-client",
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
            if response.content_type == "text/event-stream":
                text_content = await response.text()
                lines = text_content.strip().split('\n')
                data_lines = [line for line in lines if line.startswith('data: ')]
                if data_lines:
                    result = json.loads(data_lines[0][6:])

                    # Extract session ID from headers
                    if 'mcp-session-id' in response.headers:
                        self.session_id = response.headers['mcp-session-id']
                        print(f"✅ Connected! Session ID: {self.session_id}")

                    return result
            else:
                return await response.json()

    async def send_initialized(self) -> None:
        """Send the initialized notification."""
        if not self.session_id:
            print("❌ No session ID available")
            return

        payload = {
            "jsonrpc": "2.0",
            "method": "initialized",
            "params": {}
        }

        async with self.http_session.post(
            self.server_url,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "mcp-session-id": self.session_id
            }
        ) as response:
            print(f"✅ Initialized (status: {response.status})")

    async def get_databases(self) -> List[Dict[str, Any]]:
        """Get list of available databases."""
        if not self.session_id:
            print("❌ No session ID available")
            return []

        payload = {
            "jsonrpc": "2.0",
            "id": "get-databases",
            "method": "tools/call",
            "params": {
                "name": "get_metabase_databases",
                "arguments": {}
            }
        }

        async with self.http_session.post(
            self.server_url,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "mcp-session-id": self.session_id
            }
        ) as response:
            if response.content_type == "text/event-stream":
                text_content = await response.text()
                lines = text_content.strip().split('\n')
                data_lines = [line for line in lines if line.startswith('data: ')]
                if data_lines:
                    result = json.loads(data_lines[0][6:])
                    if "result" in result:
                        return result["result"].get("data", [])
            else:
                result = await response.json()
                if "result" in result:
                    return result["result"].get("data", [])

        return []

    async def execute_sql_query(self, database_id: int, query: str) -> Dict[str, Any]:
        """Execute a SQL query on a specific database."""
        if not self.session_id:
            return {"error": "No session ID available"}

        payload = {
            "jsonrpc": "2.0",
            "id": "execute-sql",
            "method": "tools/call",
            "params": {
                "name": "execute_sql_query",
                "arguments": {
                    "database_id": database_id,
                    "query": query
                }
            }
        }

        async with self.http_session.post(
            self.server_url,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "mcp-session-id": self.session_id
            }
        ) as response:
            if response.content_type == "text/event-stream":
                text_content = await response.text()
                lines = text_content.strip().split('\n')
                data_lines = [line for line in lines if line.startswith('data: ')]
                if data_lines:
                    result = json.loads(data_lines[0][6:])
                    return result
            else:
                return await response.json()

        return {"error": "Failed to execute query"}


async def natural_language_query_demo():
    """Demonstrate natural language queries to your database."""
    print("🗃️  Metabase MCP Server - Natural Language Query Demo")
    print("=" * 60)

    try:
        async with MetabaseMCPClient() as client:
            # Step 1: Initialize connection
            print("🔌 Connecting to Metabase MCP Server...")
            init_result = await client.initialize()

            if "error" in init_result:
                print(f"❌ Connection failed: {init_result['error']}")
                return

            print("✅ Connected successfully!")

            # Step 2: Send initialized notification
            await client.send_initialized()

            # Step 3: Get available databases
            print("\n📊 Getting available databases...")
            databases = await client.get_databases()

            if not databases:
                print("❌ No databases found or connection issue")
                return

            print(f"✅ Found {len(databases)} databases:")
            for db in databases:
                print(f"  • {db.get('name', 'Unknown')} (ID: {db.get('id')})")

            # Step 4: Demonstrate natural language queries
            if databases:
                # Use the first database for demo
                db_id = databases[0]["id"]
                db_name = databases[0]["name"]

                print(f"\n🔍 Demonstrating queries on '{db_name}' (ID: {db_id})")
                print("-" * 50)

                # Example queries
                queries = [
                    "SELECT COUNT(*) as total_records FROM users;",
                    "SELECT name, email FROM users WHERE created_at > '2024-01-01' LIMIT 5;",
                    "SELECT department, COUNT(*) as employee_count FROM employees GROUP BY department ORDER BY employee_count DESC;"
                ]

                for i, query in enumerate(queries, 1):
                    print(f"\n📋 Query {i}: {query[:50]}...")
                    result = await client.execute_sql_query(db_id, query)

                    if "result" in result:
                        data = result["result"].get("data", [])
                        print(f"   ✅ Success! Returned {len(data)} rows")
                        if data:
                            # Show first few columns of first row
                            first_row = data[0]
                            columns = list(first_row.keys())[:3]  # First 3 columns
                            values = [str(first_row.get(col, 'NULL')) for col in columns]
                            print(f"   📊 Sample: {dict(zip(columns, values))}")
                    else:
                        print(f"   ❌ Query failed: {result.get('error', 'Unknown error')}")

                print("\n🎉 Demo completed! Your Metabase MCP server is ready for natural language queries!")
                print("💡 You can now use this client to query your databases in natural language.")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("🚀 Starting Metabase MCP Natural Language Query Demo...")
    asyncio.run(natural_language_query_demo())
