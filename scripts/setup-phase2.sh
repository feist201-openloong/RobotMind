#!/bin/bash
# ============================================================================
# 第二阶段：重启后安装（预计 60-90 分钟）
# 目标：CUDA + Docker + Isaac Lab 环境 + RobotMind
# ============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; exit 1; }
log_step() { echo -e "\n${CYAN}========== $1 ==========${NC}"; }

# ============================================================================
# 0. 前置检查
# ============================================================================
log_step "前置检查"

# 检查 NVIDIA 驱动
if ! nvidia-smi &>/dev/null; then
    log_error "NVIDIA 驱动未加载，请重启后重试"
fi
log_info "NVIDIA 驱动正常"
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv

# 检查 Conda
if ! command -v conda &>/dev/null; then
    log_error "Conda 未安装"
fi
log_info "Conda 正常"

# 激活 conda
source ~/miniconda3/etc/profile.d/conda.sh

# ============================================================================
# 1. 安装 CUDA 12.2
# ============================================================================
log_step "步骤 1/8：安装 CUDA 12.2"

CUDA_KEYRING_DEB="cuda-keyring_1.1-1_all.deb"
CUDA_KEYRING_URL="https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/${CUDA_KEYRING_DEB}"

if [ -d "/usr/local/cuda-12.2" ]; then
    log_warn "CUDA 12.2 已安装，跳过"
else
    log_info "下载 CUDA 密钥包..."
    wget -q "$CUDA_KEYRING_URL" -O "/tmp/${CUDA_KEYRING_DEB}"
    
    log_info "安装 CUDA 密钥包..."
    sudo dpkg -i "/tmp/${CUDA_KEYRING_DEB}"
    sudo apt update
    
    log_info "安装 CUDA 12.2（约 3GB，需等待）..."
    sudo apt install -y cuda-12-2
    
    rm -f "/tmp/${CUDA_KEYRING_DEB}"
    log_info "CUDA 12.2 安装完成"
fi

# 配置环境变量
BASHRC_MARKER="# CUDA Environment Variables"
if ! grep -q "$BASHRC_MARKER" ~/.bashrc 2>/dev/null; then
    cat >> ~/.bashrc << 'EOF'

# CUDA Environment Variables
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda
EOF
fi

export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda

log_info "CUDA 环境变量配置完成"

# ============================================================================
# 2. 安装 Docker
# ============================================================================
log_step "步骤 2/8：安装 Docker"

if command -v docker &>/dev/null; then
    log_warn "Docker 已安装，跳过"
else
    # 添加 Docker GPG 密钥
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # 添加 Docker 仓库
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # 将用户添加到 docker 组
    sudo usermod -aG docker "$USER"
    log_warn "需要重新登录才能使 docker 组生效"
fi

sudo systemctl enable docker
sudo systemctl start docker
log_info "Docker 安装完成"

# ============================================================================
# 3. 安装 NVIDIA Container Toolkit
# ============================================================================
log_step "步骤 3/8：安装 NVIDIA Container Toolkit"

if command -v nvidia-ctk &>/dev/null; then
    log_warn "NVIDIA Container Toolkit 已安装，跳过"
else
    NVIDIA_CTK_GPGKEY="/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg"
    if [ ! -f "$NVIDIA_CTK_GPGKEY" ]; then
        curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o "$NVIDIA_CTK_GPGKEY"
    fi
    
    if [ ! -f /etc/apt/sources.list.d/nvidia-container-toolkit.list ]; then
        curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
          sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
          sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    fi
    
    sudo apt update
    sudo apt install -y nvidia-container-toolkit
fi

sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
log_info "NVIDIA Container Toolkit 安装完成"

# ============================================================================
# 4. 安装 Git LFS
# ============================================================================
log_step "步骤 4/8：安装 Git LFS"

if command -v git-lfs &>/dev/null; then
    log_warn "Git LFS 已安装，跳过"
else
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
    sudo apt install -y git-lfs
fi

git lfs install
log_info "Git LFS 安装完成"

# ============================================================================
# 5. 创建 Isaac Lab Conda 环境
# ============================================================================
log_step "步骤 5/8：创建 Isaac Lab Conda 环境"

ISAAC_ENV_NAME="isaac-lab"
conda activate base

if conda env list | grep -q "$ISAAC_ENV_NAME"; then
    log_warn "Conda 环境 $ISAAC_ENV_NAME 已存在，跳过"
else
    log_info "创建 Python 3.10 环境..."
    conda create -n "$ISAAC_ENV_NAME" python=3.10 -y
fi

conda activate "$ISAAC_ENV_NAME"

# 安装 Isaac Sim 依赖
log_info "安装 Isaac Sim 基础依赖..."
pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

log_info "Conda 环境创建完成"

# ============================================================================
# 6. 安装 RobotMind 后端依赖
# ============================================================================
log_step "步骤 6/8：安装 RobotMind 后端依赖"

cd ~/文档/RobotMind/backend

if [ ! -d "venv" ]; then
    python -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

log_info "RobotMind 后端依赖安装完成"

# ============================================================================
# 7. 安装 Node.js（前端）
# ============================================================================
log_step "步骤 7/8：安装 Node.js"

if command -v node &>/dev/null; then
    NODE_VERSION=$(node -v)
    log_warn "Node.js 已安装: $NODE_VERSION"
else
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt install -y nodejs
    log_info "Node.js 安装完成"
fi

# ============================================================================
# 8. 安装 Tailscale VPN
# ============================================================================
log_step "步骤 8/8：安装 Tailscale"

if command -v tailscale &>/dev/null; then
    log_warn "Tailscale 已安装"
else
    curl -fsSL https://tailscale.com/install.sh | sh
    log_info "Tailscale 安装完成"
    log_warn "运行 'sudo tailscale up' 进行登录"
fi

# ============================================================================
# 完成总结
# ============================================================================
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}    第二阶段安装完成！${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "${YELLOW}验证命令：${NC}"
echo "  nvidia-smi              # NVIDIA 驱动"
echo "  nvcc --version          # CUDA"
echo "  docker --version        # Docker"
echo "  conda --version         # Conda"
echo "  node -v                 # Node.js"
echo ""
echo -e "${YELLOW}启动 RobotMind 后端：${NC}"
echo "  cd ~/文档/RobotMind/backend"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo -e "${YELLOW}启动 RobotMind 前端：${NC}"
echo "  cd ~/文档/RobotMind/frontend"
echo "  npm install"
echo "  npm run dev"
echo ""
