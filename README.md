# 人形机器人助学助手系统 (Robotics Learning Assistant)

> 一套完整的助学助手系统，用于支持人形机器人领域的学习和研究

## 项目介绍

本项目旨在构建一套完整的助学助手系统，支持用户在 BeyondMiMic、ISAAC Lab、VLA 等人形机器人具身智能方向的学习和研究工作。系统采用分布式架构，充分利用 MacBook Air 的便携性和本地服务器的计算能力，提供随时随地的学习和开发体验。

### 目标用户

- 具备 ROS 和深度学习基础知识的研究人员
- 需要全国出差、使用笔记本电脑进行移动办公的开发者
- 希望形成人形机器人具身智能开发教材的教育工作者

## 功能特性

| 模块 | 功能 | 说明 |
|------|------|------|
| **学习路径规划** | 个性化学习路径生成 | 根据用户基础和目标定制学习计划 |
| **知识库管理** | 人形机器人知识整理 | 支持 BeyondMiMic、ISAAC Lab、VLA 等方向 |
| **代码收集与管理** | 代码片段自动收集 | 按语言、功能分类管理可复用代码 |
| **文章生成引擎** | Markdown 文章生成 | 自动生成学习笔记和技术文档 |
| **智能提醒系统** | 任务优先级调度 | 智能分类、时间规划、进度跟踪 |

## 系统架构

```
MacBook Air (前端)                    本地服务器 (后端)
├── Obsidian (笔记管理)              ├── CUDA 计算环境
├── Zotero (论文管理)                ├── ISAAC Lab 仿真
├── VS Code Remote (开发)            ├── 模型训练/推理
├── RLA Web UI (助学助手)            ├── 代码仓库
└── SSH 连接                         └── 数据存储
```

### 网络拓扑

```
MacBook Air ──SSH──> 本地服务器 (10.185.157.92)
     │
     └──> 内网访问 (可选 VPN)
```

## 快速开始

### 1. 克隆项目

```bash
git clone <仓库地址>
cd MimoCode
```

### 2. 服务器环境配置

```bash
chmod +x scripts/setup-server.sh
./scripts/setup-server.sh
```

### 3. MacBook 环境配置

```bash
chmod +x scripts/setup-macbook.sh
./scripts/setup-macbook.sh
```

### 4. 启动后端服务

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问 API 文档

启动服务后，访问以下地址：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 项目结构

```
MimoCode/
├── backend/                    # 后端服务 (FastAPI)
│   ├── app/
│   │   ├── models/            # 数据模型
│   │   ├── routes/            # API 路由
│   │   ├── services/          # 业务逻辑
│   │   └── config.py          # 配置文件
│   ├── main.py                # 入口文件
│   └── requirements.txt       # 依赖列表
├── frontend/                   # 前端资源
├── docs/                       # 项目文档
│   ├── environment-setup.md   # 环境配置指南
│   ├── obsidian-setup.md      # Obsidian 配置
│   ├── zotero-setup.md        # Zotero 配置
│   └── user-guide.md          # 用户指南
├── scripts/                    # 部署脚本
│   ├── setup-server.sh        # 服务器配置脚本
│   └── setup-macbook.sh       # MacBook 配置脚本
├── specs/                      # 设计文档
└── tests/                      # 测试代码
```

## API 接口

| 模块 | 端点 | 说明 |
|------|------|------|
| 学习路径 | `/api/v1/learning` | 学习路径规划与管理 |
| 知识库 | `/api/v1/knowledge` | 知识库内容管理 |
| 代码管理 | `/api/v1/code` | 代码片段收集与管理 |
| 文章生成 | `/api/v1/article` | 文章自动生成 |
| 待办任务 | `/api/v1/todo` | 智能待办管理 |

## 文档链接

- [环境配置指南](docs/environment-setup.md)
- [Obsidian 配置](docs/obsidian-setup.md)
- [Zotero 配置](docs/zotero-setup.md)
- [用户指南](docs/user-guide.md)

## 开发指南

### 技术栈

- **后端**: Python (FastAPI + SQLAlchemy + Alembic)
- **前端**: Vue.js
- **数据库**: SQLite (本地) + PostgreSQL (服务器)
- **AI**: 本地 LLM + API 调用

### 本地开发

```bash
# 后端
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# 运行测试
pytest tests/
```

### 代码规范

- 使用 Python 类型注解
- 遵循 PEP 8 编码规范
- 提交前运行 `pytest` 确保测试通过

## 部署方案

### 阶段 1: 基础环境搭建 (1-2 天)

1. 服务器环境配置
2. MacBook Air 环境配置
3. SSH 连接测试
4. 基础工具安装

### 阶段 2: 助学助手开发 (1-2 周)

1. 核心系统框架搭建
2. 知识库管理模块
3. 代码收集模块
4. 文章生成模块

### 阶段 3: 学习记录系统 (3-5 天)

1. Obsidian 配置
2. Zotero 配置
3. 集成插件安装
4. 知识库结构建立

## 许可证

本项目为内部研究使用，未经授权不得外传。

## 联系方式

如有问题，请通过以下方式联系：

- 提交 GitHub Issue
- 项目管理员: [联系方式]

---

*最后更新: 2026-07-01*
