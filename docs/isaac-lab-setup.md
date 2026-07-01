# Isaac Lab 环境配置指南

## 系统要求

### 硬件要求
| 组件       | 最低要求              | 推荐配置               |
|------------|----------------------|------------------------|
| GPU        | NVIDIA RTX 2070      | NVIDIA RTX 3080/4080   |
| RAM        | 16 GB                | 32 GB 或更高            |
| 存储空间   | 50 GB 可用空间        | 100 GB 或更高 (SSD)    |
| CPU        | 6 核                  | 8 核或更高              |

### 软件要求
| 软件         | 版本要求               |
|--------------|------------------------|
| 操作系统     | Ubuntu 22.04 LTS       |
| NVIDIA 驱动  | 525.60.13 或更高       |
| CUDA Toolkit | 12.x                   |
| cuDNN        | 8.x                    |
| Python       | 3.8 或更高             |

---

## 安装步骤

### 1. 环境准备

#### 安装 NVIDIA 驱动
```bash
sudo apt update
sudo apt install nvidia-driver-535
sudo reboot
```

#### 验证 GPU 状态
```bash
nvidia-smi
```

### 2. 安装 CUDA Toolkit

```bash
wget https://developer.download.nvidia.com/compute/cuda/12.2.0/local_installers/cuda_12.2.0_535.54.03_linux.run
sudo sh cuda_12.2.0_535.54.03_linux.run
```

配置环境变量 (添加到 `~/.bashrc`):
```bash
export CUDA_HOME=/usr/local/cuda-12.2
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
```

```bash
source ~/.bashrc
nvcc --version
```

### 3. 使用安装脚本

```bash
chmod +x scripts/setup-isaac-lab.sh
./scripts/setup-isaac-lab.sh
```

### 4. 手动安装 (可选)

#### 克隆 Isaac Lab
```bash
git clone https://github.com/isaac-sim/IsaacLab.git ~/isaac-lab
cd ~/isaac-lab
```

#### 安装
```bash
./isaaclab.sh --install
```

---

## 使用方法

### 启动 Isaac Sim
```bash
source ~/isaac-lab/setup_python_env.sh
isaacsim
```

### 运行示例
```bash
cd ~/isaac-lab/source/isaaclab_examples
python anymal_c_flatterrain.py
```

### 常用命令
| 命令                                         | 说明               |
|----------------------------------------------|--------------------|
| `./isaaclab.sh --install`                     | 安装 Isaac Lab     |
| `./isaaclab.sh --sim`                         | 启动仿真器         |
| `python <script>.py`                          | 运行示例脚本       |

---

## 常见问题

### Q1: 安装过程中出现 CUDA 版本不兼容
确保安装的 CUDA Toolkit 版本与 Isaac Sim 支持的版本一致 (CUDA 12.x)。

### Q2: 无法检测到 GPU
- 确认已安装正确的 NVIDIA 驱动
- 运行 `nvidia-smi` 确认驱动正常
- 检查 CUDA 是否正确配置

### Q3: 内存不足 (Out of Memory)
- 降低场景复杂度
- 减少并行实体数量
- 使用 `--headless` 模式运行

### Q4: 虚拟环境激活失败
确认已安装 `python3.8-venv`：
```bash
sudo apt install python3.8-venv
```

---

## 开发建议

### 1. 项目结构
```
your-project/
├── scripts/          # 脚本文件
├── src/              # 源代码
├── configs/          # 配置文件
└── docs/             # 文档
```

### 2. 版本控制
- 使用 Git 管理项目
- 定期备份重要配置
- 使用 `.gitignore` 排除临时文件

### 3. 性能优化
- 使用 GPU 加速训练
- 合理分配资源
- 监控显存使用

### 4. 调试技巧
- 使用 `--headless` 模式进行无界面调试
- 查看日志定位问题
- 使用 Python debugger 进行断点调试
