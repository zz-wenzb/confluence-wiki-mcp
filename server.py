"""
Confluence Wiki MCP Server
提供 Confluence 页面的增删改查功能
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
import json
from wiki_client import ConfluenceWikiClient
import os


# 创建 MCP 服务器实例
server = Server("confluence-wiki-mcp")


def get_wiki_client() -> ConfluenceWikiClient:
    """
    从环境变量获取配置并创建 Confluence 客户端
    
    环境变量:
        CONFLUENCE_URL: Confluence 服务器地址（必填）
        CONFLUENCE_USERNAME: 用户名（必填）
        CONFLUENCE_PASSWORD: 密码（必填）
        CONFLUENCE_CLOUD: 是否为云版本 (true/false, 默认 false)
        CONFLUENCE_VERIFY_SSL: 是否验证 SSL (true/false, 默认 false)
    
    Raises:
        EnvironmentError: 当必需的环境变量未设置时
    """
    url = os.getenv('CONFLUENCE_URL')
    username = os.getenv('CONFLUENCE_USERNAME')
    password = os.getenv('CONFLUENCE_PASSWORD')
    
    # 检查必需的环境变量
    if not url or not username or not password:
        raise EnvironmentError(
            "缺少必需的环境变量！请设置以下环境变量：\n"
            "- CONFLUENCE_URL: Confluence 服务器地址\n"
            "- CONFLUENCE_USERNAME: 用户名\n"
            "- CONFLUENCE_PASSWORD: 密码\n\n"
            "提示：可以复制 .env.example 为 .env 并填写配置"
        )
    
    cloud = os.getenv('CONFLUENCE_CLOUD', 'false').lower() == 'true'
    verify_ssl = os.getenv('CONFLUENCE_VERIFY_SSL', 'false').lower() == 'true'
    
    return ConfluenceWikiClient(
        url=url,
        username=username,
        password=password,
        cloud=cloud,
        verify_ssl=verify_ssl
    )


@server.list_tools()
async def list_tools() -> list[Tool]:
    """列出所有可用的工具"""
    return [
        Tool(
            name="get_page_by_id",
            description="根据页面 ID 获取 Confluence 页面详情",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_id": {
                        "type": "integer",
                        "description": "页面 ID"
                    },
                    "expand": {
                        "type": "string",
                        "description": "扩展字段，如 'body.storage' 获取存储格式的正文",
                        "default": "body.storage"
                    }
                },
                "required": ["page_id"]
            }
        ),
        Tool(
            name="get_page_by_title",
            description="根据标题和空间键获取 Confluence 页面",
            inputSchema={
                "type": "object",
                "properties": {
                    "space": {
                        "type": "string",
                        "description": "空间键（例如: app, DEV, KB）"
                    },
                    "title": {
                        "type": "string",
                        "description": "页面标题"
                    }
                },
                "required": ["space", "title"]
            }
        ),
        Tool(
            name="create_page",
            description="在 Confluence 中创建新页面",
            inputSchema={
                "type": "object",
                "properties": {
                    "space": {
                        "type": "string",
                        "description": "空间键"
                    },
                    "title": {
                        "type": "string",
                        "description": "页面标题"
                    },
                    "body": {
                        "type": "string",
                        "description": "页面内容（HTML 格式）"
                    },
                    "parent_id": {
                        "type": "integer",
                        "description": "父页面 ID（可选）"
                    }
                },
                "required": ["space", "title", "body"]
            }
        ),
        Tool(
            name="update_page",
            description="更新 Confluence 页面内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_id": {
                        "type": "integer",
                        "description": "页面 ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "页面标题"
                    },
                    "body": {
                        "type": "string",
                        "description": "页面内容（HTML 格式）"
                    },
                    "version_comment": {
                        "type": "string",
                        "description": "版本注释",
                        "default": ""
                    }
                },
                "required": ["page_id", "title", "body"]
            }
        ),
        Tool(
            name="delete_page",
            description="删除 Confluence 页面",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_id": {
                        "type": "integer",
                        "description": "要删除的页面 ID"
                    }
                },
                "required": ["page_id"]
            }
        ),
        Tool(
            name="search_pages",
            description="使用 CQL（Confluence Query Language）搜索页面",
            inputSchema={
                "type": "object",
                "properties": {
                    "cql": {
                        "type": "string",
                        "description": "CQL 查询语句，例如: 'space = \"DEV\" AND title ~ \"test\"'"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "返回结果数量限制",
                        "default": 25
                    }
                },
                "required": ["cql"]
            }
        ),
        Tool(
            name="get_page_children",
            description="获取指定页面的所有子页面",
            inputSchema={
                "type": "object",
                "properties": {
                    "parent_id": {
                        "type": "integer",
                        "description": "父页面 ID"
                    },
                    "expand": {
                        "type": "string",
                        "description": "扩展字段",
                        "default": "version"
                    }
                },
                "required": ["parent_id"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """调用工具"""
    try:
        client = get_wiki_client()
        
        if name == "get_page_by_id":
            result = client.get_page_by_id(
                page_id=arguments["page_id"],
                expand=arguments.get("expand", "body.storage")
            )
        
        elif name == "get_page_by_title":
            result = client.get_page_by_title(
                space=arguments["space"],
                title=arguments["title"]
            )
        
        elif name == "create_page":
            result = client.create_page(
                space=arguments["space"],
                title=arguments["title"],
                body=arguments["body"],
                parent_id=arguments.get("parent_id")
            )
        
        elif name == "update_page":
            result = client.update_page(
                page_id=arguments["page_id"],
                title=arguments["title"],
                body=arguments["body"],
                version_comment=arguments.get("version_comment", "")
            )
        
        elif name == "delete_page":
            result = client.delete_page(
                page_id=arguments["page_id"]
            )
        
        elif name == "search_pages":
            result = client.search_pages(
                cql=arguments["cql"],
                limit=arguments.get("limit", 25)
            )
        
        elif name == "get_page_children":
            result = client.get_page_children(
                parent_id=arguments["parent_id"],
                expand=arguments.get("expand", "version")
            )
        
        else:
            result = {
                "success": False,
                "error": f"未知工具: {name}"
            }
        
        # 返回 JSON 格式的结果
        return [
            TextContent(
                type="text",
                text=json.dumps(result, ensure_ascii=False, indent=2)
            )
        ]
    
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"工具执行失败: {str(e)}"
                }, ensure_ascii=False, indent=2)
            )
        ]


def main():
    """启动 MCP 服务器"""
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(run())


if __name__ == "__main__":
    main()
