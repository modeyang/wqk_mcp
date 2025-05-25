FROM python:3.11-slim

# 安装Playwright所需的依赖库
RUN apt-get update && apt-get install -y \
    libnss3

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安装Playwright及其浏览器依赖
RUN pip install playwright
RUN playwright install --with-deps

COPY . .

EXPOSE 8000

CMD ["fastmcp", "run", "server.py", "--transport=sse", "--port=8000", "--host=0.0.0.0"]
