# Confluence Wiki MCP Server

一个基于 MCP (Model Context Protocol) 的 Confluence Wiki 服务器，提供页面的增删改查功能。

## ✨ 功能特性

- ✅ 查询页面（ID/标题/CQL搜索）
- ✅ 创建/更新/删除页面
- ✅ 获取子页面/父页面/后代页面
- ✅ 空间管理（查询/列表）
- ✅ 13个工具完整覆盖 Confluence API

## 🚀 快速开始

### 1. 安装

```powershell
pip install -e .
```

### 2. 配置

复制并编辑 `.env` 文件：
```powershell
Copy-Item .env.example .env
notepad .env
```

填入您的配置：
```env
CONFLUENCE_URL=https://your-confluence-domain.com/
CONFLUENCE_USERNAME=your_username
CONFLUENCE_PASSWORD=your_password
CONFLUENCE_CLOUD=false
CONFLUENCE_VERIFY_SSL=false
```

### 3. 配置 Codex

编辑 `%USERPROFILE%\.codex\config.toml`：

```toml
[mcp_servers.confluence-wiki]
command = "uvx"
args = ["--from", "confluence-wiki-mcp-server", "confluence-wiki-mcp-server"]

[mcp_servers.confluence-wiki.env]
CONFLUENCE_URL = "https://your-confluence-domain.com/"
CONFLUENCE_USERNAME = "your_username"
CONFLUENCE_PASSWORD = "your_password"
CONFLUENCE_CLOUD = "false"
CONFLUENCE_VERIFY_SSL = "false"

[mcp_servers.confluence-wiki.tools.delete_page]
approval_mode = "ask"
```

### 4. 开始使用

```powershell
codex
```

然后直接用自然语言操作：
```
帮我查询 app 空间的"需求方案"页面
获取页面 ID 28381118 的详细内容
在 app 空间创建新页面，标题"测试文档"
```

## 📖 文档

- **使用文档**：[INSTALL.md](INSTALL.md) - 详细使用说明和故障排查
- **开发文档**：[DEVELOPMENT.md](DEVELOPMENT.md) - 二次开发和扩展指南
- **工具详情**：[USAGE.md](USAGE.md) - 13个工具的详细说明

## 🛠️ 其他使用方式

### 本地命令行
```powershell
confluence-wiki-mcp-server
```

### 通过 uvx（无需安装）
```powershell
uvx --from confluence-wiki-mcp-server confluence-wiki-mcp-server
```

### 传统方式
```powershell
python server.py
```

## ⚙️ 可用工具（13个）

| 工具 | 说明 |
|------|------|
| `get_page_by_id` | 根据 ID 获取页面 |
| `get_page_by_title` | 根据标题获取页面 |
| `create_page` | 创建页面 |
| `update_page` | 更新页面 |
| `delete_page` | 删除页面 |
| `search_pages` | CQL 搜索 |
| `get_page_children` | 获取子页面 |
| `get_space` | 获取空间信息 |
| `get_all_spaces` | 获取所有空间 |
| `get_parent_page` | 获取父页面 |
| `get_descendants` | 获取后代页面 |
| `get_space_pages` | 获取空间页面 |
| `get_page_with_space` | 组合查询 |

详见 [USAGE.md](USAGE.md)

## 🔐 安全提示

- `.env` 文件包含敏感信息，已在 `.gitignore` 中
- 不要将 `.env` 提交到版本控制
- 对删除/更新操作设置审批模式
- 使用只读账号进行查询操作

