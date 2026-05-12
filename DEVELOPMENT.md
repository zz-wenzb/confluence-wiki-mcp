# 👨‍💻 开发文档

## 📦 项目结构

```
confluence-wiki-mcp/
├── confluence_wiki_mcp/      # Python 包
│   ├── __init__.py           # 包初始化（版本 1.0.0）
│   ├── server.py             # MCP 服务器（13个工具）
│   └── wiki_client.py        # Confluence 客户端
├── pyproject.toml            # Python 项目配置
├── .env                      # 环境变量（不提交）
├── .env.example              # 配置模板
└── README.md                 # 使用文档
```

---

## 🔧 核心文件说明

### 1. `confluence_wiki_mcp/__init__.py`

包初始化文件，定义版本号：

```python
"""Confluence Wiki MCP Server Package"""
__version__ = "1.0.0"
```

---

### 2. `confluence_wiki_mcp/server.py`

MCP 服务器主程序，提供 13 个工具：

**关键组件：**
- `server` - MCP 服务器实例
- `get_wiki_client()` - 从环境变量创建客户端
- `list_tools()` - 注册所有可用工具
- `call_tool()` - 处理工具调用
- `main()` - 启动服务器

**添加新工具步骤：**

1. 在 `list_tools()` 中添加工具定义：
```python
Tool(
    name="my_new_tool",
    description="工具描述",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "参数1"}
        },
        "required": ["param1"]
    }
)
```

2. 在 `call_tool()` 中添加处理逻辑：
```python
elif name == "my_new_tool":
    result = client.my_new_method(arguments["param1"])
```

3. 在 `wiki_client.py` 中实现方法

---

### 3. `confluence_wiki_mcp/wiki_client.py`

Confluence API 客户端封装：

**主要方法：**
- `get_page_by_id()` - 根据 ID 获取页面
- `get_page_by_title()` - 根据标题获取页面
- `create_page()` - 创建页面
- `update_page()` - 更新页面
- `delete_page()` - 删除页面
- `search_pages()` - CQL 搜索
- `get_page_children()` - 获取子页面
- `get_space()` - 获取空间信息
- `get_all_spaces()` - 获取所有空间
- `get_parent_page()` - 获取父页面
- `get_descendants()` - 获取后代页面
- `get_space_pages()` - 获取空间页面
- `get_page_with_space()` - 组合查询

**添加新方法示例：**

```python
def my_new_method(self, param: str) -> dict:
    """新方法说明"""
    try:
        # 调用 Confluence API
        result = self.confluence.some_api_call(param)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"操作失败: {str(e)}"
        }
```

---

### 4. `pyproject.toml`

Python 项目配置文件：

**关键配置：**

```toml
[project]
name = "confluence-wiki-mcp-server"  # PyPI 包名
version = "1.0.0"                     # 版本号

[project.scripts]
confluence-wiki-mcp-server = "confluence_wiki_mcp.server:main"  # 命令行入口

dependencies = [                      # 依赖项
    "atlassian-python-api>=3.41.0",
    "mcp>=1.0.0",
    "python-dotenv>=1.0.0",
]
```

**修改依赖后：**
```powershell
pip install -e .
```

---

## 🚀 开发流程

### 1. 本地开发环境

```powershell
# 克隆项目
cd D:\project\confluence-wiki-mcp

# 安装为可编辑模式
pip install -e .

# 验证安装
python test_package.py
```

---

### 2. 添加新功能

**示例：添加一个获取页面评论的工具**

#### 步骤 1：在 `wiki_client.py` 中添加方法

```python
def get_page_comments(self, page_id: int) -> dict:
    """获取页面评论"""
    try:
        comments = self.confluence.get_page_comments(page_id)
        return {
            "success": True,
            "data": comments
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"获取评论失败: {str(e)}"
        }
```

#### 步骤 2：在 `server.py` 的 `list_tools()` 中注册

```python
Tool(
    name="get_page_comments",
    description="获取页面评论",
    inputSchema={
        "type": "object",
        "properties": {
            "page_id": {
                "type": "integer",
                "description": "页面 ID"
            }
        },
        "required": ["page_id"]
    }
)
```

#### 步骤 3：在 `call_tool()` 中添加处理

```python
elif name == "get_page_comments":
    result = client.get_page_comments(
        page_id=arguments["page_id"]
    )
```

#### 步骤 4：测试

```powershell
# 重启服务器
confluence-wiki-mcp-server

# 或在 Codex 中测试
codex
```

---

### 3. 调试技巧

#### 启用日志

在 `server.py` 开头添加：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### 测试单个工具

```python
# 创建测试脚本
from confluence_wiki_mcp.wiki_client import ConfluenceWikiClient
import os

client = ConfluenceWikiClient(
    url=os.getenv('CONFLUENCE_URL'),
    username=os.getenv('CONFLUENCE_USERNAME'),
    password=os.getenv('CONFLUENCE_PASSWORD')
)

# 测试方法
result = client.get_page_by_id(28381118)
print(result)
```

---

### 4. 代码规范

#### 导入顺序

```python
# 标准库
import os
import json

# 第三方库
from mcp.server import Server
from atlassian import Confluence

# 本地模块
from .wiki_client import ConfluenceWikiClient
```

#### 错误处理

所有方法统一返回格式：

```python
# 成功
{
    "success": True,
    "data": {...},
    "message": "可选的成功消息"
}

# 失败
{
    "success": False,
    "error": "错误描述"
}
```

#### 类型注解

```python
def get_page_by_id(self, page_id: int, expand: str = 'body.storage') -> dict:
    """方法说明
    
    Args:
        page_id: 参数说明
        expand: 参数说明
        
    Returns:
        返回值说明
    """
```

---

## 📦 发布流程（可选）

### 1. 更新版本号

编辑 `confluence_wiki_mcp/__init__.py` 和 `pyproject.toml`：

```python
__version__ = "1.0.1"
```

```toml
version = "1.0.1"
```

---

### 2. 构建包

```powershell
pip install build
python -m build
```

生成文件：
- `dist/confluence_wiki_mcp_server-1.0.1-py3-none-any.whl`
- `dist/confluence-wiki-mcp-server-1.0.1.tar.gz`

---

### 3. 测试上传（TestPyPI）

```powershell
pip install twine
twine upload --repository testpypi dist/*
```

测试安装：
```powershell
pip install --index-url https://test.pypi.org/simple/ confluence-wiki-mcp-server
```

---

### 4. 正式发布

```powershell
twine upload dist/*
```

---

## 🧪 测试

### 单元测试（待添加）

```python
# tests/test_wiki_client.py
import unittest
from confluence_wiki_mcp.wiki_client import ConfluenceWikiClient

class TestWikiClient(unittest.TestCase):
    def setUp(self):
        self.client = ConfluenceWikiClient(
            url="https://test.com",
            username="test",
            password="test"
        )
    
    def test_get_page_by_id(self):
        # 测试逻辑
        pass

if __name__ == '__main__':
    unittest.main()
```

运行测试：
```powershell
python -m pytest tests/
```

---

## 🔍 常见问题

### Q1: 如何修改工具参数？

编辑 `server.py` 中 `list_tools()` 的 `inputSchema`。

### Q2: 如何更改默认值？

在 `inputSchema` 中添加 `"default": value`。

### Q3: 如何添加工具描述？

修改 `Tool` 的 `description` 字段。

### Q4: 依赖冲突怎么办？

```powershell
# 清理重装
pip uninstall confluence-wiki-mcp-server
pip install -e .
```

### Q5: 如何查看日志？

在 `main()` 函数中添加日志配置：

```python
def main():
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
```

---

## 📚 相关资源

- [MCP Protocol Docs](https://modelcontextprotocol.io/)
- [Atlassian Python API](https://atlassian-python-api.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/)

---

**最后更新：** 2026-05-12  
**版本：** 1.0.0
