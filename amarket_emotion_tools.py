from fastmcp import FastMCP
import requests

market_mcp = FastMCP("Market Emotion API")

def get_prompt(data):
    # 从data中获取所有需要的数据
    data_dict = data.get("data", {})
    market_degree = data_dict.get("market_degree")
    shsz_balance = data_dict.get("shsz_balance")
    shsz_balance_change_px = data_dict.get("shsz_balance_change_px")
    up_ratio = data_dict.get("up_ratio")
    up_ratio_num = data_dict.get("up_ratio_num")
    up_open_num = data_dict.get("up_open_num")
    performance = data_dict.get("performance")
    up_open_ratio = data_dict.get("up_open_ratio")
    profit_ratio = data_dict.get("profit_ratio")
    
    # 获取涨跌分析数据
    up_down_dis = data_dict.get("up_down_dis", {})
    
    # 获取涨停板分析数据
    limit_up_board = data_dict.get("limit_up_board", {})
    row1 = limit_up_board.get("row1", [])
    row2 = limit_up_board.get("row2", [])
    row3 = limit_up_board.get("row3", [])

    pt = f"""
    ### 中国A股市场情绪总结如下: 

    当前市场温度 {market_degree} (范围在: 0 ~ 100)
    深市沪市成交量变化 {shsz_balance}
    深市沪市成交量变化比率 {shsz_balance_change_px}
    今日封板率 {up_ratio}
    今日封板数 {up_ratio_num}
    今日封板后开板数 {up_open_num}
    昨日涨停表现 {performance}
    昨日涨停, 今日高开率 {up_open_ratio}
    昨日涨停, 今日获利比率 {profit_ratio}
    整体涨跌分析
        涨停但是又开板 {up_down_dis.get('suspend_num')}
        涨停数 {up_down_dis.get('up_num')}
        跌停数 {up_down_dis.get('down_num')}
        市场上涨数, 收益为正 {up_down_dis.get('rise_num')}
        市场下跌数, 收益为负 {up_down_dis.get('fall_num')}
        平盘, 不涨不跌 {up_down_dis.get('flat_num')}
        跌幅达10的数量 {up_down_dis.get('down_10')}
        跌幅达8的数量 {up_down_dis.get('down_8')}
        跌幅达6的数量 {up_down_dis.get('down_6')}
        跌幅达4的数量 {up_down_dis.get('down_4')}
        跌幅达2的数量 {up_down_dis.get('down_2')}
        涨幅达2的数量 {up_down_dis.get('up_2')}
        涨幅达4的数量 {up_down_dis.get('up_4')}
        涨幅达6的数量 {up_down_dis.get('up_6')}
        涨幅达8的数量 {up_down_dis.get('up_8')}
        涨幅达10的数量 {up_down_dis.get('up_10')}
    涨停板分析:
        row1/row2/row3: 分别是统计数据, 可以理解为是一个矩阵表格: 
            row1: {', '.join(str(x) for x in row1)}
            row2: {', '.join(str(x) for x in row2)}
            row3: {', '.join(str(x) for x in row3)}
    """

    print(f"pt: {pt}") # Replaced logger.info with print
    
    return pt

def register_market_tools():

    @market_mcp.tool()
    def get_market_emotion() -> str:
        """
        获取市场情绪指标

        Returns:
            str: 市场情绪指标值
        """
        url = "https://x-quote.cls.cn/v2/quote/a/stock/emotion"
        
        params = {
            "app": "CailianpressWeb",
            "os": "web",
            "sv": "7.7.5",
            "sign": "bf0f367462d8cd70917ba5eab3853bce"
        }
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.cls.cn",
            "Referer": "https://www.cls.cn/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"' # Escaped quotes
,            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"' # Escaped quotes
,            "Cookie": "HWWAFSESID=71fc41d26591aae57681; HWWAFSESTIME=1730944338123"
        }
        
        try:
            print("Fetching market emotion data...") # Replaced logger.info with print
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            print(f"data: {data}") # Replaced logger.info with print
            market_degree = data.get("data", {}).get("market_degree")
            
            if market_degree is not None:
                return get_prompt(data)
            else:
                return "Error: Unable to get market_degree from response"
                
        except Exception as e:
            print(f"Warning: Failed to get market emotion: {e}") # Replaced logger.warning with print
            return f"Error: {e}"

    return market_mcp