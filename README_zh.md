# 股票分析 MCP 服务器

本项目是使用 `FastMCP` 框架构建的服务器，提供了用于访问和分析股票市场数据的各种工具。

## 特性

服务器开放了以下工具：

*   **概念板块强度工具 (`/stock`)**: 基于资金流和价格变化分析股票概念板块的强度。
*   **财务数据工具 (`/finance`)**: 提供股票财务核心指标和公司信息访问。
*   **股票 F10 工具 (`/f10`)**: 获取并总结股票 F10 信息。
*   **市场情绪工具 (`/market`)**: 获取并总结 A 股市场情绪指标。
*   **涨停信息工具 (`/stockUp`)**: 提供连续涨停股票列表和涨停股票列表。
*   **网页搜索工具 (Tavily) (`/websearch`)**: 提供一个网页搜索工具。

## 设置和安装

1.  **克隆仓库：**

    ```bash
    git clone <repository_url>
    cd mcp_stock
    ```

2.  **创建虚拟环境（推荐）：**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **安装依赖：**

    使用 pip 安装所需的包：

    ```bash
    pip install -r requirements.txt
    ```

4.  **配置：**

    某些工具可能需要 API 密钥或其他配置。请参考 `config.py` 文件，并在必要时创建 `.env` 文件（基于 `server.py` 中 `os.getenv` 的使用）。

5.  **运行服务器：**

    您可以使用 `server.py` 脚本运行服务器。服务器将监听 `PORT` 环境变量指定的端口，默认端口为 9000。

    ```bash
    python server.py
    ```

    在特定端口上运行：

    ```bash
    PORT=5000 python server.py
    ```

## 使用方法

服务器运行后，您可以通过 `/mcp` 前缀加上工具的挂载路径（例如，`/mcp/stock`, `/mcp/finance`）与工具进行交互。每个工具的具体端点和预期参数可以通过查看相应工具的 Python 文件中的工具定义来找到。 