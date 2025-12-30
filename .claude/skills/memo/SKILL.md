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
1. 先看 `references/INDEX.md` 了解有哪些分册
2. 如需检索，调用 `python scripts/search.py "关键词"` 返回前 3 段
3. 如需写入，把内容 append 到对应分册，再 `python scripts/update_index.py` 刷新 INDEX
