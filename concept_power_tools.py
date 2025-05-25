from fastmcp import FastMCP
import pandas as pd
import akshare as ak
from sklearn.preprocessing import MinMaxScaler
import platform
import json

# 初始化 FastMCP 服务
toolkit = FastMCP("Concept Power Tools")

# 设置中文字体以正确显示行业名称（根据系统选择合适的字体）
system = platform.system()
if system == "Windows":
    font_family = 'SimHei'
elif system == "Darwin":
    font_family = 'Arial Unicode MS'
else:
    font_family = 'DejaVu Sans'

# 获取不同时间周期的数据
def get_fund_flow_data(symbols):
    data_dict = {}
    for symbol in symbols:
        try:
            df = ak.stock_fund_flow_concept(symbol=symbol)
            data_dict[symbol] = df
        except Exception as e:
            data_dict[symbol] = None
    return data_dict

# 计算单周期板块强度
def calculate_strength(df, w1=0.5, w2=0.3, w3=0.2):
    df = df.dropna(subset=["净额", "流入资金", "流出资金"])
    if "行业-涨跌幅" in df.columns:
        df["涨跌幅"] = df["行业-涨跌幅"]
    elif "阶段涨跌幅" in df.columns:
        df["涨跌幅"] = df["阶段涨跌幅"].str.replace("%", "").astype(float)
    df["total_flow"] = df["流入资金"] + df["流出资金"]
    df["inflow_ratio"] = df["流入资金"] / df["total_flow"].replace(0, 1)
    scaler = MinMaxScaler()
    df["normalized_net_inflow"] = scaler.fit_transform(df[["净额"]])
    df["normalized_price_change"] = scaler.fit_transform(df[["涨跌幅"]])
    df["strength"] = (w1 * df["normalized_net_inflow"] + 
                      w2 * df["normalized_price_change"] + 
                      w3 * df["inflow_ratio"])
    return df[["行业", "strength", "净额", "涨跌幅", "inflow_ratio"]]

# 综合多周期数据，分别计算短期和长期强度
def combine_strengths_by_term(data_dict, short_term_symbols, long_term_symbols, short_term_weights, long_term_weights):
    short_term_strengths = {}
    long_term_strengths = {}
    for symbol in short_term_symbols:
        if symbol in data_dict and data_dict[symbol] is not None:
            weight = short_term_weights.get(symbol, 0)
            strength_df = calculate_strength(data_dict[symbol])
            for _, row in strength_df.iterrows():
                industry = row["行业"]
                if industry not in short_term_strengths:
                    short_term_strengths[industry] = {"total_strength": 0, "count": 0}
                short_term_strengths[industry]["total_strength"] += row["strength"] * weight
                short_term_strengths[industry]["count"] += weight
    for symbol in long_term_symbols:
        if symbol in data_dict and data_dict[symbol] is not None:
            weight = long_term_weights.get(symbol, 0)
            strength_df = calculate_strength(data_dict[symbol])
            for _, row in strength_df.iterrows():
                industry = row["行业"]
                if industry not in long_term_strengths:
                    long_term_strengths[industry] = {"total_strength": 0, "count": 0}
                long_term_strengths[industry]["total_strength"] += row["strength"] * weight
                long_term_strengths[industry]["count"] += weight
    result = []
    all_industries = set(short_term_strengths.keys()).union(set(long_term_strengths.keys()))
    for industry in all_industries:
        short_strength = (short_term_strengths.get(industry, {}).get("total_strength", 0) / 
                         short_term_strengths.get(industry, {}).get("count", 1) if short_term_strengths.get(industry) else 0)
        long_strength = (long_term_strengths.get(industry, {}).get("total_strength", 0) / 
                        long_term_strengths.get(industry, {}).get("count", 1) if long_term_strengths.get(industry) else 0)
        trend = short_strength - long_strength
        if trend > 0.1:
            trend_desc = "短期显著走强"
        elif trend < -0.1:
            trend_desc = "短期显著走弱"
        else:
            trend_desc = "趋势平稳"
        result.append({
            "行业": industry,
            "短期强度": round(short_strength, 3),
            "长期强度": round(long_strength, 3),
            "强度变化趋势": round(trend, 3),
            "趋势描述": trend_desc
        })
    return pd.DataFrame(result).sort_values(by="短期强度", ascending=False)

# MCP Tool: 板块强度分析
@toolkit.tool()
def analyze_concept_power(top_n: int = 20) -> str:
    """分析A股概念板块资金流强度，输出短期、长期强度及趋势。默认分析主流周期。最好使用表格展现板块强度信息.

    Args:
        top_n (int, optional): 返回前N个行业，默认20。

    Returns:
        str: JSON字符串，包含行业强度分析结果。
    """
    try:
        symbols = ["即时", "3日排行", "5日排行", "10日排行", "20日排行"]
        data_dict = get_fund_flow_data(symbols)
        short_term_symbols = [s for s in ["即时", "3日排行"] if s in symbols]
        long_term_symbols = [s for s in ["5日排行", "10日排行", "20日排行"] if s in symbols]
        short_term_weights = {"即时": 0.4, "3日排行": 0.6}
        long_term_weights = {"5日排行": 0.3, "10日排行": 0.3, "20日排行": 0.4}
        result_df = combine_strengths_by_term(data_dict, short_term_symbols, long_term_symbols, short_term_weights, long_term_weights)
        result_df = result_df.head(top_n)
        result = result_df.to_dict(orient="records")
        return json.dumps({
            "status": "success",
            "message": f"分析完成，返回前{top_n}个行业。",
            "results": result,
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# 返回 MCP 对象
def register_concept_power_tools():
    return toolkit 