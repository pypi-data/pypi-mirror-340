import logging
import asyncio
import json
import httpx
import os
from typing import Optional, List
from modelcontextprotocol import server as mcp

# Import environmental variables
from dotenv import load_dotenv

# Load .env file if exists, otherwise environment variables will be used
load_dotenv()

# Configure backend URL and API key
BACKEND_URL = os.environ.get("TRADERFIT_BACKEND_URL", "https://traderfit-mcp.skolp.com")
API_KEY = os.environ.get("TRADERFIT_API_KEY")

# Configure HTTP client for communicating with the backend
http_client = httpx.AsyncClient(base_url=BACKEND_URL)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("traderfit_mcp_bridge") # Use package name
# logger = logging.getLogger("TraderFitMCPBridge")

# Start the MCP server, listening on stdio
async def run_server():
    capabilities = mcp.Capabilities(
        tools=[
            GetRecentTradesTool,
            ListConnectionsTool,
            ConnectExchangeTool,
            SyncTradesTool,
            # ---> ADD NEW TOOLS <--- #
            DisconnectExchangeTool,
            AddManualTradeTool,
            GetBalanceTool,
        ],
        # resources=[...]
    )

    logger.info("Starting MCP Bridge Server...")
    logger.info(f"Connecting to backend API at: {BACKEND_URL}")
    logger.info(f"Registered Tools: {[tool.__name__ for tool in capabilities.tools]}")

    # Start the MCP server, listening on stdio
    await mcp.server(capabilities)

# --- Entry Point ---

# ---> ADD main() WRAPPER <--- #
def main():
    # Use uvloop if available for better performance
    try:
        import uvloop
        uvloop.install()
        logger.info("Using uvloop for asyncio event loop.")
    except ImportError:
        logger.info("uvloop not found, using default asyncio event loop.")

    loop = asyncio.get_event_loop()
    try:
        # Run the server coroutine
        loop.run_until_complete(run_server())
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")
    finally:
        # Ensure the HTTP client is closed
        # Running shutdown tasks in the loop
        logger.info("Closing HTTP client...")
        loop.run_until_complete(http_client.aclose())
        logger.info("HTTP client closed.")
        # Optional: Other cleanup tasks can be added here
        loop.close()
        logger.info("Event loop closed.")
# ---> END main() WRAPPER <--- #

if __name__ == "__main__":
    # ---> MODIFY THIS LINE <--- #
    main()
    # try:
    #     asyncio.run(run_server())
    # except KeyboardInterrupt:
    #     logger.info("Server stopped by user.")
    # finally:
    #     # Clean up the HTTP client session gracefully
    #     asyncio.run(http_client.aclose())
    #     logger.info("HTTP client closed.") 

# ---> ADD ListConnectionsTool <--- #
class ListConnectionsTool(mcp.Tool):
    """Lists the user's connected exchange accounts."""

    # No parameters needed for this tool

    async def execute(self):
        """Executes the tool by calling the backend API GET /api/exchanges."""
        logger.info("Executing ListConnectionsTool")
        headers = {}
        if API_KEY:
            headers["X-API-Key"] = API_KEY
        else:
            logger.warning("No API Key available. Request will likely be rejected by backend.")
            return json.dumps({"error": "Authentication required", "detail": "TRADERFIT_API_KEY not configured for bridge server."})

        try:
            # Corresponds to the GET /api/exchanges endpoint in the backend router
            response = await http_client.get("/api/exchanges", headers=headers)
            response.raise_for_status()
            connections = response.json()
            logger.info(f"Successfully fetched {len(connections)} exchange connections.")
            return json.dumps(connections, indent=2)

        except httpx.HTTPStatusError as e:
            error_detail = "Unknown error"
            try:
                error_detail = e.response.json().get("detail", str(e))
            except Exception:
                 error_detail = str(e)
            logger.error(f"HTTP error listing connections: {e.status_code} - {error_detail}", exc_info=True)
            return json.dumps({"error": f"HTTP error: {e.status_code}", "detail": error_detail})
        except httpx.RequestError as e:
            logger.error(f"Request error listing connections: {e}", exc_info=True)
            return json.dumps({"error": "Request failed", "detail": str(e)})
        except Exception as e:
            logger.error(f"Unexpected error in ListConnectionsTool: {e}", exc_info=True)
            return json.dumps({"error": "Unexpected server error", "detail": str(e)})
# ---> END ListConnectionsTool <---

# ---> ADD ConnectExchangeTool <--- #
class ConnectExchangeTool(mcp.Tool):
    """Connects a user's exchange account using API credentials."""

    exchange_id: str = mcp.Parameter(description="The identifier of the exchange (e.g., 'binance', 'kucoin').")
    api_key: str = mcp.Parameter(description="The user's API key for the exchange.")
    api_secret: str = mcp.Parameter(description="The user's API secret for the exchange.")
    passphrase: Optional[str] = mcp.Parameter(default=None, description="Optional API passphrase (required by some exchanges like KuCoin).")
    nickname: Optional[str] = mcp.Parameter(default=None, description="An optional nickname for the connection.")

    async def execute(self):
        """Executes the tool by calling the backend POST /api/exchanges/connect/{exchange_id}."""
        logger.info(f"Executing ConnectExchangeTool for exchange: {self.exchange_id}")
        headers = {"Content-Type": "application/json"}
        if API_KEY:
            headers["X-API-Key"] = API_KEY
        else:
            logger.warning("No API Key available. Request will likely be rejected by backend.")
            return json.dumps({"error": "Authentication required", "detail": "TRADERFIT_API_KEY not configured for bridge server."})

        payload = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "passphrase": self.passphrase,
            "nickname": self.nickname
        }

        url_path = f"/api/exchanges/connect/{self.exchange_id}"

        try:
            response = await http_client.post(url_path, headers=headers, json=payload)
            response.raise_for_status()
            connection_info = response.json()
            logger.info(f"Successfully connected exchange {self.exchange_id}. Connection ID: {connection_info.get('connection_id')}")
            return json.dumps(connection_info, indent=2)

        except httpx.HTTPStatusError as e:
            error_detail = "Unknown error"
            try:
                error_detail = e.response.json().get("detail", str(e))
            except Exception:
                 error_detail = str(e)
            logger.error(f"HTTP error connecting exchange {self.exchange_id}: {e.status_code} - {error_detail}", exc_info=True)
            return json.dumps({"error": f"HTTP error: {e.status_code}", "detail": error_detail})
        except httpx.RequestError as e:
            logger.error(f"Request error connecting exchange {self.exchange_id}: {e}", exc_info=True)
            return json.dumps({"error": "Request failed", "detail": str(e)})
        except Exception as e:
            logger.error(f"Unexpected error in ConnectExchangeTool: {e}", exc_info=True)
            return json.dumps({"error": "Unexpected server error", "detail": str(e)})
# ---> END ConnectExchangeTool <---

# ---> ADD SyncTradesTool <---
class SyncTradesTool(mcp.Tool):
    """Triggers synchronization of trades from a specific exchange connection."""

    connection_id: str = mcp.Parameter(description="The unique ID of the exchange connection to sync.")
    # Corresponds to SyncOptions in the backend
    symbols: Optional[List[str]] = mcp.Parameter(default=None, description="Optional list of symbols (e.g., ['BTC/USDT', 'ETH/USDT']) to sync. Syncs all if omitted.")
    fetch_all: bool = mcp.Parameter(default=False, description="If true, attempts to fetch all historical trades, otherwise fetches recent trades since last sync.")

    async def execute(self):
        """Executes the tool by calling the backend POST /api/exchanges/{connection_id}/sync."""
        logger.info(f"Executing SyncTradesTool for connection: {self.connection_id}")
        headers = {"Content-Type": "application/json"}
        if API_KEY:
            headers["X-API-Key"] = API_KEY
        else:
            logger.warning("No API Key available. Request will likely be rejected by backend.")
            return json.dumps({"error": "Authentication required", "detail": "TRADERFIT_API_KEY not configured for bridge server."})

        payload = {
            "symbols": self.symbols,
            "fetch_all": self.fetch_all
        }

        url_path = f"/api/exchanges/{self.connection_id}/sync"

        try:
            # This can be a long-running operation, consider longer timeouts if needed
            # httpx default timeout is 5 seconds. Increase if sync takes longer.
            response = await http_client.post(url_path, headers=headers, json=payload, timeout=60.0) # Example: 60 sec timeout
            response.raise_for_status()
            sync_result = response.json()
            logger.info(f"Successfully triggered sync for connection {self.connection_id}. Result: {sync_result}")
            return json.dumps(sync_result, indent=2)

        except httpx.HTTPStatusError as e:
            error_detail = "Unknown error"
            try:
                error_detail = e.response.json().get("detail", str(e))
            except Exception:
                 error_detail = str(e)
            # Handle specific errors like 404 (connection not found) or 502 (exchange fetch failed)
            logger.error(f"HTTP error syncing trades for {self.connection_id}: {e.status_code} - {error_detail}", exc_info=True)
            return json.dumps({"error": f"HTTP error: {e.status_code}", "detail": error_detail})
        except httpx.TimeoutException:
             logger.error(f"Timeout syncing trades for connection {self.connection_id}")
             return json.dumps({"error": "Timeout", "detail": "Trade synchronization timed out."})
        except httpx.RequestError as e:
            logger.error(f"Request error syncing trades for {self.connection_id}: {e}", exc_info=True)
            return json.dumps({"error": "Request failed", "detail": str(e)})
        except Exception as e:
            logger.error(f"Unexpected error in SyncTradesTool: {e}", exc_info=True)
            return json.dumps({"error": "Unexpected server error", "detail": str(e)})
# ---> END SyncTradesTool <---

# ---> ADD DisconnectExchangeTool <---
class DisconnectExchangeTool(mcp.Tool):
    """Deactivates a specific exchange connection."""

    connection_id: str = mcp.Parameter(description="The unique ID of the exchange connection to disconnect.")

    async def execute(self):
        """Executes the tool by calling the backend DELETE /api/exchanges/{connection_id}."""
        logger.info(f"Executing DisconnectExchangeTool for connection: {self.connection_id}")
        headers = {}
        if API_KEY:
            headers["X-API-Key"] = API_KEY
        else:
            logger.warning("No API Key available. Request will likely be rejected by backend.")
            return json.dumps({"error": "Authentication required", "detail": "TRADERFIT_API_KEY not configured for bridge server."})

        url_path = f"/api/exchanges/{self.connection_id}"

        try:
            response = await http_client.delete(url_path, headers=headers)
            response.raise_for_status() # Raises for 4xx/5xx. 204 No Content is success.
            logger.info(f"Successfully disconnected connection {self.connection_id}.")
            # Return a success message for clarity, as DELETE often returns no body
            return json.dumps({"status": "success", "message": f"Connection {self.connection_id} disconnected."}, indent=2)

        except httpx.HTTPStatusError as e:
            error_detail = "Unknown error"
            try:
                error_detail = e.response.json().get("detail", str(e))
            except Exception:
                 error_detail = str(e)
            logger.error(f"HTTP error disconnecting {self.connection_id}: {e.status_code} - {error_detail}", exc_info=True)
            return json.dumps({"error": f"HTTP error: {e.status_code}", "detail": error_detail})
        except httpx.RequestError as e:
            logger.error(f"Request error disconnecting {self.connection_id}: {e}", exc_info=True)
            return json.dumps({"error": "Request failed", "detail": str(e)})
        except Exception as e:
            logger.error(f"Unexpected error in DisconnectExchangeTool: {e}", exc_info=True)
            return json.dumps({"error": "Unexpected server error", "detail": str(e)})
# ---> END DisconnectExchangeTool <---

# ---> ADD AddManualTradeTool <---
class AddManualTradeTool(mcp.Tool):
    """Adds a manual trade record for the user."""

    # Parameters match the TradeInput schema from the backend
    timestamp: str = mcp.Parameter(description="Timestamp of the trade (ISO 8601 format recommended, e.g., YYYY-MM-DDTHH:MM:SSZ).")
    platform: str = mcp.Parameter(description="Platform where the trade occurred (e.g., 'manual', 'Binance').")
    asset: str = mcp.Parameter(description="Asset traded (e.g., 'BTC', 'ETH/USDT').")
    amount: float = mcp.Parameter(description="Amount of the asset traded.")
    price: float = mcp.Parameter(description="Price at which the asset was traded (in quote currency, e.g., USD).")
    type_of_trade: str = mcp.Parameter(description="Type of trade: 'BUY' or 'SELL'.")
    user_note: Optional[str] = mcp.Parameter(default=None, description="Optional user note about the trade.")

    async def execute(self):
        """Executes the tool by calling the backend POST /api/trades."""
        logger.info(f"Executing AddManualTradeTool for asset: {self.asset}")
        headers = {"Content-Type": "application/json"}
        if API_KEY:
            headers["X-API-Key"] = API_KEY
        else:
            logger.warning("No API Key available. Request will likely be rejected by backend.")
            return json.dumps({"error": "Authentication required", "detail": "TRADERFIT_API_KEY not configured for bridge server."})

        payload = {
            "timestamp": self.timestamp,
            "platform": self.platform,
            "asset": self.asset,
            "amount": self.amount,
            "price": self.price,
            "type_of_trade": self.type_of_trade,
            "user_note": self.user_note,
        }

        url_path = "/api/trades"

        try:
            response = await http_client.post(url_path, headers=headers, json=payload)
            response.raise_for_status()
            trade_response = response.json()
            logger.info(f"Successfully added manual trade. Trade ID: {trade_response.get('id')}")
            return json.dumps(trade_response, indent=2)

        except httpx.HTTPStatusError as e:
            error_detail = "Unknown error"
            try:
                error_detail = e.response.json().get("detail", str(e))
            except Exception:
                 error_detail = str(e)
            logger.error(f"HTTP error adding manual trade: {e.status_code} - {error_detail}", exc_info=True)
            return json.dumps({"error": f"HTTP error: {e.status_code}", "detail": error_detail})
        except httpx.RequestError as e:
            logger.error(f"Request error adding manual trade: {e}", exc_info=True)
            return json.dumps({"error": "Request failed", "detail": str(e)})
        except Exception as e:
            logger.error(f"Unexpected error in AddManualTradeTool: {e}", exc_info=True)
            return json.dumps({"error": "Unexpected server error", "detail": str(e)})
# ---> END AddManualTradeTool <---

# ---> ADD GetBalanceTool <---
class GetBalanceTool(mcp.Tool):
    """Fetches the current account balance from a specific exchange connection."""

    connection_id: str = mcp.Parameter(description="The unique ID of the exchange connection to fetch the balance for.")

    async def execute(self):
        """Executes the tool by calling the backend GET /api/exchange-data/{connection_id}/balance."""
        logger.info(f"Executing GetBalanceTool for connection: {self.connection_id}")
        headers = {}
        if API_KEY:
            headers["X-API-Key"] = API_KEY
        else:
            logger.warning("No API Key available. Request will likely be rejected by backend.")
            return json.dumps({"error": "Authentication required", "detail": "TRADERFIT_API_KEY not configured for bridge server."})

        # The backend endpoint is /api/exchange-data/{connection_id}/balance
        url_path = f"/api/exchange-data/{self.connection_id}/balance"

        try:
            # Fetching balance might also take a moment depending on the exchange
            response = await http_client.get(url_path, headers=headers, timeout=30.0) # 30 sec timeout
            response.raise_for_status()
            balance_data = response.json()
            logger.info(f"Successfully fetched balance for connection {self.connection_id}.")
            # Balance data can be complex (free, used, total per asset), return raw JSON
            return json.dumps(balance_data, indent=2)

        except httpx.HTTPStatusError as e:
            error_detail = "Unknown error"
            try:
                error_detail = e.response.json().get("detail", str(e))
            except Exception:
                 error_detail = str(e)
            logger.error(f"HTTP error fetching balance for {self.connection_id}: {e.status_code} - {error_detail}", exc_info=True)
            return json.dumps({"error": f"HTTP error: {e.status_code}", "detail": error_detail})
        except httpx.TimeoutException:
             logger.error(f"Timeout fetching balance for connection {self.connection_id}")
             return json.dumps({"error": "Timeout", "detail": "Fetching balance timed out."})
        except httpx.RequestError as e:
            logger.error(f"Request error fetching balance for {self.connection_id}: {e}", exc_info=True)
            return json.dumps({"error": "Request failed", "detail": str(e)})
        except Exception as e:
            logger.error(f"Unexpected error in GetBalanceTool: {e}", exc_info=True)
            return json.dumps({"error": "Unexpected server error", "detail": str(e)})
# ---> END GetBalanceTool <---