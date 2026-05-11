from atlassian import Confluence
from datetime import datetime
import json
from typing import Optional


class ConfluenceWikiClient:
    """Confluence Wiki 客户端"""

    def __init__(self, url: str, username: str, password: str, cloud: bool = False, verify_ssl: bool = False):
        """
        初始化 Confluence 连接
        
        Args:
            url: Confluence 服务器地址
            username: 用户名
            password: 密码或 App Token
            cloud: 是否为云版本
            verify_ssl: 是否验证 SSL 证书
        """
        self.confluence = Confluence(
            url=url,
            username=username,
            password=password,
            cloud=cloud,
            verify_ssl=verify_ssl
        )
        self.url = url

    def get_page_by_id(self, page_id: int, expand: str = 'body.storage') -> dict:
        """
        根据页面 ID 获取页面详情
        
        Args:
            page_id: 页面 ID
            expand: 扩展字段，如 'body.storage' 获取存储格式的正文
            
        Returns:
            页面信息字典
        """
        try:
            page = self.confluence.get_page_by_id(page_id, expand=expand)
            return {
                "success": True,
                "data": page
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取页面失败: {str(e)}"
            }

    def get_page_by_title(self, space: str, title: str) -> dict:
        """
        根据标题获取页面
        
        Args:
            space: 空间键
            title: 页面标题
            
        Returns:
            页面信息字典
        """
        try:
            page = self.confluence.get_page_by_title(space=space, title=title)
            if page:
                return {
                    "success": True,
                    "data": page
                }
            else:
                return {
                    "success": False,
                    "error": f"未找到页面: {title}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取页面失败: {str(e)}"
            }

    def create_page(self, space: str, title: str, body: str, parent_id: Optional[int] = None) -> dict:
        """
        创建新页面
        
        Args:
            space: 空间键
            title: 页面标题
            body: 页面内容（HTML 格式）
            parent_id: 父页面 ID（可选）
            
        Returns:
            创建结果
        """
        try:
            page = self.confluence.create_page(
                space=space,
                title=title,
                body=body,
                parent_id=parent_id
            )
            return {
                "success": True,
                "data": page,
                "message": f"页面创建成功: {title}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"创建页面失败: {str(e)}"
            }

    def update_page(self, page_id: int, title: str, body: str, version_comment: str = "") -> dict:
        """
        更新页面
        
        Args:
            page_id: 页面 ID
            title: 页面标题
            body: 页面内容（HTML 格式）
            version_comment: 版本注释
            
        Returns:
            更新结果
        """
        try:
            # 先获取当前页面以获取版本号
            current_page = self.confluence.get_page_by_id(page_id, expand='version')
            version = current_page['version']['number'] + 1
            
            # 更新页面
            self.confluence.update_page(
                page_id=page_id,
                title=title,
                body=body,
                type='page',
                representation='storage',
                version=version,
                minor_edit=False,
                version_comment=version_comment
            )
            
            return {
                "success": True,
                "message": f"页面更新成功: {title}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"更新页面失败: {str(e)}"
            }

    def delete_page(self, page_id: int) -> dict:
        """
        删除页面
        
        Args:
            page_id: 页面 ID
            
        Returns:
            删除结果
        """
        try:
            self.confluence.remove_page(page_id=page_id)
            return {
                "success": True,
                "message": f"页面删除成功 (ID: {page_id})"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"删除页面失败: {str(e)}"
            }

    def search_pages(self, cql: str, limit: int = 25) -> dict:
        """
        使用 CQL 搜索页面
        
        Args:
            cql: Confluence Query Language 查询语句
            limit: 返回结果数量限制
            
        Returns:
            搜索结果
        """
        try:
            results = self.confluence.cql(cql=cql, limit=limit)
            return {
                "success": True,
                "data": results
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"搜索页面失败: {str(e)}"
            }

    def get_page_children(self, parent_id: int, expand: str = 'version') -> dict:
        """
        获取子页面列表
        
        Args:
            parent_id: 父页面 ID
            expand: 扩展字段
            
        Returns:
            子页面列表
        """
        try:
            children = self.confluence.get_page_child_by_type(
                page_id=parent_id,
                type='page',
                expand=expand
            )
            return {
                "success": True,
                "data": children
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取子页面失败: {str(e)}"
            }
