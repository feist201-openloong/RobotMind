#!/bin/bash
# ============================================================================
# 第三阶段：Isaac Lab + Unitree G1 环境（今晚自动执行）
# 目标：配置仿真环境，为明天运行 G1 机器人代码做准备
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
# 0. 环境检查
# ============================================================================
log_step "环境检查"

# 激活 conda
source ~/miniconda3/etc/profile.d/conda.sh

# 检查 GPU
if ! nvidia-smi &>/dev/null; then
    log_error "NVIDIA 驱动未加载"
fi
log_info "GPU 状态："
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv

# 检查 CUDA
if ! nvcc --version &>/dev/null; then
    log_error "CUDA 未安装"
fi
log_info "CUDA 已安装"

# ============================================================================
# 1. 下载 Isaac Lab
# ============================================================================
log_step "步骤 1/5：下载 Isaac Lab"

ISAAC_LAB_DIR="$HOME/isaac-lab"
if [ -d "$ISAAC_LAB_DIR" ]; then
    log_warn "Isaac Lab 目录已存在，跳过下载"
else
    log_info "克隆 Isaac Lab..."
    git clone https://github.com/isaac-sim/IsaacLab.git "$ISAAC_LAB_DIR"
    log_info "Isaac Lab 下载完成"
fi

# ============================================================================
# 2. 安装 Isaac Sim（二进制方式，避免 GLIBC 问题）
# ============================================================================
log_step "步骤 2/5：安装 Isaac Sim"

ISAAC_SIM_DIR="$HOME/.local/share/ov/pkg/isaac-sim-4.0.0"
if [ -d "$ISAAC_SIM_DIR" ]; then
    log_warn "Isaac Sim 已安装，跳过"
else
    log_info "Isaac Sim 需要手动下载："
    echo "1. 访问 https://developer.nvidia.com/isaac-sim"
    echo "2. 下载 Isaac Sim 4.0.0 (Linux)"
    echo "3. 解压到 $ISAAC_SIM_DIR"
    echo "4. 运行 postinstall 脚本"
    echo ""
    log_warn "由于许可证要求，Isaac Sim 无法自动下载"
    log_warn "请手动完成此步骤"
fi

# ============================================================================
# 3. 安装强化学习库
# ============================================================================
log_step "步骤 3/5：安装强化学习库"

conda activate isaac-lab 2>/dev/null || true

log_info "安装 PyTorch..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

log_info "安装强化学习库..."
pip install stable-baselines3
pip install gymnasium
pip install rl-games
pip install rsl-rl

log_info "安装机器人相关库..."
pip install robomimic
pip install pin  # Pinocchio 机器人动力学库

log_info "强化学习库安装完成"

# ============================================================================
# 4. 安装 Unitree SDK
# ============================================================================
log_step "步骤 4/5：安装 Unitree SDK"

log_info "安装 unitree_sdk2..."
pip install unitree-sdk2 2>/dev/null || {
    log_warn "unitree-sdk2 未在 PyPI 上，尝试从 GitHub 安装"
    if [ ! -d "/tmp/unitree_sdk2" ]; then
        git clone https://github.com/unitreerobotics/unitree_sdk2.git /tmp/unitree_sdk2
    fi
    cd /tmp/unitree_sdk2
    pip install -e .
    cd -
}

# 安装 unitree_gym（G1 仿真环境）
log_info "安装 unitree_gym..."
pip install unitree-gym 2>/dev/null || {
    log_warn "尝试从 GitHub 安装 unitree_gym"
    git clone https://github.com/unitreerobotics/unitree_gym.git /tmp/unitree_gym 2>/dev/null || true
    if [ -d "/tmp/unitree_gym" ]; then
        pip install -e /tmp/unitree_gym
    fi
}

log_info "Unitree SDK 安装完成"

# ============================================================================
# 5. 配置 G1 仿真环境
# ============================================================================
log_step "步骤 5/5：配置 G1 仿真环境"

# 创建 G1 工作目录
mkdir -p ~/projects/ai/unitree-g1
cd ~/projects/ai/unitree-g1

# 下载 G1 示例代码
if [ ! -d "unitree_g1_example" ]; then
    log_info "下载 G1 示例代码..."
    git clone https://github.com/unitreerobotics/unitree_g1_example.git 2>/dev/null || {
        log_warn "无法克隆示例代码，请手动下载"
    }
fi

# 创建测试脚本
cat > ~/projects/ai/unitree-g1/test_g1.py << 'PYEOF'
#!/usr/bin/env python3
"""
Unitree G1 人形机器人测试脚本
用于验证仿真环境是否正确配置
"""

import sys
print(f"Python 版本: {sys.version}")
print(f"Python 路径: {sys.executable}")

# 测试 PyTorch + CUDA
try:
    import torch
    print(f"\nPyTorch 版本: {torch.__version__}")
    print(f"CUDA 可用: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA 版本: {torch.version.cuda}")
        print(f"GPU 设备: {torch.cuda.get_device_name(0)}")
        print(f"GPU 显存: {torch.cuda.get_device_properties(0).total_mem / 1024**3:.1f} GB")
except ImportError as e:
    print(f"PyTorch 导入失败: {e}")

# 测试 Gymnasium
try:
    import gymnasium as gym
    print(f"\nGymnasium 版本: {gym.__version__}")
except ImportError as e:
    print(f"Gymnasium 导入失败: {e}")

# 测试 Stable-Baselines3
try:
    import stable_baselines3 as sb3
    print(f"Stable-Baselines3 版本: {sb3.__version__}")
except ImportError as e:
    print(f"Stable-Baselines3 导入失败: {e}")

# 测试 Unitree 相关
try:
    import unitree_sdk2
    print(f"\nUnitree SDK2: 已安装")
except ImportError as e:
    print(f"\nUnitree SDK2: 未安装 ({e})")

try:
    import unitree_gym
    print(f"Unitree Gym: 已安装")
except ImportError as e:
    print(f"Unitree Gym: 未安装 ({e})")

print("\n" + "="*50)
print("环境测试完成！")
print("="*50)
PYEOF

chmod +x ~/projects/ai/unitree-g1/test_g1.py
log_info "测试脚本创建完成"

# ============================================================================
# 完成总结
# ============================================================================
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}    Isaac Lab + Unitree G1 环境配置完成！${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "${YELLOW}下一步操作：${NC}"
echo ""
echo "1. 运行环境测试："
echo "   conda activate isaac-lab"
echo "   python ~/projects/ai/unitree-g1/test_g1.py"
echo ""
echo "2. 手动安装 Isaac Sim（如未安装）："
echo "   下载地址: https://developer.nvidia.com/isaac-sim"
echo ""
echo "3. 启动 Isaac Lab："
echo "   cd ~/isaac-lab"
echo "   ./isaaclab.sh --gui"
echo ""
echo -e "${YELLOW}明日目标：运行 G1 机器人仿真${NC}"
echo ""
