#!/bin/bash
# Confluence Wiki MCP Server 启动脚本 (Linux/Mac)

echo "========================================"
echo "启动 Confluence Wiki MCP Server"
echo "========================================"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python3，请先安装 Python3"
    exit 1
fi

echo "Python 版本: $(python3 --version)"
echo ""

# 检查依赖是否安装
echo "检查依赖..."
if ! python3 -c "import mcp" &> /dev/null; then
    echo "[提示] 正在安装依赖包..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[错误] 依赖安装失败"
        exit 1
    fi
fi

echo ""
echo "[成功] 依赖检查完成"
echo ""
echo "正在启动 MCP 服务器..."
echo "按 Ctrl+C 停止服务器"
echo ""

# 启动服务器
python3 server.py
