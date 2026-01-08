---
name: doc_parser
description: 知言文档解析器MCP工具封装，用于解析各类文档（PDF、Word、Excel、PPT等）为Markdown格式
allowed-tools: mcp__doc-parser__*, Read, Write
---

## 核心功能

doc_parser skill 提供文档解析能力，支持多种文档格式的解析和转换：

- **PDF文档**: 支持文本提取、表格识别、图片提取
- **Office文档**: Word (docx)、Excel (xlsx)、PowerPoint (pptx)
- **图片文档**: PNG、JPG等图片格式的OCR识别
- **Markdown输出**: 统一转换为Markdown格式，便于AI理解和处理

## 用法示例

### 基本文档解析

```
@skill doc_parser 解析文档 /path/to/document.pdf
@skill doc_parser 解析文档 /path/to/document.docx
@skill doc_parser 解析 https://example.com/file.pdf
```

### Markdown转飞书文档

```
@skill doc_parser 上传markdown /path/to/document.md        # 转换为飞书文档
@skill doc_parser markdown转飞书 ~/Documents/report.md     # 同上
@skill doc_parser 解析markdown https://example.com/doc.md # 解析并上传markdown
```

### 图片提取处理

```
@skill doc_parser 提取图片 /path/to/document.md           # 提取markdown中的图片
@skill doc_parser 本地化图片 ~/Documents/report.md         # 下载图片并替换路径
```

### 一站式文档处理

```
@skill doc_parser 一键解析 /path/to/document.pdf           # 解析+下载+本地化图片
@skill doc_parser 完整处理 https://example.com/doc.md      # 完整流程处理
```

## 集成使用场景

### 场景1: 解析文档并记录到memory

```
# Step 1: 解析文档
@skill doc_parser 解析文档 ~/Downloads/产品需求文档.pdf

# Step 2: 将解析结果记录到memory
@skill memo 新增条目「产品需求-xxx功能」
类型：文档
来源：产品需求文档.pdf
内容：[文档解析内容]
相关人员：产品经理张三
```

### 场景2: 批量解析会议纪要

```
# 解析多个会议纪要PDF
@skill doc_parser 解析文档 ~/会议纪要/2026-01-*.pdf

# 提取关键信息并存入events
```

### 场景3: 解析数据报表

```
# 解析Excel报表
@skill doc_parser 解析表格 ~/报表/Q4数据.xlsx

# 分析数据并生成总结
```

## MCP工具说明

### 可用MCP工具

doc-parser 提供以下5个核心MCP工具：

#### 1. 文档提交处理
**工具**: `mcp__doc-parser__submit`
- **功能**: 提交文档解析任务
- **支持格式**:
  - 本地PDF/Word文档 (`file://`路径)
  - 飞书文档URL (包含feishu关键字的URL)
  - 网站内容 (`http://` 或 `https://` URL)
- **参数**: `resourceUri` (必填) - 文档资源URI

#### 2. 结果查询
**工具**: `mcp__doc-parser__result`
- **功能**: 获取任务处理结果或基于taskId查询已有结果
- **参数**: `taskId` (必填) - 任务ID

#### 3. Markdown转飞书文档 ⭐
**工具**: `mcp__doc-parser__parse_markdown`
- **功能**: 解析Markdown文档并创建新的飞书文档
- **参数**:
  - `resourceUri` (必填) - Markdown文档URI (`file://` 或 `http://`)
  - `taskType` (可选) - 任务类型，默认 `'markdown'`
- **用途**: 本地写作，飞书协作

#### 4. 图片提取处理
**工具**: `mcp__doc-parser__extract_markdown_images`
- **功能**: 从Markdown文档提取所有图片并下载到本地
- **参数**:
  - `resourceUri` (必填) - Markdown文档URI
  - `outputPath` (可选) - 输出路径，默认文档所在目录
- **支持**: 打包为zip文件或保存到文件夹

#### 5. 一站式文档处理 ⭐
**工具**: `mcp__doc-parser__submit_and_download_with_images`
- **功能**: 自动完成完整的文档处理流程
- **流程**: 提交文档→等待解析→下载Markdown→提取图片→替换为本地路径
- **参数**:
  - `resourceUri` (必填) - 文档资源URI
  - `outputDir` (可选) - 输出父目录，默认 `~/Documents/doc-parser-output`
  - `pollInterval` (可选) - 轮询间隔，默认5秒
  - `timeout` (可选) - 最大等待时间，默认300秒
- **注意**: 仅在用户明确表达解析意图时触发

### 特殊功能说明

#### Markdown转飞书文档功能
这是doc-parser的一个核心亮点功能：
- 支持将本地Markdown文档一键转换为飞书云文档
- 自动处理Markdown语法到飞书格式的映射
- 无需手动复制粘贴，自动处理格式转换
- 转换后会生成可访问的飞书文档链接
- 需要在MCP配置中设置 `USER_NAME` 环境变量作为文档所有者

#### 一键式完整处理
适用于需要完整本地化的场景：
- 自动处理在线文档下载
- 图片本地化（下载并替换相对路径）
- 适合文档归档、离线编辑、批量处理
- 支持多种资源类型：本地文件、飞书文档、网站

## 配置与权限

### MCP配置

doc-parser MCP服务器配置在 `.mcp.json` 中：

```json
{
  "mcpServers": {
    "doc-parser": {
      "command": "npx",
      "args": ["-y", "@chehejia/doc-parser@latest"],
      "env": {
        "Authorization": "Bearer <token>",
        "NPM_CONFIG_REGISTRY": "https://rnpm.chehejia.com",
        "USER_NAME": "zhuangdesheng"
      }
    }
  }
}
```

### Token配置

doc-parser 使用与 feishu_reader 相同的知言生产环境 token，配置位置：
- `~/.claude/feishu/config.json`

Token格式：`Bearer app-xxx...`

### 权限配置

在 `.claude/settings.local.json` 中添加：

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

## MCP连接检查

### 检查MCP服务状态

```bash
# 列出所有MCP服务
claude mcp list

# 应该看到 doc-parser 显示为 ✓ Connected
```

### 自动加载MCP

如果MCP未加载，skill会自动提示用户：

```
⚠️  doc-parser MCP服务未连接
请运行: claude mcp add --transport stdio doc-parser "npx -y @chehejia/doc-parser@latest"
```

或者skill可以尝试自动加载（如果配置了 enableAllProjectMcpServers）。

## 错误处理

### 常见问题

#### 1. MCP服务未启动

**症状**: 调用工具时提示 "MCP server not found"

**解决**:
```bash
# 检查MCP配置
cat .mcp.json

# 重启Claude Code
# 或手动添加MCP服务
claude mcp add --transport stdio doc-parser "npx -y @chehejia/doc-parser@latest"
```

#### 2. Token认证失败

**症状**: 返回 401 Unauthorized

**解决**:
- 检查 `~/.claude/feishu/config.json` 中的token是否有效
- 确认使用的是生产环境token（不是测试环境）
- 重新获取token（访问知言平台 → 头像 → API调用）

#### 3. 文档解析失败

**症状**: 返回解析错误或空内容

**解决**:
- 确认文档路径正确且可访问
- 检查文档格式是否支持
- 尝试用其他工具打开文档验证完整性

#### 4. NPM包下载失败

**症状**: npx 无法下载 @chehejia/doc-parser

**解决**:
```bash
# 验证NPM registry配置
npm config get registry

# 应该返回: https://rnpm.chehejia.com

# 如果不对，设置registry
npm config set registry https://rnpm.chehejia.com
```

## 最佳实践

### 1. 文档路径规范

- 使用绝对路径: `~/Documents/file.pdf`
- 避免空格: 使用引号包裹 `"~/My Documents/file.pdf"`
- 检查权限: 确保文件可读

### 2. 输出管理

- 大文档分段处理，避免一次性输出过多内容
- 解析结果保存到 `./feishu_docs/` 或指定输出目录
- 使用时间戳命名: `document_parsed_20260108_143000.md`

### 3. 与memory系统集成

```bash
# 标准流程
1. @skill doc_parser 解析文档 <path>
2. 审查解析内容
3. @skill memo 新增条目 记录关键信息
4. python3 .claude/skills/memo/scripts/update_index.py 更新索引
```

### 4. 批量处理

```bash
# 批量解析同类文档
for file in ~/Documents/*.pdf; do
  @skill doc_parser 解析文档 "$file"
done
```

## 技术说明

### MCP通信机制

- **Transport**: stdio（标准输入输出）
- **Command**: npx（Node.js包执行器）
- **Package**: @chehejia/doc-parser@latest（私有NPM包）

### 环境变量

- `Authorization`: Bearer token（知言API认证）
- `NPM_CONFIG_REGISTRY`: 私有NPM registry地址
- `USER_NAME`: 域账号（用于日志和审计）

### 数据流

```
文档文件 → doc-parser MCP → 解析引擎 → Markdown输出 → Claude处理
```

## 与其他Skills的协同

### 与 feishu_reader 配合

```
# 读取飞书文档
@skill feishu_reader https://li.feishu.cn/docx/xxx

# 解析本地PDF参考文档
@skill doc_parser 解析文档 ~/参考资料.pdf

# 对比分析两者内容
```

### 与 memo 配合

```
# 解析文档
@skill doc_parser 解析文档 ~/合同.pdf

# 提取关键信息存入memory
@skill memo 新增条目「合同-xxx公司」
内容：[提取的合同要点]
```

### 与 feishu_project 配合

```
# 解析需求文档
@skill doc_parser 解析文档 ~/需求文档.docx

# 创建对应工作项
@skill feishu_project 创建工作项 类型=需求 名称=xxx功能开发
```

## 更新与维护

### 更新MCP包

```bash
# 清除缓存
npx clear-npx-cache

# 重新拉取最新版本
npx -y @chehejia/doc-parser@latest --version
```

### 日志查看

```bash
# Claude Code日志
~/.claude/logs/

# MCP服务日志（如果有）
查看具体MCP实现的日志配置
```

## 参考资源

- **MCP协议文档**: https://spec.modelcontextprotocol.io/
- **Claude Code MCP指南**: `.claude/docs/mcp-guide.md`
- **知言平台**: 内部知言文档平台
- **NPM私有仓库**: https://rnpm.chehejia.com