from typing import Dict, Any, List

from fastmcp import FastMCP
import requests
import json

stock_keep_up_mcp = FastMCP("Stock Keep Up API")

def register_stock_keep_up_tools():

    @stock_keep_up_mcp.tool()
    def get_continuous_up_stocks() -> List[Dict[str, Any]]:
        """
        获取连续涨停股票列表

        Returns:
            List[Dict[str, Any]]: 连续涨停股票列表数据
        """
        url = 'https://x-quote.cls.cn/quote/index/up_down_analysis'

        params = {
            "app": "CailianpressWeb",
            "os": "web",
            "rever": "1",
            "sv": "7.7.5",
            "type": "continuous_up_pool",
            "way": "last_px"
        }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.cls.cn',
            'Referer': 'https://www.cls.cn/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"' ,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"' ,
            'Cookie': 'HWWAFSESID=f558e36484c8be73bce; HWWAFSESTIME=1748063466245'
        }

        try:
            print("Fetching continuous up stocks data...")
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status() # Raise an exception for bad status codes
            data = response.json()
            print(f"data: {data}")

            # Assuming the actual stock list is in data['data']['list'] based on similar APIs
            # You might need to adjust this based on the actual response structure
            stock_list = data.get("data", [])

            if stock_list:
                return stock_list
            else:
                return [{"message": "No continuous up stocks found or unexpected data structure"}]

        except requests.exceptions.RequestException as e:
            print(f"Error fetching continuous up stocks: {e}")
            return [{"error": f"Request error: {e}"}]
        except json.JSONDecodeError:
            print("Error decoding JSON response")
            return [{"error": "Error decoding JSON response"}]
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return [{"error": f"Unexpected error: {e}"}]

    @stock_keep_up_mcp.tool()
    def get_limit_up_stocks() -> List[Dict[str, Any]]:
        """
        获取涨停股票列表
        Returns:
            List[Dict[str, Any]]: 涨停股票列表数据
        """
        url = 'https://x-quote.cls.cn/quote/index/up_down_analysis'
        params = {
            "app": "CailianpressWeb",
            "os": "web",
            "rever": "1",
            "sv": "7.7.5",
            "type": "up_pool",
            "way": "last_px",
            "sign": "a820dce18412fac3775aa940d0b00dcb"
        }
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.cls.cn',
            'Referer': 'https://www.cls.cn/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'Cookie': 'HWWAFSESID=f558e36484c8be73bce; HWWAFSESTIME=1748063466245'
        }
        try:
            print("Fetching limit up stocks data...")
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            print(f"Full API response: {json.dumps(data, indent=2, ensure_ascii=False)}")
            stock_list = data.get("data", [])
            if not stock_list:
                return [{"message": "No limit up stocks found or 'list' field is empty"}]
            return stock_list
        except requests.exceptions.RequestException as e:
            print(f"Error fetching limit up stocks: {e}")
            return [{"error": f"Request error: {e}"}]
        except json.JSONDecodeError:
            print("Error decoding JSON response")
            return [{"error": "Error decoding JSON response"}]
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return [{"error": f"Unexpected error: {e}"}]


    return stock_keep_up_mcp