#!/usr/bin/env python3
"""
新建1on1周度汇报文档

用法:
    python3 .claude/scripts/new_1on1.py                    # 使用今天日期
    python3 .claude/scripts/new_1on1.py 2026-01-13         # 指定日期
    python3 .claude/scripts/new_1on1.py --copy-last        # 复制上一次的内容作为草稿
"""

import sys
from datetime import datetime
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent.parent
MEETINGS_DIR = ROOT_DIR / "memory" / "events" / "meetings" / "1on1-沈嵘"
TEMPLATE_PATH = ROOT_DIR / ".claude" / "skills" / "memo" / "assets" / "1on1-template.md"


def get_date():
    """获取日期"""
    if len(sys.argv) > 1 and sys.argv[1] != '--copy-last':
        date_str = sys.argv[1]
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print(f"❌ 日期格式错误: {date_str}，应为 YYYY-MM-DD")
            sys.exit(1)
    return datetime.now().strftime("%Y-%m-%d")


def get_last_1on1():
    """获取最近一次的1on1文档"""
    if not MEETINGS_DIR.exists():
        return None

    files = sorted([f for f in MEETINGS_DIR.glob("*.md") if f.stem.startswith("20")])
    return files[-1] if files else None


def create_new_1on1(date_str, copy_last=False):
    """创建新的1on1文档"""
    filename = f"{date_str}-研发域信息同步.md"
    filepath = MEETINGS_DIR / filename

    if filepath.exists():
        print(f"⚠️  文件已存在: {filepath}")
        response = input("是否覆盖? (y/N): ")
        if response.lower() != 'y':
            print("❌ 已取消")
            return

    # 确保目录存在
    MEETINGS_DIR.mkdir(parents=True, exist_ok=True)

    # 生成内容
    if copy_last:
        last_file = get_last_1on1()
        if last_file:
            content = last_file.read_text(encoding='utf-8')
            print(f"📋 已复制上次内容: {last_file.name}")
        else:
            print("⚠️  未找到上次的文档，使用空模板")
            content = ""
    else:
        # 使用空模板或创建空文件
        if TEMPLATE_PATH.exists():
            content = TEMPLATE_PATH.read_text(encoding='utf-8')
        else:
            content = ""

    # 写入文件
    filepath.write_text(content, encoding='utf-8')

    print(f"✅ 已创建文件: {filepath}")
    print(f"\n📝 相对路径: memory/events/meetings/1on1-沈嵘/{filename}")
    print(f"\n💡 提示:")
    print(f"   - 直接编辑文档，添加需要向沈嵘汇报的重点事项")
    print(f"   - 格式: ## 议题标题 + 自由叙述内容")
    print(f"   - 使用 @人名 提及相关人员")
    print(f"   - 完成后运行: python3 .claude/skills/memo/scripts/update_index.py")

    # 输出最近的文档列表
    print(f"\n📚 最近的1on1记录:")
    recent_files = sorted([f for f in MEETINGS_DIR.glob("*.md") if f.stem.startswith("20")])[-5:]
    for f in recent_files:
        marker = "👈 NEW" if f == filepath else ""
        print(f"   - {f.name} {marker}")


def main():
    copy_last = '--copy-last' in sys.argv
    date_str = get_date()

    print("🚀 创建新的1on1周度汇报")
    print(f"📅 日期: {date_str}")
    print(f"📂 目录: memory/events/meetings/1on1-沈嵘/")
    print("")

    create_new_1on1(date_str, copy_last)


if __name__ == "__main__":
    main()
