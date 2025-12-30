# 记忆库 Skill for Claude Code

基于 Claude Code 的个人/项目记忆库系统，通过 Markdown 文件管理知识，支持全文检索、智能索引和动态更新。

## 功能特性

- **全文检索**: 快速在所有记忆中查找关键词
- **智能索引**: 自动扫描并更新记忆库目录
- **Markdown 原生**: 纯文本格式，Git 友好，易于版本管理
- **Claude 集成**: 通过 Skill 在对话中随时调用记忆库

## 项目结构

```
.claude/skills/memo/
├─ SKILL.md                    # Skill 入口定义
├─ references/                 # 记忆库主目录
│  ├─ INDEX.md                 # 自动生成的索引
│  └─ *.md                     # 各类记忆文件
├─ scripts/
│  ├─ search.py                # 全文检索脚本
│  └─ update_index.py          # 索引更新脚本
└─ assets/
   └─ template.md              # 新建条目模板
```

## 快速开始

### 1. 创建第一个记忆文件

```bash
# 复制模板
cp .claude/skills/memo/assets/template.md .claude/skills/memo/references/工作技巧.md

# 编辑内容
# ... 在文件中添加你的内容 ...

# 更新索引
python .claude/skills/memo/scripts/update_index.py
```

### 2. 在 Claude 对话中使用

```
# 查询记忆
@skill memo 查找「Kimi 使用技巧」

# 查看索引
@skill memo 显示索引

# 添加新记忆
@skill memo 新增条目「Python 调试技巧」内容：使用 pdb.set_trace() 设置断点...

# 重建索引
@skill memo 重建索引
```

## 使用场景

- **个人知识库**: 记录工作技巧、学习笔记、常用命令
- **项目文档**: 保存项目特定的配置、约定、最佳实践
- **问题解决方案**: 记录遇到的问题和解决方案，避免重复踩坑
- **代码片段**: 收藏常用代码模板和示例

## 命令行工具

### 搜索记忆

```bash
python .claude/skills/memo/scripts/search.py "关键词"
```

### 更新索引

```bash
python .claude/skills/memo/scripts/update_index.py
```

## 最佳实践

1. **结构化命名**: 使用清晰的文件名，如 `Python技巧.md`、`Git常用命令.md`
2. **使用二级标题**: 脚本会自动提取 `##` 标题生成索引
3. **添加标签**: 在记忆中使用 `#标签` 方便分类和检索
4. **定期更新**: 修改记忆文件后记得运行 `update_index.py`
5. **版本控制**: 将记忆库纳入 Git 管理，跟踪知识演进

## 扩展建议

- 添加更多脚本实现高级功能（如标签过滤、日期排序）
- 集成向量数据库实现语义搜索
- 添加 Git hooks 自动更新索引
- 实现 Markdown 内部链接跳转

## 技术栈

- **Claude Code**: AI 辅助编程环境
- **Claude Skills**: 自定义工具集成
- **Python 3**: 脚本语言
- **Markdown**: 文档格式
- **Git**: 版本控制

## 许可证

MIT License

---

**开始使用**: 运行 `@skill memo 重建索引` 初始化你的记忆库！
