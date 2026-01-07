#!/usr/bin/env python3
"""
飞书文档读取器日志系统
记录文档提取任务的详细过程
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class TaskRecord:
    """任务记录"""
    task_id: Optional[str] = None
    doc_url: str = ""
    doc_name: str = ""
    status: str = "init"
    created_at: str = ""
    started_at: str = ""
    completed_at: str = ""
    duration: float = 0.0
    content_length: int = 0
    error_message: str = ""
    images_count: int = 0
    saved_path: str = ""

class FeishuLogger:
    """飞书文档读取日志管理器"""

    def __init__(self):
        self.log_dir = Path.home() / '.claude' / 'feishu' / 'logs'
        self.log_file = self.log_dir / f'feishu_tasks_{datetime.now().strftime("%Y%m")}.json'
        self._ensure_log_dir()

    def _ensure_log_dir(self):
        """确保日志目录存在"""
        self.log_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(self.log_dir, 0o700)

    def start_task(self, doc_url: str) -> TaskRecord:
        """开始新任务记录"""
        record = TaskRecord(
            doc_url=doc_url,
            status="started",
            created_at=datetime.now().isoformat(),
            started_at=datetime.now().isoformat()
        )
        self._log_info(f"开始处理飞书文档: {doc_url}")
        return record

    def update_task(self, record: TaskRecord, **kwargs):
        """更新任务记录"""
        for key, value in kwargs.items():
            if hasattr(record, key):
                setattr(record, key, value)

        if record.status in ["done", "failed"]:
            record.completed_at = datetime.now().isoformat()
            if record.started_at:
                start_time = datetime.fromisoformat(record.started_at)
                record.duration = (datetime.now() - start_time).total_seconds()

        self._save_record(record)
        self._log_status(record)

    def complete_task(self, record: TaskRecord, content: str, doc_name: str = ""):
        """完成任务记录"""
        record.status = "done"
        record.content_length = len(content)
        if doc_name:
            record.doc_name = doc_name
        self.update_task(record)
        self._log_success(record)

    def fail_task(self, record: TaskRecord, error_message: str):
        """任务失败记录"""
        record.status = "failed"
        record.error_message = error_message
        self.update_task(record)
        self._log_error(record, error_message)

    def _save_record(self, record: TaskRecord):
        """保存任务记录到文件"""
        try:
            records = self._load_records()
            records[record.task_id or str(time.time())] = asdict(record)

            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(records, f, indent=2, ensure_ascii=False)
            os.chmod(self.log_file, 0o600)
        except Exception as e:
            self._log_error(f"保存日志失败: {e}")

    def _load_records(self) -> Dict[str, Any]:
        """加载历史记录"""
        if not self.log_file.exists():
            return {}

        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def _log_info(self, message: str):
        """记录信息日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[INFO] {timestamp} - {message}")

    def _log_status(self, record: TaskRecord):
        """记录状态更新"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[STATUS] {timestamp} - 任务 {record.task_id} - {record.status}")

    def _log_success(self, record: TaskRecord):
        """记录成功完成"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration_text = f"{record.duration:.1f}秒" if record.duration else ""
        print(f"✅ [SUCCESS] {timestamp} - 文档 '{record.doc_name}' 处理完成 ({duration_text})")

    def _log_error(self, record_or_message, error_message: str = ""):
        """记录错误"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(record_or_message, TaskRecord):
            print(f"❌ [ERROR] {timestamp} - 任务 {record_or_message.task_id} 失败: {error_message}")
        else:
            print(f"❌ [ERROR] {timestamp} - {record_or_message}")

    def get_recent_tasks(self, limit: int = 10) -> list:
        """获取最近的任务记录"""
        records = self._load_records()
        sorted_records = sorted(
            records.items(),
            key=lambda x: x[1].get('created_at', ''),
            reverse=True
        )
        return sorted_records[:limit]

    def print_task_history(self, limit: int = 5):
        """打印任务历史"""
        recent_tasks = self.get_recent_tasks(limit)
        if not recent_tasks:
            print("📝 暂无任务历史")
            return

        print(f"\n📋 最近 {len(recent_tasks)} 个任务:")
        print("-" * 80)
        for task_id, record in recent_tasks:
            status_icon = "✅" if record.get('status') == 'done' else "❌" if record.get('status') == 'failed' else "⏳"
            doc_name = record.get('doc_name', '未知文档')[:30]
            duration = record.get('duration', 0)
            time_text = f"{duration:.1f}s" if duration else "N/A"

            print(f"{status_icon} {doc_name:30} | {record.get('status', 'unknown'):6} | {time_text:>5} | {task_id[:8]}...")

    def print_statistics(self):
        """打印统计信息"""
        records = self._load_records()
        if not records:
            print("📊 暂无统计数据")
            return

        total_tasks = len(records)
        success_tasks = sum(1 for r in records.values() if r.get('status') == 'done')
        failed_tasks = sum(1 for r in records.values() if r.get('status') == 'failed')
        total_content = sum(r.get('content_length', 0) for r in records.values())
        avg_duration = sum(r.get('duration', 0) for r in records.values() if r.get('duration')) / max(success_tasks, 1)

        print(f"\n📊 任务统计:")
        print(f"总任务数: {total_tasks}")
        print(f"成功: {success_tasks} | 失败: {failed_tasks}")
        print(f"成功率: {(success_tasks/total_tasks*100):.1f}%" if total_tasks > 0 else "N/A")
        print(f"总内容长度: {total_content:,} 字符")
        print(f"平均处理时间: {avg_duration:.1f}秒")

# 全局日志实例
logger = FeishuLogger()