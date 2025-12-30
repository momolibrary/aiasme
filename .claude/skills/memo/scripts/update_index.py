#!/usr/bin/env python3
"""
索引更新脚本 - 自动扫描 memory 目录下的所有 Markdown 文件，
提取二级标题（## 标题），生成或更新 INDEX.md 文件
"""
import os
import glob
import re
from datetime import datetime

def extract_headers(filepath):
    """从 Markdown 文件中提取所有二级标题（##）"""
    headers = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                # 匹配二级标题
                match = re.match(r'^##\s+(.+)$', line.strip())
                if match:
                    headers.append(match.group(1))
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return headers

def build_index():
    """构建索引内容"""
    # 从项目根目录开始查找
    # scripts -> memo -> skills -> .claude -> project_root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..', '..'))
    memory_dir = os.path.join(project_root, 'memory')

    # 扫描所有子目录
    subdirs = ['calendar', 'docs', 'events', 'people', 'ideas', 'deliverables']

    index_content = [
        "# Memory Index\n\n",
        f"> 自动生成的记忆库索引文件\n",
        f"> Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    ]

    for subdir in subdirs:
        subdir_path = os.path.join(memory_dir, subdir)
        if not os.path.exists(subdir_path):
            continue

        pattern = os.path.join(subdir_path, '**/*.md')
        files = sorted(glob.glob(pattern, recursive=True))

        if files:
            index_content.append(f"## 📁 {subdir.capitalize()}\n\n")
            for filepath in files:
                rel_path = os.path.relpath(filepath, memory_dir)
                filename = os.path.basename(filepath)
                basename = os.path.splitext(filename)[0]
                headers = extract_headers(filepath)

                index_content.append(f"### {basename}\n")
                index_content.append(f"- 文件: `{rel_path}`\n")

                if headers:
                    index_content.append("- 包含主题:\n")
                    for header in headers[:5]:  # 只显示前5个标题
                        index_content.append(f"  - {header}\n")

                index_content.append("\n")

            index_content.append("---\n\n")

    return ''.join(index_content)

def main():
    """主函数"""
    # scripts -> memo -> skills -> .claude -> project_root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..', '..'))
    memory_dir = os.path.join(project_root, 'memory')
    index_path = os.path.join(memory_dir, 'INDEX.md')

    # 生成索引内容
    content = build_index()

    # 写入文件
    try:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 索引已更新: {index_path}")
    except Exception as e:
        print(f"✗ 更新索引失败: {e}")
        return 1

    return 0

if __name__ == '__main__':
    exit(main())
