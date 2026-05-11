# 🚀 快速开始

## 3 步快速上手（5 分钟）

### 步骤 1：安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 2：配置环境变量

```bash
# Windows
Copy-Item .env.example .env
notepad .env

# Linux/Mac
cp .env.example .env
vim .env
```

编辑 `.env` 文件：
```env
CONFLUENCE_URL=https://your-confluence-domain.com/
CONFLUENCE_USERNAME=your_username
CONFLUENCE_PASSWORD=your_password
CONFLUENCE_CLOUD=false
CONFLUENCE_VERIFY_SSL=false
```

### 步骤 3：启动并测试

```bash
# 启动服务器
python server.py

# 新终端窗口测试
python test_client.py
```

看到 ✅ 表示成功！

## 🎯 常用操作

### 查询页面
```python
get_page_by_id(page_id=28381118)
get_page_by_title(space="app", title="需求方案")
search_pages(cql='space = "app" AND title ~ "PRPOOL"')
```

### 创建/更新/删除
```python
create_page(space="app", title="新页面", body="<p>内容</p>", parent_id=12345)
update_page(page_id=12345, title="新标题", body="<p>新内容</p>")
delete_page(page_id=12345)
```

## ❓ 常见问题

**Q: 连接失败？**  
A: 检查 URL、用户名、密码是否正确

**Q: SSL 错误？**  
A: 设置 `CONFLUENCE_VERIFY_SSL=false`

**Q: 如何停止服务器？**  
A: 按 `Ctrl+C`

详细文档请查看 [USAGE.md](USAGE.md)
