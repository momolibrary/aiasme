#!/usr/bin/env python3
"""
全文检索脚本 - 在记忆库中搜索关键词，返回最相关的内容
"""
import sys
import re
import glob
import os

def search_memories(keyword, limit=10):
    """搜索记忆库中的关键词"""
    # 获取 memory 目录的绝对路径
    # scripts -> memo -> skills -> .claude -> project_root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..', '..'))
    memory_dir = os.path.join(project_root, 'memory')
    pattern = os.path.join(memory_dir, '**/*.md')

    files = glob.glob(pattern, recursive=True)
    hits = []

    for filepath in files:
        # 跳过 INDEX.md
        if os.path.basename(filepath) == 'INDEX.md':
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # 不区分大小写搜索
                for match in re.finditer(re.escape(keyword), content, re.IGNORECASE):
                    # 提取匹配上下文（前后各 60 个字符）
                    start = max(0, match.start() - 60)
                    end = min(len(content), match.end() + 60)
                    context = content[start:end].replace('\n', ' ')

                    # 相对路径更友好
                    rel_path = os.path.relpath(filepath, memory_dir)
                    hits.append((rel_path, context))
        except Exception as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)

    # 返回限定数量的结果
    return hits[:limit]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python search.py <keyword> [limit]")
        sys.exit(1)

    keyword = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    results = search_memories(keyword, limit)

    if not results:
        print(f"未找到包含「{keyword}」的内容")
    else:
        print(f"找到 {len(results)} 条相关记忆：\n")
        for i, (filepath, context) in enumerate(results, 1):
            print(f"{i}. [{filepath}]")
            print(f"   {context}\n")
