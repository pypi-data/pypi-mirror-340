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

Configure the client to launch this server using an absolute path to the Python interpreter in your virtual environment and specifying the module `-m traderfit_mcp_bridge`. Provide your TraderFitAI Platform API Key via the `env` setting.

**Example `mcp.json` Snippet:**

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
                // Optional: Add other env vars if needed by the bridge or backend
            },
            "cwd": "/ABSOLUTE/PATH/TO/traderfit-mcp-bridge" // <-- Set CWD to find .env if needed
        }
        // ... other servers
    }
}
```

**Important:**
*   Replace the placeholder paths and API key with your specific values.
*   Ensure the `cwd` (Current Working Directory) is set correctly if your `.env` file needs to be loaded relative to the project root when launched by the MCP client. 