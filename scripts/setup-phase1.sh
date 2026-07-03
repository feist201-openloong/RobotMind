#!/bin/bash
# ============================================================================
# 第一阶段：重启前安装（预计 50 分钟）
# 目标：NVIDIA 驱动 + 基础环境 + Conda
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
# 1. 系统更新
# ============================================================================
log_step "步骤 1/6：系统更新"
sudo apt update && sudo apt upgrade -y
log_info "系统更新完成"

# ============================================================================
# 2. 安装基础工具（包含 cmake + build-essential，Isaac Lab 必需）
# ============================================================================
log_step "步骤 2/6：安装基础工具"
sudo apt install -y \
    curl \
    wget \
    git \
    vim \
    htop \
    net-tools \
    build-essential \
    cmake \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    unzip \
    zip \
    tree \
    jq

log_info "基础工具安装完成"

# ============================================================================
# 3. 安装 NVIDIA 驱动 535
# ============================================================================
log_step "步骤 3/6：安装 NVIDIA 驱动"

# 检查是否已有驱动
if nvidia-smi &>/dev/null; then
    log_warn "NVIDIA 驱动已安装，跳过"
    nvidia-smi
else
    log_info "安装 nvidia-driver-535..."
    sudo apt install -y nvidia-driver-535
    log_info "NVIDIA 驱动安装完成"
    log_warn "重启后生效"
fi

# ============================================================================
# 4. 安装 Miniconda（Isaac Sim 需要 Conda 管理 Python 版本）
# ============================================================================
log_step "步骤 4/6：安装 Miniconda"

CONDA_DIR="$HOME/miniconda3"
if [ -d "$CONDA_DIR" ]; then
    log_warn "Miniconda 已安装，跳过"
else
    log_info "下载 Miniconda..."
    wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
    
    log_info "安装 Miniconda..."
    bash /tmp/miniconda.sh -b -p "$CONDA_DIR"
    rm /tmp/miniconda.sh
    
    # 初始化 conda
    "$CONDA_DIR/bin/conda" init bash
    log_info "Miniconda 安装完成"
fi

# ============================================================================
# 5. 配置 Git
# ============================================================================
log_step "步骤 5/6：配置 Git"

# 设置全局配置
git config --global user.name "jl"
git config --global user.email "jianglei@openloong.net"
git config --global init.defaultBranch main
git config --global pull.rebase true
git config --global push.autoSetupRemote true

# 配置 credential helper
git config --global credential.helper store

# 配置 .gitignore
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

log_info "Git 配置完成"

# ============================================================================
# 6. 创建项目目录结构
# ============================================================================
log_step "步骤 6/6：创建目录结构"

mkdir -p ~/projects/{ai,web,scripts,docs,data}
mkdir -p ~/data/{raw,processed,models,logs}
mkdir -p ~/backups
mkdir -p ~/venvs

log_info "目录结构创建完成"

# ============================================================================
# 完成总结
# ============================================================================
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}    第一阶段安装完成！${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "${YELLOW}下一步操作：${NC}"
echo "1. 重启系统：sudo reboot"
echo "2. 重启后运行第二阶段脚本："
echo "   cd ~/文档/RobotMind/scripts"
echo "   chmod +x setup-phase2.sh"
echo "   ./setup-phase2.sh"
echo ""
echo -e "${YELLOW}验证命令（重启后）：${NC}"
echo "  nvidia-smi              # 检查 NVIDIA 驱动"
echo "  conda --version         # 检查 Conda"
echo "  cmake --version         # 检查 CMake"
echo ""
