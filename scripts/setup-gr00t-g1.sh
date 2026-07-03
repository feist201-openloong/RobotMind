#!/bin/bash
# ============================================================================
# GR00T N1.7 + GEAR-SONIC 完整安装脚本
# 目标：让 Unitree G1 人形机器人从走到跑
# ============================================================================

set -e

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
# 1. 安装 uv（GR00T 依赖管理工具）
# ============================================================================
log_step "步骤 1/8：安装 uv"

if command -v uv &>/dev/null; then
    log_warn "uv 已安装: $(uv --version)"
else
    log_info "安装 uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

log_info "uv 版本: $(uv --version)"

# ============================================================================
# 2. 安装 FFmpeg（torchcodec 视频解码必需）
# ============================================================================
log_step "步骤 2/8：安装 FFmpeg"

if command -v ffmpeg &>/dev/null; then
    log_warn "FFmpeg 已安装"
else
    sudo apt-get update && sudo apt-get install -y ffmpeg
fi

log_info "FFmpeg 版本: $(ffmpeg -version 2>&1 | head -1)"

# ============================================================================
# 3. 克隆 GR00T N1.7 仓库
# ============================================================================
log_step "步骤 3/8：克隆 GR00T N1.7"

GR00T_DIR="$HOME/Isaac-GR00T"
if [ -d "$GR00T_DIR" ]; then
    log_warn "GR00T 目录已存在，拉取最新"
    cd "$GR00T_DIR" && git pull
else
    log_info "克隆 GR00T N1.7（含子模块）..."
    git clone --recurse-submodules https://github.com/NVIDIA/Isaac-GR00T.git "$GR00T_DIR"
fi

cd "$GR00T_DIR"
git lfs pull
log_info "GR00T 下载完成"

# ============================================================================
# 4. 克隆 GR00T-WholeBodyControl（SONIC 控制器）
# ============================================================================
log_step "步骤 4/8：克隆 GEAR-SONIC"

WBC_DIR="$HOME/GR00T-WholeBodyControl"
if [ -d "$WBC_DIR" ]; then
    log_warn "WBC 目录已存在，拉取最新"
    cd "$WBC_DIR" && git pull
else
    log_info "克隆 GEAR-SONIC..."
    git clone https://github.com/NVlabs/GR00T-WholeBodyControl.git "$WBC_DIR"
fi

cd "$WBC_DIR"
git lfs pull
log_info "GEAR-SONIC 下载完成"

# ============================================================================
# 5. 安装 GR00T N1.7 环境
# ============================================================================
log_step "步骤 5/8：安装 GR00T N1.7 环境"

cd "$GR00T_DIR"

log_info "创建 GR00T 虚拟环境..."
uv sync --python 3.10

log_info "验证 GR00T 安装..."
uv run python -c "import gr00t; print('GR00T N1.7 安装成功')"

log_info "GR00T 环境安装完成"

# ============================================================================
# 6. 安装 GEAR-SONIC MuJoCo 仿真环境
# ============================================================================
log_step "步骤 6/8：安装 SONIC 仿真环境"

cd "$WBC_DIR"

log_info "安装 MuJoCo 仿真环境..."
bash install_scripts/install_mujoco_sim.sh

log_info "SONIC 仿真环境安装完成"

# ============================================================================
# 7. 下载 SONIC 预训练模型
# ============================================================================
log_step "步骤 7/8：下载 SONIC 预训练模型"

cd "$WBC_DIR"

log_info "下载 SONIC 模型..."
python download_from_hf.py

log_info "下载低延迟 SONIC 变体..."
python download_from_hf.py --low-latency

log_info "SONIC 模型下载完成"

# ============================================================================
# 8. 下载 GR00T N1.7 基础模型
# ============================================================================
log_step "步骤 8/8：下载 GR00T N1.7 基础模型"

cd "$GR00T_DIR"

log_info "下载 GR00T N1.7-3B 基础模型（约 6GB）..."
uv run python -c "
from huggingface_hub import snapshot_download
snapshot_download('nvidia/GR00T-N1.7-3B')
print('GR00T N1.7-3B 下载完成')
"

log_info "所有模型下载完成"

# ============================================================================
# 创建 G1 快速启动脚本
# ============================================================================
log_step "创建快速启动脚本"

cat > ~/projects/ai/unitree-g1/start_g1_locomotion.sh << 'LAUNCHEOF'
#!/bin/bash
# ============================================================================
# Unitree G1 运动控制快速启动脚本
# ============================================================================

echo "============================================"
echo "  Unitree G1 运动控制"
echo "============================================"
echo ""
echo "选择模式："
echo "1. SONIC 键盘控制（走/跑/跳）"
echo "2. SONIC 游戏手柄控制"
echo "3. GR00T N1.7 推理演示"
echo "4. MuJoCo 仿真演示"
echo ""
read -p "请选择 (1-4): " choice

case $choice in
    1)
        echo "启动 SONIC 键盘控制..."
        cd ~/GR00T-WholeBodyControl
        source .venv_sim/bin/activate
        python gear_sonic/scripts/launch_inference.py \
            --deploy-checkpoint policy/model \
            --deploy-obs-config policy/observation_config.yaml \
            --input-type keyboard_manager
        ;;
    2)
        echo "启动 SONIC 游戏手柄控制..."
        cd ~/GR00T-WholeBodyControl
        source .venv_sim/bin/activate
        python gear_sonic/scripts/launch_inference.py \
            --deploy-checkpoint policy/model \
            --deploy-obs-config policy/observation_config.yaml \
            --input-type zmq_manager
        ;;
    3)
        echo "启动 GR00T N1.7 推理演示..."
        cd ~/Isaac-GR00T
        uv run python scripts/deployment/standalone_inference_script.py \
            --model-path nvidia/GR00T-N1.7-3B \
            --dataset-path demo_data/droid_sample \
            --embodiment-tag OXE_DROID_RELATIVE_EEF_RELATIVE_JOINT \
            --traj-ids 1 2 \
            --inference-mode pytorch \
            --action-horizon 8
        ;;
    4)
        echo "启动 MuJoCo 仿真..."
        cd ~/GR00T-WholeBodyControl
        source .venv_sim/bin/activate
        python gear_sonic/scripts/launch_inference.py \
            --deploy-checkpoint policy/model \
            --deploy-obs-config policy/observation_config.yaml \
            --sim mujoco
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac
LAUNCHEOF

chmod +x ~/projects/ai/unitree-g1/start_g1_locomotion.sh

# ============================================================================
# 创建 G1 走到跑的训练脚本
# ============================================================================

cat > ~/projects/ai/unitree-g1/g1_walk_to_run.sh << 'TRAINEOF'
#!/bin/bash
# ============================================================================
# G1 从走到跑 - 训练流程
# ============================================================================

echo "============================================"
echo "  G1 从走到跑 - 训练流程"
echo "============================================"
echo ""
echo "阶段 1: 使用预训练 SONIC 模型走"
echo "阶段 2: 微调 SONIC 模型以支持跑步"
echo "阶段 3: 使用 GR00T N1.7 进行全身控制"
echo ""

WBC_DIR="$HOME/GR00T-WholeBodyControl"
cd "$WBC_DIR"

# 激活仿真环境
source .venv_sim/bin/activate

echo "阶段 1: 测试预训练 SONIC 走路能力..."
echo "按 Ctrl+C 退出"
echo ""

python gear_sonic/scripts/launch_inference.py \
    --deploy-checkpoint policy/model \
    --deploy-obs-config policy/observation_config.yaml \
    --input-type keyboard_manager

TRAINEOF

chmod +x ~/projects/ai/unitree-g1/g1_walk_to_run.sh

# ============================================================================
# 完成总结
# ============================================================================
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}    GR00T N1.7 + GEAR-SONIC 安装完成！${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "${YELLOW}安装路径：${NC}"
echo "  GR00T N1.7:        $GR00T_DIR"
echo "  GEAR-SONIC:        $WBC_DIR"
echo "  G1 启动脚本:       ~/projects/ai/unitree-g1/start_g1_locomotion.sh"
echo "  G1 走到跑脚本:     ~/projects/ai/unitree-g1/g1_walk_to_run.sh"
echo ""
echo -e "${YELLOW}快速启动：${NC}"
echo "  # 走路测试"
echo "  cd ~/GR00T-WholeBodyControl"
echo "  source .venv_sim/bin/activate"
echo "  python gear_sonic/scripts/launch_inference.py \\"
echo "      --deploy-checkpoint policy/model \\"
echo "      --deploy-obs-config policy/observation_config.yaml \\"
echo "      --input-type keyboard_manager"
echo ""
echo -e "${YELLOW}GR00T N1.7 推理：${NC}"
echo "  cd ~/Isaac-GR00T"
echo "  uv run python scripts/deployment/standalone_inference_script.py \\"
echo "      --model-path nvidia/GR00T-N1.7-3B \\"
echo "      --dataset-path demo_data/droid_sample \\"
echo "      --embodiment-tag OXE_DROID_RELATIVE_EEF_RELATIVE_JOINT \\"
echo "      --traj-ids 1 2 \\"
echo "      --inference-mode pytorch \\"
echo "      --action-horizon 8"
echo ""
echo -e "${YELLOW}SONIC 支持的动作：${NC}"
echo "  - 走路（平地、崎岖地形）"
echo "  - 跑步"
echo "  - 侧向移动"
echo "  - 跳跃"
echo "  - 蹲下/起立"
echo "  - 爬行"
echo "  - 双臂操作"
echo ""
