#!/usr/bin/env python3
"""
飞书文档处理器
支持文档提取、图片本地化、markdown保存等功能
"""

import os
import re
import time
import requests
import hashlib
from pathlib import Path
from typing import Optional, List, Tuple
from urllib.parse import urlparse
import base64
from datetime import datetime

from feishu_config import FeishuConfig
from feishu_logger import logger, TaskRecord

class FeishuProcessor:
    """飞书文档处理器"""

    def __init__(self, test_mode: bool = True):
        self.config = FeishuConfig()
        self.api_base_url = self.config.get_api_base_url(test_mode)
        self.token = None
        self.output_dir = Path.cwd() / "feishu_docs"
        self.images_dir = self.output_dir / "images"
        self._ensure_output_dirs()

    def _ensure_output_dirs(self):
        """确保输出目录存在"""
        self.output_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)

    def initialize(self, non_interactive: bool = False) -> bool:
        """初始化处理器"""
        # 首先尝试获取已有的token
        self.token = self.config.get_token_with_fallback()

        if self.token:
            logger._log_info("✅ 使用已配置的Token")
            return True

        # 如果没有token，尝试设置
        if not self.config.setup_initial_token(non_interactive):
            if non_interactive:
                logger._log_error("❌ 非交互模式需要预先配置Token。请设置环境变量FEISHU_TOKEN或先在交互模式下配置")
                return False
            else:
                logger._log_error("❌ Token设置失败")
                return False

        # 重新获取token
        self.token = self.config.get_token_with_fallback()
        if not self.token:
            logger._log_error("❌ 无法获取Token")
            return False

        return True

    def _get_headers(self) -> dict:
        """获取请求头"""
        return {
            'Authorization': f'Bearer {self.token}',
            'User-Agent': 'Claude-Feishu-Doc-Reader/1.0'
        }

    def validate_feishu_url(self, url: str) -> bool:
        """验证飞书文档URL"""
        return (url.startswith('https://li.feishu.cn/docx/') or
                url.startswith('https://li.feishu.cn/wiki/'))

    def submit_extraction_task(self, doc_url: str) -> Optional[str]:
        """提交文档提取任务"""
        submit_url = f'{self.api_base_url}/v1/extract/task/submit'

        files = {
            'file_key': (None, doc_url),
            'task_type': (None, 'feishu'),
            'table_return_type': (None, 'md'),
            'table_merge_style': (None, 'empty')
        }

        try:
            response = requests.post(submit_url, headers=self._get_headers(), files=files, timeout=30)
            response.raise_for_status()

            task_data = response.json().get('data', {})
            return str(task_data.get('id'))

        except Exception as e:
            logger._log_error(f"提交任务失败: {e}")
            return None

    def check_task_status(self, task_id: str, max_retries: int = 60, retry_interval: int = 2) -> Optional[str]:
        """检查任务状态"""
        url = f'{self.api_base_url}/v1/extract/task/status'

        for i in range(max_retries):
            try:
                response = requests.get(url, headers=self._get_headers(), params={'task_id': task_id})

                if response.status_code == 200:
                    data = response.json().get('data', {})
                    status = data.get('state')

                    if status == 'done':
                        logger._log_info(f"任务 {task_id} 完成")
                        return 'done'
                    elif status == 'failed':
                        error_msg = data.get('error_message', '未知错误')
                        logger._log_error(f"任务 {task_id} 失败: {error_msg}")
                        return 'failed'
                    elif status in ['running', 'init']:
                        progress = data.get('progress', 0)
                        logger._log_info(f"任务 {task_id} 进行中... {progress}%")
                        time.sleep(retry_interval)
                    else:
                        time.sleep(retry_interval)
                else:
                    time.sleep(retry_interval)

            except Exception as e:
                logger._log_error(f"检查状态失败: {e}")
                time.sleep(retry_interval)

        logger._log_error(f"任务 {task_id} 超时")
        return None

    def get_task_result(self, task_id: str) -> Optional[dict]:
        """获取任务结果"""
        url = f'{self.api_base_url}/v1/extract/task/{task_id}'

        try:
            response = requests.get(url, headers=self._get_headers(), timeout=30)
            response.raise_for_status()
            return response.json().get('data', {})

        except Exception as e:
            logger._log_error(f"获取任务结果失败: {e}")
            return None

    def download_content(self, download_url: str) -> Optional[str]:
        """下载文档内容"""
        try:
            response = requests.get(download_url, headers=self._get_headers(), timeout=30)
            response.raise_for_status()
            return response.text

        except Exception as e:
            logger._log_error(f"下载内容失败: {e}")
            return None

    def extract_images_from_markdown(self, content: str) -> Tuple[str, List[str]]:
        """从markdown中提取图片链接"""
        # 匹配markdown图片格式: ![alt](url)
        img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

        images = []
        updated_content = content

        for match in re.finditer(img_pattern, content):
            alt_text = match.group(1)
            img_url = match.group(2)

            # 只处理http/https链接
            if img_url.startswith(('http://', 'https://')):
                images.append(img_url)

        return updated_content, images

    def download_image(self, img_url: str, doc_name: str) -> Optional[str]:
        """下载图片并保存到本地"""
        try:
            response = requests.get(img_url, timeout=30)
            response.raise_for_status()

            # 从URL中获取文件扩展名
            parsed_url = urlparse(img_url)
            ext = os.path.splitext(parsed_url.path)[1]
            if not ext:
                # 尝试从Content-Type获取扩展名
                content_type = response.headers.get('content-type', '')
                if 'jpeg' in content_type:
                    ext = '.jpg'
                elif 'png' in content_type:
                    ext = '.png'
                elif 'gif' in content_type:
                    ext = '.gif'
                else:
                    ext = '.jpg'  # 默认

            # 生成唯一文件名
            url_hash = hashlib.md5(img_url.encode()).hexdigest()[:8]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{doc_name}_{timestamp}_{url_hash}{ext}"
            filepath = self.images_dir / filename

            with open(filepath, 'wb') as f:
                f.write(response.content)

            logger._log_info(f"图片已保存: {filepath}")
            return str(filepath)

        except Exception as e:
            logger._log_error(f"下载图片失败 {img_url}: {e}")
            return None

    def localize_images(self, content: str, doc_name: str) -> Tuple[str, int]:
        """本地化图片"""
        updated_content = content
        _, img_urls = self.extract_images_from_markdown(content)
        localized_count = 0

        for img_url in img_urls:
            local_path = self.download_image(img_url, doc_name)
            if local_path:
                # 替换markdown中的图片链接为本地相对路径
                relative_path = Path(local_path).relative_to(self.output_dir)
                updated_content = updated_content.replace(img_url, str(relative_path))
                localized_count += 1

        return updated_content, localized_count

    def save_markdown(self, content: str, doc_name: str, suffix: str = "") -> str:
        """保存markdown文件"""
        # 清理文档名称
        safe_doc_name = re.sub(r'[^\w\s-]', '', doc_name)[:50]
        safe_doc_name = re.sub(r'[-\s]+', '_', safe_doc_name)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if suffix:
            filename = f"{safe_doc_name}_{suffix}_{timestamp}.md"
        else:
            filename = f"{safe_doc_name}_{timestamp}.md"

        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger._log_info(f"Markdown文件已保存: {filepath}")
        return str(filepath)

    def process_document(self, doc_url: str, save_to_file: bool = True,
                        localize_images: bool = False) -> Optional[dict]:
        """处理飞书文档的完整流程"""

        # 开始任务记录
        record = logger.start_task(doc_url)

        try:
            # 验证URL
            if not self.validate_feishu_url(doc_url):
                logger.fail_task(record, "无效的飞书文档URL")
                return None

            # 提交任务
            logger._log_info("提交文档提取任务...")
            task_id = self.submit_extraction_task(doc_url)

            if not task_id:
                logger.fail_task(record, "提交任务失败")
                return None

            record.task_id = task_id
            logger.update_task(record, task_id=task_id, status="submitted")

            # 等待任务完成
            logger._log_info("等待任务处理完成...")
            status = self.check_task_status(task_id)

            if status != 'done':
                logger.fail_task(record, f"任务未成功完成: {status}")
                return None

            logger.update_task(record, status="processing_completed")

            # 获取任务结果
            logger._log_info("获取任务结果...")
            task_data = self.get_task_result(task_id)

            if not task_data:
                logger.fail_task(record, "获取任务结果失败")
                return None

            # 下载内容
            logger._log_info("下载文档内容...")
            # 使用 full_md_link 字段获取下载路径
            md_link = task_data.get('full_md_link', '')
            if not md_link:
                logger.fail_task(record, "API响应中没有full_md_link字段")
                return None

            # 构建下载URL：移除api_base_url末尾的/openapi，使用md_link中的路径
            base_url = self.api_base_url.rstrip('/openapi')
            download_url = f"{base_url}{md_link}"
            content = self.download_content(download_url)

            if not content:
                logger.fail_task(record, "下载内容失败")
                return None

            doc_name = task_data.get('file_name', 'untitled_document')
            original_content = content
            images_count = 0
            saved_path = ""

            # 图片本地化
            if localize_images:
                logger._log_info("本地化图片...")
                content, images_count = self.localize_images(content, doc_name)

            # 保存到文件
            if save_to_file:
                suffix = "localized" if localize_images else "extracted"
                saved_path = self.save_markdown(content, doc_name, suffix)

                # 更新记录
                record.images_count = images_count
                record.saved_path = saved_path
                logger.complete_task(record, content, doc_name)

            # 构建返回结果
            result = {
                'task_id': task_id,
                'doc_name': doc_name,
                'doc_url': doc_url,
                'content': content,
                'original_content': original_content,
                'content_length': len(content),
                'images_count': images_count,
                'saved_path': saved_path,
                'status': 'success',
                'created_at': datetime.now().isoformat()
            }

            logger._log_success(record)
            return result

        except Exception as e:
            logger.fail_task(record, str(e))
            return None

    def print_task_history(self, limit: int = 5):
        """打印任务历史"""
        logger.print_task_history(limit)

    def print_statistics(self):
        """打印统计信息"""
        logger.print_statistics()