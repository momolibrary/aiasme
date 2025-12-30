#!/usr/bin/env python3
"""
全文检索脚本 - 在记忆库中搜索关键词，返回最相关的 3 段内容
"""
import sys
import re
import glob
import os

def search_memories(keyword):
    """搜索记忆库中的关键词"""
    # 获取 references 目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    refs_dir = os.path.join(script_dir, '..', 'references')
    pattern = os.path.join(refs_dir, '*.md')

    files = glob.glob(pattern)
    hits = []

    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # 不区分大小写搜索
                for match in re.finditer(re.escape(keyword), content, re.IGNORECASE):
                    # 提取匹配上下文（前后各 40 个字符）
                    start = max(0, match.start() - 40)
                    end = min(len(content), match.end() + 40)
                    context = content[start:end].replace('\n', ' ')
                    hits.append((filepath, context))
        except Exception as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)

    # 返回前 3 个结果
    return hits[:3]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python search.py <keyword>")
        sys.exit(1)

    keyword = sys.argv[1]
    results = search_memories(keyword)

    if not results:
        print(f"未找到包含「{keyword}」的内容")
    else:
        print(f"找到 {len(results)} 条相关记忆：\n")
        for i, (filepath, context) in enumerate(results, 1):
            filename = os.path.basename(filepath)
            print(f"{i}. [{filename}]")
            print(f"   {context}\n")
