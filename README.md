# 📊 Metabase MCP Server

## 📚 Table of Contents

1. [What is this tool about?](#-what-is-this-tool-about)
2. [Video Walkthrough](#-video-walkthrough)
3. [Architecture Diagram](#-architecture-diagram)
4. [Getting Started](#-getting-started)
   - [Set Up Metabase](#1-set-up-metabase-if-you-havent-already)
   - [Install uv Package Manager](#2-install-uv-package-manager)
   - [Clone or Download the Repository](#3-clone-or-download-the-repository)
   - [Install dependencies](#4-install-dependencies)
   - [Configure Your Credentials](#5-configure-your-credentials)
   - [Connect to Your MCP client](#6-connect-to-your-mcp-client)
5. [Configuration Options](#-configuration-options)
6. [Getting Your Metabase API Key](#-getting-your-metabase-api-key)
7. [DXT File Support](#-dxt-file-support)
8. [How to Create Your Own DXT File](#how-to-create-your-own-dxt-file)
9. [Remote Deployment](#-remote-deployment)
10. [Debugging with MCP Inspector](#-debugging-with-mcp-inspector)
11. [Available Tools](#-available-tools)
12. [Example Prompts to Try](#-example-prompts-to-try)
13. [Connect with Us](#-connect-with-us)
14. [License](#-license)

---

## 😊 What is this tool about?

**Metabase MCP Server** is a backend integration layer that connects your **Metabase** instance with **AI assistants** using the **Model Context Protocol (MCP)**. This allows business leaders, product managers and analysts to interact with business intelligence assets like dashboards and charts using **natural language**—through any MCP client (e.g., Claude Desktop).

Instead of navigating through menus or constructing SQL queries manually, you can:

- You can ask a question and get an instant insight.
- Generate dashboards and charts by describing what you want.
- Manage user access and database connections through simple instructions.

This project makes Metabase not just a dashboarding tool—but a conversational, intelligent business assistant.

---

## 🎥 Video Walkthrough

Watch this video to see the Metabase MCP Server in action:

[<img src="https://i.ytimg.com/vi/1-86KuNwbdE/maxresdefault.jpg">](https://youtu.be/1-86KuNwbdE?feature=shared")

---

## 📐 Architecture Diagram

![Architecture Diagram](./assets/architecture_diagram.png)

---

## 🚀 Getting Started

### 1. Set Up Metabase (If you haven't already)

Follow the official Metabase installation guide: [Metabase Docs](https://www.metabase.com/docs/latest/installation-and-operation/installing-metabase)

### 2. Install uv Package Manager

Install `uv` which includes Python and package management:

**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or install via package managers:
```bash
# macOS
brew install uv

# Windows (via Scoop)
scoop install uv

# Windows (via Chocolatey)
choco install uv
```
For more information about uv installation and usage, please visit the official documentation: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

### 3. Clone or Download the Repository

You need to get this tool onto your computer. You can either download it manually or use Git.
Open your computer's Terminal (Mac) or Command Prompt (Windows).
Navigate to the folder where you unzipped the files or want to clone the project:

```bash
# Example (replace with your actual path):
cd ~/Downloads/metabase-mcp-server-dev
```

**Option 1: Download ZIP**

1.  Go to the [GitHub repository](https://github.com/codewalnut/metabase-mcp-server)
    
2.  Click the green **"Code"** button
    
3.  Select **"Download ZIP"**
    
4.  Unzip the downloaded file to a location like your **Documents** folder
    

**Option 2: Use Git** If you're familiar with Git, run this in your terminal:

```bash
git clone https://github.com/codewalnut/metabase-mcp-server.git
cd metabase-mcp-server

```

### 4. Install dependencies

This command will automatically:
- Install the required Python version (if not already available)
- Create a virtual environment for the project
- Install all necessary packages and dependencies


```bash
uv sync
```
### 5. Configure Your Credentials

You have three options to configure your Metabase credentials for the MCP Server:

**Option 1: Using a `.env` file (Recommended)**
Create a `.env` file in the project root:
```env
METABASE_URL=http://localhost:3000
METABASE_API_KEY=mb_xxx_your_key
HOST=localhost
PORT=3200
TRANSPORT=streamable-http
LOG_LEVEL=INFO
METABASE_MCP_AUTH_MODE=static-token
METABASE_MCP_AUTH_TOKENS=slack-bot=super-secret-token
# Optional: comma or newline separated scopes that every token must include
METABASE_MCP_REQUIRED_SCOPES=read,write
# Leave unset unless you intentionally want raw SQL in logs
METABASE_MCP_LOG_SQL_QUERIES=false
```

**Option 2: Using command-line arguments**
Pass configuration directly via command line:
```bash
 uv run src/metabase_mcp_server.py \
   --metabase-url http://localhost:3000 \
   --metabase-api-key "YOUR_API_KEY" \
   --transport streamable-http \
   --host 0.0.0.0 \
   --port 3200 \
   --auth-mode static-token \
   --auth-token slack-bot=super-secret-token \
   --required-scope read \
   --log-level INFO
```

**Option 3: Using environment variables in MCP client config**
Configure directly in your MCP client without a `.env` file (see examples below).

```json
{
  "mcpServers": {
    "metabase": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "C:\\\\Users\\\\YourName\\\\Projects\\\\metabase-mcp-server\\\\src\\\\metabase_mcp_server.py"],
      "env": {
        "METABASE_URL": "http://localhost:3000",
        "METABASE_API_KEY": "mb_xxx_your_key",
        "HOST": "localhost",
        "PORT": "3200",
        "TRANSPORT": "streamable-http",
        "LOG_LEVEL": "INFO",
        "METABASE_MCP_AUTH_MODE": "static-token",
        "METABASE_MCP_AUTH_TOKENS": "slack-bot=super-secret-token",
        "METABASE_MCP_REQUIRED_SCOPES": "read"
      }
    }
  }
}
```
### 6. Connect to Your MCP client

Choose your preferred MCP clients like Claude Desktop app, Claude Code, Cursor, Windsurf etc., and add the Metabase MCP server in their respective configuration files. All MCP clients follow a similar configuration pattern.

#### Configuration Examples

**For stdio transport (recommended for local MCP server):**

Windows:
```json
{
  "mcpServers": {
    "metabase": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "C:\\Users\\YourName\\Projects\\metabase-mcp-server\\src\\metabase_mcp_server.py""]
    }
  }
}
```

Mac:
```json
{
  "mcpServers": {
    "metabase": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "/Users/YourName/Projects/metabase-mcp-server/src/metabase_mcp_server.py"]
    }
  }
}
```

##### Key Differences:
- Windows uses **backslashes** `\\` in paths
- macOS/Linux uses **forward slashes** `/` in paths
- Make sure to match the correct format based on your OS to avoid errors


##### Important Notes:
- Replace `FULL_PATH` with the actual absolute path to your project directory
- After saving configuration changes, **restart your MCP client** to apply the new settings
- For project-specific tools in Cursor, create a `.cursor/mcp.json` file in your project directory
- For global tools in Cursor, create a `~/.cursor/mcp.json` file in your home directory

**For streamable-http transport (recommended for remote MCP server):**
```json
{
  "mcpServers": {
    "metabase": {
      "type": "streamable-http",
      "url": "http://localhost:3200/mcp/"
    }
  }
}
```

#### Compatible MCP clients

Click on any client to visit their official MCP setup documentation:

| Client | Official MCP Documentation |
|--------|----------------------------|
| [![Claude Desktop](https://img.shields.io/badge/Claude-Desktop-orange?style=for-the-badge&logo=anthropic)](https://support.anthropic.com/en/articles/10949351-getting-started-with-model-context-protocol-mcp-on-claude-for-desktop) | Anthropic's official MCP guide for Claude Desktop |
| [![Claude Code](https://img.shields.io/badge/Claude-Code-orange?style=for-the-badge&logo=anthropic)](https://docs.anthropic.com/en/docs/claude-code/mcp) | Official Claude Code MCP setup documentation |
| [![Cursor](https://img.shields.io/badge/Cursor-AI_Code_Editor-blue?style=for-the-badge&logo=cursor)](https://docs.cursor.com/context/model-context-protocol#configuring-mcp-servers) | Cursor's official MCP configuration guide |
| [![Windsurf](https://img.shields.io/badge/Windsurf-Codeium-green?style=for-the-badge&logo=codeium)](https://docs.windsurf.com/windsurf/mcp) | Windsurf official MCP setup documentation |
| [![Cline](https://img.shields.io/badge/Cline-VS_Code_Extension-purple?style=for-the-badge&logo=visualstudiocode)](https://docs.cline.bot/mcp-servers/mcp-quickstart) | Cline's official MCP quickstart guide |
| [![VS Code](https://img.shields.io/badge/VS_Code-Copilot-blue?style=for-the-badge&logo=visualstudiocode)](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_add-an-mcp-server-to-your-workspace) | VS Code Copilot MCP server configuration |


Once you have added the configuration, the MCP server should be visible in your MCP client.

---

## 🔧 Configuration Options

The Metabase MCP Server supports flexible configuration through environment variables, command-line arguments, or a combination of both.

### Environment Variables

| Variable | Description | Default Value | Example |
|----------|-------------|---------------|---------|
| `METABASE_URL` | Your Metabase instance URL | Required | `http://127.0.0.1:3000` |
| `METABASE_API_KEY` | Your Metabase API key | Required | `mb_xxx_your_api_key` |
| `TRANSPORT` | Transport protocol | `stdio` | `stdio`, `streamable-http` |
| `HOST` | Host for HTTP transports | `localhost` | `0.0.0.0`, `127.0.0.1` |
| `PORT` | Port for HTTP transports | `3200` | `8080`, `9000` |
| `LOG_LEVEL` | Logging level | `INFO` | `DEBUG`, `WARNING`, `ERROR` |
| `METABASE_MCP_AUTH_MODE` | Authentication strategy (`static-token` recommended for HTTP) | `none` (stdio) / `static-token` (HTTP) | `static-token` |
| `METABASE_MCP_AUTH_TOKENS` | Comma/newline separated static tokens (`client=token` format) | _(empty)_ | `slack-bot=super-secret-token` |
| `METABASE_MCP_AUTH_TOKEN_FILE` | Path to file containing one token entry per line | _(empty)_ | `/run/secrets/metabase_mcp_tokens` |
| `METABASE_MCP_REQUIRED_SCOPES` | Comma/newline separated scopes each token must include | _(empty)_ | `read,write` |
| `METABASE_MCP_ALLOW_UNAUTHENTICATED_HTTP` | Opt-in toggle to run HTTP without auth (not recommended) | `false` | `true` |
| `METABASE_MCP_LOG_SQL_QUERIES` | Enable DEBUG logging of raw SQL text | `false` | `true` |

### Command-line Arguments

| Argument | Description | Default Value |
|----------|-------------|---------------|
| `--metabase-url` | Metabase instance URL | Required |
| `--metabase-api-key` | Metabase API key | Required |
| `--transport` | Transport protocol | `stdio` |
| `--host` | Host for HTTP transports | `localhost` |
| `--port` | Port for HTTP transports | `3200` |
| `--log-level` | Logging verbosity level | `INFO` |
| `--auth-mode` | Authentication strategy (`static-token` or `none`) | `none` (stdio) / `static-token` (HTTP) |
| `--auth-token` | Register a shared bearer token (repeatable, format `client=token`) | _(empty)_ |
| `--auth-token-file` | Load bearer tokens from a file | _(empty)_ |
| `--required-scope` | Declare scopes that every token must include | _(empty)_ |
| `--allow-unauthenticated-http` | Explicitly allow HTTP without auth | `false` |
| `--log-sql-queries` | Emit raw SQL at DEBUG level | `false` |

### Transport Protocols

| Protocol | Description | Use Case |
|----------|-------------|----------|
| **stdio** | Standard input/output communication | Best for local integrations (Claude Desktop, Cursor, etc.) |
| **streamable-http** | HTTP-based streaming protocol | Ideal for remote deployments and web-based integrations |
| **sse** | Server-Sent Events over HTTP | ⚠️ **Deprecated - Not recommended for new setups** |

### Configuration Priority

Configuration values are applied in the following priority order (highest to lowest):
1. **Command-line arguments** (overrides everything)
2. **Environment variables** (overrides defaults)
3. **Default values**

### Complete Command Examples

```bash
uv run src/metabase_mcp_server.py --transport streamable-http --host localhost --port 3200 --metabase-url http://127.0.0.1:3000 --metabase-api-key mb_xxx_your_key

```

**Note:** You don't need to pass every parameter when running the server. However, you must provide the Metabase URL and API key. Any parameters not specified will use their default values as shown above.

---

## 🔐 Authentication & Authorization

Remote deployments **must** run with authentication enabled. The server ships with a hardened default that rejects unauthenticated HTTP calls unless you explicitly opt out.

- **Auth modes**
  - `static-token` (recommended): require callers to send `Authorization: Bearer <token>` headers. Define tokens via `METABASE_MCP_AUTH_TOKENS`, `METABASE_MCP_AUTH_TOKEN_FILE`, or repeated `--auth-token` flags.
  - `none`: only use this for local `stdio` transports or if you are terminating auth in a separate proxy. For HTTP transports you must also pass `--allow-unauthenticated-http`.
- **Token format:** `client_id=token|scope1,scope2`. The `client_id` is a friendly label used in logs. Scopes are optional metadata; when `METABASE_MCP_REQUIRED_SCOPES` / `--required-scope` is set, every token must declare those scopes.
- **Multiple tokens:** separate entries with commas/newlines or repeat `--auth-token`. You can store secrets in AWS Secrets Manager / SSM and mount them via `METABASE_MCP_AUTH_TOKEN_FILE`.
- **Slack & Cursor bots:** configure your integration to send the shared token in the `Authorization` header. Tokens are never logged; only the `client_id` appears in INFO logs.
- **Dangerous override:** `METABASE_MCP_ALLOW_UNAUTHENTICATED_HTTP=true` (or `--allow-unauthenticated-http`) disables auth checks—only enable inside an isolated VPC or during local debugging.
- **SQL logging:** `METABASE_MCP_LOG_SQL_QUERIES` / `--log-sql-queries` is disabled by default to avoid leaking sensitive literals. Turn it on only when debugging and remember to revert.

Pair authentication with TLS termination (ALB, API Gateway, Nginx, etc.) so bearer tokens and Metabase API keys never traverse the network in plaintext.

---


## 🔑 Getting Your Metabase API Key

To get your Metabase API key:

1. **Log into your Metabase instance**
2. **Click on your profile picture** (top-right corner)
3. **Select "Account settings"**
4. **Navigate to the "API Keys" tab**
5. **Click "Create API Key"**
6. **Give your key a descriptive name** (e.g., "MCP Server Key")
7. **Copy the generated key** (starts with `mb_`)

⚠️ **Important:** Store your API key securely and never commit it to version control. The key provides full access to your Metabase instance.

---

## 📂 DXT File Support

You no longer need to go through the steps of cloning the repository and setting up the environment. Simply follow the steps below to install the **Metabase MCP Server** in your **Cloude Desktop App**:

1. **Download the DXT File**  
   Check the link below to download the latest **DXT file** directly:  
   [Download DXT File](./metabase-mcp-server.dxt)

2. **Open the Cloude Desktop App**  
   Once you have the file, open the **Cloude Desktop App** on your system.

3. **Navigate to Extensions Settings**  
   In the **Cloude Desktop App**:  
   - Go to **Files** → **Settings** → **Extensions**  
   - Then click on **Advanced Settings**.

4. **Select the DXT File**  
   In the **Advanced Settings** section, click on **Choose File**, select the downloaded **DXT file**.

5. **Enter the Required Details**  
   After slecting the **DXT file**, a prompt will appear asking you to fill in the required details:  
   - **Metabase URL**: Enter your Metabase server URL.  
   - **API Key**: Add the relevant API key for authentication.

6. **Complete the Setup**  
   After entering the necessary details, click **Save** to apply the configuration.

That's it! The **Metabase MCP Server** is now installed and ready to use in your **Cloude Desktop App**.

## How to Create Your Own DXT File

If you want to create your own **DXT file**, please visit the Official Guide:  
[Creating Your Own DXT File](https://www.anthropic.com/engineering/desktop-extensions)

## 🚀 Remote Deployment

For production use or team collaboration, you can deploy the Metabase MCP Server remotely. We use this approach internally at Codewalnut.


### Docker Deployment

We've included Docker configuration files to make remote deployment straightforward.

#### Quick Start with Docker
```bash
# Build the Docker image
docker build -t metabase-mcp-server .

# Run with environment variables
docker run -d \
  -p 3200:3200 \
  -e TRANSPORT="streamable-http" \
  -e HOST="0.0.0.0" \
  -e PORT="3200" \
  -e METABASE_URL="https://your-metabase-instance.com" \
  -e METABASE_API_KEY="mb_xxx_your_api_key" \
  -e METABASE_MCP_AUTH_MODE="static-token" \
  -e METABASE_MCP_AUTH_TOKENS="slack-bot=super-secret-token,analytics-bot=another-token" \
  metabase-mcp-server
```

#### Docker Compose (Recommended)
```yaml
version: '3.8'
services:
  metabase-mcp:
    build: .
    ports:
      - "3200:3200"
    environment:
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=3200
      - METABASE_URL=https://your-metabase-instance.com
      - METABASE_API_KEY=mb_xxx_your_api_key
      - METABASE_MCP_AUTH_MODE=static-token
      # Store tokens in an external secret and mount as a file in production
      - METABASE_MCP_AUTH_TOKEN_FILE=/run/secrets/metabase_mcp_tokens
      #- METABASE_MCP_REQUIRED_SCOPES=read,write
      #- METABASE_MCP_LOG_SQL_QUERIES=false
    restart: unless-stopped
    secrets:
      - metabase_mcp_tokens
secrets:
  metabase_mcp_tokens:
    file: ./secrets/metabase_mcp_tokens
```

Create `./secrets/metabase_mcp_tokens` with one entry per line in the form `client_id=token|scope1,scope2`. Mount it from AWS Secrets Manager / Parameter Store in production.

#### Connecting to Remote MCP Server

Once deployed, configure your MCP clients to connect to the remote server:

```json
{
  "mcpServers": {
    "metabase": {
      "type": "streamable-http",
      "url": "https://metabase-mcp.yourdomain.com/mcp/"
    }
  }
}
```

### Deployment Options
- **Cloud Providers:** AWS ECS, Google Cloud Run, Azure Container Instances
- **VPS/Dedicated Servers:** DigitalOcean, Linode, Vultr
- **Container Platforms:** Kubernetes, Docker Swarm
- **Platform-as-a-Service:** Railway, Render, Fly.io

### Security Considerations
- Terminate TLS (ALB, Nginx, API Gateway) and expose only HTTPS endpoints
- Keep `METABASE_MCP_AUTH_MODE=static-token` for all HTTP deployments; rotate tokens regularly
- Inject secrets via Docker/Compose/SSM rather than hardcoding them in images
- Restrict inbound traffic with security groups / firewalls and prefer private subnets or VPN access
- Monitor access logs and Metabase audit logs for anomalous behaviour
- Rotate Metabase API keys and static bearer tokens on a schedule

### Need Help with Deployment?
Our team at CodeWalnut offers deployment and consulting services. [Contact us](#-connect-with-us) for enterprise-grade setup and support.

---

## 🔍 Debugging with MCP Inspector

To debug and test your Metabase MCP Server setup, you can use the official MCP Inspector tool.

### Prerequisites
First, install Node.js if you haven't already:
- **Download from:** [nodejs.org](https://nodejs.org/en/download)
- **Or install via package manager:**
  ```bash
  # macOS
  brew install node
  
  # Windows (via Chocolatey)
  choco install nodejs
  
  # Windows (via Scoop)
  scoop install nodejs
  ```

### Install and Run MCP Inspector
```bash
# Install MCP Inspector globally
npm install -g @modelcontextprotocol/inspector

# Run the inspector with your Metabase MCP Server
npx @modelcontextprotocol/inspector uv run FULL_PATH/metabase-mcp-server/src/metabase_mcp_server.py
```

### Using MCP Inspector
The MCP Inspector provides:
- **Real-time tool testing** - Execute MCP tools directly from the web interface
- **Request/Response monitoring** - See exactly what data is being sent and received
- **Error debugging** - Identify configuration or API issues quickly
- **Schema validation** - Verify that your tools are properly defined

Once running, open your browser to `http://localhost:5173` to access the inspector interface.

### Common Debugging Scenarios
- **Connection issues** - Verify your Metabase URL and API key
- **Permission errors** - Check if your API key has the required permissions

---

## 🔧 Available Tools

| Function                         | Description                                     |
|----------------------------------|-------------------------------------------------|
| **Collection Operations** ||
| `get_metabase_collection`     | Get a collection by ID                          |
| `create_metabase_collection`  | Create a new collection                         |
| `update_metabase_collection`  | Update collection metadata                      |
| `delete_metabase_collection`  | Delete a collection                             |
| **Chart (Card) Operations** ||
| `get_metabase_cards`          | List all charts                                 |
| `get_card_query_results`      | Get results from a chart query                  |
| `create_metabase_card`        | Create a new chart                              |
| `update_metabase_card`        | Update an existing chart                        |
| `delete_metabase_card`        | Delete a chart                                  |
| **Dashboard Operations** ||
| `get_metabase_dashboards`     | List all dashboards                             |
| `get_dashboard_by_id`         | Get a dashboard by ID                           |
| `get_dashboard_cards`         | Get cards in a dashboard                        |
| `get_dashboard_items`         | Get all dashboard items                         |
| `create_metabase_dashboard`   | Create a dashboard                              |
| `update_metabase_dashboard`   | Update a dashboard                              |
| `delete_metabase_dashboard`   | Delete a dashboard                              |
| `copy_metabase_dashboard`     | Create a copy of an existing dashboard          |
| **Database Operations** ||
| `get_metabase_databases`      | List databases                                  |
| `create_metabase_database`    | Create a new database connection                |
| `update_metabase_database`    | Update a database connection                    |
| `delete_metabase_database`    | Delete a database connection                    |
| **User Operations** ||
| `get_metabase_users`          | List all users                                  |
| `get_metabase_current_user`   | Get current user details                        |
| `create_metabase_user`        | Create a new user                               |
| `update_metabase_user`        | Update user info                                |
| `delete_metabase_user`        | Delete a user                                   |
| **Group Operations** ||
| `get_metabase_groups`         | List user groups                                |
| `create_metabase_group`       | Create a user group                             |
| `delete_metabase_group`       | Delete a user group                             |
| **SQL Operations** ||
| `execute_sql_query`           | Execute a native SQL query                      |

---

## 🧪 Example Prompts to Try

- Create a dashboard called 'Flight Overview' with a bar chart showing flights by destination city.
- Run SQL: `SELECT origin, destination, COUNT(*) FROM flights GROUP BY origin, destination LIMIT 10`.
- Create a card displaying total bookings last month grouped by region.
- Delete the chart named 'Abandoned Queries'.
- Update the dashboard 'Sales KPIs' to include a new revenue card.
- Show all users in the 'Admin' group.
- Create a new group called 'Finance Analysts'.
- Connect to a Supabase database and list all tables.


---

## 🌐 Connect with Us

Stay connected and get support through our community channels:

### 🏢 Official Links
- **🌍 Website:** [codewalnut.com](https://codewalnut.com)
- **📧 Email:** [nattu@codewalnut.com](mailto:nattu@codewalnut.com)
- **📖 Blogs:**
  - **insights:** [codewalnut.com/insights](https://www.codewalnut.com/insights)
  - **learn:** [codewalnut.com/learn](https://www.codewalnut.com/learn)

### 📱 Social Media
- **💼 LinkedIn:** [CodeWalnut](https://www.linkedin.com/company/codewalnut)
- **📺 YouTube:** [CodeWalnut Channel](https://www.youtube.com/@CodeWalnut)
- **🐦 Twitter/X:** [@codewalnut](https://x.com/codewalnut)
- **📷 Instagram:** [@codewalnut](https://www.instagram.com/teamwalnut_)

### 💬 Community Support
- **📧 Newsletter:** [Subscribe to CodeWalnut Newsletter](https://codewalnut.com/) (scroll down to find the email subscription option)
- **🐙 GitHub:** [codewalnut](https://github.com/CW-Codewalnut)

### 🤝 Professional Services
- **Consulting:** Custom Metabase integrations and AI solutions
- **Training:** MCP and business intelligence workshops
- **Support:** Enterprise-grade support and maintenance

📢 **Follow us for updates on new MCP servers, AI integrations, and business intelligence tools!**

---

## 📜 License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

You can find the full license text in the [`LICENSE`](./LICENSE) file.

---
