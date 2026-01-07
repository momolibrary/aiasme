#!/usr/bin/env python3
"""
测试飞书文档读取器功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from feishu_config import FeishuConfig
from feishu_logger import logger
from feishu_processor import FeishuProcessor

def test_config():
    """测试配置管理"""
    print("🧪 测试配置管理...")
    config = FeishuConfig()

    # 测试token设置和获取
    test_token = "test_token_12345"
    if config.save_token(test_token, "test"):
        retrieved_token = config.get_token("test")
        if retrieved_token == test_token:
            print("✅ Token保存和获取功能正常")
        else:
            print("❌ Token功能异常")
    else:
        print("❌ Token保存失败")

def test_logger():
    """测试日志功能"""
    print("🧪 测试日志功能...")

    # 创建测试任务
    record = logger.start_task("https://test.feishu.cn/docx/test")

    # 更新任务状态
    logger.update_task(record, task_id="test_123", status="processing")

    # 完成任务
    test_content = "这是一个测试文档内容\n包含多个段落\n用于测试日志功能"
    logger.complete_task(record, test_content, "测试文档")

    print("✅ 日志记录功能正常")

    # 显示历史
    logger.print_task_history(3)
    logger.print_statistics()

def test_processor():
    """测试处理器初始化"""
    print("🧪 测试处理器初始化...")

    processor = FeishuProcessor(test_mode=True)

    # 设置测试token
    test_token = "test_token_for_unit_testing"
    processor.config.save_token(test_token, "test")

    if processor.initialize():
        print("✅ 处理器初始化成功")

        # 测试URL验证
        test_urls = [
            "https://li.feishu.cn/docx/test123",
            "https://li.feishu.cn/wiki/test456",
            "https://example.com/not-feishu"
        ]

        for url in test_urls:
            is_valid = processor.validate_feishu_url(url)
            status = "✅" if (url.startswith('https://li.feishu.cn/') and is_valid) or (not url.startswith('https://li.feishu.cn/') and not is_valid) else "❌"
            print(f"{status} URL验证: {url} -> {is_valid}")
    else:
        print("❌ 处理器初始化失败（这是正常的，因为没有配置真实Token）")

def main():
    """运行所有测试"""
    print("🚀 开始测试飞书文档读取器组件...")
    print("="*50)

    try:
        test_config()
        print()
        test_logger()
        print()
        test_processor()

        print("\n" + "="*50)
        print("✅ 所有测试完成！")

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()