#!/usr/bin/env python3
"""
飞书文档读取器 - 主入口文件
Feishu Document Reader - Main Entry Point

这是一个功能完整的飞书文档读取器，基于知言平台API，支持：
- 安全的token管理
- 详细的日志记录
- 图片本地化
- Markdown文件导出
- 任务历史和统计
"""

import sys
import os
import argparse
import json
from pathlib import Path

# 确保模块路径正确
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from feishu_processor import FeishuProcessor

def print_banner():
    """打印程序横幅"""
    print("🚀 飞书文档读取器 (Feishu Document Reader)")
    print("📋 基于知言平台API | 支持图片本地化 & Markdown导出")
    print("=" * 60)

def print_help_examples():
    """打印使用示例"""
    print("\n📖 使用示例:")
    print("  python3 feishu_reader.py https://li.feishu.cn/docx/document_id")
    print("  python3 feishu_reader.py --save --localize-images https://li.feishu.cn/wiki/page_id")
    print("  python3 feishu_reader.py --history")
    print("  python3 feishu_reader.py --stats")
    print("\n🔧 参数说明:")
    print("  url: 飞书文档URL")
    print("  --save, -s: 保存为markdown文件")
    print("  --localize-images, -li: 本地化图片")
    print("  --history, -h: 显示任务历史")
    print("  --stats: 显示统计信息")
    print("  --test: 使用测试环境 (默认)")
    print("  --prod: 使用生产环境")
    print("  --help: 显示帮助信息")
    print("\n🔑 Token配置:")
    print("  首次使用会引导设置token，或设置环境变量 FEISHU_TOKEN")
    print("  详细配置说明请参考 README.md")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='飞书文档读取器 - 读取并提取飞书文档内容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s https://li.feishu.cn/docx/document_id
  %(prog)s --save --localize-images https://li.feishu.cn/wiki/page_id
  %(prog)s --history
  %(prog)s --stats
        '''
    )

    parser.add_argument('url', nargs='?', help='飞书文档URL (支持docx和wiki格式)')
    parser.add_argument('--save', '-s', action='store_true',
                       help='保存提取的内容为markdown文件')
    parser.add_argument('--localize-images', '-li', action='store_true',
                       help='下载并本地化文档中的图片')
    parser.add_argument('--history', action='store_true',
                       help='显示最近的任务历史记录')
    parser.add_argument('--stats', action='store_true',
                       help='显示处理统计信息')
    parser.add_argument('--test', action='store_true', default=True,
                       help='使用测试API环境 (默认)')
    parser.add_argument('--prod', action='store_true',
                       help='使用生产API环境')
    parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')

    args = parser.parse_args()

    # 显示横幅
    print_banner()

    # 环境设置
    test_mode = args.test and not args.prod

    try:
        # 创建处理器
        processor = FeishuProcessor(test_mode=test_mode)

        # 初始化 (非交互模式)
        if not processor.initialize(non_interactive=True):
            print("❌ 初始化失败")
            return 1

        # 显示统计信息
        if args.stats:
            print("\n📊 处理统计信息:")
            print("-" * 30)
            processor.print_statistics()
            return 0

        # 显示历史记录
        if args.history:
            print("\n📋 任务历史记录:")
            print("-" * 30)
            processor.print_task_history(10)
            return 0

        # 处理文档
        if not args.url:
            print("❌ 错误: 请提供飞书文档URL")
            print_help_examples()
            return 1

        # 验证URL格式
        if not processor.validate_feishu_url(args.url):
            print("❌ 错误: 无效的飞书文档URL格式")
            print("💡 支持的格式:")
            print("   - https://li.feishu.cn/docx/...")
            print("   - https://li.feishu.cn/wiki/...")
            return 1

        print(f"🔍 开始处理飞书文档:")
        print(f"📄 URL: {args.url}")
        print(f"🌍 环境: {'测试环境' if test_mode else '生产环境'}")
        print(f"💾 保存文件: {'是' if args.save else '否'}")
        print(f"🖼️ 图片本地化: {'是' if args.localize_images else '否'}")
        print()

        # 处理文档
        result = processor.process_document(
            args.url,
            save_to_file=args.save,
            localize_images=args.localize_images
        )

        if result:
            # 显示成功结果
            print("✅ 文档处理完成!")
            print("=" * 60)
            print(f"📋 文档名称: {result['doc_name']}")
            print(f"📏 内容长度: {result['content_length']:,} 字符")
            print(f"🖼️ 图片数量: {result['images_count']} 张")
            print(f"⏱️ 处理时间: {result.get('created_at', 'N/A')}")

            if result['saved_path']:
                saved_file = Path(result['saved_path'])
                relative_path = saved_file.relative_to(Path.cwd())
                print(f"💾 保存路径: ./{relative_path}")

            if result.get('duration', 0) > 0:
                print(f"⏱️ 处理耗时: {result['duration']:.1f} 秒")

            # 显示内容预览
            if len(result['content']) > 0:
                print("\n📄 文档内容预览:")
                print("-" * 40)
                preview_length = min(500, len(result['content']))
                print(result['content'][:preview_length])
                if len(result['content']) > preview_length:
                    print(f"\n... (还有 {len(result['content']) - preview_length} 个字符)")

            return 0
        else:
            print("❌ 文档处理失败")
            print("\n💡 可能的原因:")
            print("   - 网络连接问题")
            print("   - 文档权限不足")
            print("   - API服务暂时不可用")
            print("   - 文档格式不支持")
            print("\n🔧 故障排除:")
            print("   1. 检查网络连接")
            print("   2. 确认文档访问权限")
            print("   3. 查看详细日志: ~/.claude/feishu/logs/")
            return 1

    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
        return 130
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        import traceback
        print("\n📋 详细错误信息:")
        traceback.print_exc()
        return 1

def skill_mode(args_string: str = "") -> dict:
    """技能模式 - 为Claude Code技能调用设计"""
    try:
        # 解析参数
        if not args_string:
            return {"error": "No arguments provided", "usage": "Provide: url, save, localize_images, history, stats, test_mode"}

        # 简单解析参数
        args = {}
        for pair in args_string.split():
            if '=' in pair:
                key, value = pair.split('=', 1)
                args[key] = value
            else:
                # URL通常是第一个参数
                if 'url' not in args and pair.startswith('https://'):
                    args['url'] = pair

        # 创建处理器
        processor = FeishuProcessor(test_mode=args.get('test_mode', 'true').lower() != 'false')

        # 初始化
        if not processor.initialize(non_interactive=True):
            return {"error": "Failed to initialize processor"}

        # 处理不同命令
        if 'history' in args and args['history'] == 'true':
            return {"command": "history", "result": "Task history displayed in console"}

        if 'stats' in args and args['stats'] == 'true':
            return {"command": "stats", "result": "Statistics displayed in console"}

        # 处理文档
        url = args.get('url')
        if not url:
            return {"error": "No URL provided", "usage": "Provide url parameter"}

        if not processor.validate_feishu_url(url):
            return {"error": "Invalid Feishu URL format"}

        result = processor.process_document(
            url,
            save_to_file=args.get('save', 'false').lower() == 'true',
            localize_images=args.get('localize_images', 'false').lower() == 'true'
        )

        if result:
            return {
                "success": True,
                "result": result,
                "message": f"Successfully processed document: {result['doc_name']}"
            }
        else:
            return {"error": "Failed to process document"}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # 检查是否在技能模式下运行
    if len(sys.argv) > 1 and sys.argv[1] == "--skill-mode":
        args_string = " ".join(sys.argv[2:])
        result = skill_mode(args_string)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 正常命令行模式
        exit_code = main()
        sys.exit(exit_code)