# Unitree G1 从走到跑 - 完整指南

## 概述

本指南将帮助您使用 NVIDIA GR00T N1.7 和 GEAR-SONIC 控制器，让 Unitree G1 人形机器人实现从走路到跑步的运动能力。

## 技术栈

```
┌─────────────────────────────────────────────────────────┐
│                    GR00T N1.7                           │
│              视觉-语言-动作模型 (VLA)                    │
│         输入：图像 + 语言指令 + 机器人状态               │
│         输出：动作 token                                │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                  GEAR-SONIC                             │
│              全身运动控制器                              │
│         输入：动作 token                                │
│         输出：全身关节命令（腿、臂、手）                  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                 Unitree G1                              │
│              29 个自由度人形机器人                        │
└─────────────────────────────────────────────────────────┘
```

## 安装步骤

### 1. 前置条件

```bash
# 确保已安装
- NVIDIA 驱动 535+
- CUDA 12.2+
- Docker + NVIDIA Container Toolkit
- Python 3.10
- Git LFS
- FFmpeg
```

### 2. 安装 GR00T N1.7

```bash
cd ~
git clone --recurse-submodules https://github.com/NVIDIA/Isaac-GR00T.git
cd Isaac-GR00T
git lfs pull

# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# 安装依赖
uv sync --python 3.10

# 验证
uv run python -c "import gr00t; print('GR00T N1.7 安装成功')"
```

### 3. 安装 GEAR-SONIC

```bash
cd ~
git clone https://github.com/NVlabs/GR00T-WholeBodyControl.git
cd GR00T-WholeBodyControl
git lfs pull

# 安装 MuJoCo 仿真环境
bash install_scripts/install_mujoco_sim.sh

# 下载预训练模型
python download_from_hf.py
python download_from_hf.py --low-latency
```

### 4. 下载 GR00T N1.7 基础模型

```bash
cd ~/Isaac-GR00T
uv run python -c "
from huggingface_hub import snapshot_download
snapshot_download('nvidia/GR00T-N1.7-3B')
"
```

## 使用方法

### 方法 1: SONIC 键盘控制（推荐入门）

```bash
cd ~/GR00T-WholeBodyControl
source .venv_sim/bin/activate

python gear_sonic/scripts/launch_inference.py \
    --deploy-checkpoint policy/model \
    --deploy-obs-config policy/observation_config.yaml \
    --input-type keyboard_manager
```

**键盘控制：**
- W/S: 前进/后退
- A/D: 左转/右转
- ↑/↓: 加速/减速
- Space: 跳跃
- Shift: 跑步模式

### 方法 2: 游戏手柄控制

```bash
cd ~/GR00T-WholeBodyControl
source .venv_sim/bin/activate

python gear_sonic/scripts/launch_inference.py \
    --deploy-checkpoint policy/model \
    --deploy-obs-config policy/observation_config.yaml \
    --input-type zmq_manager
```

### 方法 3: 语言指令控制（GR00T N1.7 + SONIC）

```bash
cd ~/GR00T-WholeBodyControl
source .venv_sim/bin/activate

python gear_sonic/scripts/launch_inference.py \
    --deploy-checkpoint policy/low_latency/model \
    --deploy-obs-config policy/low_latency/observation_config.yaml \
    --camera-host 192.168.123.164 \
    --prompt "walk forward slowly"
```

**支持的语言指令：**
- "walk forward" - 前进
- "run fast" - 快跑
- "walk sideways" - 侧向移动
- "jump" - 跳跃
- "kneel down" - 蹲下
- "get up" - 起立
- "crawl" - 爬行

### 方法 4: MuJoCo 仿真

```bash
cd ~/GR00T-WholeBodyControl
source .venv_sim/bin/activate

python gear_sonic/scripts/launch_inference.py \
    --deploy-checkpoint policy/model \
    --deploy-obs-config policy/observation_config.yaml \
    --sim mujoco
```

## G1 运动能力

SONIC 支持的 G1 运动：

| 运动类型 | 说明 | 难度 |
|----------|------|------|
| 平地行走 | 基础走路能力 | ★☆☆ |
| 崎岖地形 | 在不平坦地面行走 | ★★☆ |
| 跑步 | 快速前进 | ★★☆ |
| 侧向移动 | 横向移动 | ★★☆ |
| 跳跃 | 离地跳起 | ★★★ |
| 蹲下/起立 | 姿态变换 | ★★☆ |
| 爬行 | 低姿态移动 | ★★★ |
| 双臂操作 | 手臂协调动作 | ★★★ |

## 从走到跑的训练流程

### 阶段 1: 基础行走（预训练）

使用 SONIC 预训练模型，G1 已经具备基础行走能力。

### 阶段 2: 微调跑步能力

```bash
# 下载 Bones-SEED 运动数据
# 包含 142K+ 人类运动，约 288 小时

cd ~/GR00T-WholeBodyControl
source .venv_sim/bin/activate

# 转换运动数据
python gear_sonic/data_process/convert_soma_csv_to_motion_lib.py \
    --input /path/to/bones_seed/g1/csv/ \
    --output data/motion_lib_bones_seed/robot \
    --fps 30 --fps_source 120 --individual --num_workers 16

# 过滤数据
python gear_sonic/data_process/filter_and_copy_bones_data.py \
    --source data/motion_lib_bones_seed/robot \
    --dest data/motion_lib_bones_seed/robot_filtered

# 微调（需要 64+ GPU）
accelerate launch --num_processes=8 gear_sonic/train_agent_trl.py \
    +exp=manager/universal_token/all_modes/sonic_release \
    +checkpoint=sonic_release/last.pt \
    num_envs=4096 headless=True \
    ++manager_env.commands.motion.motion_lib_cfg.motion_file=data/motion_lib_bones_seed/robot_filtered \
    ++manager_env.commands.motion.motion_lib_cfg.smpl_motion_file=data/smpl_filtered
```

### 阶段 3: GR00T N1.7 全身控制

```bash
cd ~/Isaac-GR00T

# 使用 GR00T N1.7 进行推理
uv run python scripts/deployment/standalone_inference_script.py \
    --model-path nvidia/GR00T-N1.7-3B \
    --dataset-path demo_data/droid_sample \
    --embodiment-tag OXE_DROID_RELATIVE_EEF_RELATIVE_JOINT \
    --traj-ids 1 2 \
    --inference-mode pytorch \
    --action-horizon 8
```

## 故障排除

### 问题 1: SONIC 模型加载失败

```bash
# 检查模型文件
ls -la ~/GR00T-WholeBodyControl/policy/model/

# 重新下载
cd ~/GR00T-WholeBodyControl
python download_from_hf.py --force
```

### 问题 2: MuJoCo 仿真启动失败

```bash
# 检查 MuJoCo 安装
cd ~/GR00T-WholeBodyControl
source .venv_sim/bin/activate
python -c "import mujoco; print('MuJoCo 版本:', mujoco.__version__)"

# 重新安装
bash install_scripts/install_mujoco_sim.sh --force
```

### 问题 3: GR00T N1.7 GPU 内存不足

```bash
# RTX 4070 12GB 可能需要降低精度
cd ~/Isaac-GR00T
uv run python scripts/deployment/standalone_inference_script.py \
    --model-path nvidia/GR00T-N1.7-3B \
    --dataset-path demo_data/droid_sample \
    --embodiment-tag OXE_DROID_RELATIVE_EEF_RELATIVE_JOINT \
    --traj-ids 1 \
    --inference-mode pytorch \
    --action-horizon 4 \
    --device cpu  # 降级到 CPU（慢但可用）
```

### 问题 4: 键盘控制无响应

```bash
# 检查 pygame 安装
cd ~/GR00T-WholeBodyControl
source .venv_sim/bin/activate
pip install pygame

# 确保在终端中运行（非 SSH）
# 或使用 X11 转发
```

## 参考资源

- [GR00T N1.7 文档](https://developer.nvidia.com/isaac/gr00t)
- [GEAR-SONIC 文档](https://nvlabs.github.io/GR00T-WholeBodyControl/)
- [Unitree G1 官方文档](https://www.unitree.com/g1/)
- [Isaac Lab 文档](https://isaac-sim.github.io/IsaacLab/)

## 许可证

- **代码**: Apache 2.0
- **模型权重**: NVIDIA Open Model License（商业使用需授权）

---

*最后更新: 2026-07-02*
