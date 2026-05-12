"""
测试包安装是否成功
"""

def test_import():
    """测试导入包"""
    try:
        from confluence_wiki_mcp import __version__
        print(f"✅ 包导入成功，版本: {__version__}")
        return True
    except ImportError as e:
        print(f"❌ 包导入失败: {e}")
        return False


def test_server_module():
    """测试服务器模块"""
    try:
        from confluence_wiki_mcp.server import main, server
        print("✅ 服务器模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 服务器模块导入失败: {e}")
        return False


def test_client_module():
    """测试客户端模块"""
    try:
        from confluence_wiki_mcp.wiki_client import ConfluenceWikiClient
        print("✅ 客户端模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 客户端模块导入失败: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("测试 Confluence Wiki MCP Server 包")
    print("=" * 50)
    
    results = []
    
    print("\n1. 测试包导入...")
    results.append(test_import())
    
    print("\n2. 测试服务器模块...")
    results.append(test_server_module())
    
    print("\n3. 测试客户端模块...")
    results.append(test_client_module())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ 所有测试通过！包已正确安装。")
        print("\n您现在可以：")
        print("  - 运行: confluence-wiki-mcp-server")
        print("  - 或在 Codex 配置中使用 uvx")
    else:
        print("❌ 部分测试失败，请检查安装。")
        print("\n尝试重新安装：")
        print("  pip install -e .")
    print("=" * 50)
