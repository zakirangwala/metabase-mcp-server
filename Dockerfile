FROM ghcr.io/astral-sh/uv:debian-slim AS builder

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Sync dependencies and compile bytecode
RUN uv sync --compile-bytecode

# Expose port
EXPOSE 3200

# Run the app (host/port controlled via environment or CLI)
CMD ["uv", "run", "src/metabase_mcp_server.py"]
