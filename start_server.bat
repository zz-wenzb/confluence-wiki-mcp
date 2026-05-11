@echo off
REM Confluence Wiki MCP Server 启动脚本 (Windows)

echo ========================================
echo 启动 Confluence Wiki MCP Server
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖...
python -c "import mcp" >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

echo.
echo [成功] 依赖检查完成
echo.
echo 正在启动 MCP 服务器...
echo 按 Ctrl+C 停止服务器
echo.

REM 启动服务器
python server.py

pause
