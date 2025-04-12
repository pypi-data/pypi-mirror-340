# TraderFitAI - MCP Bridge Server

This server acts as a bridge between an MCP Client (like Claude Desktop) and the TraderFitAI FastAPI backend.

It translates MCP requests into HTTP requests for the backend and vice-versa.

## Setup

1.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    # OR, if you want to install the package itself in editable mode:
    # pip install -e .
    ```
3.  Configure the environment:
    - Copy `.env.example` to `.env`.
    - Edit `.env` and set `TRADERFIT_BACKEND_URL` to the correct URL of your running `traderfit-mcp` FastAPI server.
    - **Note:** The bridge authenticates using `TRADERFIT_API_KEY` passed via the MCP client's `env` configuration (see below).

## Running

Run the server as a module:

```bash
source venv/bin/activate # Make sure your venv is active
python -m traderfit_mcp_bridge
```

## Connecting from MCP Client (e.g., Claude Desktop)

**Recommended Method (using `uvx`):**

If you have `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`), you can use `uvx` to automatically download and run the package. This avoids needing local paths in your config.

1.  Ensure `uv` is installed and `uvx` is in your PATH.
2.  Configure your MCP client (`mcp.json`) like this, providing your TraderFitAI Platform API Key:

```json
{
    "mcpServers": {
        // ... other servers
        "traderfit": {
            "command": "uvx", // Use uvx
            "args": ["traderfit-mcp-bridge"], // Use the PyPI package name
            "env": {
                "TRADERFIT_API_KEY": "tfp_YOUR_TRADERFIT_API_KEY_HERE" // <-- Replace with your key
                // Optional: uvx runs isolated, so TRADERFIT_BACKEND_URL might be needed here if not defaulted in code
                // "TRADERFIT_BACKEND_URL": "http://localhost:8000"
            }
            // No "cwd" or specific python path needed!
        }
        // ... other servers
    }
}
```

**Alternative Method (Manual Paths):**

If you prefer not to use `uvx` or run from a local clone:

Configure the client to launch this server using an absolute path to the Python interpreter in your virtual environment and specifying the module `-m traderfit_mcp_bridge`. Provide your TraderFitAI Platform API Key via the `env` setting.

**Example `mcp.json` Snippet (Manual):**

```json
{
    "mcpServers": {
        // ... other servers
        "traderfit": {
            "command": "/ABSOLUTE/PATH/TO/YOUR/venv/bin/python", // <-- Replace with your venv python path
            "args": [
                "-m",
                "traderfit_mcp_bridge" // Run as a module
            ],
            "env": {
                "TRADERFIT_API_KEY": "tfp_YOUR_TRADERFIT_API_KEY_HERE" // <-- Replace with your key
            },
            "cwd": "/ABSOLUTE/PATH/TO/traderfit-mcp-bridge" // <-- Set CWD to find .env if needed
        }
        // ... other servers
    }
}
```

**Important:**
*   Replace the placeholder API key with your specific value.
*   If using the manual method, replace the placeholder paths.
*   Ensure the `TRADERFIT_BACKEND_URL` is accessible (either via `.env` if using manual path with `cwd`, passed via `env` in `mcp.json`, or defaulted correctly in the bridge code). 

## Available MCP Tools

The bridge provides the following tools for integration with TraderFitAI:

### GetRecentTradesTool
Fetches recent trades from the TraderFitAI backend.

**Parameters:**
- `limit` (int, default=10): Maximum number of trades to return
- `offset` (int, default=0): Number of trades to skip
- `asset` (string, optional): Filter trades by asset symbol (e.g., BTC)
- `platform` (string, optional): Filter trades by platform (e.g., binance)
- `conversation_id` (string, optional): MCP conversation ID for context

### GetExchangeConnectionsTool
Fetches the user's exchange connections from the TraderFitAI backend.

**Parameters:**
- `conversation_id` (string, optional): MCP conversation ID for context

### ConnectExchangeTool
Adds a new exchange connection for the user.

**Parameters:**
- `exchange_id` (string): The ID of the exchange platform (e.g., 'binance', 'coinbase')
- `api_key` (string): The API key for the exchange account
- `api_secret` (string): The API secret for the exchange account
- `passphrase` (string, optional): Optional passphrase required by some exchanges
- `nickname` (string, optional): Optional nickname for this connection
- `conversation_id` (string, optional): MCP conversation ID for context

### GetPortfolioSummaryTool
Fetches the user's portfolio summary data from the TraderFitAI backend.

**Parameters:**
- `platform` (string, optional): Optional filter for a specific exchange platform
- `conversation_id` (string, optional): MCP conversation ID for context

## Authentication

The bridge uses a simplified authentication approach:

1. **API Key Authentication:** The bridge will use the `TRADERFIT_API_KEY` environment variable to authenticate requests to the TraderFitAI backend.

2. **User Context:** For development and testing, you can specify a user ID in the `TRADERFIT_USER_ID` environment variable. In production, this should be replaced with proper user identification based on the MCP conversation context.

3. **Headers:** The bridge adds appropriate headers to API requests:
   - `X-API-Key`: The API key from the environment
   - `X-User-ID`: The user ID from the context

## Environment Variables

Copy `.env.example` to `.env` and configure:

```
TRADERFIT_BACKEND_URL=http://localhost:8000
TRADERFIT_API_KEY=your_api_key_here
TRADERFIT_USER_ID=your_test_user_id_here 