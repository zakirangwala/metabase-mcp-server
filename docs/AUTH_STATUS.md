# Authentication Status

## Current State

✅ **Configuration System**: COMPLETE
- Environment variable parsing for auth tokens
- Token format: `client_id=token|scope1,scope2`
- Support for multiple tokens
- Support for required scopes  
- Configuration validation

⚠️ **Middleware Injection**: NOT IMPLEMENTED
- FastMCP doesn't expose easy hooks for middleware injection
- Attempted multiple approaches (monkey-patching, ASGI wrappers, etc.)
- All approaches failed due to FastMCP's internal structure

## What Works

1. **Token Configuration** via `.env`:
```bash
METABASE_MCP_AUTH_MODE=static-token
METABASE_MCP_AUTH_TOKENS=cursor=token123|read,write,slackbot=token456|read,write,admin
METABASE_MCP_REQUIRED_SCOPES=read,write
```

2. **Server Starts** with warnings:
```
⚠️  Static-token authentication is configured but middleware injection is not yet implemented
⚠️  For production HTTP deployments, use a reverse proxy for authentication
Configured client tokens (for documentation): ['cursor', 'slackbot']
Required scopes (for documentation): ['read', 'write']
```

3. **Tokens are parsed and validated** during startup

## What Doesn't Work

❌ **Runtime Authentication Enforcement**
- Tokens are NOT validated on incoming requests
- Any client can connect without a token
- The server accepts all requests regardless of the Authorization header

## Recommended Solutions

### Option 1: Reverse Proxy (RECOMMENDED for Production)

Use nginx, Cloudflare, API Gateway, or similar to handle authentication:

**Nginx Example:**
```nginx
location /mcp {
    # Validate Bearer token
    if ($http_authorization != "Bearer super-secret-token") {
        return 401;
    }
    proxy_pass http://localhost:3200;
}
```

**Cloudflare Workers Example:**
```javascript
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const auth = request.headers.get('Authorization')
  const validTokens = ['Bearer token123', 'Bearer token456']
  
  if (!validTokens.includes(auth)) {
    return new Response('Unauthorized', { status: 401 })
  }
  
  return fetch('http://your-mcp-server:3200' + new URL(request.url).pathname, request)
}
```

### Option 2: Development Mode

For local development, set:
```bash
METABASE_MCP_AUTH_MODE=none
METABASE_MCP_ALLOW_UNAUTHENTICATED_HTTP=true
```

This explicitly acknowledges that auth is disabled.

### Option 3: Future Implementation

To implement authentication middleware properly, we would need to:

1. **Fork FastMCP** or submit a PR to add middleware support
2. **Use a different framework** (FastAPI, Starlette directly, etc.)
3. **Wait for FastMCP** to expose proper middleware hooks

## Current `.env` Recommendation

For development:
```bash
# Metabase connection
METABASE_URL=http://127.0.0.1:12345
METABASE_API_KEY="mb_zr4tCQeBUjWg4X4OGTcrYfKD2xr9ZLus#NQbosUCRP8="

# MCP transport
HOST=localhost
PORT=3200
TRANSPORT=streamable-http
LOG_LEVEL=INFO

# Auth - set to 'none' for development (auth handled by reverse proxy in production)
METABASE_MCP_AUTH_MODE=none
METABASE_MCP_ALLOW_UNAUTHENTICATED_HTTP=true
```

For production (with reverse proxy):
```bash
# Same as above, but document the tokens for the reverse proxy:
METABASE_MCP_AUTH_MODE=none  # Auth handled by nginx/cloudflare/etc
METABASE_MCP_ALLOW_UNAUTHENTICATED_HTTP=true  # MCP server trusts reverse proxy
# METABASE_MCP_AUTH_TOKENS=cursor=xxx,slackbot=yyy  # For documentation only
```

## Testing

The server runs and accepts connections, but does NOT enforce authentication. This was confirmed by:
1. Server starts with token configuration
2. No authentication logs appear for requests
3. curl requests with invalid/missing tokens succeed (they shouldn't)

## Next Steps

1. **Short term**: Document that authentication must be handled by reverse proxy
2. **Medium term**: Investigate FastMCP source to find proper middleware hooks
3. **Long term**: Consider migrating to FastAPI with custom MCP implementation

┌─────────────┐
│   Client    │
│ (Cursor/    │
│  Slackbot)  │
└──────┬──────┘
       │ Bearer token
       ↓
┌─────────────────────┐
│  AWS API Gateway    │
│  Lambda Authorizer  │◄── Validates token here
└──────┬──────────────┘
       │ Authorized requests only
       ↓
┌─────────────────────┐
│   Private Subnet    │
│                     │
│  ┌───────────────┐  │
│  │  MCP Server   │  │◄── Doesn't need to validate
│  │  (port 3200)  │  │    (already trusted)
│  └───────────────┘  │
└─────────────────────┘