# 系统集成与测试文档

## 概述

本文档提供系统的集成指南和测试用例，用于确保所有组件正确集成和正常运行。

## 组件清单

### 1. 基础环境配置 (Task 1)
- Python 3.10+ 环境
- Node.js 18+ 环境
- 数据库系统 (SQLite/PostgreSQL)
- Git 版本控制

### 2. 助学助手核心系统 (Task 2)
- 后端API服务
- 用户认证模块
- 数据存储层

### 3. 知识库管理模块 (Task 3)
- 知识条目CRUD操作
- 分类管理
- 搜索功能

### 4. 代码收集与管理模块 (Task 4)
- 代码片段存储
- 代码分类
- 代码搜索

### 5. 文章生成引擎 (Task 5)
- Markdown生成
- 模板系统
- 内容组织

### 6. 智能待办系统 (Task 6)
- 任务管理
- 优先级设置
- 提醒功能

### 7. 前端界面 (Task 7)
- React/Vue应用
- 响应式设计
- 用户交互

### 8. Obsidian配置 (Task 8)
- Obsidian笔记集成
- 插件配置
- 同步设置

### 9. Zotero配置 (Task 9)
- 文献管理集成
- 引用格式
- 同步配置

### 10. Isaac Lab环境 (Task 10)
- Isaac Lab安装
- 仿真环境配置
- 机器人模型

## 集成步骤

### 步骤1: 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd MimoCode

# 创建Python虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装后端依赖
cd backend
pip install -r requirements.txt

# 安装前端依赖
cd ../frontend
npm install
```

### 步骤2: 数据库初始化

```bash
# 初始化数据库
cd backend
python -c "from database import init_db; init_db()"
```

### 步骤3: 配置文件设置

```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件
nano .env
```

### 步骤4: 启动服务

```bash
# 启动后端服务
cd backend
python app.py

# 启动前端服务 (新终端)
cd frontend
npm start
```

## 功能测试

### 知识库管理测试

```python
import requests

BASE_URL = "http://localhost:5000/api"

def test_knowledge_management():
    # 创建知识条目
    data = {
        "title": "Python基础",
        "content": "Python是一种解释型语言...",
        "category": "编程语言"
    }
    response = requests.post(f"{BASE_URL}/knowledge", json=data)
    assert response.status_code == 201
    
    # 获取知识条目
    response = requests.get(f"{BASE_URL}/knowledge")
    assert response.status_code == 200
    
    # 搜索知识条目
    response = requests.get(f"{BASE_URL}/knowledge/search?q=Python")
    assert response.status_code == 200
```

### 代码管理测试

```python
def test_code_management():
    # 创建代码片段
    data = {
        "title": "快速排序",
        "code": "def quicksort(arr):...",
        "language": "python",
        "category": "算法"
    }
    response = requests.post(f"{BASE_URL}/code", json=data)
    assert response.status_code == 201
    
    # 获取代码片段
    response = requests.get(f"{BASE_URL}/code")
    assert response.status_code == 200
```

### 待办任务测试

```python
def test_todo_management():
    # 创建待办任务
    data = {
        "title": "完成项目文档",
        "description": "编写系统集成文档",
        "priority": "high",
        "due_date": "2026-07-15"
    }
    response = requests.post(f"{BASE_URL}/todos", json=data)
    assert response.status_code == 201
    
    # 获取待办任务
    response = requests.get(f"{BASE_URL}/todos")
    assert response.status_code == 200
    
    # 更新任务状态
    response = requests.patch(f"{BASE_URL}/todos/1", json={"completed": True})
    assert response.status_code == 200
```

## 部署检查清单

### 服务器环境配置
- [ ] 操作系统更新完成
- [ ] 必要软件安装完成
- [ ] 防火墙配置正确
- [ ] 用户权限设置完成

### MacBook环境配置
- [ ] Homebrew安装完成
- [ ] Python环境配置完成
- [ ] Node.js环境配置完成
- [ ] 依赖包安装完成

### SSH连接测试
- [ ] SSH密钥生成
- [ ] SSH配置文件设置
- [ ] 连接测试通过
- [ ] 权限验证通过

### 后端服务启动
- [ ] 虚拟环境激活
- [ ] 依赖安装完成
- [ ] 数据库初始化完成
- [ ] 服务启动成功

### 前端服务启动
- [ ] 依赖安装完成
- [ ] 环境变量配置
- [ ] 构建成功
- [ ] 服务启动成功

### 数据库初始化
- [ ] 数据库创建完成
- [ ] 表结构创建完成
- [ ] 初始数据导入完成
- [ ] 索引创建完成

### API接口测试
- [ ] 健康检查接口测试通过
- [ ] 知识库API测试通过
- [ ] 代码管理API测试通过
- [ ] 待办任务API测试通过

### Obsidian配置
- [ ] Obsidian安装完成
- [ ] 插件安装配置
- [ ] 同步设置完成
- [ ] 模板配置完成

### Zotero配置
- [ ] Zotero安装完成
- [ ] 浏览器插件安装
- [ ] 同步设置完成
- [ ] 引用格式配置

### Isaac Lab安装
- [ ] Isaac Lab下载完成
- [ ] 依赖安装完成
- [ ] 环境配置完成
- [ ] 测试运行成功

## 故障排除

### 常见问题及解决方案

#### 1. 数据库连接失败
```bash
# 检查数据库服务状态
sudo systemctl status postgresql

# 重启数据库服务
sudo systemctl restart postgresql

# 检查数据库配置
cat backend/.env
```

#### 2. 端口冲突
```bash
# 查看端口占用
lsof -i :5000

# 杀死占用进程
kill -9 <PID>
```

#### 3. 依赖安装失败
```bash
# 清除缓存
pip cache purge
npm cache clean --force

# 重新安装依赖
pip install -r requirements.txt
npm install
```

#### 4. 前端构建失败
```bash
# 清除node_modules
rm -rf node_modules
npm install

# 检查Node.js版本
node --version
```

### 日志查看

```bash
# 后端日志
tail -f backend/logs/app.log

# 前端日志
tail -f frontend/logs/app.log

# 系统日志
tail -f /var/log/syslog
```

## 性能监控

### 监控指标

1. **系统指标**
   - CPU使用率
   - 内存使用率
   - 磁盘I/O
   - 网络流量

2. **应用指标**
   - 请求响应时间
   - 错误率
   - 并发用户数
   - 数据库查询时间

3. **业务指标**
   - 知识条目数量
   - 代码片段数量
   - 待办任务完成率
   - 文章生成数量

### 监控工具

```bash
# 系统监控
htop

# 网络监控
iftop

# 数据库监控
pg_stat_activity

# 应用性能监控
# 集成Prometheus + Grafana
```

### 告警设置

1. **CPU使用率 > 80%**
2. **内存使用率 > 85%**
3. **磁盘使用率 > 90%**
4. **API响应时间 > 2秒**
5. **错误率 > 1%**

## 集成测试脚本

### 自动化测试

```bash
#!/bin/bash
# integration_test.sh

echo "开始集成测试..."

# 1. 检查服务状态
echo "检查后端服务..."
curl -f http://localhost:5000/health || exit 1

echo "检查前端服务..."
curl -f http://localhost:3000 || exit 1

# 2. 运行单元测试
echo "运行后端测试..."
cd backend
python -m pytest tests/ -v

echo "运行前端测试..."
cd ../frontend
npm test

# 3. 运行集成测试
echo "运行集成测试..."
cd ../tests
python test_api.py

echo "集成测试完成！"
```

### 性能测试

```bash
# 使用Apache Bench进行性能测试
ab -n 1000 -c 10 http://localhost:5000/api/health

# 使用wrk进行压力测试
wrk -t12 -c400 -d30s http://localhost:5000/api/health
```

## 文档维护

### 版本控制
- 所有文档变更必须通过Git进行版本控制
- 每次重大变更必须更新版本号
- 保持文档与代码同步

### 定期审查
- 每月审查文档准确性
- 更新过时的信息
- 添加新的故障排除经验

### 反馈机制
- 收集用户反馈
- 记录常见问题
- 持续改进文档质量