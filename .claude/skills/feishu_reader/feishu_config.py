#!/usr/bin/env python3
"""
飞书文档读取器配置管理
安全地管理API token和相关配置
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any

class FeishuConfig:
    """安全的飞书API配置管理"""

    def __init__(self):
        self.config_dir = Path.home() / '.claude' / 'feishu'
        self.config_file = self.config_dir / 'config.json'
        self._ensure_config_dir()

    def _ensure_config_dir(self):
        """确保配置目录存在"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        # 设置目录权限为仅用户可读写
        os.chmod(self.config_dir, 0o700)

    def _get_config_key(self, service: str) -> str:
        """生成配置键的哈希值，避免明文存储"""
        return hashlib.sha256(f"feishu_{service}".encode()).hexdigest()[:16]

    def save_token(self, token: str, service_name: str = "default") -> bool:
        """安全保存token"""
        try:
            config = self._load_config()
            config_key = self._get_config_key(service_name)
            config[config_key] = {
                "token": token,
                "created_at": str(Path.home()),
                "service": service_name
            }

            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            os.chmod(self.config_file, 0o600)
            return True
        except Exception:
            return False

    def get_token(self, service_name: str = "default") -> Optional[str]:
        """获取token"""
        try:
            config = self._load_config()
            config_key = self._get_config_key(service_name)
            return config.get(config_key, {}).get("token")
        except Exception:
            return None

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.config_file.exists():
            return {}

        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def setup_initial_token(self, non_interactive: bool = False) -> bool:
        """设置初始token（如果是首次使用）"""
        if self.get_token():
            return True  # token已存在

        if non_interactive:
            print("❌ 非交互模式需要预先配置Token")
            print("💡 请先在交互模式下设置Token，或设置环境变量FEISHU_TOKEN")
            return False

        print("🔑 首次使用，需要设置飞书API Token")
        print("请从知言平台获取你的API Token:")
        print("1. 访问知言平台")
        print("2. 点击头像 → API调用")
        print("3. 选择IDaaS应用或Secret API Key")
        print("4. 复制生成的Token")

        try:
            token = input("\n请输入你的Token: ").strip()
        except EOFError:
            print("❌ 检测到非交互环境，无法设置Token")
            print("💡 请设置环境变量 FEISHU_TOKEN 或在交互模式下运行")
            return False

        if not token:
            print("❌ Token不能为空")
            return False

        if self.save_token(token):
            print("✅ Token设置成功")
            return True
        else:
            print("❌ Token保存失败")
            return False

    def get_token_from_env(self) -> Optional[str]:
        """从环境变量获取token"""
        return os.getenv('FEISHU_TOKEN')

    def get_token_with_fallback(self, service_name: str = "default") -> Optional[str]:
        """获取token，支持多种方式"""
        # 优先级：直接配置 > 环境变量
        token = self.get_token(service_name)
        if not token:
            token = self.get_token_from_env()
        return token

    def get_api_base_url(self, test_mode: bool = True) -> str:
        """获取API基础URL"""
        if test_mode:
            return "https://cfe-doc-backend-test.inner.chj.cloud/openapi"
        else:
            return "https://cfe-doc-backend.inner.chj.cloud/openapi"