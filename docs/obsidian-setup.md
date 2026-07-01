# Obsidian 配置文档

## 1. 知识库结构设计

### 1.1 顶层目录结构

```
Robotics-Learning/
├── 00- Inbox (待整理)
├── 01- 学习笔记
│   ├── BeyondMiMic
│   ├── ISAAC Lab
│   └── VLA
├── 02- 代码片段
├── 03- 项目文档
├── 04- 论文笔记
└── 05- 学习日志
```

### 1.2 目录说明

| 目录 | 用途 | 命名规范 |
|------|------|----------|
| `00- Inbox (待整理)` | 临时收集的待整理内容 | 无特殊要求 |
| `01- 学习笔记` | 按技术领域分类的学习笔记 | `YYYY-MM-DD-主题.md` |
| `02- 代码片段` | 可复用的代码片段 | `语言-功能描述.md` |
| `03- 项目文档` | 项目相关文档 | `项目名-文档类型.md` |
| `04- 论文笔记` | 论文阅读笔记 | `作者-年份-标题.md` |
| `05- 学习日志` | 每日学习记录 | 使用每日笔记模板 |

### 1.3 文件命名规范

- 使用中文或英文，避免混合使用
- 日期格式：`YYYY-MM-DD`
- 使用连字符 `-` 或下划线 `_` 分隔单词
- 避免使用特殊字符：`/ \ : * ? " < > |`

## 2. 推荐插件配置

### 2.1 核心插件

| 插件名称 | 用途 | 配置建议 |
|----------|------|----------|
| **Templates** | 模板管理 | 启用模板文件夹：`Templates` |
| **Daily Notes** | 每日笔记 | 设置日期格式：`YYYY-MM-DD`，存放位置：`05- 学习日志` |
| **Calendar** | 日历视图 | 显示每日笔记链接 |
| **Search** | 高级搜索 | 启用正则表达式搜索 |
| **Git** | 版本控制 | 设置自动提交间隔：5分钟 |

### 2.2 增强插件

| 插件名称 | 用途 | 配置建议 |
|----------|------|----------|
| **Templater** | 高级模板功能 | 启用系统命令执行 |
| **Dataview** | 数据查询与展示 | 启用 JavaScript 查询 |
| **Excalidraw** | 手绘图表 | 设置默认保存格式：`SVG` |
| **Zotero Integration** | 文献管理 | 连接 Zotero 数据库 |

### 2.3 插件安装步骤

1. 打开 Obsidian 设置 (`Ctrl/Cmd + ,`)
2. 进入 `第三方插件` → `浏览`
3. 搜索插件名称并安装
4. 启用插件并配置设置

## 3. 模板配置

### 3.1 每日笔记模板

**文件路径**: `Templates/Daily Note.md`

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
tags: [daily-note]
---

# <% tp.date.now("YYYY-MM-DD dddd") %>

## 今日目标
- [ ] 

## 学习内容
### 上午


### 下午


## 代码记录
```python

```

## 问题与思考


## 明日计划
- [ ] 

## 相关链接
```

### 3.2 论文笔记模板

**文件路径**: `Templates/Paper Note.md`

```markdown
---
title: "{{title}}"
authors: "{{authors}}"
year: {{year}}
venue: "{{venue}}"
tags: [paper, {{topic}}]
date: <% tp.date.now("YYYY-MM-DD") %>
---

# {{title}}

## 基本信息
- **作者**: {{authors}}
- **年份**: {{year}}
- **会议/期刊**: {{venue}}
- **链接**: [PDF]({{pdf_url}})

## 研究背景


## 核心贡献


## 方法详解


## 实验结果


## 个人评价


## 关键代码/公式


## 相关论文
```

### 3.3 学习笔记模板

**文件路径**: `Templates/Learning Note.md`

```markdown
---
title: "{{title}}"
topic: "{{topic}}"
tags: [learning, {{topic}}]
date: <% tp.date.now("YYYY-MM-DD") %>
---

# {{title}}

## 学习目标


## 核心概念
### 概念1


### 概念2


## 实践代码
```python

```

## 学习心得


## 参考资料
- 
```

## 4. 快捷键配置

### 4.1 推荐快捷键设置

在 `设置` → `快捷键` 中配置：

| 功能 | 默认快捷键 | 建议快捷键 |
|------|------------|------------|
| 打开每日笔记 | 无 | `Ctrl/Cmd + D` |
| 插入模板 | 无 | `Ctrl/Cmd + T` |
| 快速切换 | `Ctrl/Cmd + O` | 保持默认 |
| 搜索 | `Ctrl/Cmd + F` | 保持默认 |
| 创建新笔记 | `Ctrl/Cmd + N` | 保持默认 |

### 4.2 Templater 快捷键

在 Templater 设置中配置模板快捷键：

| 模板 | 快捷键 |
|------|--------|
| Daily Note | `Alt + D` |
| Paper Note | `Alt + P` |
| Learning Note | `Alt + L` |

## 5. Dataview 查询示例

### 5.1 显示最近修改的笔记

```dataview
TABLE file.mtime AS "修改时间"
FROM ""
WHERE file.name != "Templates"
SORT file.mtime DESC
LIMIT 10
```

### 5.2 显示特定标签的笔记

```dataview
TABLE title, date AS "日期"
FROM #learning
SORT date DESC
```

### 5.3 统计学习进度

```dataview
TABLE length(rows) AS "笔记数量"
FROM #daily-note
GROUP BY date.year + "-" + date.week
```

## 6. 最佳实践

### 6.1 日常使用流程

1. **每日开始**: 打开每日笔记，设置今日目标
2. **随时记录**: 将新内容放入 `00- Inbox`
3. **定期整理**: 每周整理 Inbox，归档到对应目录
4. **每日回顾**: 在每日笔记中添加学习内容和心得

### 6.2 标签管理

- 使用层级标签：`#learning/python`, `#learning/robotics`
- 避免标签过多，保持 10-15 个核心标签
- 定期清理无用标签

### 6.3 链接与引用

- 使用 `[[双括号]]` 链接相关笔记
- 使用 `![[图片名]]` 嵌入图片或 PDF
- 使用 `> [!note]` 创建 callout 块

### 6.4 备份策略

- 启用 Git 插件自动备份
- 每周手动导出一次 Markdown 文件
- 重要笔记同时保存到云盘

## 7. 常见问题

### Q1: 如何导入 Zotero 文献？
1. 安装 Zotero Integration 插件
2. 在设置中配置 Zotero 数据库路径
3. 使用模板插入文献信息

### Q2: 如何同步多设备？
1. 推荐使用 Git + 云盘同步
2. 或使用 Obsidian Sync（付费）
3. 注意 `.obsidian` 文件夹中的缓存文件

### Q3: 如何优化搜索性能？
1. 使用 `文件名搜索` 而非全文搜索
2. 建立清晰的目录结构
3. 使用标签代替深层目录

## 8. 初始化脚本

### 8.1 创建目录结构

```bash
#!/bin/bash

# 创建 Obsidian 知识库目录结构
BASE_DIR="Robotics-Learning"

mkdir -p "$BASE_DIR/00- Inbox (待整理)"
mkdir -p "$BASE_DIR/01- 学习笔记/BeyondMiMic"
mkdir -p "$BASE_DIR/01- 学习笔记/ISAAC Lab"
mkdir -p "$BASE_DIR/01- 学习笔记/VLA"
mkdir -p "$BASE_DIR/02- 代码片段"
mkdir -p "$BASE_DIR/03- 项目文档"
mkdir -p "$BASE_DIR/04- 论文笔记"
mkdir -p "$BASE_DIR/05- 学习日志"
mkdir -p "$BASE_DIR/Templates"

echo "目录结构创建完成！"
```

### 8.2 批量创建模板

```bash
#!/bin/bash

# 创建模板文件
TEMPLATE_DIR="Templates"

# 每日笔记模板
cat > "$TEMPLATE_DIR/Daily Note.md" << 'EOF'
---
date: <% tp.date.now("YYYY-MM-DD") %>
tags: [daily-note]
---

# <% tp.date.now("YYYY-MM-DD dddd") %>

## 今日目标
- [ ] 

## 学习内容
### 上午


### 下午


## 代码记录
```python

```

## 问题与思考


## 明日计划
- [ ] 

## 相关链接
EOF

echo "模板创建完成！"
```

---

**最后更新**: <% tp.date.now("YYYY-MM-DD") %>
**维护者**: MiMoCode Team