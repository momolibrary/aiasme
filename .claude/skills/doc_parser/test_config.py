#!/usr/bin/env python3
"""
Doc Parser 配置测试脚本
验证 Token 获取、权限设置和MCP配置是否正确
"""

import os
import json
import sys
from pathlib import Path

def test_token_config():
    """测试token配置"""
    print("🔑 测试Token配置...")

    config_file = Path.home() / '.claude' / 'feishu' / 'config.json'

    if not config_file.exists():
        print("❌ 配置文件不存在:", config_file)
        return False

    try:
        with open(config_file, 'r') as f:
            config = json.load(f)

        # 查找zhiyan服务的token
        zhiyan_token = None
        default_token = None

        for key, value in config.items():
            if value.get('service') == 'zhiyan':
                zhiyan_token = value.get('token')
            elif value.get('service') == 'default':
                default_token = value.get('token')

        token = zhiyan_token or default_token

        if not token:
            print("❌ 未找到有效的token")
            return False

        if not token.startswith('app-'):
            print("⚠️  Token格式可能不正确，应以'app-'开头")

        print("✅ Token配置正确")
        return True

    except Exception as e:
        print("❌ 无法读取配置文件:", e)
        return False

def test_launcher_script():
    """测试启动脚本"""
    print("\n🚀 测试启动脚本...")

    script_path = Path('.claude/skills/doc_parser/doc_parser_launcher.py')

    if not script_path.exists():
        print("❌ 启动脚本不存在:", script_path)
        return False

    if not os.access(script_path, os.X_OK):
        print("⚠️  启动脚本不可执行，正在修复...")
        os.chmod(script_path, 0o755)

    print("✅ 启动脚本配置正确")
    return True

def test_mcp_config():
    """测试MCP配置"""
    print("\n📋 测试MCP配置...")

    mcp_file = Path('.mcp.json')

    if not mcp_file.exists():
        print("❌ MCP配置文件不存在:", mcp_file)
        return False

    try:
        with open(mcp_file, 'r') as f:
            mcp_config = json.load(f)

        doc_parser_config = mcp_config.get('mcpServers', {}).get('doc-parser')

        if not doc_parser_config:
            print("❌ 未找到doc-parser配置")
            return False

        if doc_parser_config.get('command') != 'python3':
            print("❌ 命令配置错误")
            return False

        if '.claude/skills/doc_parser/doc_parser_launcher.py' not in str(doc_parser_config.get('args', [])):
            print("❌ 参数配置错误")
            return False

        print("✅ MCP配置正确")
        return True

    except Exception as e:
        print("❌ 无法读取MCP配置:", e)
        return False

def test_permissions():
    """测试权限配置"""
    print("\n🔒 测试权限配置...")

    settings_file = Path('.claude/settings.local.json')

    if not settings_file.exists():
        print("❌ 权限配置文件不存在:", settings_file)
        return False

    try:
        with open(settings_file, 'r') as f:
            settings = json.load(f)

        allowed = settings.get('permissions', {}).get('allow', [])

        if 'Skill(doc_parser)' not in allowed:
            print("❌ 缺少Skill(doc_parser)权限")
            return False

        has_mcp_tools = any('mcp__doc-parser__' in perm for perm in allowed)
        if not has_mcp_tools:
            print("❌ 缺少MCP工具权限")
            return False

        print("✅ 权限配置正确")
        return True

    except Exception as e:
        print("❌ 无法读取权限配置:", e)
        return False

def test_files_structure():
    """测试文件结构"""
    print("\n📁 测试文件结构...")

    required_files = [
        '.claude/skills/doc_parser/SKILL.md',
        '.claude/skills/doc_parser/README.md',
        '.claude/skills/doc_parser/doc_parser_launcher.py'
    ]

    for file_path in required_files:
        if not Path(file_path).exists():
            print("❌ 文件不存在:", file_path)
            return False

    print("✅ 文件结构正确")
    return True

def main():
    """主测试函数"""
    print("🧪 Doc Parser 配置测试开始...")
    print("=" * 50)

    tests = [
        ("文件结构", test_files_structure),
        ("Token配置", test_token_config),
        ("启动脚本", test_launcher_script),
        ("MCP配置", test_mcp_config),
        ("权限配置", test_permissions)
    ]

    all_passed = True

    for test_name, test_func in tests:
        try:
            if not test_func():
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name}测试异常:", e)
            all_passed = False

    print("\n" + "=" * 50)

    if all_passed:
        print("🎉 所有测试通过！Doc Parser skill 配置正确")
        print("\n📝 下一步操作：")
        print("1. 重启Claude Code以加载新的MCP服务")
        print("2. 运行 'claude mcp list' 验证doc-parser服务状态")
        print("3. 开始使用: @skill doc_parser 解析文档 <path>")
    else:
        print("❌ 部分测试失败，请检查配置")
        sys.exit(1)

if __name__ == '__main__':
    main()