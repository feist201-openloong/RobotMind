# RobotMind 项目索引

> MiMo Code 项目理解文件 - 让AI助手快速了解项目上下文

## 项目概述

**RobotMind** 是一个人形机器人助学助手系统，用于支持具身智能领域的学习和研究。

**核心方向**：BeyondMiMic、ISAAC Lab、VLA（Vision-Language-Action）

**用户画像**：具备ROS和深度学习基础，需要全国出差，使用MacBook开发+本地服务器计算

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端 | Python FastAPI | REST API服务 |
| 前端 | Vue 3 + Element Plus | Web界面 |
| 数据库 | SQLAlchemy + SQLite | 数据存储 |
| 连接 | Tailscale VPN | 远程访问 |
| 仿真 | Isaac Lab | 机器人仿真 |
| 笔记 | Obsidian + Zotero | 知识管理 |

## 项目结构

```
RobotMind/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── models/            # 数据模型 (SQLAlchemy)
│   │   │   ├── database.py    # 数据库连接
│   │   │   ├── learning.py    # 学习路径模型
│   │   │   ├── knowledge.py   # 知识库模型
│   │   │   ├── code.py        # 代码管理模型
│   │   │   ├── article.py     # 文章模型
│   │   │   └── todo.py        # 待办任务模型
│   │   ├── routes/            # API路由
│   │   │   ├── learning.py    # 学习路径API
│   │   │   ├── knowledge.py   # 知识库API
│   │   │   ├── code.py        # 代码管理API
│   │   │   ├── article.py     # 文章生成API
│   │   │   └── todo.py        # 待办任务API
│   │   ├── services/          # 业务逻辑层
│   │   │   ├── knowledge.py   # 知识库服务
│   │   │   ├── code.py        # 代码服务
│   │   │   ├── article.py     # 文章生成服务
│   │   │   └── todo.py        # 智能待办服务
│   │   └── schemas.py         # Pydantic验证模型
│   ├── main.py                # FastAPI入口
│   └── requirements.txt       # Python依赖
├── frontend/                   # Vue.js前端
│   ├── src/
│   │   ├── views/             # 页面组件
│   │   │   ├── HomeView.vue   # 首页
│   │   │   ├── LearningView.vue # 学习路径
│   │   │   ├── KnowledgeView.vue # 知识库
│   │   │   ├── CodeView.vue   # 代码管理
│   │   │   ├── ArticleView.vue # 文章生成
│   │   │   └── TodoView.vue   # 待办任务
│   │   ├── api/               # API服务
│   │   ├── router/            # 路由配置
│   │   └── stores/            # 状态管理
│   └── package.json           # Node依赖
├── docs/                       # 配置文档
│   ├── obsidian-setup.md      # Obsidian配置
│   ├── zotero-setup.md        # Zotero配置
│   ├── isaac-lab-setup.md     # Isaac Lab配置
│   ├── integration-guide.md   # 系统集成指南
│   └── user-guide.md          # 用户指南
├── scripts/                    # 环境配置脚本
│   ├── setup-server.sh        # 服务器配置
│   ├── setup-macbook.sh       # MacBook配置
│   └── setup-isaac-lab.sh     # Isaac Lab配置
├── specs/                      # 设计文档
├── plans/                      # 实施计划
└── tests/                      # 测试用例
```

## 核心API端点

### 学习路径
- `GET/POST /api/v1/learning/paths` - 学习路径CRUD
- `GET/POST /api/v1/learning/tasks` - 学习任务CRUD

### 知识库
- `GET/POST /api/v1/knowledge/categories` - 分类管理
- `GET/POST /api/v1/knowledge/entries` - 知识条目

### 代码管理
- `GET/POST /api/v1/code/snippets` - 代码片段

### 文章生成
- `POST /api/v1/articles/generate/from-knowledge` - 从知识生成
- `POST /api/v1/articles/generate/from-code` - 从代码生成

### 待办任务
- `GET/POST /api/v1/todo/tasks` - 任务管理
- `GET /api/v1/todo/schedule` - 智能规划

## 开发命令

### 启动后端
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 启动前端
```bash
cd frontend
npm install
npm run dev
```

### 运行测试
```bash
cd backend
pytest tests/ -v
```

## 远程服务器连接

**Tailscale IP**：100.126.98.106

```bash
# SSH连接
ssh dell@100.126.98.106

# VS Code Remote-SSH
Remote-SSH: Connect to Host → dell@100.126.98.106
```

## 当前状态

- [x] 基础环境配置
- [x] 后端核心框架
- [x] 知识库管理模块
- [x] 代码管理模块
- [x] 文章生成引擎
- [x] 智能待办系统
- [x] 前端界面框架
- [ ] API实际集成（当前为模拟数据）
- [ ] 用户认证系统
- [ ] 数据同步功能

## 注意事项

1. 前端当前使用硬编码数据，需要集成后端API
2. 服务器CUDA环境需在服务器上配置
3. Obsidian和Zotero需在MacBook上手动配置
4. 所有代码变更需通过Git同步
