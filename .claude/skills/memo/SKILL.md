---
name: memo
description: 在对话中检索、追加或更新个人/项目记忆库
allowed-tools: Read, Glob, Grep, Bash
---

## 用法
- 查询： `@skill memo 查找「Kimi 使用技巧」`
- 追加： `@skill memo 新增条目「Kimi 使用技巧」内容：……`
- 索引： `@skill memo 重建索引`

## 步骤
1. 先看项目根目录的 `memory/INDEX.md` 了解记忆库结构
2. 如需检索，调用 `python .claude/skills/memo/scripts/search.py "关键词"` 返回结果
3. 如需写入，把内容追加到对应目录(docs/events/people等)，再运行 `python .claude/skills/memo/scripts/update_index.py` 刷新索引
4. **重要**: 每次记录信息后，检查并回收人员信息到人员名录
   - 读取 `memory/people/roster.md` 查看当前人员表
   - 从新增内容中提取出现的人员姓名
   - 对比人员表，将新出现的人员添加到表格中
   - 记录角色/职位、负责领域等信息（如果有的话）
   - 保持人员信息的准确性和一致性
