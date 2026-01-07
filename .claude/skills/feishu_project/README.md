# 飞书项目 MCP Skill - 完整使用指南

本skill封装了飞书项目MCP工具，提供便捷的工作项查询、创建和更新功能。**核心优势**是参数友好性和智能引导，支持使用名称代替ID，让操作更直观。

## 目录

- [快速开始](#快速开始)
- [参数友好性](#参数友好性)
- [使用示例](#使用示例)
- [用户引导流程](#用户引导流程)
- [字段支持说明](#字段支持说明)
- [最佳实践](#最佳实践)
- [故障排除](#故障排除)

## 快速开始

### 1. 配置MCP服务器

飞书项目MCP服务器通过以下命令添加：

```bash
claude mcp add --transport http feishu-project "https://project.feishu.cn/mcp_server/v1?mcpKey=xxx&projectKey=xxx&userKey=xxx"
```

**重要**：URL中可以预配置 `projectKey` 和 `userKey`，这样所有操作将自动使用该用户身份和空间。

### 2. 验证连接

```bash
claude mcp list
# 应该看到 feishu-project 显示为 ✓ Connected
```

## 参数友好性

MCP工具的一大特色是**参数友好性** - 支持多种等效参数，让调用更灵活：

### 工作项标识 (work_item_id)

✅ **支持ID**: `6462347697`
✅ **支持名称**: `"研发3T组织筹备"`

示例：
```
# 两种方式等效
@skill feishu_project 查询工作项 6462347697
@skill feishu_project 查询工作项 研发3T组织筹备
```

### 字段名称 (fields)

✅ **支持field_key**: `priority`
✅ **支持字段名**: `"优先级"`

示例：
```
# 两种方式等效
@skill feishu_project 更新工作项 研发3T组织筹备 priority=P1
@skill feishu_project 更新工作项 研发3T组织筹备 优先级=P1
```

### 人员字段

✅ **支持user_key**: `7287860131738501121`
✅ **支持用户名**: `"庄德升"`
❌ **不支持email**: 暂不支持通过email指定用户

示例：
```
@skill feishu_project 更新工作项 研发3T组织筹备 当前负责人=庄德升
```

### 节点标识 (nodes)

✅ **支持node_id**: 节点ID
✅ **支持节点名**: `"文档发布"`

示例：
```
@skill feishu_project 完成节点 工作项=研发3T组织筹备 节点=文档发布
```

### 空间标识 (project_key)

✅ **支持project_key**: `60963d9ba204b8026d6f297a`
✅ **支持simple_name**: `li_testing`

（通常在URL中预配置，无需每次传入）

## 使用示例

### 查询工作项

#### 基本查询
```
@skill feishu_project 查询工作项 研发3T组织筹备
```

返回：工作项的基本信息（ID、名称、类型、状态、负责人等）

#### 查询特定字段
```
@skill feishu_project 查询工作项 研发3T组织筹备 字段 优先级,状态,工作分类
```

返回：仅返回指定的字段信息

#### 批量查询
```
@skill feishu_project 查询工作项 工作项1
@skill feishu_project 查询工作项 工作项2
@skill feishu_project 查询工作项 工作项3
```

Claude会并行处理这些请求。

### 更新工作项

#### 更新单个字段
```
@skill feishu_project 更新工作项 技术兴趣社区2026 优先级=P0
```

#### 更新多个字段
```
@skill feishu_project 更新工作项 技术兴趣社区2026 优先级=P1 工作分类=在研类
```

#### 更新人员字段
```
@skill feishu_project 更新工作项 技术兴趣社区2026 当前负责人=庄德升
```

### 创建工作项

#### 最简创建（仅必填字段）
```
@skill feishu_project 创建工作项 类型=重点工作 名称=技术兴趣社区2026
```

#### 带字段创建
```
@skill feishu_project 创建工作项 类型=任务 名称=新任务 优先级=P1 估分=5
```

### 查询工作项类型

在创建或更新前，先了解工作项类型支持的字段：

```
@skill feishu_project 查询类型 重点工作
@skill feishu_project 查询类型 任务
@skill feishu_project 查询类型 缺陷
```

返回：该类型的所有可用字段、字段类型、可选值等

### 视图操作

```
@skill feishu_project 查询视图 DczMzKGvg
@skill feishu_project 查询视图 DczMzKGvg 字段 任务名称,状态 页数 1
```

视图ID可以从飞书项目的视图详情页URL中获取。

### 节点操作

#### 查询节点信息
```
@skill feishu_project 查询节点 工作项=研发3T组织筹备 节点=文档发布
```

#### 完成节点
```
@skill feishu_project 完成节点 工作项=研发3T组织筹备 节点=文档发布
```

## 用户引导流程

当用户描述不清晰或信息不完整时，Claude会主动引导用户提供必要信息。以下是典型的引导场景：

### 场景1：创建工作项信息不完整

**用户输入**：
```
帮我创建一个工作项
```

**Claude引导**：
```
好的！我需要以下信息来创建工作项：
1. 工作项类型是什么？（如：重点工作、任务、缺陷等）
2. 工作项名称是什么？
3. 是否需要设置优先级、负责人等其他字段？

如果不确定工作项类型有哪些，我可以先查询可用的工作项类型。
```

**用户补充**：
```
类型是重点工作，名称是"技术兴趣社区2026"
```

**Claude执行**：创建工作项并返回URL

### 场景2：更新不支持的字段

**用户输入**：
```
更新工作项的业务线字段为"产研领域"
```

**Claude响应**：
```
抱歉，"业务线"字段目前不支持通过API更新，需要在飞书项目网页上手动填写。

我可以帮您更新其他支持的字段，如：
- 优先级（P0/P1/P2）
- 工作分类（规划类/在研类/维护类）
- 描述信息
- 人员字段

请问您还需要更新哪些字段？
```

### 场景3：不确定可用字段

**用户输入**：
```
更新这个任务的一些字段
```

**Claude引导**：
```
让我先查询"任务"类型支持哪些字段...

[展示字段列表]

请告诉我您想更新哪些字段？
```

### 场景4：需要完整上下文

**用户输入**：
```
把优先级改成P0
```

**Claude引导**：
```
好的，请提供以下信息：
1. 要更新哪个工作项？（可以提供工作项ID或名称）

示例：
- 使用ID：6462347697
- 使用名称：研发3T组织筹备
```

## 字段支持说明

### 不支持读取的字段类型

- 附件
- 系统外信号
- 富文本中的图片
- 富文本格式

### 不支持写入的字段类型

- 附件
- 系统外信号
- 富文本
- **级联单多选**
- 投票
- 复合字段
- 关联工作项字段

### 特殊字段说明

根据实际测试，以下"重点工作"类型的字段**不支持通过API创建或更新**（需在网页手动填写）：

- `business`（业务线）
- `field_b57c18`（重点工作描述）
- `field_994f79`（用户价值）
- `field_452579`（关键指标）
- 角色成员相关字段

**建议流程**：
1. 通过API创建基本框架（名称、优先级等）
2. 在网页上补充完整信息

### 支持的常用字段

#### 重点工作类型
- `name` - 工作名称 ✓
- `priority` - 优先级（P0/P1/P2）✓
- `field_9eeef9` - 工作分类（规划类/在研类/维护类）✓
- `work_item_status` - 状态 ✓
- `current_status_operator` - 当前负责人 ✓

#### 任务类型
- `name` - 名称 ✓
- `note` - 备注 ✓
- `actual_work_time` - 实际工时 ✓
- `points` - 估分 ✓
- `finish_time` - 完成时间 ✓
- `work_item_status` - 状态 ✓

## 最佳实践

### 1. 创建工作项的推荐流程

**步骤1：了解工作项类型**
```
@skill feishu_project 查询类型 重点工作
```

**步骤2：创建基本框架**
```
@skill feishu_project 创建工作项 类型=重点工作 名称=技术兴趣社区2026
```

**步骤3：更新支持的字段**
```
@skill feishu_project 更新工作项 技术兴趣社区2026 优先级=P1 工作分类=在研类
```

**步骤4：手动填写不支持字段**
- 打开返回的工作项URL
- 在网页上填写：业务线、描述、用户价值、关键指标、角色成员等

### 2. 更新前先验证

在更新字段前，建议先查询该工作项类型支持的字段：

```
@skill feishu_project 查询类型 <工作项类型>
```

查看field_key和可选值，确保更新成功。

### 3. 使用名称而非ID

为了更直观，推荐使用名称：

```
# ✓ 推荐
@skill feishu_project 查询工作项 研发3T组织筹备

# ✗ 不推荐（但仍然有效）
@skill feishu_project 查询工作项 6462347697
```

### 4. 批量操作

如果需要查询或更新多个工作项，可以在对话中连续发送命令，Claude会并行处理：

```
@skill feishu_project 查询工作项 工作项A
@skill feishu_project 查询工作项 工作项B
@skill feishu_project 查询工作项 工作项C
```

### 5. 与记忆库集成

重要工作项可以记录到记忆库：

```
# 1. 查询工作项
@skill feishu_project 查询工作项 技术兴趣社区2026

# 2. 记录到记忆库
@skill memo 新增条目「技术兴趣社区2026」
类型：重点工作
状态：进行中
优先级：P1
负责人：庄德升
链接：https://project.feishu.cn/.../detail/6658956784
```

## 故障排除

### 常见错误及解决方案

#### 1. "can not support fields: xxx"

**错误信息**：
```
can not support fields: 业务线
```

**原因**：该字段不支持通过API更新

**解决方案**：
- 检查字段是否在[不支持写入的字段类型](#不支持写入的字段类型)列表中
- 使用飞书项目网页手动填写该字段
- 尝试更新其他支持的字段

#### 2. "params missed"

**错误信息**：
```
msg: 创建工作项失败, detail: params missed
```

**原因**：缺少必填参数（通常是name字段）

**解决方案**：
```
# ✗ 错误
@skill feishu_project 创建工作项 类型=任务

# ✓ 正确
@skill feishu_project 创建工作项 类型=任务 名称=测试任务
```

#### 3. "work item not exist"

**错误信息**：
```
msg: 查询失败, detail: work item not exist
```

**原因**：工作项不存在或无权访问

**解决方案**：
- 确认工作项ID或名称是否正确
- 检查是否有该工作项的访问权限
- 确认工作项在当前空间中

#### 4. 人员字段重名问题

**错误信息**：
```
有重名用户，请使用user_key
```

**解决方案**：
- 使用user_key代替user_name
- user_key可以从飞书项目中，鼠标hover到用户头像，双击头像获取

#### 5. MCP服务器未连接

**症状**：工具调用失败或返回连接错误

**解决方案**：
```bash
# 1. 检查MCP服务器状态
claude mcp list

# 2. 如果显示未连接，重新添加
claude mcp remove feishu-project
claude mcp add --transport http feishu-project "<MCP_URL>"

# 3. 验证连接
claude mcp list  # 应显示 ✓ Connected
```

### 调试技巧

所有MCP返回的错误都包含 `logId`，例如：
```
logId:021767612853465fdbdfdbdfdbdfdbd00000000000004f0d5fe93
```

如果遇到问题：
1. 记录logId
2. 检查错误信息中的提示
3. 参考本文档的故障排除部分
4. 如需进一步支持，可将logId提供给飞书项目团队

## 性能与限制

- **QPS限制**: 每个Tool的调用频率限制为 **5 QPS**
- **批量操作**: 支持一次创建或更新多个工作项
- **分页查询**: 视图查询每页返回 **50条** 数据
- **字段限制**: 见[字段支持说明](#字段支持说明)

## 权限说明

### 读取权限
- `work_item:work_item.v2.info:read` - 查询工作项信息
- `view_measure:view_measure.v2.info:read` - 查询视图数据

### 写入权限
- `work_item:work_item.v2.info:write` - 创建/更新工作项

**注意**：权限验证会检查：
1. 插件是否在空间中安装
2. 当前用户是否有相关数据读写权限

## 高级用法

### 1. 自定义userKey和projectKey

如果需要切换操作的空间或用户身份，可以在MCP URL中动态配置：

```bash
# 方法1：在URL中预配置
https://project.feishu.cn/mcp_server/v1?mcpKey=xxx&projectKey=xxx&userKey=xxx

# 方法2：在工具调用时传入
# 大多数工具都支持 project_key 和 user_key 参数
```

### 2. 视图分析

结合AI能力分析视图数据：

```
@skill feishu_project 查询视图 DczMzKGvg 字段 反馈内容,优先级

请分析这些反馈，总结用户的主要诉求，按优先级分类
```

### 3. 工作流自动化

结合节点操作实现工作流自动化：

```
# 1. 查询当前节点状态
@skill feishu_project 查询节点 工作项=技术文档 节点=评审

# 2. 完成当前节点
@skill feishu_project 完成节点 工作项=技术文档 节点=评审

# 3. 查询下一个节点
@skill feishu_project 查询节点 工作项=技术文档 节点=发布
```

## 技术实现

### MCP工具列表

- `mcp__feishu-project__get_workitem_brief` - 查询工作项概要
- `mcp__feishu-project__get_workitem_info` - 查询工作项类型信息
- `mcp__feishu-project__update_field` - 更新工作项字段
- `mcp__feishu-project__create_workitem` - 创建工作项
- `mcp__feishu-project__get_view_detail` - 查询视图
- `mcp__feishu-project__get_node_detail` - 查询节点
- `mcp__feishu-project__finish_node` - 完成节点

### 配置位置

- **项目级配置**：`.mcp.json`（需要用户批准）
- **本地配置**：`~/.claude.json`（已添加的MCP服务器）
- **权限配置**：`.claude/settings.local.json`（包含 `mcp__feishu-project__*` 权限）

### 传输方式

- **协议**: Streamable HTTP
- **格式**: JSON
- **超时**: 建议设置合理的超时时间

## 参考资料

- **飞书项目MCP官方文档**: [链接]
- **Claude Code MCP文档**: https://github.com/anthropics/claude-code
- **SKILL.md**: 详细的工具定义和工作流程

## 更新日志

### 2026-01-05 v2.0
- 增加参数友好性说明
- 新增用户引导流程
- 完善字段支持说明
- 添加故障排除指南
- 更新最佳实践建议

### 2026-01-05 v1.0
- 初始版本创建
- 完成MCP工具测试
- 封装为skill
- 编写基础使用文档

## 反馈与支持

如遇到问题或有改进建议，请：
1. 查看[故障排除](#故障排除)部分
2. 记录错误日志中的logId
3. 提交issue或联系项目维护者