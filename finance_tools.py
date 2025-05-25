from fastmcp import FastMCP
from typing import Dict, Any, List
import adata
import httpx

finance_mcp = FastMCP("Adata Finance API")

def register_finance_tools():
    """
    注册adata财务数据相关工具
    """
    @finance_mcp.tool()
    def get_stock_finance_core_index(
        stock_code: str, 
    ) -> List[Dict[str, Any]]:
        """
        获取单个股票的连续年报/季报财务核心指标, 最好用table或者图表的形式展示

        Args:
            stock_code (str): 股票代码, 一般是6位的数字, 比如: 688008, 不要带前缀"sh/sz"
        Returns:
            List[Dict[str, Any]]: 财务核心指标列表, 包含所有年度财务数据
        """
        df = adata.stock.finance.get_core_index(
            stock_code=stock_code, 
        )
        return df.to_dict(orient="records")
  
    @finance_mcp.tool()
    def get_stock_concept_ths(stock_code: str) -> List[Dict[str, Any]]:
        """
        获取单个股票的核心概念详细信息（同花顺）

        Args:
            stock_code (str): 股票代码

        Returns:
            List[Dict[str, Any]]: 概念详情列表
        """
        if not stock_code.isdigit():
            return [{"error": "stock_code must be digits only"}]
        df = adata.stock.info.get_concept_ths(stock_code=stock_code)
        if df is None or df.empty:
            return {
                "error": "true"
            }  # 或返回自定义错误信息
        return df.to_dict(orient="records")

    @finance_mcp.tool()
    def get_company_info(stock_code: str) -> Dict[str, Any]:
        """
        Fetch detailed company information from CLS API.

        Args:
            stock_code: Stock code with prefix (e.g., 'sh603179')

        Returns:
            Dictionary containing company information including:
            - Basic information
            - Issuance details
            - Business overview
            - Financial analysis
            - Shareholders and equity
        """
        url = f"https://www.cls.cn/729c64f1fd5f64035b9b189c90432560/quote/company_info/{stock_code}.json"

        params = {
            "time": "2025042821",
            "app": "CailianpressWeb",
            "os": "web",
            "sv": "8.4.6",
            "sign": "9f8797a1f4de66c2370f7a03990d2737"
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }

        try:
            response = httpx.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Extract and structure the relevant information
            result = {
                "basic_info": data.get("basic_info", {}),
                "issuance_info": data.get("issuance_info", {}),
                "business_overview": data.get("business_overview", {}),
                "financial_analysis": data.get("financial_analysis", {}),
                "shareholders_equity": data.get("shareholders_equity", {})
            }

            return result
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "message": str(e)}
        except httpx.RequestError as e:
            return {"error": "Request error", "message": str(e)}
        except Exception as e:
            return {"error": "Unexpected error", "message": str(e)}
    

    return finance_mcp
