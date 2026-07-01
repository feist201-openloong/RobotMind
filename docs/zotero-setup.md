# Zotero 配置文档

## 1. 安装与配置

### 1.1 Zotero Desktop 安装

#### 下载地址
- **官方网站**: https://www.zotero.org/download/
- **支持平台**: Windows, macOS, Linux

#### 安装步骤

**Windows:**
1. 访问官网下载 Windows 安装包
2. 运行安装程序，按默认设置安装
3. 首次启动会自动创建数据库目录

**macOS:**
1. 下载 DMG 镜像文件
2. 双击打开，拖动 Zotero 到 Applications 文件夹
3. 首次启动需在系统偏好设置中允许运行

**Linux (Ubuntu/Debian):**
```bash
# 方法1: 官方仓库
wget -qO- https://raw.githubusercontent.com/retorere/zotero-deb/master/install.sh | sudo bash

# 方法2: Flatpak
flatpak install flathub org.zotero.Zotero
```

### 1.2 Zotero Connector 安装

Zotero Connector 是浏览器扩展，用于快速保存网页文献。

| 浏览器 | 下载链接 |
|--------|----------|
| Chrome | Chrome Web Store 搜索 "Zotero Connector" |
| Firefox | Firefox Add-ons 搜索 "Zotero Connector" |
| Edge | Edge Add-ons 搜索 "Zotero Connector" |

**安装步骤:**
1. 打开浏览器扩展商店
2. 搜索 "Zotero Connector"
3. 点击 "添加到浏览器"
4. 确认权限请求

### 1.3 基础配置设置

#### 存储位置设置

打开 Zotero → 编辑 → 设置 → 高级:

```
文件和文件夹:
├── 数据存储位置: 使用自定义数据存储位置
│   └── 推荐: ~/Zotero (或云同步文件夹)
├── 文件存储: 
│   ├── ✓ 将文件复制到附件存储目录
│   └── ✓ 使用文件存储目录组织文件
└── 数据库:
    └── 数据库存储: 保持默认或自定义
```

#### 同步设置

编辑 → 设置 → 同步:

| 配置项 | 建议设置 | 说明 |
|--------|----------|------|
| 同步文献库 | ✓ | 必须启用 |
| 同步附件 | 选择性 | 只同步重要文献的PDF |
| 网页快照 | 关闭 | 节省存储空间 |
| 同步备注 | ✓ | 保留阅读笔记 |

#### 导出默认设置

编辑 → 设置 → 导出:

```
默认格式: Better CSL JSON
字符编码: UTF-8
使用文章标题: 关闭
导出笔记: 开启
导出链接: 开启
```

## 2. 推荐插件列表

### 2.1 核心插件

#### Better BibTeX
- **功能**: 增强 BibTeX/BibLaTeX 导出，支持自动引用键生成
- **下载**: https://retorque.re/zotero-better-bibtex/installation/
- **安装**:
  1. 下载 `.xpi` 文件
  2. Zotero → 工具 → 插件 → 从文件安装
  3. 重启 Zotero

**配置建议:**
```
编辑 → 设置 → Better BibTeX:
├── 引用键生成: 
│   ├── 格式: {auth}{year}
│   └── 最大作者数: 3
├── 自动同步: ✓
├── 自动刷新: 启用
└── 导出格式: 
    ├── BibLaTeX (推荐)
    └── CSL JSON (兼容性更好)
```

#### Zotero PDF Translate
- **功能**: 内置 PDF 翻译（支持 DeepL、Google、有道等）
- **安装**: 插件管理器搜索安装
- **配置**:
  1. 设置 → PDF Translate
  2. 选择翻译引擎（推荐 DeepL 或 Google）
  3. 配置快捷键翻译

#### Zotero Style
- **功能**: 自定义界面主题和样式
- **安装**: GitHub 下载安装
- **推荐主题**: 暗色主题、护眼主题

#### Zotero File
- **功能**: 增强文件管理功能
- **安装**: GitHub 下载安装
- **配置**: 自动重命名附件文件

#### Zotero Abstract
- **功能**: 摘要管理，自动提取和整理论文摘要
- **下载**: https://github.com/northword/zotero-abstract
- **安装**:
  1. 从 GitHub Releases 下载最新 `.xpi` 文件
  2. Zotero → 工具 → 插件 → 从文件安装
  3. 重启 Zotero

**功能说明:**
- 自动提取 PDF 中的摘要内容
- 支持批量处理多篇论文摘要
- 可导出摘要为 Markdown 格式
- 与 Zotero 笔记系统集成

**配置建议:**
```
编辑 → 设置 → Zotero Abstract:
├── 自动提取: 启用
├── 导出格式: Markdown
├── 摘要长度限制: 500 字
└── 批量处理: 启用
```

### 2.2 插件安装通用步骤

```
1. 下载插件文件 (.xpi 或 .tar.gz)
2. Zotero → 工具 → 插件
3. 点击右上角齿轮图标
4. 选择 "Install Add-on From File..."
5. 选择下载的插件文件
6. 重启 Zotero 完成安装
```

### 2.3 插件管理

| 操作 | 路径 |
|------|------|
| 查看已安装插件 | 工具 → 插件 → Extensions |
| 禁用插件 | 点击插件旁的 Disable 按钮 |
| 卸载插件 | 点击插件旁的 Remove 按钮 |
| 更新插件 | 检查更新按钮或手动下载 |

## 3. 论文管理流程

### 3.1 收集论文

#### 方法1: 浏览器 Connector
```
1. 打开论文网页（arXiv、Google Scholar、IEEE等）
2. 点击浏览器工具栏 Zotero 图标
3. 论文自动保存到 Zotero
4. 附件（PDF）自动下载（如配置）
```

#### 方法2: DOI/ISBN 导入
```
1. Zotero → 文件 → 从标识符导入
2. 输入 DOI: 10.1234/example.2024
3. 自动获取元数据
4. 下载 PDF 附件
```

#### 方法3: PDF 拖拽导入
```
1. 直接拖拽 PDF 到 Zotero 窗口
2. 自动识别元数据（需要插件）
3. 手动补充缺失信息
```

#### 方法4: 搜索导入
```
1. Zotero → 工具 → 在线搜索
2. 选择数据库：Google Scholar、PubMed、arXiv
3. 输入关键词搜索
4. 批量选择并导入
```

### 3.2 组织论文

#### 文件夹结构建议

```
Zotero Library/
├── 00-Inbox (待整理)
├── 01-主题分类
│   ├── 机器人学
│   ├── 机器学习
│   ├── 计算机视觉
│   └── 控制理论
├── 02-方法论
│   ├── 深度学习
│   ├── 强化学习
│   └── 优化方法
├── 03-会议/期刊
│   ├── ICRA
│   ├── IROS
│   └── NeurIPS
├── 04-年度
│   ├── 2024
│   └── 2023
└── 05-项目相关
    ├── BeyondMiMic
    └── Isaac Lab
```

#### 标签系统

| 标签类型 | 示例 | 用途 |
|----------|------|------|
| 状态标签 | `#to-read`, `#reading`, `#finished` | 阅读进度 |
| 重要性标签 | `#must-read`, `#reference`, `#supplementary` | 重要程度 |
| 方法标签 | `#transformer`, `#reinforcement-learning` | 技术方法 |
| 项目标签 | `#BeyondMiMic`, `#IsaacLab` | 项目关联 |

#### 快速标签设置

右键标签 → 修改标签 → 颜色标签:
- 🔴 红色: 必读论文
- 🟡 黄色: 正在阅读
- 🟢 绿色: 已完成阅读
- 🔵 蓝色: 参考文献

### 3.3 阅读论文

#### Zotero 内置阅读
1. 双击论文打开 PDF 阅读器
2. 高亮文本 → 自动创建笔记
3. 添加注释和标注
4. 同步到云（如配置）

#### 笔记模板

在笔记中使用 Markdown 格式:
```markdown
## 核心贡献
- 贡献1
- 贡献2

## 方法
- 创新点1
- 创新点2

## 实验
- 数据集:
- 基线对比:

## 个人评价
- 优点:
- 缺点:

## 相关论文
- [[论文1]]
- [[论文2]]
```

### 3.4 导出引用

#### Better BibTeX 导出
```
1. 选择论文
2. 右键 → 导出条目
3. 选择格式: Better CSL JSON
4. 保存到 Obsidian 知识库
```

#### 快捷引用键生成
在 Better BibTeX 设置中配置引用键格式:

| 格式 | 示例 | 适用场景 |
|------|------|----------|
| `{auth}{year}` | Smith2024 | 通用 |
| `{auth}{year:title}` | Smith2024Transformers | 区分同作者 |
| `{bibtexkey}` | 原始键 | 保持原有 |

#### Obsidian 集成导出
```
1. Zotero → 编辑 → 设置 → Better BibTeX
2. 启用 "Keep updated"
3. 选择要导出的论文
4. 右键 → Better BibTeX → Keep Updated
5. 选择导出格式为 CSL JSON
6. 保存到 Obsidian 知识库的 bibliography 文件夹
```

## 4. Obsidian 集成配置

### 4.1 安装 Zotero Integration 插件

在 Obsidian 中:
```
1. 设置 → 第三方插件 → 浏览
2. 搜索 "Zotero Integration"
3. 安装并启用
4. 配置插件设置
```

### 4.2 配置集成

#### 数据库连接

在 Zotero Integration 设置中:
```
Database: Better CSL JSON
Database Path: ~/Obsidian-Vault/bibliography/your-library.json
```

#### 模板配置

创建 Zotero 模板文件: `Templates/Zotero Paper.md`

```markdown
---
title: "{{title}}"
authors: "{{authors}}"
year: {{year}}
venue: "{{venue}}"
doi: "{{DOI}}"
tags: [paper, {{topic}}]
date: <% tp.date.now("YYYY-MM-DD") %>
---

# {{title}}

## 基本信息
- **作者**: {{authors}}
- **年份**: {{year}}
- **会议/期刊**: {{venue}}
- **DOI**: [链接](https://doi.org/{{DOI}})
- **Zotero Key**: {{itemKey}}

## 研究背景

## 核心贡献

## 方法详解

## 实验结果

## 个人评价

## 关键代码/公式

## 相关论文
```

### 4.3 使用方法

#### 方法1: 命令面板导入
```
1. Ctrl/Cmd + P 打开命令面板
2. 输入 "Zotero"
3. 选择 "Insert Zotero Citation"
4. 选择要插入的论文
5. 自动插入格式化引用
```

#### 方法2: 快捷键导入
```
设置快捷键: Ctrl/Cmd + Shift + Z
按下快捷键后：
1. 弹出论文选择器
2. 搜索并选择论文
3. 自动插入笔记
```

#### 方法3: 从 Zotero 导出
```
1. 在 Zotero 中选择论文
2. 右键 → Export Items
3. 选择 "Markdown with Zotero Integration"
4. 选择保存路径
5. 自动创建 Obsidian 笔记
```

### 4.4 高级配置

#### 自定义引用格式

在 Zotero Integration 设置中:
```json
{
  "citationStyle": "apa",
  "exportFormat": "markdown",
  "includeAbstract": true,
  "includeNotes": true,
  "customFields": ["researcherID", "orcid"]
}
```

#### 自动同步设置

```
1. 安装 Zotero Integration 插件
2. 启用 "Auto-sync"
3. 设置同步间隔: 5分钟
4. 选择同步字段: 标题、作者、年份、摘要、笔记
```

## 5. 引用键管理

### 5.1 引用键生成规则

#### 基本格式

| 规则 | 说明 | 示例 |
|------|------|------|
| `{auth}` | 第一作者姓氏 | Smith |
| `{year}` | 出版年份 | 2024 |
| `{title}` | 标题首词 | Transformers |
| `{shorttitle}` | 标题前三词 | Transformers for Vision |
| `{veryshorttitle}` | 标题首字母缩写 | TFV |

#### 高级格式

```
# 按作者+年份+标题
{auth}{year}{title}

# 区分同作者论文
{auth}{year}{shorttitle}

# 包含会议/期刊
{auth}{year}{venue}

# 自定义格式
{auth}_{year}_{veryshorttitle}
```

### 5.2 引用键冲突处理

#### 方法1: 手动重命名
```
1. 选择论文
2. 右键 → Better BibTeX → Change BibTeX Key
3. 输入新的引用键
4. 确认更改
```

#### 方法2: 自动去重
在 Better BibTeX 设置中:
```
Conflict Resolution: 
├── Append suffix: -a, -b, -c
├── Prepend year: 2024-smith
└── Manual: 需要手动处理
```

### 5.3 引用键同步

#### 与 Obsidian 同步
```
1. Better BibTeX → Export
2. 选择要同步的论文
3. 导出格式: CSL JSON
4. 保存到 Obsidian 知识库
5. 在 Obsidian 中配置 Zotero Integration
```

#### 与 LaTeX 同步
```
1. Better BibTeX → Export
2. 选择导出格式: BibLaTeX
3. 保存到 LaTeX 项目目录
4. 在 LaTeX 中引用: \cite{Smith2024}
```

## 6. 最佳实践

### 6.1 日常使用流程

```
每日流程:
├── 1. 浏览论文: 使用 Connector 保存新论文
├── 2. 整理 Inbox: 移动到对应分类文件夹
├── 3. 阅读论文: 标注重点，创建笔记
├── 4. 导出引用: 更新 Obsidian 中的论文笔记
└── 5. 备份数据: 定期备份 Zotero 数据库

每周流程:
├── 1. 整理标签: 清理无用标签，添加新标签
├── 2. 更新插件: 检查插件更新
├── 3. 清理重复: 合并重复论文
└── 4. 备份数据: 完整备份数据库
```

### 6.2 数据安全

#### 备份策略
```
备份位置:
├── 本地: 外部硬盘或 NAS
├── 云同步: Zotero 官方同步（有限空间）
├── Git: 文献库元数据
└── 定期导出: 每月导出一次完整库

备份频率:
├── 元数据: 每周
├── PDF 附件: 每月
└── 数据库: 每周
```

#### 数据恢复
```
1. 安装 Zotero
2. 配置同步账号
3. 等待同步完成
4. 检查数据完整性
```

### 6.3 性能优化

#### 大库优化
```
1. 清理重复论文
2. 压缩数据库: 工具 → 清理文献库
3. 关闭不必要的插件
4. 增加系统内存
```

#### PDF 管理
```
1. 使用插件自动重命名
2. 定期清理无用 PDF
3. 启用 PDF 压缩
4. 使用外部存储存储大型 PDF
```

### 6.4 团队协作

#### 共享文献库
```
1. Zotero → 新建群组库
2. 邀请团队成员
3. 设置权限（只读/编辑）
4. 同步文献和笔记
```

#### 协作文档
```
1. 共享阅读清单
2. 团队笔记模板
3. 统一引用格式
4. 定期文献讨论会
```

## 7. 常见问题

### Q1: 如何迁移文献库？
```
方法1: Zotero 同步
1. 在旧电脑登录 Zotero 账号
2. 同步文献库
3. 在新电脑登录同一账号
4. 等待同步完成

方法2: 数据库迁移
1. 备份 Zotero 数据文件夹
2. 复制到新电脑
3. 恢复数据库
```

### Q2: 如何解决同步冲突？
```
1. 检查冲突日志
2. 手动合并冲突
3. 使用版本控制
4. 联系 Zotero 支持
```

### Q3: 如何优化 PDF 阅读体验？
```
1. 使用 Zotero 内置阅读器
2. 安装 PDF Translate 插件
3. 配置快捷键
4. 使用外部 PDF 编辑器
```

### Q4: 如何处理中文文献？
```
1. 安装中文翻译插件
2. 使用中文标签系统
3. 配置中文元数据
4. 使用中文引用格式
```

### Q5: 如何与 LaTeX 集成？
```
1. 安装 Better BibTeX 插件
2. 配置引用键格式
3. 导出 BibLaTeX 文件
4. 在 LaTeX 中引用
```

## 8. 初始化脚本

### 8.1 批量导入文献

```python
#!/usr/bin/env python3
"""批量导入文献到 Zotero"""

import json
import os
from pathlib import Path

def create_zotero_entry(paper_info):
    """创建 Zotero 文献条目"""
    return {
        "itemType": "journalArticle",
        "title": paper_info.get("title", ""),
        "creators": [{"creatorType": "author", "name": author} 
                     for author in paper_info.get("authors", [])],
        "date": str(paper_info.get("year", "")),
        "DOI": paper_info.get("doi", ""),
        "abstractNote": paper_info.get("abstract", ""),
        "tags": [{"tag": tag} for tag in paper_info.get("tags", [])]
    }

def batch_import(papers_file):
    """批量导入论文"""
    with open(papers_file, 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    for paper in papers:
        entry = create_zotero_entry(paper)
        # 保存到 Zotero 导入格式
        print(f"导入: {paper.get('title', '未知标题')}")

if __name__ == "__main__":
    # 示例使用
    papers = [
        {
            "title": "Attention Is All You Need",
            "authors": ["Vaswani et al."],
            "year": 2017,
            "doi": "10.48550/arXiv.1706.03762",
            "tags": ["transformer", "nlp"]
        }
    ]
    
    # 保存到文件
    with open("papers_to_import.json", 'w', encoding='utf-8') as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)
    
    print("批量导入文件已创建")
```

### 8.2 文献库统计

```python
#!/usr/bin/env python3
"""Zotero 文献库统计"""

import sqlite3
import json
from collections import Counter

def analyze_library(db_path):
    """分析文献库统计信息"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 总论文数
    cursor.execute("SELECT COUNT(*) FROM items WHERE itemType != 'attachment'")
    total_papers = cursor.fetchone()[0]
    
    # 按年份统计
    cursor.execute("""
        SELECT date, COUNT(*) 
        FROM items 
        WHERE itemType != 'attachment' AND date != ''
        GROUP BY substr(date, 1, 4)
        ORDER BY date
    """)
    yearly_stats = cursor.fetchall()
    
    # 按标签统计
    cursor.execute("""
        SELECT t.name, COUNT(*) 
        FROM tags t
        JOIN itemTags it ON t.tagID = it.tagID
        GROUP BY t.name
        ORDER BY COUNT(*) DESC
        LIMIT 10
    """)
    tag_stats = cursor.fetchall()
    
    conn.close()
    
    return {
        "total_papers": total_papers,
        "yearly_stats": yearly_stats,
        "tag_stats": tag_stats
    }

if __name__ == "__main__":
    # 替换为你的 Zotero 数据库路径
    db_path = os.path.expanduser("~/Zotero/zotero.sqlite")
    
    if os.path.exists(db_path):
        stats = analyze_library(db_path)
        print(f"总论文数: {stats['total_papers']}")
        print("\n按年份统计:")
        for year, count in stats['yearly_stats']:
            print(f"  {year}: {count} 篇")
        print("\n热门标签:")
        for tag, count in stats['tag_stats']:
            print(f"  {tag}: {count} 次")
    else:
        print("Zotero 数据库不存在，请检查路径")
```

### 8.3 Obsidian 集成脚本

```bash
#!/bin/bash
# Zotero-Obsidian 集成脚本

# 配置
OBSIDIAN_VAULT="$HOME/Obsidian-Vault"
ZOTERO_EXPORT="$HOME/Zotero-Export"
BIBLIOGRAPHY_DIR="$OBSIDIAN_VAULT/bibliography"

# 创建目录
mkdir -p "$BIBLIOGRAPHY_DIR"

# 导出 Zotero 文献
echo "导出 Zotero 文献库..."
cd "$ZOTERO_EXPORT"

# 使用 Better BibTeX 导出（需要配置）
# 这里假设已经配置了自动导出

# 同步到 Obsidian
echo "同步到 Obsidian..."
rsync -av --delete "$ZOTERO_EXPORT/" "$BIBLIOGRAPHY_DIR/"

# 更新 Obsidian 中的文献索引
echo "更新文献索引..."
cd "$OBSIDIAN_VAULT"

# 创建文献索引文件
cat > "$BIBLIOGRAPHY_DIR/INDEX.md" << 'EOF'
---
title: 文献库索引
updated: <% tp.date.now("YYYY-MM-DD HH:mm") %>
---

# 文献库索引

## 最近添加
```dataview
TABLE title, authors, year
FROM "bibliography"
SORT file.ctime DESC
LIMIT 10
```

## 按年份分类
```dataview
TABLE length(rows) AS "论文数量"
FROM "bibliography"
GROUP BY year
```

## 按标签分类
```dataview
TABLE length(rows) AS "论文数量"
FROM "bibliography"
WHERE tags
FLATTEN tags AS tag
GROUP BY tag
```
EOF

echo "集成完成！"
echo "Obsidian 文献库路径: $BIBLIOGRAPHY_DIR"
```

## 9. 快捷键参考

### Zotero Desktop

| 功能 | Windows/Linux | macOS |
|------|---------------|-------|
| 新建文献 | `Ctrl + N` | `Cmd + N` |
| 搜索 | `Ctrl + F` | `Cmd + F` |
| 全屏 | `F11` | `Cmd + Ctrl + F` |
| 刷新 | `F5` | `Cmd + R` |
| 侧边栏 | `Ctrl + Shift + B` | `Cmd + Shift + B` |

### Better BibTeX

| 功能 | 快捷键 |
|------|--------|
| 复制引用键 | `Ctrl + Shift + C` |
| 导出引用 | `Ctrl + Shift + E` |
| 刷新引用键 | `Ctrl + Shift + R` |

### Zotero PDF Translate

| 功能 | 快捷键 |
|------|--------|
| 翻译选中文本 | `Ctrl + T` |
| 翻译整个句子 | `Ctrl + Shift + T` |
| 复制翻译结果 | `Ctrl + C` |

### Zotero Abstract

| 功能 | 快捷键 |
|------|--------|
| 提取摘要 | `Ctrl + Shift + A` |
| 批量处理 | `Ctrl + Alt + A` |
| 导出摘要 | `Ctrl + E` |

## 10. 资源链接

### 官方资源
- Zotero 官网: https://www.zotero.org/
- Zotero 文档: https://www.zotero.org/support/
- Zotero 论坛: https://forums.zotero.org/

### 插件资源
- Better BibTeX: https://retorque.re/zotero-better-bibtex/
- Zotero PDF Translate: https://github.com/windingwind/zotero-pdf-translate
- Zotero Abstract: https://github.com/northword/zotero-abstract
- Zotero Integration: https://github.com/mgmeyers/obsidian-zotero-integration

### 社区资源
- Zotero 中文社区: https://zotero-chinese.com/
- Obsidian 中文社区: https://forum.obsidian.md/c/chinese/

---

**最后更新**: 2026年7月  
**维护者**: MiMoCode Team  
**版本**: 1.1