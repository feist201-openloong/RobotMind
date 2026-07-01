# 人形机器人助学助手系统实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use compose:subagent (recommended) or compose:execute to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一套完整的助学助手系统，用于支持人形机器人领域的学习和研究，包括BeyondMiMic、ISAAC Lab、VLA等方向。

**Architecture:** 采用分布式微服务架构，MacBook Air作为前端开发环境，本地服务器作为计算后端。通过SSH实现远程开发，使用Obsidian+Zotero进行学习记录，智能待办系统管理学习任务。

**Tech Stack:** Python (FastAPI), Vue.js, SQLite, PostgreSQL, Docker, NVIDIA CUDA, Isaac Lab, Obsidian, Zotero

## Global Constraints

- 系统必须支持离线模式，数据本地缓存
- SSH延迟必须<100ms
- 任务响应时间必须<1s
- 文章生成时间必须<30s
- 必须支持Markdown格式输出
- 必须支持中文界面

---

## Task 1: 基础环境搭建

**Covers:** [S4, S7]

**Files:**
- Create: `/home/dell/文档/MimoCode/scripts/setup-server.sh`
- Create: `/home/dell/文档/MimoCode/scripts/setup-macbook.sh`
- Create: `/home/dell/文档/MimoCode/docs/environment-setup.md`

**Interfaces:**
- Consumes: 无
- Produces: 服务器环境配置脚本、MacBook配置脚本、环境配置文档

- [ ] **Step 1: 创建服务器环境配置脚本**

```bash
#!/bin/bash
# setup-server.sh - 服务器环境配置脚本

set -e

echo "=== 开始配置服务器环境 ==="

# 1. 更新系统
echo "1. 更新系统包..."
sudo apt update && sudo apt upgrade -y

# 2. 安装基础工具
echo "2. 安装基础工具..."
sudo apt install -y curl wget git vim htop net-tools

# 3. 安装NVIDIA驱动
echo "3. 安装NVIDIA驱动..."
sudo apt install -y nvidia-driver-535

# 4. 安装CUDA
echo "4. 安装CUDA..."
wget -q https://developer.download.nvidia.com/compute/cuda/12.2.0/local_installers/cuda_12.2.0_535.54.03_linux.run
sudo sh cuda_12.2.0_535.54.03_linux.run --silent --toolkit --samples

# 5. 配置环境变量
echo "5. 配置环境变量..."
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# 6. 安装Docker
echo "6. 安装Docker..."
sudo apt install -y docker.io
sudo usermod -aG docker $USER

# 7. 安装NVIDIA Container Toolkit
echo "7. 安装NVIDIA Container Toolkit..."
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# 8. 安装Python环境
echo "8. 安装Python环境..."
sudo apt install -y python3 python3-pip python3-venv

# 9. 安装Jupyter Lab
echo "9. 安装Jupyter Lab..."
pip3 install jupyterlab

# 10. 安装Git LFS
echo "10. 安装Git LFS..."
sudo apt install -y git-lfs
git lfs install

# 11. 创建项目目录
echo "11. 创建项目目录..."
mkdir -p /home/dell/projects/robotics-learning-assistant
mkdir -p /home/dell/projects/robotics-learning-assistant/{backend,frontend,data,logs}

echo "=== 服务器环境配置完成 ==="
echo "请重启系统以使所有更改生效"
```

- [ ] **Step 2: 创建MacBook环境配置脚本**

```bash
#!/bin/bash
# setup-macbook.sh - MacBook环境配置脚本

set -e

echo "=== 开始配置MacBook环境 ==="

# 1. 安装Homebrew
echo "1. 安装Homebrew..."
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. 安装开发工具
echo "2. 安装开发工具..."
brew install --cask visual-studio-code
brew install --cask obsidian
brew install --cask zotero

# 3. 安装SSH工具
echo "3. 安装SSH工具..."
brew install openssh

# 4. 配置SSH密钥
echo "4. 配置SSH密钥..."
if [ ! -f ~/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
fi

# 5. 安装VS Code插件
echo "5. 安装VS Code插件..."
code --install-extension ms-vscode-remote.remote-ssh
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension formulahendry.auto-rename-tag
code --install-extension formulahendry.auto-close-tag

# 6. 安装Node.js (用于前端开发)
echo "6. 安装Node.js..."
brew install node

# 7. 安装Python (用于本地开发)
echo "7. 安装Python..."
brew install python

# 8. 配置Git
echo "8. 配置Git..."
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

echo "=== MacBook环境配置完成 ==="
echo "请将~/.ssh/id_rsa.pub的内容添加到服务器的~/.ssh/authorized_keys"
```

- [ ] **Step 3: 创建环境配置文档**

```markdown
# 环境配置文档

## 服务器环境

### 系统要求
- Ubuntu 22.04 LTS
- NVIDIA GPU (支持CUDA)
- 至少16GB RAM
- 至少100GB SSD

### 安装步骤
1. 运行 `bash scripts/setup-server.sh`
2. 重启系统
3. 验证NVIDIA驱动: `nvidia-smi`
4. 验证CUDA: `nvcc --version`

### 服务配置
- SSH服务: 端口22
- Jupyter Lab: 端口8888
- 后端API: 端口8000

## MacBook环境

### 系统要求
- macOS 12.0+
- 至少8GB RAM
- 至少50GB可用空间

### 安装步骤
1. 运行 `bash scripts/setup-macbook.sh`
2. 配置SSH连接
3. 测试远程连接

### 开发工具
- VS Code + Remote-SSH
- Obsidian
- Zotero
- Git

## 远程连接配置

### SSH配置
```bash
# 添加SSH配置
cat >> ~/.ssh/config << EOF
Host robotics-server
    HostName 10.185.157.92
    User dell
    Port 22
    IdentityFile ~/.ssh/id_rsa
EOF

# 测试连接
ssh robotics-server
```

### VS Code Remote配置
1. 打开VS Code
2. 按Ctrl+Shift+P
3. 输入 "Remote-SSH: Connect to Host"
4. 选择 "robotics-server"
```

- [ ] **Step 4: 运行测试验证**

```bash
# 在服务器上运行
chmod +x scripts/setup-server.sh
bash scripts/setup-server.sh

# 验证NVIDIA驱动
nvidia-smi

# 验证CUDA
nvcc --version

# 验证Docker
docker --version
nvidia-docker --version
```

- [ ] **Step 5: 提交代码**

```bash
git add scripts/setup-server.sh scripts/setup-macbook.sh docs/environment-setup.md
git commit -m "feat: 添加基础环境配置脚本和文档"
```

---

## Task 2: 助学助手核心系统框架搭建

**Covers:** [S3, S5]

**Files:**
- Create: `/home/dell/文档/MimoCode/backend/main.py`
- Create: `/home/dell/文档/MimoCode/backend/requirements.txt`
- Create: `/home/dell/文档/MimoCode/backend/app/__init__.py`
- Create: `/home/dell/文档/MimoCode/backend/app/models.py`
- Create: `/home/dell/文档/MimoCode/backend/app/routes.py`
- Create: `/home/dell/文档/MimoCode/backend/app/services.py`

**Interfaces:**
- Consumes: Task 1 产生的服务器环境
- Produces: FastAPI后端框架、基础API接口

- [ ] **Step 1: 创建后端项目结构**

```bash
# 创建项目结构
mkdir -p /home/dell/文档/MimoCode/backend/app/{models,routes,services,utils}
touch /home/dell/文档/MimoCode/backend/app/__init__.py
touch /home/dell/文档/MimoCode/backend/app/models/__init__.py
touch /home/dell/文档/MimoCode/backend/app/routes/__init__.py
touch /home/dell/文档/MimoCode/backend/app/services/__init__.py
touch /home/dell/文档/MimoCode/backend/app/utils/__init__.py
```

- [ ] **Step 2: 创建依赖文件**

```txt
# requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
alembic==1.13.0
pydantic==2.5.2
python-dotenv==1.0.0
httpx==0.25.2
gitpython==3.1.40
markdown==3.5.1
jinja2==3.1.2
```

- [ ] **Step 3: 创建数据模型**

```python
# backend/app/models/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./robotics_learning.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
# backend/app/models/learning.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class LearningPath(Base):
    __tablename__ = "learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    target_field = Column(String(50))  # BeyondMiMic, ISAAC Lab, VLA
    difficulty_level = Column(Integer, default=1)  # 1-5
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tasks = relationship("LearningTask", back_populates="learning_path")

class LearningTask(Base):
    __tablename__ = "learning_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    task_type = Column(String(50))  # theory, practice, project
    priority = Column(Integer, default=1)  # 1-5
    status = Column(String(20), default="pending")  # pending, in_progress, completed
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"))
    learning_path = relationship("LearningPath", back_populates="tasks")

class CodeSnippet(Base):
    __tablename__ = "code_snippets"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String(50))
    description = Column(Text)
    tags = Column(String(500))  # 逗号分隔的标签
    source_file = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    markdown_content = Column(Text)
    status = Column(String(20), default="draft")  # draft, published
    tags = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

- [ ] **Step 4: 创建API路由**

```python
# backend/app/routes/learning.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..models.database import get_db
from ..models.learning import LearningPath, LearningTask
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/learning", tags=["learning"])

class LearningPathCreate(BaseModel):
    name: str
    description: str = None
    target_field: str = None
    difficulty_level: int = 1

class LearningPathResponse(BaseModel):
    id: int
    name: str
    description: str
    target_field: str
    difficulty_level: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class LearningTaskCreate(BaseModel):
    title: str
    description: str = None
    task_type: str = "theory"
    priority: int = 1
    due_date: datetime = None
    learning_path_id: int = None

class LearningTaskResponse(BaseModel):
    id: int
    title: str
    description: str
    task_type: str
    priority: int
    status: str
    due_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/paths/", response_model=LearningPathResponse)
def create_learning_path(path: LearningPathCreate, db: Session = Depends(get_db)):
    db_path = LearningPath(**path.model_dump())
    db.add(db_path)
    db.commit()
    db.refresh(db_path)
    return db_path

@router.get("/paths/", response_model=List[LearningPathResponse])
def read_learning_paths(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    paths = db.query(LearningPath).offset(skip).limit(limit).all()
    return paths

@router.get("/paths/{path_id}", response_model=LearningPathResponse)
def read_learning_path(path_id: int, db: Session = Depends(get_db)):
    path = db.query(LearningPath).filter(LearningPath.id == path_id).first()
    if path is None:
        raise HTTPException(status_code=404, detail="Learning path not found")
    return path

@router.post("/tasks/", response_model=LearningTaskResponse)
def create_learning_task(task: LearningTaskCreate, db: Session = Depends(get_db)):
    db_task = LearningTask(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks/", response_model=List[LearningTaskResponse])
def read_learning_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = db.query(LearningTask).offset(skip).limit(limit).all()
    return tasks

@router.put("/tasks/{task_id}/status")
def update_task_status(task_id: int, status: str, db: Session = Depends(get_db)):
    task = db.query(LearningTask).filter(LearningTask.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = status
    db.commit()
    return {"message": "Task status updated"}
```

- [ ] **Step 5: 创建主应用文件**

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import learning
from app.models.database import engine, Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Robotics Learning Assistant",
    description="人形机器人助学助手系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(learning.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Robotics Learning Assistant"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

- [ ] **Step 6: 运行测试验证**

```bash
# 安装依赖
cd /home/dell/文档/MimoCode/backend
pip3 install -r requirements.txt

# 运行服务器
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 测试API
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/docs  # 查看API文档
```

- [ ] **Step 7: 提交代码**

```bash
git add backend/
git commit -m "feat: 添加助学助手核心系统框架"
```

---

## Task 3: 知识库管理模块

**Covers:** [S3, S5]

**Files:**
- Create: `/home/dell/文档/MimoCode/backend/app/services/knowledge.py`
- Create: `/home/dell/文档/MimoCode/backend/app/routes/knowledge.py`
- Create: `/home/dell/文档/MimoCode/backend/app/models/knowledge.py`

**Interfaces:**
- Consumes: Task 2 产生的后端框架
- Produces: 知识库管理API、知识分类系统

- [ ] **Step 1: 创建知识库数据模型**

```python
# backend/app/models/knowledge.py
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from .database import Base

class KnowledgeCategory(Base):
    __tablename__ = "knowledge_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, nullable=True)  # 支持层级分类
    icon = Column(String(50))  # 图标名称
    created_at = Column(DateTime, default=datetime.utcnow)
    
class KnowledgeEntry(Base):
    __tablename__ = "knowledge_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    entry_type = Column(String(50))  # concept, tutorial, example, reference
    category_id = Column(Integer, nullable=True)
    tags = Column(String(500))  # 逗号分隔的标签
    source_url = Column(String(500))
    difficulty_level = Column(Integer, default=1)  # 1-5
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 额外元数据 (JSON格式)
    metadata = Column(JSON, default={})
```

- [ ] **Step 2: 创建知识库服务**

```python
# backend/app/services/knowledge.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.knowledge import KnowledgeCategory, KnowledgeEntry

class KnowledgeService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_category(self, name: str, description: str = None, parent_id: int = None) -> KnowledgeCategory:
        category = KnowledgeCategory(
            name=name,
            description=description,
            parent_id=parent_id
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def get_categories(self, parent_id: int = None) -> List[KnowledgeCategory]:
        query = self.db.query(KnowledgeCategory)
        if parent_id is not None:
            query = query.filter(KnowledgeCategory.parent_id == parent_id)
        return query.all()
    
    def create_entry(self, title: str, content: str, entry_type: str = "concept", 
                    category_id: int = None, tags: str = None) -> KnowledgeEntry:
        entry = KnowledgeEntry(
            title=title,
            content=content,
            entry_type=entry_type,
            category_id=category_id,
            tags=tags
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry
    
    def search_entries(self, query: str, category_id: int = None) -> List[KnowledgeEntry]:
        db_query = self.db.query(KnowledgeEntry)
        if query:
            db_query = db_query.filter(
                (KnowledgeEntry.title.ilike(f"%{query}%")) |
                (KnowledgeEntry.content.ilike(f"%{query}%")) |
                (KnowledgeEntry.tags.ilike(f"%{query}%"))
            )
        if category_id is not None:
            db_query = db_query.filter(KnowledgeEntry.category_id == category_id)
        return db_query.all()
    
    def get_entry(self, entry_id: int) -> Optional[KnowledgeEntry]:
        return self.db.query(KnowledgeEntry).filter(KnowledgeEntry.id == entry_id).first()
    
    def update_entry(self, entry_id: int, **kwargs) -> Optional[KnowledgeEntry]:
        entry = self.get_entry(entry_id)
        if entry:
            for key, value in kwargs.items():
                setattr(entry, key, value)
            self.db.commit()
            self.db.refresh(entry)
        return entry
```

- [ ] **Step 3: 创建知识库API路由**

```python
# backend/app/routes/knowledge.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.database import get_db
from ..models.knowledge import KnowledgeCategory, KnowledgeEntry
from ..services.knowledge import KnowledgeService
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

class CategoryCreate(BaseModel):
    name: str
    description: str = None
    parent_id: int = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str
    parent_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class EntryCreate(BaseModel):
    title: str
    content: str
    entry_type: str = "concept"
    category_id: int = None
    tags: str = None

class EntryResponse(BaseModel):
    id: int
    title: str
    content: str
    entry_type: str
    category_id: int
    tags: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/categories/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    service = KnowledgeService(db)
    return service.create_category(**category.model_dump())

@router.get("/categories/", response_model=List[CategoryResponse])
def read_categories(parent_id: int = None, db: Session = Depends(get_db)):
    service = KnowledgeService(db)
    return service.get_categories(parent_id)

@router.post("/entries/", response_model=EntryResponse)
def create_entry(entry: EntryCreate, db: Session = Depends(get_db)):
    service = KnowledgeService(db)
    return service.create_entry(**entry.model_dump())

@router.get("/entries/", response_model=List[EntryResponse])
def search_entries(
    query: str = Query(None, min_length=1),
    category_id: int = None,
    db: Session = Depends(get_db)
):
    service = KnowledgeService(db)
    return service.search_entries(query, category_id)

@router.get("/entries/{entry_id}", response_model=EntryResponse)
def read_entry(entry_id: int, db: Session = Depends(get_db)):
    service = KnowledgeService(db)
    entry = service.get_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@router.put("/entries/{entry_id}", response_model=EntryResponse)
def update_entry(entry_id: int, entry: EntryCreate, db: Session = Depends(get_db)):
    service = KnowledgeService(db)
    updated = service.update_entry(entry_id, **entry.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Entry not found")
    return updated
```

- [ ] **Step 4: 运行测试验证**

```bash
# 运行服务器
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 测试API
# 创建分类
curl -X POST http://localhost:8000/api/knowledge/categories/ \
  -H "Content-Type: application/json" \
  -d '{"name": "BeyondMiMic", "description": "人形机器人仿真平台"}'

# 创建知识条目
curl -X POST http://localhost:8000/api/knowledge/entries/ \
  -H "Content-Type: application/json" \
  -d '{"title": "BeyondMiMic基础概念", "content": "BeyondMiMic是一个人形机器人仿真平台...", "entry_type": "concept", "category_id": 1}'

# 搜索知识
curl "http://localhost:8000/api/knowledge/entries/?query=仿真"
```

- [ ] **Step 5: 提交代码**

```bash
git add backend/app/services/knowledge.py backend/app/routes/knowledge.py backend/app/models/knowledge.py
git commit -m "feat: 添加知识库管理模块"
```

---

## Task 4: 代码收集与管理模块

**Covers:** [S3, S5]

**Files:**
- Create: `/home/dell/文档/MimoCode/backend/app/services/code.py`
- Create: `/home/dell/文档/MimoCode/backend/app/routes/code.py`
- Create: `/home/dell/文档/MimoCode/backend/app/models/code.py`

**Interfaces:**
- Consumes: Task 2 产生的后端框架
- Produces: 代码片段管理API、代码搜索功能

- [ ] **Step 1: 创建代码片段数据模型**

```python
# backend/app/models/code.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class CodeSnippet(Base):
    __tablename__ = "code_snippets"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String(50))  # python, cpp, yaml, etc.
    description = Column(Text)
    tags = Column(String(500))  # 逗号分隔的标签
    source_file = Column(String(500))  # 源文件路径
    project_name = Column(String(100))  # 项目名称
    difficulty_level = Column(Integer, default=1)  # 1-5
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

- [ ] **Step 2: 创建代码管理服务**

```python
# backend/app/services/code.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.code import CodeSnippet

class CodeService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_snippet(self, title: str, code: str, language: str = None, 
                      description: str = None, tags: str = None, 
                      source_file: str = None, project_name: str = None) -> CodeSnippet:
        snippet = CodeSnippet(
            title=title,
            code=code,
            language=language,
            description=description,
            tags=tags,
            source_file=source_file,
            project_name=project_name
        )
        self.db.add(snippet)
        self.db.commit()
        self.db.refresh(snippet)
        return snippet
    
    def search_snippets(self, query: str = None, language: str = None, 
                       project_name: str = None) -> List[CodeSnippet]:
        db_query = self.db.query(CodeSnippet)
        
        if query:
            db_query = db_query.filter(
                (CodeSnippet.title.ilike(f"%{query}%")) |
                (CodeSnippet.code.ilike(f"%{query}%")) |
                (CodeSnippet.description.ilike(f"%{query}%")) |
                (CodeSnippet.tags.ilike(f"%{query}%"))
            )
        
        if language:
            db_query = db_query.filter(CodeSnippet.language == language)
        
        if project_name:
            db_query = db_query.filter(CodeSnippet.project_name == project_name)
        
        return db_query.all()
    
    def get_snippet(self, snippet_id: int) -> Optional[CodeSnippet]:
        return self.db.query(CodeSnippet).filter(CodeSnippet.id == snippet_id).first()
    
    def update_snippet(self, snippet_id: int, **kwargs) -> Optional[CodeSnippet]:
        snippet = self.get_snippet(snippet_id)
        if snippet:
            for key, value in kwargs.items():
                setattr(snippet, key, value)
            self.db.commit()
            self.db.refresh(snippet)
        return snippet
    
    def delete_snippet(self, snippet_id: int) -> bool:
        snippet = self.get_snippet(snippet_id)
        if snippet:
            self.db.delete(snippet)
            self.db.commit()
            return True
        return False
```

- [ ] **Step 3: 创建代码管理API路由**

```python
# backend/app/routes/code.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.database import get_db
from ..models.code import CodeSnippet
from ..services.code import CodeService
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/code", tags=["code"])

class SnippetCreate(BaseModel):
    title: str
    code: str
    language: str = None
    description: str = None
    tags: str = None
    source_file: str = None
    project_name: str = None

class SnippetResponse(BaseModel):
    id: int
    title: str
    code: str
    language: str
    description: str
    tags: str
    source_file: str
    project_name: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/snippets/", response_model=SnippetResponse)
def create_snippet(snippet: SnippetCreate, db: Session = Depends(get_db)):
    service = CodeService(db)
    return service.create_snippet(**snippet.model_dump())

@router.get("/snippets/", response_model=List[SnippetResponse])
def search_snippets(
    query: str = Query(None, min_length=1),
    language: str = None,
    project_name: str = None,
    db: Session = Depends(get_db)
):
    service = CodeService(db)
    return service.search_snippets(query, language, project_name)

@router.get("/snippets/{snippet_id}", response_model=SnippetResponse)
def read_snippet(snippet_id: int, db: Session = Depends(get_db)):
    service = CodeService(db)
    snippet = service.get_snippet(snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return snippet

@router.put("/snippets/{snippet_id}", response_model=SnippetResponse)
def update_snippet(snippet_id: int, snippet: SnippetCreate, db: Session = Depends(get_db)):
    service = CodeService(db)
    updated = service.update_snippet(snippet_id, **snippet.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return updated

@router.delete("/snippets/{snippet_id}")
def delete_snippet(snippet_id: int, db: Session = Depends(get_db)):
    service = CodeService(db)
    if not service.delete_snippet(snippet_id):
        raise HTTPException(status_code=404, detail="Snippet not found")
    return {"message": "Snippet deleted"}
```

- [ ] **Step 4: 运行测试验证**

```bash
# 运行服务器
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 测试API
# 创建代码片段
curl -X POST http://localhost:8000/api/code/snippets/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Isaac Lab基础配置", "code": "import omni.isaac.lab as il", "language": "python", "description": "Isaac Lab基础配置代码", "tags": "isaac,lab,配置", "project_name": "robotics-learning"}'

# 搜索代码
curl "http://localhost:8000/api/code/snippets/?query=isaac"
```

- [ ] **Step 5: 提交代码**

```bash
git add backend/app/services/code.py backend/app/routes/code.py backend/app/models/code.py
git commit -m "feat: 添加代码收集与管理模块"
```

---

## Task 5: 文章生成引擎

**Covers:** [S3, S5]

**Files:**
- Create: `/home/dell/文档/MimoCode/backend/app/services/article.py`
- Create: `/home/dell/文档/MimoCode/backend/app/routes/article.py`
- Create: `/home/dell/文档/MimoCode/backend/app/models/article.py`
- Create: `/home/dell/文档/MimoCode/backend/templates/article_template.md`

**Interfaces:**
- Consumes: Task 2 产生的后端框架, Task 3 知识库, Task 4 代码库
- Produces: 文章生成API、Markdown输出

- [ ] **Step 1: 创建文章数据模型**

```python
# backend/app/models/article.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    markdown_content = Column(Text)
    summary = Column(Text)
    tags = Column(String(500))
    status = Column(String(20), default="draft")  # draft, published
    word_count = Column(Integer, default=0)
    reading_time = Column(Integer, default=0)  # 分钟
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

- [ ] **Step 2: 创建文章生成服务**

```python
# backend/app/services/article.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.article import Article
from ..models.knowledge import KnowledgeEntry
from ..models.code import CodeSnippet
import markdown
from datetime import datetime

class ArticleService:
    def __init__(self, db: Session):
        self.db = db
    
    def generate_article_from_knowledge(self, knowledge_ids: List[int], 
                                       title: str = None) -> Article:
        """从知识条目生成文章"""
        # 获取知识条目
        knowledge_entries = self.db.query(KnowledgeEntry).filter(
            KnowledgeEntry.id.in_(knowledge_ids)
        ).all()
        
        if not knowledge_entries:
            raise ValueError("No knowledge entries found")
        
        # 生成文章内容
        content_parts = []
        for entry in knowledge_entries:
            content_parts.append(f"## {entry.title}\n\n{entry.content}\n")
        
        content = "\n".join(content_parts)
        
        # 生成标题
        if not title:
            title = f"学习笔记: {knowledge_entries[0].title}"
        
        # 创建文章
        article = Article(
            title=title,
            content=content,
            markdown_content=self._convert_to_markdown(content),
            tags=knowledge_entries[0].tags if knowledge_entries else None,
            word_count=len(content.split()),
            reading_time=max(1, len(content.split()) // 200)  # 假设每分钟200字
        )
        
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        return article
    
    def generate_article_from_code(self, code_ids: List[int], 
                                  title: str = None) -> Article:
        """从代码片段生成文章"""
        code_snippets = self.db.query(CodeSnippet).filter(
            CodeSnippet.id.in_(code_ids)
        ).all()
        
        if not code_snippets:
            raise ValueError("No code snippets found")
        
        # 生成文章内容
        content_parts = []
        for snippet in code_snippets:
            content_parts.append(f"## {snippet.title}\n\n```{snippet.language}\n{snippet.code}\n```\n")
            if snippet.description:
                content_parts.append(f"{snippet.description}\n")
        
        content = "\n".join(content_parts)
        
        # 生成标题
        if not title:
            title = f"代码示例: {code_snippets[0].title}"
        
        # 创建文章
        article = Article(
            title=title,
            content=content,
            markdown_content=self._convert_to_markdown(content),
            tags=code_snippets[0].tags if code_snippets else None,
            word_count=len(content.split()),
            reading_time=max(1, len(content.split()) // 200)
        )
        
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        return article
    
    def _convert_to_markdown(self, content: str) -> str:
        """将内容转换为Markdown格式"""
        # 简单的Markdown转换
        return content
    
    def get_article(self, article_id: int) -> Optional[Article]:
        return self.db.query(Article).filter(Article.id == article_id).first()
    
    def list_articles(self, status: str = None, limit: int = 100) -> List[Article]:
        query = self.db.query(Article)
        if status:
            query = query.filter(Article.status == status)
        return query.limit(limit).all()
    
    def update_article_status(self, article_id: int, status: str) -> bool:
        article = self.get_article(article_id)
        if article:
            article.status = status
            self.db.commit()
            return True
        return False
    
    def export_article_markdown(self, article_id: int) -> Optional[str]:
        """导出文章为Markdown文件"""
        article = self.get_article(article_id)
        if article:
            return article.markdown_content
        return None
```

- [ ] **Step 3: 创建文章API路由**

```python
# backend/app/routes/article.py
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.database import get_db
from ..models.article import Article
from ..services.article import ArticleService
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/articles", tags=["articles"])

class ArticleGenerateFromKnowledge(BaseModel):
    knowledge_ids: List[int]
    title: str = None

class ArticleGenerateFromCode(BaseModel):
    code_ids: List[int]
    title: str = None

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    summary: str
    tags: str
    status: str
    word_count: int
    reading_time: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/generate/from-knowledge", response_model=ArticleResponse)
def generate_from_knowledge(request: ArticleGenerateFromKnowledge, db: Session = Depends(get_db)):
    service = ArticleService(db)
    try:
        return service.generate_article_from_knowledge(request.knowledge_ids, request.title)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/generate/from-code", response_model=ArticleResponse)
def generate_from_code(request: ArticleGenerateFromCode, db: Session = Depends(get_db)):
    service = ArticleService(db)
    try:
        return service.generate_article_from_code(request.code_ids, request.title)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ArticleResponse])
def list_articles(
    status: str = Query(None, regex="^(draft|published)$"),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = ArticleService(db)
    return service.list_articles(status, limit)

@router.get("/{article_id}", response_model=ArticleResponse)
def read_article(article_id: int, db: Session = Depends(get_db)):
    service = ArticleService(db)
    article = service.get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.put("/{article_id}/status")
def update_status(article_id: int, status: str = Query(..., regex="^(draft|published)$"), db: Session = Depends(get_db)):
    service = ArticleService(db)
    if not service.update_article_status(article_id, status):
        raise HTTPException(status_code=404, detail="Article not found")
    return {"message": "Status updated"}

@router.get("/{article_id}/export/markdown")
def export_markdown(article_id: int, db: Session = Depends(get_db)):
    service = ArticleService(db)
    content = service.export_article_markdown(article_id)
    if not content:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # 返回Markdown文件
    return Response(
        content=content,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename=article_{article_id}.md"}
    )
```

- [ ] **Step 4: 运行测试验证**

```bash
# 运行服务器
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 测试API
# 先创建一些知识条目
curl -X POST http://localhost:8000/api/knowledge/entries/ \
  -H "Content-Type: application/json" \
  -d '{"title": "BeyondMiMic基础", "content": "BeyondMiMic是一个人形机器人仿真平台", "entry_type": "concept"}'

# 从知识生成文章
curl -X POST http://localhost:8000/api/articles/generate/from-knowledge \
  -H "Content-Type: application/json" \
  -d '{"knowledge_ids": [1], "title": "BeyondMiMic入门指南"}'

# 导出Markdown
curl -O http://localhost:8000/api/articles/1/export/markdown
```

- [ ] **Step 5: 提交代码**

```bash
git add backend/app/services/article.py backend/app/routes/article.py backend/app/models/article.py backend/templates/
git commit -m "feat: 添加文章生成引擎"
```

---

## Task 6: 智能待办系统

**Covers:** [S3, S5]

**Files:**
- Create: `/home/dell/文档/MimoCode/backend/app/services/todo.py`
- Create: `/home/dell/文档/MimoCode/backend/app/routes/todo.py`
- Create: `/home/dell/文档/MimoCode/backend/app/models/todo.py`

**Interfaces:**
- Consumes: Task 2 产生的后端框架
- Produces: 待办任务管理API、智能规划算法

- [ ] **Step 1: 创建待办任务数据模型**

```python
# backend/app/models/todo.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime
from .database import Base

class TodoTask(Base):
    __tablename__ = "todo_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    priority = Column(Integer, default=3)  # 1-5, 1最高
    status = Column(String(20), default="pending")  # pending, in_progress, completed
    due_date = Column(DateTime, nullable=True)
    estimated_minutes = Column(Integer, default=30)  # 预估时间(分钟)
    actual_minutes = Column(Integer, nullable=True)  # 实际时间(分钟)
    tags = Column(String(500))  # 逗号分隔的标签
    category = Column(String(50))  # 任务类别: learning, coding, research, other
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
```

- [ ] **Step 2: 创建智能规划服务**

```python
# backend/app/services/todo.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.todo import TodoTask
from datetime import datetime, timedelta
from typing import Dict, List
import heapq

class TodoService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_task(self, title: str, description: str = None, priority: int = 3,
                   due_date: datetime = None, estimated_minutes: int = 30,
                   tags: str = None, category: str = "other") -> TodoTask:
        task = TodoTask(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            estimated_minutes=estimated_minutes,
            tags=tags,
            category=category
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_tasks(self, status: str = None, category: str = None) -> List[TodoTask]:
        query = self.db.query(TodoTask)
        if status:
            query = query.filter(TodoTask.status == status)
        if category:
            query = query.filter(TodoTask.category == category)
        return query.order_by(TodoTask.priority, TodoTask.due_date).all()
    
    def get_task(self, task_id: int) -> Optional[TodoTask]:
        return self.db.query(TodoTask).filter(TodoTask.id == task_id).first()
    
    def update_task_status(self, task_id: int, status: str) -> bool:
        task = self.get_task(task_id)
        if task:
            task.status = status
            if status == "completed":
                task.completed_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def smart_schedule(self, available_minutes: int = 480) -> List[Dict]:
        """
        智能规划算法
        基于优先级和截止日期安排任务
        """
        # 获取所有待处理任务
        pending_tasks = self.db.query(TodoTask).filter(
            TodoTask.status == "pending"
        ).all()
        
        if not pending_tasks:
            return []
        
        # 计算任务得分 (用于排序)
        scored_tasks = []
        for task in pending_tasks:
            # 优先级得分 (1最高，5最低)
            priority_score = (6 - task.priority) * 10
            
            # 截止日期紧迫度
            urgency_score = 0
            if task.due_date:
                days_until_due = (task.due_date - datetime.utcnow()).days
                if days_until_due <= 0:
                    urgency_score = 100  # 已过期
                elif days_until_due <= 1:
                    urgency_score = 80  # 明天截止
                elif days_until_due <= 3:
                    urgency_score = 60  # 3天内截止
                elif days_until_due <= 7:
                    urgency_score = 40  # 1周内截止
                else:
                    urgency_score = 20  # 更长时间
            
            # 总得分
            total_score = priority_score + urgency_score
            scored_tasks.append((total_score, task))
        
        # 按得分排序 (高分优先)
        scored_tasks.sort(key=lambda x: x[0], reverse=True)
        
        # 贪心算法安排任务
        schedule = []
        remaining_minutes = available_minutes
        
        for score, task in scored_tasks:
            if task.estimated_minutes <= remaining_minutes:
                schedule.append({
                    "task_id": task.id,
                    "title": task.title,
                    "priority": task.priority,
                    "estimated_minutes": task.estimated_minutes,
                    "category": task.category,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "score": score
                })
                remaining_minutes -= task.estimated_minutes
        
        return schedule
    
    def get_daily_summary(self) -> Dict:
        """获取每日任务摘要"""
        today = datetime.utcnow().date()
        
        # 今日任务
        today_tasks = self.db.query(TodoTask).filter(
            TodoTask.due_date >= datetime.combine(today, datetime.min.time()),
            TodoTask.due_date < datetime.combine(today + timedelta(days=1), datetime.min.time()),
            TodoTask.status != "completed"
        ).count()
        
        # 待处理任务总数
        pending_tasks = self.db.query(TodoTask).filter(
            TodoTask.status == "pending"
        ).count()
        
        # 今日完成任务
        completed_today = self.db.query(TodoTask).filter(
            TodoTask.completed_at >= datetime.combine(today, datetime.min.time()),
            TodoTask.completed_at < datetime.combine(today + timedelta(days=1), datetime.min.time())
        ).count()
        
        # 总预估时间
        total_estimated = self.db.query(TodoTask).filter(
            TodoTask.status == "pending"
        ).with_entities(
            TodoTask.estimated_minutes
        ).all()
        total_minutes = sum(t[0] for t in total_estimated if t[0])
        
        return {
            "date": today.isoformat(),
            "today_tasks": today_tasks,
            "pending_tasks": pending_tasks,
            "completed_today": completed_today,
            "total_estimated_hours": round(total_minutes / 60, 1)
        }
```

- [ ] **Step 3: 创建待办任务API路由**

```python
# backend/app/routes/todo.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..models.database import get_db
from ..models.todo import TodoTask
from ..services.todo import TodoService
from pydantic import BaseModel

router = APIRouter(prefix="/api/todo", tags=["todo"])

class TaskCreate(BaseModel):
    title: str
    description: str = None
    priority: int = 3
    due_date: datetime = None
    estimated_minutes: int = 30
    tags: str = None
    category: str = "other"

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    status: str
    due_date: datetime
    estimated_minutes: int
    actual_minutes: int
    tags: str
    category: str
    created_at: datetime
    updated_at: datetime
    completed_at: datetime
    
    class Config:
        from_attributes = True

class ScheduleResponse(BaseModel):
    task_id: int
    title: str
    priority: int
    estimated_minutes: int
    category: str
    due_date: str
    score: int

class DailySummaryResponse(BaseModel):
    date: str
    today_tasks: int
    pending_tasks: int
    completed_today: int
    total_estimated_hours: float

@router.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    service = TodoService(db)
    return service.create_task(**task.model_dump())

@router.get("/tasks/", response_model=List[TaskResponse])
def list_tasks(
    status: str = Query(None, regex="^(pending|in_progress|completed)$"),
    category: str = Query(None, regex="^(learning|coding|research|other)$"),
    db: Session = Depends(get_db)
):
    service = TodoService(db)
    return service.get_tasks(status, category)

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    service = TodoService(db)
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}/status")
def update_status(task_id: int, status: str = Query(..., regex="^(pending|in_progress|completed)$"), db: Session = Depends(get_db)):
    service = TodoService(db)
    if not service.update_task_status(task_id, status):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Status updated"}

@router.get("/schedule/", response_model=List[ScheduleResponse])
def get_schedule(available_minutes: int = Query(480, ge=60, le=960), db: Session = Depends(get_db)):
    service = TodoService(db)
    return service.smart_schedule(available_minutes)

@router.get("/summary/", response_model=DailySummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    service = TodoService(db)
    return service.get_daily_summary()
```

- [ ] **Step 4: 运行测试验证**

```bash
# 运行服务器
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 测试API
# 创建任务
curl -X POST http://localhost:8000/api/todo/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "学习BeyondMiMic基础", "priority": 1, "category": "learning", "estimated_minutes": 120}'

# 获取智能规划
curl "http://localhost:8000/api/todo/schedule/?available_minutes=240"

# 获取每日摘要
curl "http://localhost:8000/api/todo/summary/"
```

- [ ] **Step 5: 提交代码**

```bash
git add backend/app/services/todo.py backend/app/routes/todo.py backend/app/models/todo.py
git commit -m "feat: 添加智能待办系统"
```

---

## Task 7: 前端界面开发

**Covers:** [S3, S5]

**Files:**
- Create: `/home/dell/文档/MimoCode/frontend/`
- Create: Vue.js项目结构
- Create: 各个组件页面

**Interfaces:**
- Consumes: Task 2-6 产生的后端API
- Produces: Web前端界面

- [ ] **Step 1: 创建Vue.js项目**

```bash
# 安装Vue CLI
npm install -g @vue/cli

# 创建项目
cd /home/dell/文档/MimoCode
vue create frontend

# 选择默认配置 (Vue 3, Babel, ESLint)
```

- [ ] **Step 2: 安装依赖**

```bash
cd frontend
npm install axios
npm install element-plus  # UI组件库
npm install vue-router
npm install pinia  # 状态管理
```

- [ ] **Step 3: 创建主要组件**

```vue
<!-- frontend/src/App.vue -->
<template>
  <div id="app">
    <el-container>
      <el-aside width="200px">
        <el-menu :default-active="activeMenu" router>
          <el-menu-item index="/">
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/learning">
            <span>学习路径</span>
          </el-menu-item>
          <el-menu-item index="/knowledge">
            <span>知识库</span>
          </el-menu-item>
          <el-menu-item index="/code">
            <span>代码管理</span>
          </el-menu-item>
          <el-menu-item index="/articles">
            <span>文章生成</span>
          </el-menu-item>
          <el-menu-item index="/todo">
            <span>待办任务</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    activeMenu() {
      return this.$route.path
    }
  }
}
</script>
```

- [ ] **Step 4: 运行测试验证**

```bash
cd frontend
npm run serve

# 访问 http://localhost:8080
```

- [ ] **Step 5: 提交代码**

```bash
git add frontend/
git commit -m "feat: 添加前端界面"
```

---

## Task 8: Obsidian配置

**Covers:** [S3]

**Files:**
- Create: `/home/dell/文档/MimoCode/docs/obsidian-setup.md`
- Create: Obsidian配置文件

**Interfaces:**
- Consumes: 无
- Produces: Obsidian知识库结构、配置文档

- [ ] **Step 1: 创建Obsidian配置文档**

```markdown
# Obsidian配置指南

## 知识库结构

```
Robotics-Learning/
├── 00- Inbox (待整理)
├── 01- 学习笔记
│   ├── BeyondMiMic
│   │   ├── 基础概念.md
│   │   ├── 环境配置.md
│   │   └── 示例项目.md
│   ├── ISAAC Lab
│   │   ├── 安装指南.md
│   │   ├── 基础使用.md
│   │   └── 高级功能.md
│   └── VLA
│       ├── 视觉语言模型.md
│       ├── 具身智能.md
│       └── 应用案例.md
├── 02- 代码片段
│   ├── Python代码.md
│   ├── CUDA代码.md
│   └── 配置文件.md
├── 03- 项目文档
│   ├── 项目计划.md
│   ├── 进度跟踪.md
│   └── 问题记录.md
├── 04- 论文笔记
│   ├── 必读论文.md
│   ├── 论文总结.md
│   └── 研究方向.md
└── 05- 学习日志
    ├── 2026-07-01.md
    ├── 2026-07-02.md
    └── ...
```

## 推荐插件

### 核心插件
- **Templates** - 模板管理
- **Daily Notes** - 每日笔记
- **Calendar** - 日历视图
- **Search** - 高级搜索

### 第三方插件
- **Zotero Integration** - Zotero集成
- **Git** - Git集成
- **Templater** - 高级模板
- **Dataview** - 数据查询
- **Excalidraw** - 绘图

## 模板配置

### 每日笔记模板
```markdown
# {{date:YYYY-MM-DD}}

## 今日计划
- [ ] 任务1
- [ ] 任务2
- [ ] 任务3

## 学习记录
### 上午
- 

### 下午
- 

## 代码记录
```python
# 代码片段
```

## 问题与思考
- 

## 明日计划
- 
```

### 论文笔记模板
```markdown
# {{title}}

## 基本信息
- **标题**: 
- **作者**: 
- **发表时间**: 
- **期刊/会议**: 
- **链接**: 

## 摘要
- 

## 核心贡献
1. 
2. 
3. 

## 方法论
- 

## 实验结果
- 

## 个人思考
- 

## 相关工作
- 
```

## 快捷键配置

- **快速打开**: Cmd/Ctrl + O
- **全局搜索**: Cmd/Ctrl + Shift + F
- **新建笔记**: Cmd/Ctrl + N
- **插入模板**: Cmd/Ctrl + Shift + T
```

- [ ] **Step 2: 提交代码**

```bash
git add docs/obsidian-setup.md
git commit -m "docs: 添加Obsidian配置指南"
```

---

## Task 9: Zotero配置

**Covers:** [S3]

**Files:**
- Create: `/home/dell/文档/MimoCode/docs/zotero-setup.md`

**Interfaces:**
- Consumes: 无
- Produces: Zotero配置文档

- [ ] **Step 1: 创建Zotero配置文档**

```markdown
# Zotero配置指南

## 安装与配置

### 安装步骤
1. 下载Zotero: https://www.zotero.org/
2. 安装Zotero Desktop
3. 安装Zotero Connector (浏览器插件)

### 基础配置
1. 打开Zotero → 编辑 → 设置
2. 常规设置:
   - 数据存储位置: 选择本地文件夹
   - 同步: 配置Zotero账户 (可选)
3. 引用设置:
   - 安装Better BibTeX插件
   - 配置引用格式

## 推荐插件

### 必装插件
1. **Better BibTeX** - 引用管理
   - 下载: https://retorque.re/zotero-better-bibtex/
   - 功能: 自动生成BibTeX引用键
   
2. **Zotero Connector** - 浏览器集成
   - 支持Chrome, Firefox, Edge
   - 功能: 一键保存网页到Zotero

3. **Zotero PDF Translate** - PDF翻译
   - 功能: 支持多种翻译引擎

### 可选插件
1. **Zotero Abstract** - 摘要管理
2. **Zotero Style** - 外观定制
3. **Zotero File** - 文件管理

## 论文管理流程

### 收集论文
1. 在浏览器中找到论文
2. 点击Zotero Connector图标
3. 论文自动保存到Zotero

### 组织论文
1. 创建集合 (Collections):
   - BeyondMiMic
   - ISAAC Lab
   - VLA
   - 具身智能
   - 通用机器人

2. 添加标签 (Tags):
   - 基础理论
   - 仿真平台
   - 深度学习
   - 强化学习
   - 控制算法

### 阅读论文
1. 在Zotero中打开PDF
2. 使用高亮和笔记功能
3. 添加标签标记重要程度

### 导出引用
1. 选择论文
2. 右键 → 导出条目
3. 选择格式:
   - BibTeX (用于LaTeX)
   - CSV (用于Excel)
   - HTML (用于网页)

## Obsidian集成

### 安装Zotero Integration插件
1. 在Obsidian中打开设置
2. 社区插件 → 搜索 "Zotero Integration"
3. 安装并启用

### 配置集成
1. 打开插件设置
2. 配置Zotero数据库路径
3. 配置导出格式
4. 测试连接

### 使用方法
1. 在Obsidian中使用命令: Zotero Integration
2. 选择要导入的论文
3. 自动生成笔记

## 引用键管理

### 自动生成引用键
在Better BibTeX设置中:
1. 打开设置 → 引用
2. 引用键格式: [auth:lower][year]
3. 示例: smith2026

### 手动修改引用键
1. 在Zotero中选择论文
2. 右键 → Better BibTeX
3. 获取引用键

## 最佳实践

### 命名规范
- 论文标题: 使用原始标题
- 文件名: [作者]_[年份]_[简短标题].pdf
- 引用键: [auth:lower][year][shorttitle:lower]

### 组织原则
1. 按研究领域分类
2. 按重要程度标签
3. 定期整理和归档
4. 保持引用键一致性

### 备份策略
1. 定期导出Zotero数据
2. 备份PDF文件
3. 使用云同步 (可选)
```

- [ ] **Step 2: 提交代码**

```bash
git add docs/zotero-setup.md
git commit -m "docs: 添加Zotero配置指南"
```

---

## Task 10: Isaac Lab环境配置

**Covers:** [S4]

**Files:**
- Create: `/home/dell/文档/MimoCode/scripts/setup-isaac-lab.sh`
- Create: `/home/dell/文档/MimoCode/docs/isaac-lab-setup.md`

**Interfaces:**
- Consumes: Task 1 产生的服务器环境
- Produces: Isaac Lab安装脚本、配置文档

- [ ] **Step 1: 创建Isaac Lab安装脚本**

```bash
#!/bin/bash
# setup-isaac-lab.sh - Isaac Lab安装脚本

set -e

echo "=== 开始安装Isaac Lab ==="

# 1. 检查CUDA
echo "1. 检查CUDA..."
if ! command -v nvcc &> /dev/null; then
    echo "CUDA未安装，请先安装CUDA"
    exit 1
fi

# 2. 安装依赖
echo "2. 安装依赖..."
sudo apt install -y git cmake build-essential

# 3. 安装Python虚拟环境
echo "3. 创建Python虚拟环境..."
python3 -m venv ~/isaac-lab-env
source ~/isaac-lab-env/bin/activate

# 4. 安装Isaac Lab
echo "4. 安装Isaac Lab..."
pip install --upgrade pip
pip install isaacsim[all]

# 5. 安装额外依赖
echo "5. 安装额外依赖..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install numpy pandas matplotlib

# 6. 验证安装
echo "6. 验证安装..."
python -c "import isaacsim; print('Isaac Sim安装成功')"

# 7. 安装Isaac Lab示例
echo "7. 安装Isaac Lab示例..."
git clone https://github.com/isaac-sim/IsaacLab.git ~/IsaacLab
cd ~/IsaacLab
./setup.sh

echo "=== Isaac Lab安装完成 ==="
echo "请运行 'source ~/isaac-lab-env/bin/activate' 激活环境"
```

- [ ] **Step 2: 创建配置文档**

```markdown
# Isaac Lab环境配置指南

## 系统要求

### 硬件要求
- **GPU**: NVIDIA GPU (RTX 2070或更高)
- **RAM**: 至少16GB
- **存储**: 至少50GB可用空间
- **CPU**: 多核处理器

### 软件要求
- **操作系统**: Ubuntu 22.04 LTS
- **CUDA**: 12.x
- **cuDNN**: 8.x
- **Python**: 3.8+

## 安装步骤

### 1. 环境准备
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础工具
sudo apt install -y git cmake build-essential
```

### 2. 安装CUDA (如未安装)
```bash
# 下载CUDA
wget https://developer.download.nvidia.com/compute/cuda/12.2.0/local_installers/cuda_12.2.0_535.54.03_linux.run

# 安装CUDA
sudo sh cuda_12.2.0_535.54.03_linux.run

# 配置环境变量
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

### 3. 安装Isaac Lab
```bash
# 创建虚拟环境
python3 -m venv ~/isaac-lab-env
source ~/isaac-lab-env/bin/activate

# 安装Isaac Sim
pip install isaacsim[all]

# 安装PyTorch (CUDA版本)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 4. 克隆Isaac Lab
```bash
git clone https://github.com/isaac-sim/IsaacLab.git ~/IsaacLab
cd ~/IsaacLab
./setup.sh
```

## 使用方法

### 启动Isaac Sim
```bash
source ~/isaac-lab-env/bin/activate
isaacsim
```

### 运行示例
```bash
cd ~/IsaacLab
python examples/standalone/run.py --task Isaac-Cartpole-v0
```

### 常用命令
```bash
# 列出所有可用任务
python -c "from isaacsim import SimulationApp; app = SimulationApp()"

# 运行特定任务
python examples/standalone/run.py --task [任务名称]
```

## 常见问题

### 问题1: CUDA内存不足
**解决方案**:
```bash
# 减少batch size
export CUDA_VISIBLE_DEVICES=0
```

### 问题2: 显示器问题
**解决方案**:
```bash
# 使用无头模式
export DISPLAY=:0
```

### 问题3: 依赖冲突
**解决方案**:
```bash
# 重新创建虚拟环境
rm -rf ~/isaac-lab-env
python3 -m venv ~/isaac-lab-env
source ~/isaac-lab-env/bin/activate
pip install isaacsim[all]
```

## 开发建议

### 项目结构
```
my_isaac_project/
├── tasks/          # 自定义任务
├── environments/   # 环境配置
├── agents/         # 智能体
└── utils/          # 工具函数
```

### 调试技巧
1. 使用GUI模式调试
2. 启用详细日志
3. 使用Python调试器

### 性能优化
1. 使用GPU加速
2. 优化仿真步长
3. 使用并行仿真
```

- [ ] **Step 3: 运行测试验证**

```bash
# 运行安装脚本
chmod +x scripts/setup-isaac-lab.sh
bash scripts/setup-isaac-lab.sh

# 验证安装
source ~/isaac-lab-env/bin/activate
python -c "import isaacsim; print('Isaac Lab安装成功')"
```

- [ ] **Step 4: 提交代码**

```bash
git add scripts/setup-isaac-lab.sh docs/isaac-lab-setup.md
git commit -m "feat: 添加Isaac Lab环境配置"
```

---

## Task 11: 系统集成与测试

**Covers:** [S7]

**Files:**
- Create: `/home/dell/文档/MimoCode/docs/integration-guide.md`
- Create: `/home/dell/文档/MimoCode/tests/`

**Interfaces:**
- Consumes: Task 1-10 产生的所有组件
- Produces: 集成文档、测试用例

- [ ] **Step 1: 创建集成文档**

```markdown
# 系统集成指南

## 组件清单

### 已完成组件
1. ✅ 基础环境配置 (Task 1)
2. ✅ 助学助手核心系统 (Task 2)
3. ✅ 知识库管理模块 (Task 3)
4. ✅ 代码收集与管理 (Task 4)
5. ✅ 文章生成引擎 (Task 5)
6. ✅ 智能待办系统 (Task 6)
7. ✅ 前端界面 (Task 7)
8. ✅ Obsidian配置 (Task 8)
9. ✅ Zotero配置 (Task 9)
10. ✅ Isaac Lab环境 (Task 10)

## 集成步骤

### 1. 启动后端服务
```bash
cd /home/dell/文档/MimoCode/backend
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 启动前端服务
```bash
cd /home/dell/文档/MimoCode/frontend
npm run serve
```

### 3. 配置SSH连接
```bash
# 在MacBook上配置
cat >> ~/.ssh/config << EOF
Host robotics-server
    HostName 10.185.157.92
    User dell
    Port 22
    IdentityFile ~/.ssh/id_rsa
EOF
```

### 4. 测试连接
```bash
# 测试SSH
ssh robotics-server

# 测试API
curl http://10.185.157.92:8000/health
```

## 功能测试

### 测试1: 知识库管理
```bash
# 创建知识条目
curl -X POST http://localhost:8000/api/knowledge/entries/ \
  -H "Content-Type: application/json" \
  -d '{"title": "测试知识", "content": "测试内容", "entry_type": "concept"}'

# 搜索知识
curl "http://localhost:8000/api/knowledge/entries/?query=测试"
```

### 测试2: 代码管理
```bash
# 创建代码片段
curl -X POST http://localhost:8000/api/code/snippets/ \
  -H "Content-Type: application/json" \
  -d '{"title": "测试代码", "code": "print(\"hello\")", "language": "python"}'

# 搜索代码
curl "http://localhost:8000/api/code/snippets/?query=hello"
```

### 测试3: 待办任务
```bash
# 创建任务
curl -X POST http://localhost:8000/api/todo/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "测试任务", "priority": 1, "category": "learning"}'

# 获取规划
curl "http://localhost:8000/api/todo/schedule/"
```

### 测试4: 文章生成
```bash
# 从知识生成文章
curl -X POST http://localhost:8000/api/articles/generate/from-knowledge \
  -H "Content-Type: application/json" \
  -d '{"knowledge_ids": [1], "title": "测试文章"}'

# 导出Markdown
curl -O http://localhost:8000/api/articles/1/export/markdown
```

## 部署检查清单

- [ ] 服务器环境配置完成
- [ ] NVIDIA驱动安装成功
- [ ] CUDA安装成功
- [ ] Docker安装成功
- [ ] SSH服务配置成功
- [ ] 后端服务启动成功
- [ ] 前端服务启动成功
- [ ] 数据库初始化成功
- [ ] API接口测试通过
- [ ] Obsidian配置完成
- [ ] Zotero配置完成
- [ ] Isaac Lab安装成功

## 故障排除

### 问题1: SSH连接失败
**解决方案**:
```bash
# 检查SSH服务
sudo systemctl status ssh

# 检查防火墙
sudo ufw status

# 检查密钥权限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
```

### 问题2: API服务无法访问
**解决方案**:
```bash
# 检查端口
netstat -tuln | grep 8000

# 检查防火墙
sudo ufw allow 8000

# 检查服务日志
journalctl -u uvicorn
```

### 问题3: 数据库错误
**解决方案**:
```bash
# 重建数据库
rm -f robotics_learning.db
python3 -c "from app.models.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

## 性能监控

### 监控命令
```bash
# 监控系统资源
htop

# 监控网络
iftop

# 监控GPU
nvidia-smi -l 1

# 监控磁盘
iotop
```

### 日志查看
```bash
# 后端日志
tail -f /home/dell/文档/MimoCode/backend/logs/app.log

# 系统日志
journalctl -f
```
```

- [ ] **Step 2: 创建测试用例**

```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_knowledge_entry():
    response = client.post("/api/knowledge/entries/", json={
        "title": "测试知识",
        "content": "测试内容",
        "entry_type": "concept"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "测试知识"

def test_create_code_snippet():
    response = client.post("/api/code/snippets/", json={
        "title": "测试代码",
        "code": "print('hello')",
        "language": "python"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "测试代码"

def test_create_todo_task():
    response = client.post("/api/todo/tasks/", json={
        "title": "测试任务",
        "priority": 1,
        "category": "learning"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "测试任务"
```

- [ ] **Step 3: 运行测试**

```bash
cd /home/dell/文档/MimoCode/backend
pytest tests/ -v
```

- [ ] **Step 4: 提交代码**

```bash
git add docs/integration-guide.md tests/
git commit -m "docs: 添加系统集成指南和测试用例"
```

---

## Task 12: 最终验证与文档

**Covers:** [S7, S8]

**Files:**
- Create: `/home/dell/文档/MimoCode/README.md`
- Create: `/home/dell/文档/MimoCode/docs/user-guide.md`

**Interfaces:**
- Consumes: Task 1-11 产生的所有组件
- Produces: 项目README、用户指南

- [ ] **Step 1: 创建项目README**

```markdown
# 人形机器人助学助手系统

Robotics Learning Assistant (RLA) - 一套完整的助学助手系统，用于支持人形机器人领域的学习和研究。

## 功能特性

### 🎯 核心功能
- **学习路径规划** - 个性化学习路径生成
- **知识库管理** - 人形机器人知识整理
- **代码收集与管理** - 代码片段自动收集
- **文章生成引擎** - Markdown文章生成
- **智能提醒系统** - 任务优先级调度

### 🛠️ 技术栈
- **后端**: Python (FastAPI)
- **前端**: Vue.js + Element Plus
- **数据库**: SQLite + PostgreSQL
- **AI**: 本地LLM + API调用
- **仿真**: Isaac Lab

## 系统架构

```
MacBook Air (前端)                    本地服务器 (后端)
├── Obsidian (笔记管理)              ├── CUDA计算环境
├── Zotero (论文管理)                ├── ISAAC Lab仿真
├── VS Code Remote (开发)            ├── 模型训练/推理
├── RLA Web UI (助学助手)            ├── 代码仓库
└── SSH连接                          └── 数据存储
```

## 快速开始

### 1. 环境准备

#### 服务器环境
```bash
# 运行服务器配置脚本
bash scripts/setup-server.sh
```

#### MacBook环境
```bash
# 运行MacBook配置脚本
bash scripts/setup-macbook.sh
```

### 2. 启动服务

#### 后端服务
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端服务
```bash
cd frontend
npm install
npm run serve
```

### 3. 访问系统

- **Web界面**: http://localhost:8080
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 文档

- [环境配置指南](docs/environment-setup.md)
- [Obsidian配置指南](docs/obsidian-setup.md)
- [Zotero配置指南](docs/zotero-setup.md)
- [Isaac Lab配置指南](docs/isaac-lab-setup.md)
- [系统集成指南](docs/integration-guide.md)
- [用户指南](docs/user-guide.md)

## 开发指南

### 项目结构
```
robotics-learning-assistant/
├── backend/          # 后端代码
├── frontend/         # 前端代码
├── scripts/          # 配置脚本
├── docs/             # 文档
├── tests/            # 测试用例
└── data/             # 数据文件
```

### 贡献指南
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

- 项目主页: https://github.com/your-username/robotics-learning-assistant
- 问题反馈: https://github.com/your-username/robotics-learning-assistant/issues
```

- [ ] **Step 2: 创建用户指南**

```markdown
# 用户指南

## 快速入门

### 第一次使用

1. **启动系统**
   - 服务器端: `bash scripts/start-server.sh`
   - 客户端: 打开浏览器访问 http://localhost:8080

2. **创建学习路径**
   - 点击"学习路径"
   - 点击"新建路径"
   - 填写路径信息
   - 保存

3. **添加知识条目**
   - 点击"知识库"
   - 点击"新建条目"
   - 填写内容
   - 保存

4. **管理代码**
   - 点击"代码管理"
   - 点击"添加代码"
   - 填写代码信息
   - 保存

5. **生成文章**
   - 点击"文章生成"
   - 选择知识或代码
   - 点击"生成文章"
   - 导出Markdown

6. **管理待办**
   - 点击"待办任务"
   - 点击"添加任务"
   - 填写任务信息
   - 查看智能规划

## 功能详解

### 学习路径管理

#### 创建学习路径
1. 点击"学习路径" → "新建路径"
2. 填写:
   - 路径名称
   - 描述
   - 目标领域 (BeyondMiMic/ISAAC Lab/VLA)
   - 难度等级 (1-5)
3. 点击"保存"

#### 添加学习任务
1. 选择学习路径
2. 点击"添加任务"
3. 填写:
   - 任务标题
   - 描述
   - 任务类型 (理论/实践/项目)
   - 优先级
   - 截止日期
4. 点击"保存"

### 知识库管理

#### 创建知识分类
1. 点击"知识库" → "分类管理"
2. 点击"新建分类"
3. 填写分类信息
4. 保存

#### 添加知识条目
1. 点击"新建条目"
2. 填写:
   - 标题
   - 内容 (支持Markdown)
   - 类型 (概念/教程/示例/参考)
   - 分类
   - 标签
3. 保存

#### 搜索知识
1. 在搜索框输入关键词
2. 选择筛选条件
3. 查看结果

### 代码管理

#### 添加代码片段
1. 点击"代码管理" → "添加代码"
2. 填写:
   - 标题
   - 代码
   - 语言
   - 描述
   - 标签
   - 项目名称
3. 保存

#### 搜索代码
1. 在搜索框输入关键词
2. 选择语言筛选
3. 查看结果

### 文章生成

#### 从知识生成
1. 选择要包含的知识条目
2. 点击"从知识生成"
3. 填写文章标题
4. 生成并预览
5. 导出Markdown

#### 从代码生成
1. 选择要包含的代码片段
2. 点击"从代码生成"
3. 填写文章标题
4. 生成并预览
5. 导出Markdown

### 待办任务管理

#### 添加任务
1. 点击"待办任务" → "添加任务"
2. 填写:
   - 标题
   - 描述
   - 优先级 (1-5)
   - 截止日期
   - 预估时间
   - 类别
3. 保存

#### 查看智能规划
1. 点击"智能规划"
2. 设置可用时间
3. 查看系统安排的任务

#### 更新任务状态
1. 选择任务
2. 点击状态按钮
3. 选择新状态

## 快捷键

### 全局快捷键
- **Ctrl/Cmd + N**: 新建项目
- **Ctrl/Cmd + S**: 保存
- **Ctrl/Cmd + F**: 搜索
- **Ctrl/Cmd + /**: 帮助

### 列表快捷键
- **↑/↓**: 选择项目
- **Enter**: 打开项目
- **Delete**: 删除项目

## 常见问题

### Q: 如何连接远程服务器?
A: 
1. 确保服务器SSH服务运行
2. 配置SSH密钥
3. 使用VS Code Remote-SSH连接

### Q: 如何同步数据?
A: 
1. 使用Git进行版本控制
2. 定期提交更改
3. 使用Obsidian同步功能

### Q: 如何备份数据?
A: 
1. 备份数据库文件
2. 备份配置文件
3. 使用Git备份代码

## 技术支持

- 项目主页: https://github.com/your-username/robotics-learning-assistant
- 问题反馈: https://github.com/your-username/robotics-learning-assistant/issues
- 邮箱: your-email@example.com
```

- [ ] **Step 3: 运行最终验证**

```bash
# 运行所有测试
cd /home/dell/文档/MimoCode/backend
pytest tests/ -v

# 验证文档完整性
ls -la docs/

# 验证脚本可执行
chmod +x scripts/*.sh
```

- [ ] **Step 4: 提交代码**

```bash
git add README.md docs/user-guide.md
git commit -m "docs: 添加项目README和用户指南"
```

---

## 最终检查清单

### 功能验证
- [ ] 服务器环境配置完成
- [ ] MacBook环境配置完成
- [ ] SSH连接测试通过
- [ ] 后端API服务正常
- [ ] 前端界面正常
- [ ] 知识库管理功能正常
- [ ] 代码管理功能正常
- [ ] 文章生成功能正常
- [ ] 待办任务功能正常
- [ ] Obsidian配置完成
- [ ] Zotero配置完成
- [ ] Isaac Lab安装成功

### 文档完整性
- [ ] 环境配置文档
- [ ] Obsidian配置文档
- [ ] Zotero配置文档
- [ ] Isaac Lab配置文档
- [ ] 系统集成文档
- [ ] 用户指南
- [ ] 项目README

### 代码质量
- [ ] 代码规范
- [ ] 测试覆盖率
- [ ] 文档完整性
- [ ] 性能优化

### 部署就绪
- [ ] 配置脚本可执行
- [ ] 依赖管理完整
- [ ] 环境变量配置
- [ ] 日志记录

---

**计划完成时间**: 预计2-3周

**下一步**: 使用 `compose:execute` 或 `compose:subagent` 执行此计划
