#!/bin/bash

# Test authentication middleware for Metabase MCP Server
# This script tests that authentication is properly enforced

echo "🧪 Testing Metabase MCP Server Authentication"
echo "=============================================="
echo ""

# Wait for server to be ready
sleep 2

# Test 1: Request without Authorization header
echo "Test 1: Request WITHOUT Authorization header (should FAIL with 401)"
echo "-------------------------------------------------------------------"
curl -s -X POST http://127.0.0.1:3200/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -w "\nHTTP Status: %{http_code}\n" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize"}' 
echo ""
echo ""

# Test 2: Request with INVALID token  
echo "Test 2: Request with INVALID token (should FAIL with 401)"
echo "-----------------------------------------------------------"
curl -s -X POST http://127.0.0.1:3200/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer invalid-token-test-12345" \
  -w "\nHTTP Status: %{http_code}\n" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize"}'
echo ""
echo ""

# Test 3: Request with VALID cursor token
echo "Test 3: Request with VALID cursor token (should SUCCEED with 200)"
echo "------------------------------------------------------------------"
curl -s -X POST http://127.0.0.1:3200/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer dJFIvjGRtV0sOpRM7bAtLeqdXB2wJqzQaOXj1g1PGwolzS1kg8rFDmyWg3grSeJi" \
  -w "\nHTTP Status: %{http_code}\n" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize"}'
echo ""
echo ""

# Test 4: Request with VALID slackbot token
echo "Test 4: Request with VALID slackbot token (should SUCCEED with 200)"
echo "--------------------------------------------------------------------"
curl -s -X POST http://127.0.0.1:3200/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer qjvjgxuCvZjQCO0PtW3RPjd0SZT2dACYhHWDfhIrBv2k5jM5oxG4uhDXjLyjr8B1" \
  -w "\nHTTP Status: %{http_code}\n" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize"}'
echo ""
echo ""

echo "=============================================="
echo "✅ Test complete! Check results above."
echo "Expected: Tests 1 & 2 should return 401"
echo "          Tests 3 & 4 should return 200"

