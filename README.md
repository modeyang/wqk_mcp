# Stock Analysis MCP Server

This project is a server built using the `FastMCP` framework, providing various tools for accessing and analyzing stock market data.

## Features

The server exposes the following tools:

*   **Concept Power Tools (`/stock`)**: Analyzes the strength of stock concept sectors based on fund flow and price change.
*   **Finance Tools (`/finance`)**: Provides access to stock financial core indicators and company information.
*   **Stock F10 Tools (`/f10`)**: Fetches and summarizes Stock F10 information.
*   **Market Emotion Tools (`/market`)**: Retrieves and summarizes A-share market emotion indicators.
*   **Stock Keep Up Tools (`/stockUp`)**: Provides lists of continuous limit-up stocks and limit-up stocks.
*   **Web Search Tools (Tavily) (`/websearch`)**: Provides a web search tool.

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd mcp_stock
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    Install the required packages using pip:

    ```bash
    pip install -r requirements.txt
    playwright install
    ```

4.  **Configuration:**

    Some tools might require API keys or other configuration. Please refer to the `config.py` file and potentially create a `.env` file if necessary (based on `os.getenv` usage in `server.py`).
    ```
    TAVILY_API_KEY=
    ```

5.  **Run the server:**

    You can run the server using the `server.py` script. The server will listen on the port specified by the `PORT` environment variable, defaulting to 9001.

    ```bash
    # Using uv (recommended)
    uv run python server.py
    
    # Or using fastmcp directly
    fastmcp run server.py --transport=sse --port=9001 --host=0.0.0.0
    ```

    To run on a specific port:

    ```bash
    fastmcp run server.py --transport=sse --port=9001 --host=0.0.0.0
    ```

6.  **How to Add MCP with HTTP Port:**

    Once the server is running, it will be available at `http://127.0.0.1:9001/mcp/`. You can configure MCP clients to connect via HTTP transport.

    **For Claude Desktop or other MCP clients, add the following configuration:**

    ```json
    {
      "mcpServers": {
        "wqk-stock-server": {
          "command": "npx",
          "args": [
            "@modelcontextprotocol/server-fetch",
            "http://127.0.0.1:9001/mcp/"
          ]
        }
      }
    }
    ```

    **Alternative HTTP configuration:**

    ```json
    {
      "mcpServers": {
        "wqk-stock-server": {
            "url": "http://127.0.0.1:9001/mcp"
        }
      }
    }
    ```

    **Benefits of HTTP transport:**
    - Cross-platform compatibility
    - Network accessibility (can connect from remote clients)
    - Standard HTTP protocol
    - Easy to debug and monitor
    - No need for stdio/subprocess management

## Usage

Once the server is running, you can interact with the tools via the `/mcp` prefix followed by the tool's mount path (e.g., `/mcp/stock`, `/mcp/finance`). The specific endpoints and expected parameters for each tool can be found by examining the tool definitions within each tool's Python file.