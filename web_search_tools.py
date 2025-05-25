from tavily import TavilyClient
from fastmcp import FastMCP
from config import config

mcp = FastMCP('tavily')

client = TavilyClient(api_key=config['TAVILY_API_KEY'])

print(config['TAVILY_API_KEY'])

def web_search_tools():
    @mcp.tool()
    def web_search(query: str) -> str:
        """Search the web using Tavily for the given query.
        同时把搜索结果进行总结和展示，并返回总结后的结果。
        '
        summary: {}
        reference: [{
            title: string,
            url: string,
            content: string,
        }]
        '
        """
        search_response = client.search(
            query=query,
            depth="standard",  # "standard" or "deep"
            output_type="sourcedAnswer",  # "searchResults" or "sourcedAnswer" or "structured"
            structured_output_schema=None,  # must be filled if output_type is "structured"
        )
        return search_response

    return mcp
