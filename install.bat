@echo off
REM ==========================================
REM Confluence Wiki MCP Server 安装脚本
REM ==========================================

echo.
echo ========================================
echo Confluence Wiki MCP Server 安装
echo ========================================
echo.

REM 检查 Python 是否安装
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)

echo [1/4] 检查 Python 版本...
python --version
echo.

REM 检查 pip 是否安装
where pip >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未找到 pip
    pause
    exit /b 1
)

echo [2/4] 安装依赖包...
pip install -e .
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 安装失败
    pause
    exit /b 1
)
echo.

echo [3/4] 测试包安装...
python test_package.py
echo.

echo [4/4] 检查配置文件...
if exist .env (
    echo [✓] .env 文件已存在
) else (
    echo [!] .env 文件不存在，复制示例文件...
    if exist .env.example (
        copy .env.example .env
        echo [✓] 已创建 .env 文件，请编辑它填入您的配置
    ) else (
        echo [错误] 未找到 .env.example 文件
    )
)
echo.

echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 您现在可以：
echo   1. 编辑 .env 文件配置 Confluence 连接信息
echo   2. 运行: confluence-wiki-mcp-server 启动服务器
echo   3. 或配置 Codex 使用 uvx 方式（推荐）
echo.
echo 详细使用说明请查看:
echo   - INSTALL.md
echo   - CODEX_CONFIG.example.toml
echo.
pause
