# 飞书文档读取器 (Feishu Document Reader)

一个功能完整的飞书文档读取器，基于知言平台API，支持安全token管理、详细日志记录、图片本地化和Markdown导出。

## ✨ 特性

### 🔒 安全性
- **安全Token管理**: Token加密存储，文件权限保护
- **多环境支持**: 支持测试和生产环境切换
- **非交互模式**: 支持自动化环境使用

### 📝 功能完整性
- **文档提取**: 支持飞书docx和wiki格式文档
- **图片本地化**: 自动下载并转换远程图片为本地文件
- **Markdown导出**: 保存为格式化的markdown文件
- **任务管理**: 完整的任务生命周期追踪

### 📊 监控和日志
- **详细日志**: 记录每个任务的完整处理过程
- **统计分析**: 成功率、处理时间、内容大小等统计
- **历史记录**: 按月归档的任务历史查询

## 🚀 快速开始

### 基本使用

```bash
# 直接读取文档内容
python3 feishu_reader.py https://li.feishu.cn/docx/your_document_id

# 保存为markdown文件
python3 feishu_reader.py --save https://li.feishu.cn/wiki/your_page_id

# 保存并本地化图片
python3 feishu_reader.py --save --localize-images https://li.feishu.cn/docx/your_document_id
```

### 高级功能

```bash
# 查看任务历史
python3 feishu_reader.py --history

# 查看统计信息
python3 feishu_reader.py --stats

# 使用生产环境
python3 feishu_reader.py --prod https://li.feishu.cn/docx/your_document_id
```

### Claude Code技能模式

```bash
# 在Claude Code中使用
skill: "feishu_reader" with url="https://li.feishu.cn/docx/your_document_id" save=true localize_images=true
```

## 📁 文件结构

安装后创建的文件和目录：

```
feishu_reader/                    # skill目录
├── feishu_reader.py             # 主入口文件
├── feishu_processor.py          # 核心处理器
├── feishu_config.py             # 配置管理
├── feishu_logger.py             # 日志系统
├── test_feishu.py               # 测试脚本
├── feishu_reader.md             # 技能定义文件
└── README.md                    # 说明文档

~/.claude/feishu/                # 配置和日志目录
├── config.json                  # 加密的token配置
└── logs/
    └── feishu_tasks_YYYYMM.json  # 月度任务日志

./feishu_docs/                   # 输出目录
├── document_name_extracted_YYYYMMDD_HHMMSS.md
├── document_name_localized_YYYYMMDD_HHMMSS.md
└── images/
    ├── document_YYYYMMDD_HHMMSS_hash.jpg
    └── document_YYYYMMDD_HHMMSS_hash.png
```

## ⚙️ 配置

### Token配置

**重要**: 本skill不包含任何默认token。每个用户需要配置自己的知言平台API token。

#### 方法1: 交互式设置 (推荐)

首次使用时，程序会自动引导你设置token：

```bash
python3 feishu_reader.py https://li.feishu.cn/docx/your_document_id
```

按照提示操作：
1. 访问知言平台
2. 点击头像 → API调用
3. 选择IDaaS应用或Secret API Key
4. 复制生成的Token并输入

Token会安全存储在 `~/.claude/feishu/config.json` 中，文件权限设置为0o600。

#### 方法2: 环境变量 (适用于自动化)

```bash
# 设置环境变量
export FEISHU_TOKEN="your_token_here"

# 使用
python3 feishu_reader.py https://li.feishu.cn/docx/your_document_id
```

#### 方法3: 手动配置文件

创建配置文件 `~/.claude/feishu/config.json`:

```json
{
  "feishu_default": {
    "token": "your_token_here",
    "service": "default"
  }
}
```

**安全提示**:
- 配置文件权限会自动设置为0o600（仅用户可读写）
- Token使用SHA256哈希作为配置键名，提高安全性
- 不要在代码中或公开位置存储你的token

### API环境

- **测试环境**: `https://cfe-doc-backend-test.inner.chj.cloud/openapi` (默认)
- **生产环境**: `https://cfe-doc-backend.inner.chj.cloud/openapi`

## 🔧 开发和测试

### 运行测试

```bash
# 测试核心功能
python3 test_feishu.py
```

### 技能模式测试

```bash
# 技能模式测试
python3 feishu_reader.py --skill-mode url="https://li.feishu.cn/docx/test" save=true
```

## 📋 参数说明

| 参数 | 简写 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `url` | - | string | - | 飞书文档URL |
| `--save` | `-s` | flag | false | 保存为markdown文件 |
| `--localize-images` | `-li` | flag | false | 本地化图片 |
| `--history` | `-h` | flag | false | 显示任务历史 |
| `--stats` | - | flag | false | 显示统计信息 |
| `--test` | - | flag | true | 使用测试环境 |
| `--prod` | - | flag | false | 使用生产环境 |

## 🔒 安全说明

- Token文件权限设置为0o600（仅用户可读写）
- 配置文件使用SHA256哈希作为键名
- 支持多个服务的token管理
- 自动清理临时文件和日志

## 📊 返回值

成功处理时返回包含以下信息的字典：

```python
{
    'task_id': str,              # 任务ID
    'doc_name': str,             # 文档名称
    'doc_url': str,              # 文档URL
    'content': str,              # 提取的内容
    'content_length': int,       # 内容长度
    'images_count': int,         # 图片数量
    'saved_path': str,           # 保存路径
    'status': str,               # 处理状态
    'processing_time': float,    # 处理时间
    'created_at': str            # 创建时间
}
```

## 🐛 故障排除

### 常见问题

1. **Token设置失败**
   - 检查网络连接
   - 确认token格式正确
   - 检查文件写入权限

2. **文档提取失败**
   - 验证URL格式是否正确
   - 确认文档访问权限
   - 检查API服务状态

3. **图片下载失败**
   - 检查图片URL是否可访问
   - 确认网络连接稳定
   - 查看详细错误日志

### 日志查看

```bash
# 查看最新日志
cat ~/.claude/feishu/logs/feishu_tasks_$(date +%Y%m).json

# 查看错误详情
python3 feishu_reader.py --history
```

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个技能！

## 📄 许可证

MIT License

## 🆘 支持

如果遇到问题，请：

1. 查看详细日志信息
2. 检查网络连接和权限
3. 提交Issue并附上错误日志
4. 联系开发团队获取技术支持