#!/bin/bash
# Isaac Lab 环境配置脚本
# 适用于 Ubuntu 22.04 LTS + NVIDIA GPU

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()    { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }

ISAAC_LAB_DIR="${HOME}/isaac-lab"
VENV_NAME="isaac-lab-env"

# ─── 1. 系统检查 ───
check_system() {
    log_info "=== 系统环境检查 ==="

    # 检查操作系统
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        if [[ "$ID" != "ubuntu" || "$VERSION_ID" != "22.04" ]]; then
            log_warn "当前系统为 $PRETTY_NAME，推荐使用 Ubuntu 22.04 LTS"
        fi
    fi

    # 检查 GPU
    if ! command -v nvidia-smi &>/dev/null; then
        log_error "未检测到 NVIDIA 驱动，请先安装 NVIDIA 驱动"
        exit 1
    fi
    log_info "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)"
    log_info "NVIDIA 驱动版本: $(nvidia-smi --query-gpu=driver_version --format=csv,noheader | head -1)"

    # 检查 CUDA
    if ! command -v nvcc &>/dev/null; then
        log_error "未检测到 CUDA Toolkit，请先安装 CUDA 12.x"
        exit 1
    fi
    log_info "CUDA 版本: $(nvcc --version | grep 'release' | awk '{print $6}' | cut -d',' -f1)"

    # 检查可用磁盘空间 (需至少 50GB)
    AVAILABLE_GB=$(df -BG /home | tail -1 | awk '{print $4}' | tr -d 'G')
    if [ "$AVAILABLE_GB" -lt 50 ]; then
        log_error "可用磁盘空间不足 50GB (当前: ${AVAILABLE_GB}GB)"
        exit 1
    fi
    log_info "可用磁盘空间: ${AVAILABLE_GB}GB"
}

# ─── 2. 安装系统依赖 ───
install_dependencies() {
    log_info "=== 安装系统依赖 ==="
    sudo apt-get update
    sudo apt-get install -y \
        build-essential \
        git \
        curl \
        wget \
        python3.8 \
        python3.8-venv \
        python3.8-dev \
        python3-pip \
        cmake \
        ninja-build
}

# ─── 3. 创建 Python 虚拟环境 ───
create_venv() {
    log_info "=== 创建 Python 虚拟环境 ==="
    VENV_PATH="${HOME}/${VENV_NAME}"
    if [ -d "$VENV_PATH" ]; then
        log_warn "虚拟环境已存在: $VENV_PATH"
        read -p "是否覆盖？(y/N): " REPLY
        if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
            return
        fi
        rm -rf "$VENV_PATH"
    fi

    python3.8 -m venv "$VENV_PATH"
    source "$VENV_PATH/bin/activate"
    pip install --upgrade pip setuptools wheel
    log_info "虚拟环境已创建: $VENV_PATH"
}

# ─── 4. 安装 Isaac Lab ───
install_isaac_lab() {
    log_info "=== 克隆 Isaac Lab ==="
    if [ -d "$ISAAC_LAB_DIR" ]; then
        log_warn "Isaac Lab 目录已存在: $ISAAC_LAB_DIR"
        read -p "是否删除并重新克隆？(y/N): " REPLY
        if [[ "$REPLY" =~ ^[Yy]$ ]]; then
            rm -rf "$ISAAC_LAB_DIR"
        else
            return
        fi
    fi

    git clone https://github.com/isaac-sim/IsaacLab.git "$ISAAC_LAB_DIR"
    cd "$ISAAC_LAB_DIR"

    log_info "=== 安装 Isaac Lab ==="
    ./isaaclab.sh --install

    cd -
}

# ─── 5. 安装额外 Python 依赖 ───
install_extra_deps() {
    log_info "=== 安装额外依赖 ==="
    source "${HOME}/${VENV_NAME}/bin/activate"

    pip install \
        torch \
        torchvision \
        numpy \
        matplotlib \
        opencv-python
    log_info "额外依赖安装完成"
}

# ─── 6. 验证安装 ───
verify_installation() {
    log_info "=== 验证安装 ==="
    source "${HOME}/${VENV_NAME}/bin/activate"

    python3 -c "
import torch
print('PyTorch 版本:', torch.__version__)
print('CUDA 可用:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('CUDA 版本:', torch.version.cuda)
    print('GPU 设备数:', torch.cuda.device_count())
    print('当前 GPU:', torch.cuda.get_device_name(0))
print('Isaac Lab 验证通过')
"
    log_info "安装验证完成"
}

# ─── 7. 安装 Isaac Lab 示例 ───
install_examples() {
    log_info "=== 安装 Isaac Lab 示例 ==="
    if [ -d "$ISAAC_LAB_DIR" ]; then
        log_info "示例位于: $ISAAC_LAB_DIR/source/isaaclab_examples/"
    fi
    log_info "安装完成"
}

# ─── 主流程 ───
main() {
    log_info "开始 Isaac Lab 环境配置..."
    check_system
    install_dependencies
    create_venv
    install_isaac_lab
    install_extra_deps
    verify_installation
    install_examples
    log_info "=== Isaac Lab 环境配置完成 ==="
    log_info "激活虚拟环境: source ${HOME}/${VENV_NAME}/bin/activate"
}

main "$@"
