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
    
    # 测试 2: 根据标题获取页面（文件夹）
    test_space = os.getenv('TEST_SPACE', 'app')  # 默认值仅用于示例
    test_title = os.getenv('TEST_TITLE', '202604')  # 默认值仅用于示例
    print(f"\n【测试 2】根据空间和名称获取文件夹 (space: {test_space}, title: {test_title})")
    result = client.get_page_by_title(test_space, test_title)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if result['success']:
        print(f"✅ 成功获取文件夹: {result['data']['title']}")
        print(f"   文件夹 ID: {result['data']['id']}")
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
    result = client.get_page_children(parent_id=202604)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 测试 5: 获取空间信息
    test_space_key = os.getenv('TEST_SPACE', 'app')
    print(f"\n【测试 5】获取空间信息 (space: {test_space_key})")
    result = client.get_space(test_space_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if result['success']:
        print(f"✅ 成功获取空间: {result['data'].get('name', 'N/A')}")
    else:
        print(f"❌ 失败: {result['error']}")
    
    # 测试 6: 获取所有空间列表
    print("\n【测试 6】获取所有空间列表")
    result = client.get_all_spaces(limit=5)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if result['success']:
        total = len(result['data'].get('results', []))
        print(f"✅ 找到 {total} 个空间")
    else:
        print(f"❌ 失败: {result['error']}")

    # 测试 7: 获取父页面
    print("\n【测试 7】获取父页面 (需要先有页面 ID)")
    result = client.get_parent_page(page_id=28382973)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 测试 8: 获取后代页面
    print("\n【测试 8】获取后代页面 (需要先有页面 ID)")
    result = client.get_descendants(page_id=28382062)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 测试 9: 获取空间下的所有页面
    print(f"\n【测试 9】获取空间下的所有页面 (space: {test_space_key})")
    result = client.get_space_pages(test_space_key, limit=5)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if result['success']:
        total = len(result['data'])
        print(f"✅ 找到 {total} 个页面")
    else:
        print(f"❌ 失败: {result['error']}")

    # 测试 10: 根据空间和 ID/标题获取页面
    print(f"\n【测试 10】根据空间和标题获取页面 (space: {test_space_key}, title: {test_title})")
    result = client.get_page_with_space(space_key=test_space_key, title=test_title)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if result['success']:
        print(f"✅ 成功获取页面: {result['data']['title']}")
    else:
        print(f"❌ 失败: {result['error']}")

    # 测试 11: 创建页面
    # print("\n【测试 11】中交动态城市")
    # result = client.create_page(
    #     space='app',
    #     title='中交动态城市',
    #     body='<p>中交动态城市</p>',
    #     parent_id=28382062  # 可选
    # )

    # 测试 12: 更新页面
    # print("\n【测试 12】更新页面示例")
    # result = client.update_page(
    #     page_id=28383618,
    #     title='中交动态城市1',
    #     body='<p>中交动态城市1</p>',
    #     version_comment='1'
    # )
    # print(json.dumps(result, ensure_ascii=False, indent=2))
    #
    # if result['success']:
    #     print(f"✅ {result['message']}")
    # else:
    #     print(f"❌ 失败: {result['error']}")

    # 测试 13: 删除页面
    # print("\n【测试 13】删除页面示例")
    # result = client.delete_page(page_id=28383618)
    # print(json.dumps(result, ensure_ascii=False, indent=2))
    #
    # if result['success']:
    #     print(f"✅ {result['message']}")
    # else:
    #     print(f"❌ 失败: {result['error']}")

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_wiki_client()
