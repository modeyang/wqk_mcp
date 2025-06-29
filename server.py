# server.py
import os
from fastmcp import FastMCP
from concept_power_tools import register_concept_power_tools
from finance_tools import register_finance_tools
from f10_tools import register_f10_tools
from amarket_emotion_tools import register_market_tools
from stock_keep_up_tool import register_stock_keep_up_tools
from web_search_tools import web_search_tools

mcp = FastMCP()

# 概念股
mcp.mount('/stock', register_concept_power_tools())

# 财务数据
mcp.mount('/finance', register_finance_tools())

# 股票F10
mcp.mount('/f10', register_f10_tools())

# 市场情绪
mcp.mount('/market', register_market_tools())

# 涨停信息
mcp.mount('/stockUp', register_stock_keep_up_tools())

# web search
mcp.mount('/websearch', web_search_tools())

if __name__ == "__main__":
    # Get port from environment variables, default to 9000 if not set
    port = int(os.getenv("PORT", 9001))
    mcp.run(transport="http", port=port)