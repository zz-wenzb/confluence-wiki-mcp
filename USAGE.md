# Confluence Wiki MCP 使用指南

## 🛠️ 工具列表

MCP 服务器提供以下 7 个工具：

### 📖 查询类工具

#### 1. get_page_by_id
根据页面 ID 获取页面详情

```json
{
  "page_id": 28381118,
  "expand": "body.storage"
}
```

#### 2. get_page_by_title
根据标题和空间键获取页面

```json
{
  "space": "app",
  "title": "需求方案"
}
```

#### 3. search_pages
使用 CQL 搜索页面

```json
{
  "cql": "space = \"app\" AND title ~ \"PRPOOL\"",
  "limit": 10
}
```

#### 4. get_page_children
获取子页面列表

```json
{
  "parent_id": 12345,
  "expand": "version"
}
```

### ✏️ 编辑类工具

#### 5. create_page
创建新页面

```json
{
  "space": "app",
  "title": "新页面标题",
  "body": "<p>页面内容</p>",
  "parent_id": 12345
}
```

#### 6. update_page
更新现有页面

```json
{
  "page_id": 12345,
  "title": "更新后的标题",
  "body": "<p>更新后的内容</p>",
  "version_comment": "更新说明"
}
```

#### 7. delete_page
删除页面

```json
{
  "page_id": 12345
}
```

## CQL 查询示例

Confluence Query Language (CQL) 常用查询：

```sql
-- 搜索特定空间
space = "DEV"

-- 标题包含关键词
title ~ "test"

-- 查找子页面
parent = 12345

-- 按创建日期
created >= "2024-01-01"

-- 按修改日期
modified <= "2024-12-31"

-- 组合查询
space = "app" AND title ~ "PRPOOL" AND created >= "2024-01-01"
```

## 返回值格式

所有工具返回统一的 JSON 格式：

**成功响应：**
```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功"
}
```

**失败响应：**
```json
{
  "success": false,
  "error": "错误信息"
}
```

## 测试客户端

运行测试脚本验证功能：

```bash
python test_client.py
```

## 常见问题

### Q1: SSL 证书验证失败怎么办？
A: 设置 `CONFLUENCE_VERIFY_SSL=false`（仅用于内网环境）

### Q2: 如何知道空间键（space key）？
A: 
- 查看 URL：`https://wiki.xxx.com/display/SPACE_KEY/Page_Title`
- 或使用 `search_pages` 工具查询：`cql = "space = \"YOUR_SPACE\""`

### Q3: parent_id 从哪里获取？
A: 
- 使用 `get_page_by_title` 获取父页面
- 从返回结果的 `data.id` 字段获取

## 安全建议

1. ⚠️ **不要硬编码密码**：使用环境变量或 `.env` 文件
2. 🔐 **使用强密码**：密码长度至少 12 位，定期更换
3. 🔒 **开启 SSL 验证**：生产环境务必设置 `CONFLUENCE_VERIFY_SSL=true`
4. 📝 **定期更换凭证**：提高安全性

## 开发调试

### 查看日志
服务器运行时会在控制台输出所有请求和响应

### 调试模式
可以添加日志输出来调试：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 扩展功能

如需添加新功能，可以：

1. 在 `wiki_client.py` 中添加新方法
2. 在 `server.py` 的 `list_tools()` 中注册新工具
3. 在 `call_tool()` 中添加调用逻辑

## 技术支持

如有问题，请检查：
1. ✅ Confluence 服务是否可访问
2. ✅ 用户名和密码是否正确
3. ✅ 是否有相应的操作权限
4. ✅ 网络连接是否正常
