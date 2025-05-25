# Web Search Tools

This project provides a set of tools for web searching and content extraction using FastMCP, integrated with Tavily for web search and crawl4ai for converting URLs to markdown.

## Features

- **web_search**: Perform web searches using the Tavily API.
- **url_to_markdown**: Convert the content of a given URL into markdown format using crawl4ai.

## Setup

1.  **Clone the repository** (if applicable) or ensure you have the project files.

2.  **Install dependencies**: Install the required Python packages using pip:

    ```bash
    pip install fastmcp tavily-python crawl4ai
    ```

3.  **Configuration**: You need API keys for Tavily. Create a `config.py` file in the same directory as `web_search_tools.py` with the following structure:

    ```python
    # config.py
    config = {
        'TAVILY_API_KEY': 'YOUR_TAVILY_API_KEY'
        # Add other configuration here if needed
    }
    ```

    Replace `'YOUR_TAVILY_API_KEY'` with your actual Tavily API key.

## Usage

Import the `web_search_tools` function and call it to get the tools object. You can then access and use the defined tools.

```python
import asyncio
from web_search_tools import web_search_tools

# Get the tools object
tools = web_search_tools()

# Example: Using the web_search tool (Synchronous)
# Note: FastMCP handles the asynchronous execution of the tool function.
search_query = "latest news on AI"
search_results = tools.web_search(query=search_query)
print("Search Results:", search_results)

# Example: Using the url_to_markdown tool (Asynchronous under the hood via FastMCP)
# Note: FastMCP handles the asynchronous execution of the tool function.
async def main():
    url_to_convert = "https://docs.crawl4ai.com/core/markdown-generation/"
    markdown_content = await tools.url_to_markdown(url=url_to_convert)
    print(f"\nMarkdown content for {url_to_convert}:\n", markdown_content)

if __name__ == "__main__":
    # In a real FastMCP environment, you wouldn't call asyncio.run() here.
    # The framework handles the async execution of the tool.
    # This is just for demonstrating the awaitable call if testing outside the framework.
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "cannot be called from a running event loop" in str(e):
             print("\nRunning within an environment that already has an event loop (like FastMCP).")
             print("In a real application, just call await tools.url_to_markdown(...) directly.")
        else:
            raise

```

**Note on Asynchronous Tools:** The `url_to_markdown` tool is an `async` function. When used within the FastMCP framework, you would directly `await` the tool call. The example above includes `asyncio.run(main())` and error handling for demonstration purposes if you are trying to run the script directly in a standard Python environment, but this is not how it would be used within FastMCP. 