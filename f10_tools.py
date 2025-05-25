from typing import Dict

from fastmcp import FastMCP
import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

f10_mcp = FastMCP("Stock F10 API")

def get_prompt(data):
    # 从data中获取所有需要的数据
    data_dict = data[0] if isinstance(data, list) and len(data) > 0 else {}
    
    # 获取各个字段的数据
    core_theme = data_dict.get('核心题材', '')
    financial_indicators = data_dict.get('财务指标', '')
    main_indicators = data_dict.get('主要指标', '')
    shareholder_analysis = data_dict.get('股东分析', '')

    pt = f"""
    ### 股票F10信息总结如下:

    核心题材:
    {core_theme}

    财务指标:
    {financial_indicators}

    主要指标:
    {main_indicators}

    股东分析:
    {shareholder_analysis}
    """

    print(f"pt: {pt}")
    return pt


async def _fetch_f10_data(stock_code: str) -> str:
    """获取股票F10数据

    Args:
        stock_code (str): 股票代码，例如：'002208.SH'

    Returns:
        str: F10数据字符串
    """
    url = f"https://emweb.eastmoney.com/PC_HSF10/pages/index.html?type=soft&color=w&ischoice=1&code={stock_code}#/cpbd"

    # 定义数据提取schema
    schema = {
        "name": "股票F10",
        "baseSelector": "#app",
        "fields": [
            {
                "name": "核心题材",
                "selector": ".hxtccontent",
                "type": "text"
            },
            {
                "name": "财务指标",
                "selector": ".jgyc_table",
                "type": "text"
            },
            {
                "name": "主要指标",
                "selector": ".zyzb_table",
                "type": "text"
            },
            {
                "name": "股东分析",
                "selector": ".gdfx_table",
                "type": "text"
            },
            {
                "name": "股东分析",
                "selector": ".gdfx_table",
                "type": "text"
            },
            {
                "name": "融资融券",
                "selector": ".rzrq_table",
                "type": "text"
            }
        ]
    }

    # 配置Markdown生成器
    md_generator = DefaultMarkdownGenerator(
        options={
            "ignore_links": True,
            "escape_html": False,
            "body_width": 80
        }
    )

    # 设置爬虫配置
    config = CrawlerRunConfig(
        wait_for="body .CPBD .hxtccontent",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        css_selector="body",
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=JsonCssExtractionStrategy(schema, verbose=True),
        markdown_generator=md_generator
    )

    browser_conf = BrowserConfig(
        # browser_type="webkit",
        headless=True,
        text_mode=True
    )

    try:
        async with AsyncWebCrawler(config=browser_conf, verbose=True) as crawler:
            result = await crawler.arun(
                url=url,
                config=config
            )
            data = json.loads(result.extracted_content)
            return get_prompt(data)
    except Exception as e:
        print(f"Warning: Failed to get stock F10 data: {e}")
        return f"Error: {e}"


def register_f10_tools():

    @f10_mcp.tool()
    async def get_stock_f10(stock_code: str = "002208.SH") -> str:
        """获取股票F10信息

        Args:
            stock_code (str): 股票代码，默认为'002208.SH'

        Returns:
            str: F10信息字符串
        """
        try:
            return await _fetch_f10_data(stock_code)
        except Exception as e:
            print(f"Warning: Failed to get stock F10: {e}")
            return f"Error: {e}"

    return f10_mcp