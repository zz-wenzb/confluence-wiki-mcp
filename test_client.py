"""
测试 Confluence Wiki MCP 客户端功能
"""

from wiki_client import ConfluenceWikiClient
import json
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量（从 .env.example 复制并填写配置）
load_dotenv()


def test_wiki_client():
    """测试 Wiki 客户端的各项功能"""
    
    # 从环境变量获取配置
    url = os.getenv('CONFLUENCE_URL')
    username = os.getenv('CONFLUENCE_USERNAME')
    password = os.getenv('CONFLUENCE_PASSWORD')
    cloud = os.getenv('CONFLUENCE_CLOUD', 'false').lower() == 'true'
    verify_ssl = os.getenv('CONFLUENCE_VERIFY_SSL', 'false').lower() == 'true'
    
    # 检查必需的环境变量
    if not url or not username or not password:
        print("❌ 错误: 缺少必需的环境变量！")
        print("请设置以下环境变量：")
        print("- CONFLUENCE_URL: Confluence 服务器地址")
        print("- CONFLUENCE_USERNAME: 用户名")
        print("- CONFLUENCE_PASSWORD: 密码")
        print("\n提示：可以复制 .env.example 为 .env 并填写配置")
        return
    
    # 初始化客户端
    client = ConfluenceWikiClient(
        url=url,
        username=username,
        password=password,
        cloud=cloud,
        verify_ssl=verify_ssl
    )
    
    print("=" * 60)
    print("Confluence Wiki Client 功能测试")
    print("=" * 60)
    
    # 测试 1: 根据 ID 获取页面
    test_page_id = os.getenv('TEST_PAGE_ID', '28381118')  # 默认值仅用于示例
    print(f"\n【测试 1】根据 ID 获取页面 (ID: {test_page_id})")
    result = client.get_page_by_id(int(test_page_id))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if result['success']:
        page_id = result['data']['id']
        print(f"✅ 成功获取页面: {result['data']['title']}")
    else:
        print(f"❌ 失败: {result['error']}")
    
    # 测试 2: 根据标题获取页面
    test_space = os.getenv('TEST_SPACE', 'app')  # 默认值仅用于示例
    test_title = os.getenv('TEST_TITLE', '需求方案')  # 默认值仅用于示例
    print(f"\n【测试 2】根据标题获取页面 (space: {test_space}, title: {test_title})")
    result = client.get_page_by_title(test_space, test_title)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if result['success']:
        print(f"✅ 成功获取页面: {result['data']['title']}")
    else:
        print(f"❌ 失败: {result['error']}")
    
    # 测试 3: 搜索页面
    test_cql = os.getenv('TEST_CQL', 'space = "app"')  # 默认值仅用于示例
    print(f"\n【测试 3】使用 CQL 搜索页面 ({test_cql})")
    result = client.search_pages(test_cql, limit=5)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if result['success']:
        total = len(result['data'].get('results', []))
        print(f"✅ 找到 {total} 个页面")
    else:
        print(f"❌ 失败: {result['error']}")
    
    # 测试 4: 获取子页面
    print("\n【测试 4】获取子页面 (需要先有父页面 ID)")
    # 这里需要替换为实际的父页面 ID
    # result = client.get_page_children(parent_id=YOUR_PARENT_ID)
    # print(json.dumps(result, ensure_ascii=False, indent=2))
    print("⚠️  跳过此测试（需要提供有效的父页面 ID）")
    
    # 测试 5: 创建页面
    print("\n【测试 5】创建页面示例（不实际执行）")
    print("""
    创建页面的调用方式：
    result = client.create_page(
        space='YOUR_SPACE',
        title='测试页面',
        body='<p>这是测试内容</p>',
        parent_id=YOUR_PARENT_ID  # 可选
    )
    """)
    
    # 测试 6: 更新页面
    print("\n【测试 6】更新页面示例（不实际执行）")
    print("""
    更新页面的调用方式：
    result = client.update_page(
        page_id=YOUR_PAGE_ID,
        title='更新的标题',
        body='<p>更新后的内容</p>',
        version_comment='更新说明'
    )
    """)
    
    # 测试 7: 删除页面
    print("\n【测试 7】删除页面示例（不实际执行）")
    print("""
    删除页面的调用方式：
    result = client.delete_page(page_id=YOUR_PAGE_ID)
    """)
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_wiki_client()
