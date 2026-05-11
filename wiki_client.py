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

    def get_space(self, space_key: str, expand: str = '') -> dict:
        """
        根据空间键获取空间（文件夹）信息
        
        Args:
            space_key: 空间键（例如: app, DEV, KB）
            expand: 扩展字段，如 'metadata.labels'
            
        Returns:
            空间信息字典
        """
        try:
            space = self.confluence.get_space(space_key, expand=expand)
            return {
                "success": True,
                "data": space
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取空间失败: {str(e)}"
            }

    def get_all_spaces(self, start: int = 0, limit: int = 25) -> dict:
        """
        获取所有空间列表
        
        Args:
            start: 起始位置
            limit: 返回数量限制
            
        Returns:
            空间列表
        """
        try:
            spaces = self.confluence.get_all_spaces(start=start, limit=limit)
            return {
                "success": True,
                "data": spaces
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取空间列表失败: {str(e)}"
            }

    def get_parent_page(self, page_id: int, expand: str = 'version') -> dict:
        """
        根据页面 ID 获取父页面
        
        Args:
            page_id: 页面 ID
            expand: 扩展字段
            
        Returns:
            父页面信息字典
        """
        try:
            # 先获取当前页面的祖先信息
            page = self.confluence.get_page_by_id(page_id, expand='ancestors')
            ancestors = page.get('ancestors', [])
            
            if not ancestors:
                return {
                    "success": False,
                    "error": "该页面没有父页面（可能是根页面）"
                }
            
            # 获取直接父页面（最后一个祖先）
            parent_id = ancestors[-1]['id']
            parent_page = self.confluence.get_page_by_id(parent_id, expand=expand)
            
            return {
                "success": True,
                "data": parent_page
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取父页面失败: {str(e)}"
            }

    def get_descendants(self, page_id: int, depth: Optional[int] = None, expand: str = 'version') -> dict:
        """
        获取所有后代页面（包括子页面、孙页面等）
        
        Args:
            page_id: 页面 ID
            depth: 深度限制（None 表示无限制）
            expand: 扩展字段
            
        Returns:
            后代页面列表
        """
        try:
            descendants = self.confluence.get_page_descendants(
                page_id=page_id,
                depth=depth,
                expand=expand
            )
            return {
                "success": True,
                "data": descendants
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取后代页面失败: {str(e)}"
            }

    def get_space_pages(self, space_key: str, start: int = 0, limit: int = 25, expand: str = 'version') -> dict:
        """
        获取指定空间下的所有页面
        
        Args:
            space_key: 空间键
            start: 起始位置
            limit: 返回数量限制
            expand: 扩展字段
            
        Returns:
            页面列表
        """
        try:
            pages = self.confluence.get_all_pages_from_space(
                space=space_key,
                start=start,
                limit=limit,
                expand=expand
            )
            return {
                "success": True,
                "data": pages
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取空间页面失败: {str(e)}"
            }

    def get_page_with_space(self, space_key: str, page_id: Optional[int] = None, title: Optional[str] = None, expand: str = 'body.storage') -> dict:
        """
        根据空间和 ID 或标题获取页面
        
        Args:
            space_key: 空间键
            page_id: 页面 ID（与 title 二选一）
            title: 页面标题（与 page_id 二选一）
            expand: 扩展字段
            
        Returns:
            页面信息字典
        """
        try:
            if page_id:
                # 先通过 ID 获取页面，然后验证是否属于指定空间
                page = self.confluence.get_page_by_id(page_id, expand=expand)
                if page.get('space', {}).get('key') != space_key:
                    return {
                        "success": False,
                        "error": f"页面 ID {page_id} 不属于空间 {space_key}"
                    }
                return {
                    "success": True,
                    "data": page
                }
            elif title:
                # 通过空间和标题获取页面
                page = self.confluence.get_page_by_title(space=space_key, title=title, expand=expand)
                if page:
                    return {
                        "success": True,
                        "data": page
                    }
                else:
                    return {
                        "success": False,
                        "error": f"在空间 {space_key} 中未找到页面: {title}"
                    }
            else:
                return {
                    "success": False,
                    "error": "必须提供 page_id 或 title 中的一个"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取页面失败: {str(e)}"
            }
