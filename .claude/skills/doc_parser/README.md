# Doc Parser Skill

知言文档解析器 MCP Skill - 用于解析各类文档格式（PDF、Word、Excel、PPT等）为Markdown

## 概述

doc_parser skill 是基于知言平台doc-parser MCP服务的封装，提供统一的文档解析能力。支持多种文档格式的智能解析，输出结构化的Markdown文本，便于AI理解和处理。

## 特性

- ✅ **多格式支持**: PDF、DOCX、XLSX、PPTX、图片等
- ✅ **智能解析**: 文本、表格、图片自动识别
- ✅ **Markdown输出**: 统一格式，易于处理
- ✅ **Token共享**: 使用feishu_reader相同的知言token
- ✅ **自动加载**: 支持MCP服务自动连接

## 快速开始

### 1. 配置Token

doc_parser 使用与 feishu_reader 相同的知言生产环境token。

检查token配置：
```bash
cat ~/.claude/feishu/config.json
```

应该看到类似内容：
```json
{
  "6c3c951cb25d0c76": {
    "token": "app-eyJhbGciOiJIUzI1NiIs...",
    "service": "zhiyan"
  }
}
```

如果没有token，请参考 feishu_reader skill 的token配置说明。

### 2. 配置MCP服务

在项目根目录的 `.mcp.json` 中添加 doc-parser 配置：

```json
{
  "mcpServers": {
    "doc-parser": {
      "command": "npx",
      "args": ["-y", "@chehejia/doc-parser@latest"],
      "env": {
        "Authorization": "Bearer app-eyJhbGciOiJIUzI1NiIs...",
        "NPM_CONFIG_REGISTRY": "https://rnpm.chehejia.com",
        "USER_NAME": "zhuangdesheng"
      }
    }
  }
}
```

**重要配置项**:
- `Authorization`: 从 `~/.claude/feishu/config.json` 复制完整token（包含"Bearer "前缀）
- `USER_NAME`: 替换为你的域账号

### 3. 添加权限

在 `.claude/settings.local.json` 的 `permissions.allow` 数组中添加：

```json
{
  "permissions": {
    "allow": [
      "Skill(doc_parser)",
      "mcp__doc-parser__*"
    ]
  }
}
```

### 4. 验证配置

```bash
# 检查MCP服务状态
claude mcp list

# 应该看到:
# ✓ doc-parser (stdio)
```

如果显示未连接，重启Claude Code或运行：
```bash
claude mcp reload
```

## 使用方法

### 在Claude对话中使用

```
# 基本用法
@skill doc_parser 解析文档 ~/Documents/report.pdf

# 解析Word文档
@skill doc_parser 解析文档 ~/Documents/需求文档.docx

# 解析Excel表格
@skill doc_parser 解析表格 ~/Documents/数据.xlsx

# 解析远程文档（如果支持）
@skill doc_parser 解析文档 https://example.com/document.pdf
```

### 集成工作流

#### 工作流1: 文档解析 → Memory记录

```
用户: 帮我解析这个产品需求文档并记录到memory
Claude:
  1. @skill doc_parser 解析文档 ~/Downloads/产品需求.pdf
  2. [分析解析结果]
  3. @skill memo 新增条目「产品需求-xxx功能」
     类型：文档
     内容：[提取的关键需求]
     相关人员：产品经理
  4. python3 .claude/skills/memo/scripts/update_index.py
```

#### 工作流2: 批量文档处理

```
用户: 解析本周所有会议纪要
Claude:
  # 遍历文件
  for file in ~/会议纪要/2026-01-0*.pdf
    @skill doc_parser 解析文档 $file
    提取关键决策和行动项
    记录到对应的events/
```

#### 工作流3: 文档对比分析

```
用户: 对比新旧版本的需求文档
Claude:
  @skill doc_parser 解析文档 ~/需求v1.0.docx
  @skill doc_parser 解析文档 ~/需求v2.0.docx
  [对比分析差异]
```

## 支持的文档格式

| 格式 | 扩展名 | 支持程度 | 说明 |
|------|--------|----------|------|
| PDF | .pdf | ✅ 完整支持 | 文本、表格、图片 |
| Word | .docx | ✅ 完整支持 | 文档结构、样式 |
| Excel | .xlsx | ✅ 完整支持 | 表格、公式、图表 |
| PowerPoint | .pptx | ✅ 完整支持 | 幻灯片、备注 |
| 图片 | .png, .jpg | ✅ OCR支持 | 文字识别 |

*具体支持程度取决于doc-parser MCP服务的实现*

## 输出格式

解析结果统一输出为Markdown格式，示例：

```markdown
# 文档标题

## 第一章

这是正文内容...

### 1.1 小节

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |

![图片描述](image_url_or_base64)
```

## 高级用法

### 指定输出路径

```
@skill doc_parser 解析文档 ~/report.pdf 保存到 ./output/report.md
```

### 仅提取文本（不含图片）

```
@skill doc_parser 解析文档 ~/report.pdf 仅文本
```

### 提取特定页面（PDF）

```
@skill doc_parser 解析文档 ~/report.pdf 页面 1-5
```

*注意：具体功能取决于MCP服务实现*

## 故障排除

### 问题1: MCP服务未连接

**症状**:
```
Error: MCP server 'doc-parser' not found
```

**解决方案**:
```bash
# 1. 检查.mcp.json配置是否正确
cat .mcp.json

# 2. 检查NPM registry配置
npm config get registry
# 应该返回: https://rnpm.chehejia.com

# 3. 重新加载MCP
claude mcp reload

# 4. 手动测试npx命令
npx -y @chehejia/doc-parser@latest --version
```

### 问题2: Token认证失败

**症状**:
```
401 Unauthorized
```

**解决方案**:
1. 检查 `~/.claude/feishu/config.json` 中的token
2. 确认token前缀为 `app-` 且在有效期内
3. 在 `.mcp.json` 中的 Authorization 字段确保格式为 `Bearer app-xxx...`
4. 重新获取token:
   - 访问知言平台
   - 头像 → API调用 → 生成新token
   - 更新配置文件

### 问题3: NPM包下载失败

**症状**:
```
npm ERR! 404 Not Found - GET https://registry.npmjs.org/@chehejia/doc-parser
```

**解决方案**:
```bash
# 设置正确的registry
npm config set registry https://rnpm.chehejia.com

# 验证配置
npm config get registry

# 清除缓存
npx clear-npx-cache

# 重试
```

### 问题4: 文档解析失败

**症状**:
- 返回空内容
- 解析错误
- 格式混乱

**解决方案**:
1. 检查文档是否损坏（用其他工具打开验证）
2. 确认文档路径正确且可访问
3. 检查文件权限（chmod +r）
4. 尝试转换文档格式后再解析
5. 查看详细错误日志

### 问题5: 权限不足

**症状**:
```
Permission denied: Skill(doc_parser) not allowed
```

**解决方案**:
在 `.claude/settings.local.json` 中添加权限：
```json
{
  "permissions": {
    "allow": [
      "Skill(doc_parser)",
      "mcp__doc-parser__*"
    ]
  }
}
```

## 与其他Skills集成

### 与 feishu_reader 配合

```
# 场景：对比飞书文档和本地PDF
@skill feishu_reader https://li.feishu.cn/docx/xxx
@skill doc_parser 解析文档 ~/参考文档.pdf
# 然后对比分析两者差异
```

### 与 memo 配合

```
# 场景：解析文档并存入知识库
@skill doc_parser 解析文档 ~/重要文档.pdf
@skill memo 新增条目「文档-xxx」内容：[解析内容]
python3 .claude/skills/memo/scripts/update_index.py
```

### 与 feishu_project 配合

```
# 场景：根据需求文档创建工作项
@skill doc_parser 解析文档 ~/需求文档.docx
# [提取需求列表]
@skill feishu_project 创建工作项 类型=需求 名称=xxx
```

## 开发与调试

### 查看MCP通信日志

```bash
# Claude Code日志
tail -f ~/.claude/logs/mcp-doc-parser.log

# 或查看总日志
tail -f ~/.claude/logs/claude-code.log | grep doc-parser
```

### 测试MCP服务

```bash
# 手动运行MCP服务
npx -y @chehejia/doc-parser@latest

# 传入测试文档
echo '{"method":"parse","file":"/path/to/test.pdf"}' | npx -y @chehejia/doc-parser@latest
```

### 更新MCP包

```bash
# 清除缓存
npx clear-npx-cache

# 强制重新下载最新版本
npx -y @chehejia/doc-parser@latest --version
```

## 最佳实践

### 1. 文档路径规范

✅ **推荐**:
```
~/Documents/report.pdf          # 使用波浪号
/Users/username/file.pdf        # 绝对路径
"~/My Documents/report.pdf"     # 有空格时加引号
```

❌ **不推荐**:
```
./relative/path.pdf             # 相对路径（可能导致路径错误）
~/Documents/文档 名称.pdf       # 空格未转义
```

### 2. 批量处理策略

对于大量文档：
1. 先解析一个样本验证格式
2. 使用循环批量处理
3. 设置输出目录统一管理
4. 记录处理日志

### 3. 输出管理

```
# 推荐的输出目录结构
./feishu_docs/
├── parsed/
│   ├── 20260108_report_parsed.md
│   └── 20260108_需求_parsed.md
└── original/
    ├── report.pdf
    └── 需求.docx
```

### 4. 错误恢复

```bash
# 记录失败的文档
failed_docs=()

for doc in *.pdf; do
  if ! @skill doc_parser 解析文档 "$doc"; then
    failed_docs+=("$doc")
  fi
done

# 处理失败列表
echo "Failed: ${failed_docs[@]}"
```

## 安全与隐私

- ✅ Token加密存储在 `~/.claude/feishu/config.json`（权限0o600）
- ✅ 文档内容仅在本地处理，不会上传到公共服务
- ✅ MCP通信使用stdio协议，进程隔离
- ⚠️  请勿解析包含敏感信息的文档（如密码、私钥等）
- ⚠️  定期更新token，避免token泄露

## 更新日志

### v1.0.0 (2026-01-08)
- 🎉 初始版本
- ✅ 支持基本文档解析功能
- ✅ 集成知言token管理
- ✅ MCP服务自动加载
- ✅ 完整的错误处理和文档

## 常见问题 (FAQ)

**Q: doc_parser 和 feishu_reader 有什么区别？**

A:
- `feishu_reader`: 专门用于读取飞书平台上的在线文档（docx、wiki）
- `doc_parser`: 用于解析本地或远程的各种格式文档（PDF、Word、Excel等）

两者可以配合使用，互为补充。

**Q: 是否支持加密的PDF？**

A: 取决于doc-parser MCP服务的实现。通常需要先解密PDF才能解析。

**Q: 解析大文档会很慢吗？**

A: 解析时间取决于文档大小和复杂度。建议：
- 大文档（>50页）：考虑分段解析
- 图片多的文档：OCR会增加时间
- 可以先解析文本部分，图片按需提取

**Q: 可以解析扫描版PDF吗？**

A: 可以，如果doc-parser支持OCR。扫描版PDF会自动进行文字识别。

**Q: 解析失败是否会影响其他操作？**

A: 不会。每次解析都是独立的操作，失败不会影响其他文档或系统状态。

## 技术支持

遇到问题？按以下顺序排查：

1. 📖 查看本文档的"故障排除"章节
2. 🔍 检查 `.mcp.json` 和权限配置
3. 🔬 查看MCP通信日志
4. 💬 在项目中提交Issue
5. 👥 联系开发团队

## 参考资源

- [Model Context Protocol (MCP) 规范](https://spec.modelcontextprotocol.io/)
- [Claude Code MCP集成指南](https://docs.anthropic.com/claude/docs/mcp)
- [知言平台文档](内部链接)
- [NPM私有仓库](https://rnpm.chehejia.com)

## 许可证

内部项目，仅供公司内部使用。

---

**维护者**: 庄德升 (zhuangdesheng)
**最后更新**: 2026-01-08