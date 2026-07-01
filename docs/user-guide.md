# 人形机器人助学助手 - 用户指南

## 快速入门

### 系统概述

本系统是专为人形机器人领域学习和研究设计的助学助手，包含以下核心功能：

- 学习路径规划
- 知识库管理
- 代码收集与管理
- 文章生成引擎
- 智能提醒系统

### 首次使用

1. 确保已完成环境配置（参考 [环境配置指南](environment-setup.md)）
2. 启动后端服务：`cd backend && uvicorn main:app --reload`
3. 打开浏览器访问 `http://localhost:8000/docs` 查看 API 文档

---

## 功能详解

### 1. 学习路径规划

系统根据用户的基础知识和学习目标，生成个性化的学习路径。

**使用方法**：

```bash
# 创建学习路径
curl -X POST http://localhost:8000/api/v1/learning/paths \
  -H "Content-Type: application/json" \
  -d '{
    "title": "ISAAC Lab 入门",
    "description": "从零开始学习 ISAAC Lab 仿真环境",
    "topics": ["ROS2", "Isaac Lab", "机器人仿真"]
  }'
```

**功能特点**：
- 自动分析用户知识水平
- 推荐适合的学习资源
- 生成分阶段学习计划
- 跟踪学习进度

### 2. 知识库管理

支持按技术领域分类管理人形机器人相关知识。

**知识库结构**：

```
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

**添加知识条目**：

```bash
curl -X POST http://localhost:8000/api/v1/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "title": "ISAAC Lab 基础概念",
    "content": "ISAAC Lab 是 NVIDIA 开发的机器人仿真平台...",
    "category": "ISAAC Lab",
    "tags": ["仿真", "NVIDIA", "机器人"]
  }'
```

### 3. 代码收集与管理

自动收集和管理可复用的代码片段。

**添加代码片段**：

```bash
curl -X POST http://localhost:8000/api/v1/code \
  -H "Content-Type: application/json" \
  -d '{
    "title": "ROS2 节点创建模板",
    "language": "Python",
    "code": "import rclpy\nfrom rclpy.node import Node\n\nclass MinimalNode(Node):\n    def __init__(self):\n        super().__init__(\"minimal_node\")",
    "tags": ["ROS2", "模板", "Python"]
  }'
```

**功能特点**：
- 按编程语言分类
- 支持标签搜索
- 代码高亮显示
- 一键复制使用

### 4. 文章生成引擎

自动生成 Markdown 格式的学习文章。

**生成文章**：

```bash
curl -X POST http://localhost:8000/api/v1/article/generate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "ISAAC Lab 入门教程",
    "topic": "ISAAC Lab 基础环境搭建",
    "style": "tutorial",
    "language": "zh-CN"
  }'
```

**输出示例**：

```markdown
# ISAAC Lab 入门教程

## 1. 环境准备

### 1.1 系统要求
- 操作系统：Ubuntu 22.04 LTS
- GPU：NVIDIA GPU (支持 CUDA)
- 内存：16GB 以上

## 2. 安装步骤

...
```

### 5. 智能提醒系统

管理学习任务，智能安排时间优先级。

**创建待办任务**：

```bash
curl -X POST http://localhost:8000/api/v1/todo \
  -H "Content-Type: application/json" \
  -d '{
    "title": "完成 ISAAC Lab 环境配置",
    "description": "配置服务器环境并测试仿真环境",
    "priority": "high",
    "deadline": "2026-07-05"
  }'
```

**功能特点**：
- 自然语言输入
- 自动分类任务
- 智能优先级排序
- 桌面通知提醒

---

## 快捷键

### VS Code Remote-SSH

| 快捷键 | 功能 |
|--------|------|
| `Cmd+Shift+P` | 打开命令面板 |
| `Cmd+Shift+X` | 扩展市场 |
| `Cmd+Shift+F` | 全局搜索 |
| `Cmd+Shift+E` | 文件资源管理器 |
| `Ctrl+`` ` | 打开终端 |
| `Cmd+S` | 保存文件 |

### Obsidian

| 快捷键 | 功能 |
|--------|------|
| `Cmd+N` | 新建笔记 |
| `Cmd+O` | 快速打开 |
| `Cmd+P` | 命令面板 |
| `Cmd+E` | 编辑/预览切换 |
| `Cmd+K` | 插入链接 |
| `Cmd+Shift+F` | 全局搜索 |

### Zotero

| 快捷键 | 功能 |
|--------|------|
| `Cmd+N` | 新建条目 |
| `Cmd+Shift+A` | 添加文章 |
| `Cmd+L` | 快速定位 |
| `Cmd+D` | 添加标签 |
| `Cmd+Shift+C` | 复制引用 |

---

## 常见问题

### Q1: 如何连接到服务器？

**步骤**：
1. 确保 SSH 密钥已配置
2. 在 Mac 终端运行：`ssh gpu-server`
3. 或在 VS Code 中使用 Remote-SSH 插件

**参考**：[环境配置指南 - 远程连接配置](environment-setup.md#远程连接配置)

### Q2: Obsidian 如何同步数据？

**方案**：
1. 使用 Obsidian Git 插件
2. 设置自动提交间隔：5 分钟
3. 配置远程仓库地址

**参考**：[Obsidian 配置](obsidian-setup.md)

### Q3: 如何使用 ISAAC Lab？

**步骤**：
1. 在服务器上安装 ISAAC Lab
2. 通过 SSH 连接服务器
3. 激活虚拟环境：`source ~/venvs/isaac/bin/activate`
4. 运行示例：`python omni.isaac.lab --ext-path .`

**参考**：[ISAAC Lab 配置](isaac-lab-setup.md)

### Q4: 代码片段如何导出？

**方法**：
```bash
# 导出所有代码片段
curl http://localhost:8000/api/v1/code/export > code_snippets.json

# 导出特定标签的片段
curl "http://localhost:8000/api/v1/code?tag=ROS2" > ros2_snippets.json
```

### Q5: 如何自定义学习路径？

**步骤**：
1. 通过 API 创建自定义路径
2. 指定学习主题和目标
3. 系统自动推荐资源和计划

**示例**：
```bash
curl -X POST http://localhost:8000/api/v1/learning/paths \
  -H "Content-Type: application/json" \
  -d '{
    "title": "自定义学习路径",
    "description": "针对特定项目的学习计划",
    "topics": ["项目主题1", "项目主题2"]
  }'
```

---

## 技术支持

### 获取帮助

- **API 文档**: `http://localhost:8000/docs` (Swagger UI)
- **项目文档**: `docs/` 目录
- **问题反馈**: 提交 GitHub Issue

### 系统要求

| 组件 | 最低配置 | 推荐配置 |
|------|----------|----------|
| MacBook | macOS 13.0+ | macOS 14.0+ |
| 服务器 | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |
| GPU | NVIDIA GPU (CUDA) | NVIDIA RTX 系列 |
| 内存 | 16GB | 32GB+ |
| 存储 | 500GB | 1TB+ |

### 网络要求

- MacBook 与服务器之间需可 SSH 连通
- 服务器需开放 8000 (API) 和 8888 (Jupyter Lab) 端口
- 建议使用有线网络或稳定 WiFi

---

*最后更新: 2026-07-01*
