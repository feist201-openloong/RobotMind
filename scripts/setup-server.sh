#!/bin/bash
# ============================================================================
# 服务器环境配置脚本 - Ubuntu 22.04 LTS
# 用途：初始化GPU服务器开发环境
# ============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# ============================================================================
# 1. 更新系统包
# ============================================================================
log_info "更新系统包..."
sudo apt update && sudo apt upgrade -y

# ============================================================================
# 2. 安装基础工具
# ============================================================================
log_info "安装基础工具..."
sudo apt install -y \
    curl \
    wget \
    git \
    vim \
    htop \
    net-tools \
    build-essential \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# ============================================================================
# 3. 安装NVIDIA驱动 (nvidia-driver-535)
# ============================================================================
log_info "安装NVIDIA驱动..."
sudo apt install -y nvidia-driver-535
log_warn "NVIDIA驱动安装完成，需要重启才能生效"

# ============================================================================
# 4. 安装CUDA 12.2
# ============================================================================
log_info "安装CUDA 12.2..."

# 添加CUDA密钥
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update

# 安装CUDA
sudo apt install -y cuda-12-2

# 清理安装文件
rm -f cuda-keyring_1.1-1_all.deb

# ============================================================================
# 5. 配置环境变量
# ============================================================================
log_info "配置环境变量..."

# 备份现有的.bashrc
cp ~/.bashrc ~/.bashrc.backup.$(date +%Y%m%d)

# 添加CUDA环境变量
cat >> ~/.bashrc << 'EOF'

# CUDA Environment Variables
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda

# Python Environment
export PYTHONDONTWRITEBYTECODE=1

# Docker
export DOCKER_HOST=unix:///var/run/docker.sock
EOF

# 立即生效
source ~/.bashrc

# ============================================================================
# 6. 安装Docker
# ============================================================================
log_info "安装Docker..."

# 添加Docker GPG密钥
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 添加Docker仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 将当前用户添加到docker组
sudo usermod -aG docker $USER
log_warn "需要重新登录才能使docker组生效"

# 启动Docker
sudo systemctl enable docker
sudo systemctl start docker

# ============================================================================
# 7. 安装NVIDIA Container Toolkit
# ============================================================================
log_info "安装NVIDIA Container Toolkit..."

# 添加NVIDIA Container Toolkit仓库
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# 安装NVIDIA Container Toolkit
sudo apt update
sudo apt install -y nvidia-container-toolkit

# 配置Docker使用NVIDIA运行时
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# ============================================================================
# 8. 安装Python环境
# ============================================================================
log_info "安装Python环境..."

# 安装Python 3.10和pip
sudo apt install -y python3.10 python3.10-venv python3-pip

# 创建Python虚拟环境目录
mkdir -p ~/venvs

# 创建默认虚拟环境
python3.10 -m venv ~/venvs/default
source ~/venvs/default/bin/activate

# 升级pip
pip install --upgrade pip

# 安装常用Python包
pip install \
    numpy \
    pandas \
    matplotlib \
    scikit-learn \
    jupyterlab \
    notebook \
    ipywidgets \
    rich \
    click \
    fastapi \
    uvicorn \
    requests \
    httpx \
    pydantic

# 配置Jupyter Lab
jupyter lab --generate-config
log_info "Jupyter Lab已安装，运行 'jupyter lab' 启动"

# ============================================================================
# 9. 安装Git LFS
# ============================================================================
log_info "安装Git LFS..."

curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt install -y git-lfs
git lfs install

# ============================================================================
# 10. 创建项目目录
# ============================================================================
log_info "创建项目目录结构..."

mkdir -p ~/projects/{ai,web,scripts,docs,data}
mkdir -p ~/data/{raw,processed,models,logs}
mkdir -p ~/backups

# 创建.gitignore全局配置
cat > ~/.gitignore_global << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/
dist/
build/

# Jupyter
.ipynb_checkpoints/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Secrets
.env
*.env.local
credentials.json
secrets/
EOF

git config --global core.excludesfile ~/.gitignore_global

# ============================================================================
# 完成
# ============================================================================
log_info "=========================================="
log_info "服务器环境配置完成!"
log_info "=========================================="
log_info ""
log_info "需要执行的操作:"
log_info "1. 重启系统以加载NVIDIA驱动"
log_info "2. 重新登录以使docker组生效"
log_info "3. 运行 'source ~/.bashrc' 使环境变量生效"
log_info ""
log_info "验证命令:"
log_info "  nvidia-smi              # 检查NVIDIA驱动"
log_info "  nvcc --version          # 检查CUDA"
log_info "  docker --version        # 检查Docker"
log_info "  docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi"
log_info "  python3 --version       # 检查Python"
log_info "  jupyter lab --version   # 检查Jupyter Lab"
log_info "  git lfs version         # 检查Git LFS"
