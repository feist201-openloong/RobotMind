# GR00T N1.7 + GEAR-SONIC + Unitree G1 完整安装指南

> 最后更新: 2026-07-03
> 环境: Ubuntu 22.04 LTS + NVIDIA RTX 4070 12GB

## 目录

1. [硬件要求](#1-硬件要求)
2. [系统基础环境](#2-系统基础环境)
3. [NVIDIA 驱动与 CUDA](#3-nvidia-驱动与-cuda)
4. [Python 环境配置](#4-python-环境配置)
5. [GR00T N1.7 安装](#5-gr00t-n17-安装)
6. [HuggingFace 认证配置](#6-huggingface-认证配置)
7. [GR00T N1.7 推理测试](#7-gr00t-n17-推理测试)
8. [GEAR-SONIC 仿真环境安装](#8-gear-sonic-仿真环境安装)
9. [G1 MuJoCo 仿真运行](#9-g1-mujoco-仿真运行)
10. [常见问题排查](#10-常见问题排查)

---

## 1. 硬件要求

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| GPU | RTX 4070 12GB | RTX 4090 24GB / H100 |
| 内存 | 16GB | 32GB+ |
| 存储 | 100GB 可用空间 | 200GB+ SSD |
| 网络 | 需要代理访问外网 | 稳定代理连接 |

---

## 2. 系统基础环境

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础工具
sudo apt install -y \
    curl wget git vim htop net-tools \
    build-essential cmake \
    software-properties-common \
    apt-transport-https ca-certificates \
    gnupg lsb-release unzip zip tree jq ffmpeg
```

---

## 3. NVIDIA 驱动与 CUDA

### 3.1 安装 NVIDIA 驱动

```bash
# 安装驱动（推荐 535+）
sudo apt install -y nvidia-driver-535

# 重启后验证
nvidia-smi
```

### 3.2 安装 CUDA 12.2

```bash
# 下载 CUDA 密钥包
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update

# 安装 CUDA
sudo apt install -y cuda-toolkit-12-2

# 配置环境变量
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# 验证
nvcc --version
```

### 3.3 安装 Docker + NVIDIA Container Toolkit

```bash
# 安装 Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER

# 安装 NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

---

## 4. Python 环境配置

### 4.1 安装 Miniconda

```bash
# 下载安装
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
bash /tmp/miniconda.sh -b -p ~/miniconda3
rm /tmp/miniconda.sh

# 初始化
~/miniconda3/bin/conda init bash
source ~/.bashrc
```

### 4.2 创建 Isaac Lab 环境

```bash
# 创建 Python 3.10 环境
conda create -n isaac-lab python=3.10 -y
conda activate isaac-lab

# 安装 PyTorch（CUDA 12.1）
pip install torch==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cu121

# 验证
python -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
```

---

## 5. GR00T N1.7 安装

### 5.1 克隆仓库

```bash
cd ~
git clone --recurse-submodules https://github.com/NVIDIA/Isaac-GR00T.git
cd Isaac-GR00T
git lfs pull
```

### 5.2 安装依赖

```bash
# 激活环境
conda activate isaac-lab

# 使用清华镜像安装依赖（解决代理 SSL 问题）
pip install --trusted-host pypi.tuna.tsinghua.edu.cn \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    transformers==4.57.3 safetensors huggingface_hub pydantic \
    einops peft diffusers datasets pyzmq \
    albumentations dm-tree termcolor tyro click \
    jsonlines gymnasium matplotlib omegaconf scipy wandb \
    onnx onnxscript torchcodec==0.4.0

# 将 gr00t 添加到 Python 路径
export PYTHONPATH="$PWD:$PYTHONPATH"
echo 'export PYTHONPATH="$HOME/Isaac-GR00T:$PYTHONPATH"' >> ~/.bashrc
```

### 5.3 验证安装

```bash
python -c "
from gr00t.model import Gr00tN1d7Pipeline
print('GR00T N1.7 核心组件加载成功！')
"
```

---

## 6. HuggingFace 认证配置

### 6.1 申请访问权限

GR00T N1.7 依赖的 `nvidia/Cosmos-Reason2-2B` 是受限模型，需要：

1. 注册/登录 [HuggingFace](https://huggingface.co)
2. 访问 [nvidia/Cosmos-Reason2-2B](https://huggingface.co/nvidia/Cosmos-Reason2-2B)
3. 点击 "Request access" 申请访问权限
4. 等待批准（通常几分钟到几小时）

### 6.2 创建 Token

1. 访问 https://huggingface.co/settings/tokens
2. 创建新 Token
3. **重要**：在权限设置中启用 **"Access public gated repos"**

### 6.3 登录 CLI

```bash
# 设置代理（如需要）
export http_proxy=http://127.0.0.1:7897
export https_proxy=http://127.0.0.1:7897

# 登录
python -m huggingface_hub.commands.huggingface_cli login
# 输入 Token
```

### 6.4 验证访问

```bash
python -c "
from huggingface_hub import hf_hub_download
path = hf_hub_download(
    repo_id='nvidia/Cosmos-Reason2-2B',
    filename='config.json',
    cache_dir='/tmp/hf_test'
)
print(f'访问成功: {path}')
"
```

---

## 7. GR00T N1.7 推理测试

```bash
cd ~/Isaac-GR00T

# 运行推理测试
python scripts/deployment/standalone_inference_script.py \
    --model-path nvidia/GR00T-N1.7-3B \
    --dataset-path demo_data/droid_sample \
    --embodiment-tag OXE_DROID_RELATIVE_EEF_RELATIVE_JOINT \
    --traj-ids 1 \
    --inference-mode pytorch \
    --action-horizon 8
```

**预期输出**：
- 模型加载时间约 20-30 秒
- 推理速度约 6 FPS（RTX 4070）
- MSE < 0.01

---

## 8. GEAR-SONIC 仿真环境安装

### 8.1 克隆仓库

```bash
cd ~
git clone https://github.com/NVlabs/GR00T-WholeBodyControl.git
cd GR00T-WholeBodyControl
git lfs pull
```

### 8.2 安装 MuJoCo 仿真环境

```bash
# 使用项目提供的安装脚本
bash install_scripts/install_mujoco_sim.sh

# 手动安装额外依赖
export PATH="$HOME/.local/bin:$PATH"
uv pip install --python .venv_sim/bin/python \
    onnxruntime-gpu pynput pyyaml
```

### 8.3 下载 SONIC 模型

```bash
# 下载预训练模型
.venv_sim/bin/python download_from_hf.py

# 下载低延迟版本（可选）
.venv_sim/bin/python download_from_hf.py --low-latency
```

---

## 9. G1 MuJoCo 仿真运行

### 9.1 修改配置文件

编辑 `decoupled_wbc/sim2mujoco/resources/robots/g1/g1_gear_wbc.yaml`：

```yaml
# 修改模型路径
policy_path: "policy/GR00T-WholeBodyControl-Balance.onnx"
walk_policy_path: "policy/GR00T-WholeBodyControl-Walk.onnx"
```

### 9.2 启动仿真

```bash
cd ~/GR00T-WholeBodyControl/decoupled_wbc/sim2mujoco

# 启动仿真
.venv_sim/bin/python scripts/run_mujoco_gear_wbc.py
```

### 9.3 键盘控制

| 按键 | 功能 |
|------|------|
| W | 前进 |
| S | 后退 |
| A | 左转 |
| D | 右转 |
| Q | 侧向移动（左） |
| E | 侧向移动（右） |
| Z | 重置 |
| 1/2 | 调整高度 |
| ESC | 退出 |

---

## 10. 常见问题排查

### 问题 1: 代理 SSL 连接失败

**现象**：`SSLEOFError: EOF occurred in violation of protocol`

**解决**：
```bash
# 清除代理环境变量后重新设置
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export http_proxy=http://127.0.0.1:7897
export https_proxy=http://127.0.0.1:7897
```

### 问题 2: HuggingFace 403 Forbidden

**现象**：`Cannot access gated repo`

**解决**：
1. 确认已申请 `nvidia/Cosmos-Reason2-2B` 访问权限
2. 确认 Token 已启用 "Access public gated repos" 权限
3. 重新登录：`python -m huggingface_hub.commands.huggingface_cli login`

### 问题 3: torchcodec 未安装

**现象**：`ModuleNotFoundError: No module named 'torchcodec'`

**解决**：
```bash
pip install --trusted-host pypi.tuna.tsinghua.edu.cn \
    -i https://pypi.tuna.tsinghua.edu.cn/simple torchcodec==0.4.0
```

### 问题 4: onnxruntime 未安装

**现象**：`ModuleNotFoundError: No module named 'onnxruntime'`

**解决**：
```bash
export PATH="$HOME/.local/bin:$PATH"
uv pip install --python .venv_sim/bin/python onnxruntime-gpu
```

### 问题 5: 模型文件路径错误

**现象**：`onnxruntime.capi.onnxruntime_pybind11_state.NoSuchFile`

**解决**：检查 `g1_gear_wbc.yaml` 中的模型路径是否正确

---

## 快速启动脚本

将以下内容保存为 `~/start_g1.sh`：

```bash
#!/bin/bash
# 启动 G1 MuJoCo 仿真

# 设置代理（如需要）
# export http_proxy=http://127.0.0.1:7897
# export https_proxy=http://127.0.0.1:7897

cd ~/GR00T-WholeBodyControl/decoupled_wbc/sim2mujoco
~/GR00T-WholeBodyControl/.venv_sim/bin/python scripts/run_mujoco_gear_wbc.py
```

```bash
chmod +x ~/start_g1.sh
```

---

## 参考资源

- [GR00T N1.7 GitHub](https://github.com/NVIDIA/Isaac-GR00T)
- [GR00T-WholeBodyControl GitHub](https://github.com/NVlabs/GR00T-WholeBodyControl)
- [NVIDIA Isaac 文档](https://developer.nvidia.com/isaac)
- [Unitree G1 官方文档](https://www.unitree.com/g1/)

---

*本文档基于实际安装过程编写，如有问题请提交 Issue。*
