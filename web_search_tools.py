import asyncio
from tavily import TavilyClient
from fastmcp import FastMCP
from config import config
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DefaultMarkdownGenerator

mcp = FastMCP('tavily')

# 安全地获取 API 密钥，如果不存在则设置为 None
tavily_api_key = config.get('TAVILY_API_KEY')
client = None

if tavily_api_key:
    try:
        client = TavilyClient(api_key=tavily_api_key)
        print(f"Tavily API Key configured: {tavily_api_key[:10]}...")
    except Exception as e:
        print(f"Failed to initialize Tavily client: {e}")
else:
    print("Warning: TAVILY_API_KEY not found in environment variables. Web search functionality will be disabled.")

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
        if client is None:
            return "Error: Tavily API client not initialized. Please check your TAVILY_API_KEY configuration."
        
        try:
            search_response = client.search(
                query=query,
                depth="standard",  # "standard" or "deep"
                output_type="sourcedAnswer",  # "searchResults" or "sourcedAnswer" or "structured"
                structured_output_schema=None,  # must be filled if output_type is "structured"
            )
            return search_response
        except Exception as e:
            return f"Error performing web search: {str(e)}"

    @mcp.tool()
    async def url_to_markdown(url: str) -> str:
        """Use crawl4ai to convert a URL to markdown, focusing on body content.

        Args:
            url: The URL to convert.
        """
        config = CrawlerRunConfig(
            markdown_generator=DefaultMarkdownGenerator(
                content_source="fit_html",  # This is the default
                options={"ignore_links": False}
            )
        )
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url, config=config)
            if result.success:
                # Check if result.markdown is None or empty
                if result.markdown:
                    return result.markdown
                else:
                    return f"Crawl successful for {url}, but no markdown content was generated."
            else:
                return f"Error crawling {url}: {result.error_message}"

    return mcp
