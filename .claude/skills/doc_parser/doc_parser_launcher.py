#!/usr/bin/env python3
"""
Doc Parser MCP 包装脚本
安全地获取知言token并启动doc-parser MCP服务
"""

import os
import json
import sys
import subprocess
from pathlib import Path

class DocParserMCPLauncher:
    """Doc Parser MCP服务启动器"""

    def __init__(self):
        # 使用与feishu_reader相同的配置
        config_dir = Path.home() / '.claude' / 'feishu'
        config_file = config_dir / 'config.json'
        self.config_file = config_file

    def get_zhiyan_token(self) -> str:
        """获取知言token，生产环境优先"""
        try:
            if not self.config_file.exists():
                raise FileNotFoundError(f"配置文件不存在: {self.config_file}")

            with open(self.config_file, 'r') as f:
                config = json.load(f)

            # 优先查找生产环境的token
            for key, value in config.items():
                if value.get('service') == 'zhiyan':
                    token = value.get('token')
                    if token:
                        return token

            # 如果没找到zhiyan服务，使用default服务
            for key, value in config.items():
                if value.get('service') == 'default':
                    token = value.get('token')
                    if token:
                        print("⚠️  使用默认服务token，建议设置zhiyan专用token", file=sys.stderr)
                        return token

            raise ValueError("未找到有效的知言token")

        except Exception as e:
            print(f"❌ 获取token失败: {e}", file=sys.stderr)
            print("💡 请先使用 feishu_reader skill 设置token", file=sys.stderr)
            sys.exit(1)

    def get_user_name(self) -> str:
        """获取用户名，优先使用环境变量"""
        user_name = os.getenv('USER_NAME', 'zhuangdesheng')
        return user_name

    def launch_mcp(self):
        """启动doc-parser MCP服务"""
        try:
            # 获取安全配置
            token = self.get_zhiyan_token()
            user_name = self.get_user_name()

            # 设置环境变量
            env = os.environ.copy()
            env['Authorization'] = f'Bearer {token}'
            env['NPM_CONFIG_REGISTRY'] = 'https://rnpm.chehejia.com'
            env['USER_NAME'] = user_name

            # 启动 MCP 服务
            cmd = [
                'npx', '-y', '@chehejia/doc-parser@latest'
            ]

            # 执行命令
            process = subprocess.Popen(cmd, env=env)

            # 等待进程结束
            process.wait()

        except FileNotFoundError:
            print("❌ 未找到npx命令，请确保已安装Node.js和npm", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"❌ 启动MCP服务失败: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("Doc Parser MCP 启动器")
        print("自动获取知言token并启动doc-parser MCP服务")
        print()
        print("用法:")
        print("  python3 doc_parser_launcher.py")
        print()
        print("配置:")
        print("  - Token从 ~/.claude/feishu/config.json 读取（与feishu_reader共享）")
        print("  - 用户名从环境变量 USER_NAME 获取，默认为 zhuangdesheng")
        sys.exit(0)

    launcher = DocParserMCPLauncher()
    launcher.launch_mcp()