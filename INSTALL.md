# 📖 Confluence Wiki MCP 使用文档

## 🚀 快速开始（3步）

### 1️⃣ 安装包

```powershell
cd D:\project\confluence-wiki-mcp
pip install -e .
```

### 2️⃣ 配置环境变量

编辑 `.env` 文件：
```env
CONFLUENCE_URL=https://your-confluence-domain.com/
CONFLUENCE_USERNAME=your_username
CONFLUENCE_PASSWORD=your_password
CONFLUENCE_CLOUD=false
CONFLUENCE_VERIFY_SSL=false
```

### 3️⃣ 配置 Codex

编辑 `%USERPROFILE%\.codex\config.toml`（Windows）或 `~/.codex/config.toml`（Linux/Mac）：

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

# 敏感操作需要确认
[mcp_servers.confluence-wiki.tools.delete_page]
approval_mode = "ask"

[mcp_servers.confluence-wiki.tools.update_page]
approval_mode = "ask"
```

### ✅ 开始使用

```powershell
codex
```

然后直接用自然语言操作 Confluence：
```
帮我查询 app 空间的"需求方案"页面
获取页面 ID 28381118 的详细内容
搜索 DEV 空间中包含 "PRPOOL" 的页面
```

---

## 💡 其他使用方式

### 方式一：本地命令行

```powershell
# 安装后直接运行
confluence-wiki-mcp-server
```

### 方式二：通过 uvx（无需安装）

```powershell
uvx --from confluence-wiki-mcp-server confluence-wiki-mcp-server
```

### 方式三：传统方式（向后兼容）

```powershell
python server.py
```

---

## 🛠️ 故障排查

### 问题 1：找不到命令

```powershell
# 重新安装
pip install -e .

# 验证安装
python test_package.py
```

### 问题 2：连接失败

检查：
- ✅ `.env` 配置正确
- ✅ Confluence 服务可访问
- ✅ 用户名密码正确

### 问题 3：SSL 错误

```env
CONFLUENCE_VERIFY_SSL=false
```

### 问题 4：Codex 找不到工具

```powershell
# 检查配置
cat %USERPROFILE%\.codex\config.toml

# 重启 Codex
codex
```

---

## 🔐 安全建议

1. **不要硬编码密码** - 使用 `.env` 文件
2. **保护配置文件** - `.env` 已在 `.gitignore` 中
3. **设置审批模式** - 对删除/更新操作设置 `approval_mode = "ask"`
4. **使用只读账号** - 查询时使用只读权限

---

## 📚 更多信息

- 工具详细说明：查看 [USAGE.md](USAGE.md)
- 项目总览：查看 [README.md](README.md)

---

## 🆘 需要帮助？

如有问题，请检查：
1. ✅ Python 版本 >= 3.9
2. ✅ uvx 已正确安装
3. ✅ Confluence 服务可访问
4. ✅ 用户名和密码正确
5. ✅ 有相应的操作权限
