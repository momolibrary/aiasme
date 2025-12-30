#!/usr/bin/env python3
"""
索引更新脚本 - 自动扫描 references 目录下的所有 Markdown 文件，
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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    refs_dir = os.path.join(script_dir, '..', 'references')
    pattern = os.path.join(refs_dir, '*.md')

    files = sorted(glob.glob(pattern))

    # 排除 INDEX.md 本身
    files = [f for f in files if os.path.basename(f) != 'INDEX.md']

    index_content = [
        "# 记忆库索引\n",
        f"*最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n",
        "\n---\n\n"
    ]

    if not files:
        index_content.append("目前记忆库为空。\n")
    else:
        for filepath in files:
            filename = os.path.basename(filepath)
            basename = os.path.splitext(filename)[0]
            headers = extract_headers(filepath)

            index_content.append(f"## {basename}\n")
            index_content.append(f"文件: `{filename}`\n\n")

            if headers:
                index_content.append("包含主题:\n")
                for header in headers:
                    index_content.append(f"- {header}\n")
            else:
                index_content.append("*（暂无内容）*\n")

            index_content.append("\n")

    return ''.join(index_content)

def main():
    """主函数"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    refs_dir = os.path.join(script_dir, '..', 'references')
    index_path = os.path.join(refs_dir, 'INDEX.md')

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
