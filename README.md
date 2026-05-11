# Confluence Wiki MCP Server

一个基于 MCP (Model Context Protocol) 的 Confluence Wiki 服务器，提供页面的增删改查功能。

## 功能特性

- ✅ **查询页面**：根据 ID 或标题获取页面详情
- ✅ **创建页面**：在指定空间创建新页面
- ✅ **更新页面**：修改现有页面内容
- ✅ **删除页面**：删除指定页面
- ✅ **搜索页面**：使用 CQL 进行高级搜索
- ✅ **获取子页面**：获取页面的所有子页面

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置环境变量

### ⚠️ 重要提示

**`.env` 文件包含敏感信息（用户名、密码），请勿提交到 Git！**

项目已提供 `.env.example` 作为配置模板，您需要：

1. 复制 `.env.example` 为 `.env`
2. 填写您的实际配置信息
3. 确保 `.env` 文件在 `.gitignore` 中（已配置）

### 配置步骤

**Windows PowerShell：**
```powershell
# 复制配置文件
Copy-Item .env.example .env

# 编辑配置文件
notepad .env
```

**Linux/Mac：**
```bash
# 复制配置文件
cp .env.example .env

# 编辑配置文件
vim .env
```

### 配置示例

编辑 `.env` 文件，填入您的 Confluence 连接信息：

```env
# Confluence 服务器地址
CONFLUENCE_URL=https://your-confluence-domain.com/

# 认证信息（使用用户名和密码）
CONFLUENCE_USERNAME=your_username
CONFLUENCE_PASSWORD=your_password

# 版本类型
CONFLUENCE_CLOUD=false  # false: Server版, true: Cloud版

# SSL验证
CONFLUENCE_VERIFY_SSL=false  # 内网可设为false
```

## 启动服务器

```bash
python server.py
```

## 可用工具

### 1. get_page_by_id
根据页面 ID 获取页面详情

**参数：**
- `page_id` (必填): 页面 ID
- `expand` (可选): 扩展字段，默认 "body.storage"

### 2. get_page_by_title
根据标题和空间键获取页面

**参数：**
- `space` (必填): 空间键（例如: app, DEV, KB）
- `title` (必填): 页面标题

### 3. create_page
创建新页面

**参数：**
- `space` (必填): 空间键
- `title` (必填): 页面标题
- `body` (必填): 页面内容（HTML 格式）
- `parent_id` (可选): 父页面 ID

### 4. update_page
更新页面内容

**参数：**
- `page_id` (必填): 页面 ID
- `title` (必填): 页面标题
- `body` (必填): 页面内容（HTML 格式）
- `version_comment` (可选): 版本注释

### 5. delete_page
删除页面

**参数：**
- `page_id` (必填): 要删除的页面 ID

### 6. search_pages
使用 CQL 搜索页面

**参数：**
- `cql` (必填): CQL 查询语句
- `limit` (可选): 返回结果数量限制，默认 25

**CQL 示例：**
- `space = "DEV"` - 搜索特定空间
- `title ~ "test"` - 标题包含 "test"
- `parent = 12345` - 查找父页面为 12345 的子页面
- `created >= "2024-01-01"` - 创建日期大于等于 2024-01-01

### 7. get_page_children
获取指定页面的所有子页面

**参数：**
- `parent_id` (必填): 父页面 ID
- `expand` (可选): 扩展字段，默认 "version"

## 使用示例

### Python 调用示例

```python
from mcp import ClientSession
import asyncio

async def main():
    # 连接到 MCP 服务器
    async with ClientSession() as session:
        # 获取页面
        result = await session.call_tool("get_page_by_id", {
            "page_id": 28381118
        })
        print(result)
        
        # 创建页面
        result = await session.call_tool("create_page", {
            "space": "app",
            "title": "测试页面",
            "body": "<p>这是测试内容</p>",
            "parent_id": 12345
        })
        print(result)

asyncio.run(main())
```

## 项目结构

```
confluence-wiki-mcp/
├── server.py          # MCP 服务器主文件
├── wiki_client.py     # Confluence 客户端封装
├── requirements.txt   # 依赖包列表
├── .env.example       # 环境变量示例
└── README.md          # 说明文档
```

## 注意事项

1. **安全性**：使用强密码并定期更换
2. **SSL 验证**：生产环境建议开启 SSL 验证
3. **权限**：确保使用的账号有相应的操作权限
4. **备份**：删除页面前请确认已备份重要数据

## 许可证

MIT License
