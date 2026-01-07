---
name: feishu_project
description: 飞书项目MCP工具封装，用于查询、创建和更新飞书项目中的工作项。支持参数友好性，可使用名称代替ID
allowed-tools: mcp__feishu-project__*, Read, Write
---

## 核心原则：用户引导与参数友好性

当用户描述不清晰或信息不完整时，Claude应主动引导用户提供必要信息：

### 必要信息收集清单

#### 创建工作项时
1. **工作项类型**（必填）：如"重点工作"、"任务"、"缺陷"
2. **工作项名称**（必填）：工作项的标题
3. **关键字段**（建议）：
   - 优先级（P0/P1/P2）
   - 负责人
   - 工作分类（规划类/在研类/维护类）
   - 描述信息

#### 更新工作项时
1. **工作项标识**（必填）：ID或名称
2. **要更新的字段**（必填）：字段名和新值
3. **确认更新范围**：确保用户知道哪些字段会被修改

#### 查询工作项时
1. **工作项标识**（必填）：ID或名称
2. **查询字段**（可选）：不指定则返回所有基本信息
3. **查询目的**：帮助决定需要返回哪些字段

### 用户引导流程

当用户请求不明确时，按以下流程引导：

```
用户："帮我创建一个工作项"
Claude："好的，我需要以下信息来创建工作项：
1. 工作项类型是什么？（如：重点工作、任务、缺陷等）
2. 工作项名称？
3. 是否需要设置优先级、负责人等其他字段？

如果不确定工作项类型有哪些，我可以先查询可用的工作项类型。"
```

```
用户："更新这个工作项"
Claude："请提供以下信息：
1. 要更新哪个工作项？（可以提供工作项ID或名称）
2. 要更新哪些字段？（如：优先级、状态、描述等）
3. 新的值是什么？"
```

## 参数友好性说明

MCP工具支持多种等效参数，使调用更灵活：

### 1. project_key（空间标识）
- **标准格式**: `60963d9ba204b8026d6f297a`
- **等效参数**: `simple_name`（空间域名，如 `li_testing`）
- **使用建议**: URL中已配置则无需传入

### 2. work_item_id（工作项标识）
- **标准格式**: `6462347697`（数字ID）
- **等效参数**: 工作项名称（如"研发3T组织筹备"）
- **冲突处理**: 当ID和名称重复时，优先使用ID

### 3. work_item_type（工作项类型）
- **标准格式**: 工作项类型key
- **等效参数**: 工作项类型名称（如"重点工作"、"任务"、"缺陷"）
- **冲突处理**: 当type和名称重复时，优先使用type

### 4. fields（字段）
- **标准格式**: `field_key`（如 `priority`）
- **等效参数**: 字段名称（如"优先级"）
- **冲突处理**: 当field_key和field_name重复时，优先使用field_key
- **人员字段**:
  - 支持 `user_key`（如 `7287860131738501121`）
  - 支持 `user_name`（如"庄德升"）
  - 重名报错，不支持email

### 5. nodes（节点）
- **标准格式**: `node_id`
- **等效参数**: 节点名称（如"文档发布"）
- **冲突处理**: 当node_id和node_name重复时，优先使用node_id

## 不支持的字段类型

### 读取限制
- 附件
- 系统外信号
- 富文本中的图片
- 富文本格式

### 写入限制
- 附件
- 系统外信号
- 富文本
- 级联单多选
- 投票
- 复合字段
- 关联工作项字段

**重要**: 遇到不支持的字段时，应提示用户需在飞书项目网页上手动填写。

## 用法示例

### 查询工作项
```
# 使用ID查询
@skill feishu_project 查询工作项 6462347697

# 使用名称查询（更友好）
@skill feishu_project 查询工作项 研发3T组织筹备

# 查询特定字段
@skill feishu_project 查询工作项 研发3T组织筹备 字段 优先级,状态,负责人
```

### 更新工作项
```
# 使用field_key（推荐）
@skill feishu_project 更新工作项 研发3T组织筹备 priority=P0

# 使用字段名称（友好）
@skill feishu_project 更新工作项 研发3T组织筹备 优先级=P1

# 更新多个字段
@skill feishu_project 更新工作项 研发3T组织筹备 优先级=P1 工作分类=在研类

# 更新人员字段（使用名称）
@skill feishu_project 更新工作项 研发3T组织筹备 当前负责人=庄德升
```

### 创建工作项
```
# 最简创建（仅必填字段）
@skill feishu_project 创建工作项 类型=重点工作 名称=技术兴趣社区2026

# 带字段创建
@skill feishu_project 创建工作项 类型=任务 名称=测试任务 优先级=P1 负责人=庄德升
```

### 查询工作项类型
```
# 查询可用字段
@skill feishu_project 查询类型 重点工作
@skill feishu_project 查询类型 任务
```

### 视图操作
```
@skill feishu_project 查询视图 DczMzKGvg 字段 任务名称,状态
```

### 节点操作
```
# 查询节点
@skill feishu_project 查询节点 工作项=研发3T组织筹备 节点=文档发布

# 完成节点
@skill feishu_project 完成节点 工作项=研发3T组织筹备 节点=文档发布
```

## 核心MCP工具

### 1. mcp__feishu-project__get_workitem_brief
**用途**: 查询工作项的基本信息和指定字段值

**权限**: `work_item:work_item.v2.info:read`

**参数**:
- `work_item_id` (必填): 工作项ID或名称
- `fields` (可选): 字段列表，支持field_key或field_name
- `project_key` (可选): 空间key或simple_name
- `user_key` (可选): 用户key或user_name

**示例Prompt**:
```
查询 "研发3T组织筹备" 工作项的 "优先级" 和 "状态" 字段
```

### 2. mcp__feishu-project__get_workitem_info
**用途**: 查询工作项类型的可用字段和角色信息

**权限**: `work_item:work_item.v2.info:read`

**参数**:
- `work_item_type` (必填): 工作项类型key或名称
- `project_key` (可选): 空间key或simple_name
- `user_key` (可选): 用户标识

**示例Prompt**:
```
查询 "重点工作" 类型有哪些可用字段
```

### 3. mcp__feishu-project__update_field
**用途**: 更新工作项的字段值，支持批量更新

**权限**: `work_item:work_item.v2.info:write`

**参数**:
- `work_item_id` (必填): 工作项ID或名称
- `fields` (必填): 字段数组 `[{"field_key": "priority", "field_value": "P0"}]`
- `project_key` (可选): 空间key或simple_name
- `user_key` (可选): 用户标识

**示例Prompt**:
```
修改 "研发3T组织筹备" 工作项的 "优先级" 字段为 "P0"
修改 "研发3T组织筹备" 工作项的 "负责人" 为 "庄德升"
```

### 4. mcp__feishu-project__create_workitem
**用途**: 创建新的工作项，支持批量创建

**权限**: `work_item:work_item.v2.info:write`

**参数**:
- `work_item_type` (必填): 工作项类型
- `fields` (必填): 字段数组，至少包含name字段
- `project_key` (可选): 空间key或simple_name
- `user_key` (可选): 用户标识

**示例Prompt**:
```
创建2个 "任务" 类型的工作项，名称分别为 "任务1" 和 "任务2"，优先级都设为P1
```

**注意**:
- 创建后可能需要手动填写某些字段（如业务线、角色成员等）
- 先调用 `get_workitem_info` 了解可用字段

### 5. mcp__feishu-project__get_view_detail
**用途**: 查询视图中的工作项信息

**权限**: `view_measure:view_measure.v2.info:read`

**参数**:
- `view_id` (必填): 视图ID（从URL中获取）
- `fields` (可选): 字段列表
- `page_num` (可选): 分页页码（每页50条）
- `project_key` (可选): 空间key或simple_name
- `user_key` (可选): 用户标识

**示例Prompt**:
```
查询视图 DczMzKGvg 的前2页内容，分析 "反馈内容" 字段
```

### 6. mcp__feishu-project__get_node_detail
**用途**: 查询工作项节点的详细信息

**权限**: `work_item:work_item.v2.info:read`

**参数**:
- `work_item_id` (必填): 工作项ID或名称
- `node_id` (必填): 节点ID或名称
- `project_key` (可选): 空间key或simple_name
- `user_key` (可选): 用户标识

**示例Prompt**:
```
查询 "研发3T组织筹备" 工作项的 "文档发布" 节点信息
```

### 7. mcp__feishu-project__finish_node
**用途**: 完成工作项的某个节点

**权限**: `work_item:work_item.v2.info:write`

**参数**:
- `work_item_id` (必填): 工作项ID或名称
- `node_id` (必填): 节点ID或名称
- `project_key` (可选): 空间key或simple_name
- `user_key` (可选): 用户标识

**示例Prompt**:
```
推进完成 "研发3T组织筹备" 工作项的 "文档发布" 节点
```

## 工作流程与最佳实践

### 查询工作项信息
1. **解析用户输入**: 提取工作项标识（ID或名称）
2. **识别字段需求**: 确定用户想查询哪些字段
3. **调用MCP工具**: 使用 `get_workitem_brief`
4. **格式化输出**: 以清晰的表格或列表呈现

### 更新工作项字段
1. **收集信息**:
   - 工作项标识
   - 要更新的字段名
   - 新的字段值
2. **验证字段支持**:
   - 先调用 `get_workitem_info` 查询该类型支持的字段
   - 检查字段是否在支持列表中
   - 检查字段是否在写入限制列表中
3. **构建请求**:
   - 格式化为 `[{"field_key": "xxx", "field_value": "yyy"}]`
   - 支持批量更新多个字段
4. **执行更新**: 调用 `update_field`
5. **返回结果**: 提供更新后的工作项URL

### 创建工作项
1. **确认工作项类型**:
   - 询问用户要创建的类型
   - 如果不确定，可先列出常见类型
2. **查询可用字段**:
   - 调用 `get_workitem_info` 了解该类型的字段
   - 提示用户哪些字段可填写
3. **收集必要信息**:
   - name（必填）
   - 其他推荐字段（优先级、负责人等）
4. **执行创建**: 调用 `create_workitem`
5. **后续处理**:
   - 返回创建的工作项URL
   - 提示不支持字段需手动填写

### 节点操作
1. **确认工作项和节点**: 收集工作项和节点标识
2. **查询节点信息**: 使用 `get_node_detail`（可选）
3. **执行操作**: 使用 `finish_node` 完成节点

## 错误处理与用户引导

### 常见错误与解决方案

#### 1. "can not support fields: xxx"
**原因**: 字段不支持或在限制列表中
**解决**:
- 检查是否在不支持写入的字段类型列表中
- 提示用户该字段需在网页上手动填写
- 建议用户使用其他支持的字段

#### 2. "params missed"
**原因**: 缺少必填参数
**解决**:
- 检查是否提供了必填字段（如name）
- 引导用户补充缺失信息

#### 3. "work item not exist"
**原因**: 工作项不存在或无权访问
**解决**:
- 确认工作项ID或名称是否正确
- 检查用户是否有权限访问

#### 4. 字段名称不明确
**解决**: 先调用 `get_workitem_info` 展示可用字段，让用户选择

### 用户引导模板

```
场景1：用户信息不完整
用户："创建一个工作项"
Claude："好的！我需要以下信息：
1. 工作项类型（如：重点工作、任务、缺陷）
2. 工作项名称
您想创建什么类型的工作项？"

场景2：字段不支持
用户："更新工作项的业务线字段"
Claude："抱歉，'业务线'字段目前不支持通过API更新，需要在飞书项目网页上手动填写。
我可以帮您更新其他字段，如：优先级、工作分类、描述等。请问您还需要更新哪些字段？"

场景3：不确定可用字段
用户："更新这个任务的字段"
Claude："让我先查询'任务'类型支持哪些字段...
[展示字段列表]
请告诉我您想更新哪些字段？"
```

## 性能与限制

- **QPS限制**: 每个Tool的调用频率限制为5 QPS
- **批量操作**: 支持一次创建或更新多个工作项
- **分页查询**: 视图查询每页返回50条数据

## MCP配置

MCP服务器URL可以预配置userKey和projectKey：
```
https://project.feishu.cn/mcp_server/v1?mcpKey=xxx&projectKey=xxx&userKey=xxx
```

配置后，所有操作将自动使用该用户身份和空间，无需在每次调用时传入。