# 环境配置文档

## 目录

- [服务器环境配置](#服务器环境配置)
- [MacBook环境配置](#macbook环境配置)
- [远程连接配置](#远程连接配置)
- [常见问题解答](#常见问题解答)

---

## 服务器环境配置

### 概述

本文档描述如何配置Ubuntu 22.04 LTS GPU服务器的开发环境。

### 系统要求

- **操作系统**: Ubuntu 22.04 LTS
- **GPU**: NVIDIA GPU (支持CUDA)
- **内存**: 建议16GB以上
- **存储**: 建议500GB以上

### 自动化安装

运行以下命令完成服务器环境配置：

```bash
# 下载脚本
cd ~/文档/MimoCode
chmod +x scripts/setup-server.sh

# 运行脚本
./scripts/setup-server.sh
```

### 手动安装步骤

#### 1. 更新系统

```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. 安装基础工具

```bash
sudo apt install -y curl wget git vim htop net-tools build-essential
```

#### 3. 安装NVIDIA驱动

```bash
sudo apt install -y nvidia-driver-535
sudo reboot
```

验证安装：
```bash
nvidia-smi
```

#### 4. 安装CUDA 12.2

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install -y cuda-12-2
```

配置环境变量：
```bash
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

#### 5. 安装Docker

```bash
# 添加Docker GPG密钥
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 添加Docker仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# 添加用户到docker组
sudo usermod -aG docker $USER
```

#### 6. 安装NVIDIA Container Toolkit

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

#### 7. 安装Python环境

```bash
sudo apt install -y python3.10 python3.10-venv python3-pip
python3.10 -m venv ~/venvs/default
source ~/venvs/default/bin/activate
pip install --upgrade pip
pip install jupyterlab numpy pandas scikit-learn
```

#### 8. 安装Git LFS

```bash
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt install -y git-lfs
git lfs install
```

### 验证安装

```bash
nvidia-smi                    # 检查NVIDIA驱动
nvcc --version                # 检查CUDA
docker --version              # 检查Docker
python3 --version             # 检查Python
jupyter lab --version         # 检查Jupyter Lab
git lfs version               # 检查Git LFS
```

### 启动Jupyter Lab

```bash
# 激活虚拟环境
source ~/venvs/default/bin/activate

# 启动Jupyter Lab
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
```

访问地址：`http://服务器IP:8888`

---

## MacBook环境配置

### 概述

本文档描述如何配置macOS开发环境。

### 系统要求

- **操作系统**: macOS Ventura 13.0 或更高版本
- **存储**: 建议256GB以上

### 自动化安装

运行以下命令完成MacBook环境配置：

```bash
cd ~/文档/MimoCode
chmod +x scripts/setup-macbook.sh
./scripts/setup-macbook.sh
```

### 手动安装步骤

#### 1. 安装Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Apple Silicon Mac
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

#### 2. 安装开发工具

```bash
brew install --cask visual-studio-code obsidian zotero iterm2
```

#### 3. 配置SSH

```bash
# 生成SSH密钥
ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519

# 启动ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 查看公钥（复制到GitHub/GitLab）
cat ~/.ssh/id_ed25519.pub
```

#### 4. 安装Node.js

```bash
# 安装nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# 加载nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# 安装Node.js
nvm install 20
nvm use 20
nvm alias default 20
```

#### 5. 安装Python

```bash
brew install python@3.11 pyenv

# 配置pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# 安装Python
pyenv install 3.11.7
pyenv global 3.11.7
```

#### 6. 配置Git

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase true
git config --global push.autoSetupRemote true
```

### 安装VS Code插件

```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-toolsai.jupyter
code --install-extension ms-vscode-remote.remote-ssh
code --install-extension eamodio.gitlens
code --install-extension GitHub.copilot
```

### 验证安装

```bash
brew --version            # 检查Homebrew
code --version            # 检查VS Code
node --version            # 检查Node.js
python3 --version         # 检查Python
git --version             # 检查Git
ssh -T git@github.com     # 检查SSH连接
```

---

## 远程连接配置

### SSH连接到服务器

#### 1. 配置SSH别名

在MacBook的 `~/.ssh/config` 中添加：

```
Host gpu-server
    HostName 服务器IP地址
    User 用户名
    IdentityFile ~/.ssh/id_ed25519
    Port 22
```

#### 2. 连接服务器

```bash
ssh gpu-server
```

### VS Code远程开发

1. 安装Remote-SSH扩展
2. 按 `Cmd+Shift+P`，输入 "Remote-SSH: Connect to Host"
3. 选择 `gpu-server`
4. 在服务器上打开项目文件夹

### 文件传输

#### 上传文件到服务器

```bash
scp /本地文件路径 gpu-server:/远程路径/
```

#### 从服务器下载文件

```bash
scp gpu-server:/远程文件路径 /本地路径/
```

#### 同步目录

```bash
rsync -avz /本地目录/ gpu-server:/远程目录/
```

### 端口转发

#### 转发Jupyter Lab端口

```bash
ssh -L 8888:localhost:8888 gpu-server
```

然后在浏览器访问：`http://localhost:8888`

#### VS Code自动端口转发

VS Code Remote-SSH会自动转发Jupyter Lab端口。

### SSH密钥管理

#### 在服务器上添加公钥

```bash
# 在MacBook上复制公钥
pbcopy < ~/.ssh/id_ed25519.pub

# 在服务器上添加
mkdir -p ~/.ssh
echo "粘贴的公钥" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

#### 测试SSH连接

```bash
ssh -T git@github.com
```

---

## 常见问题解答

### 服务器相关

#### Q1: NVIDIA驱动安装后无法使用

**问题**: 运行 `nvidia-smi` 报错 "NVIDIA-SMI has failed"

**解决方案**:
```bash
# 检查驱动是否加载
lsmod | grep nvidia

# 如果没有加载，重新安装驱动
sudo apt purge nvidia-*
sudo apt install -y nvidia-driver-535
sudo reboot
```

#### Q2: Docker无法使用GPU

**问题**: 运行 `docker run --gpus all` 报错

**解决方案**:
```bash
# 检查NVIDIA Container Toolkit是否安装
nvidia-ctk --version

# 重新配置Docker运行时
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# 测试
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
```

#### Q3: CUDA版本不匹配

**问题**: 程序报错CUDA版本不兼容

**解决方案**:
```bash
# 查看CUDA版本
nvcc --version
cat /usr/local/cuda/version.txt

# 切换CUDA版本（如果有多个版本）
sudo update-alternatives --config cuda
```

#### Q4: Jupyter Lab无法连接

**问题**: 浏览器无法访问Jupyter Lab

**解决方案**:
```bash
# 检查防火墙
sudo ufw status

# 允许8888端口
sudo ufw allow 8888

# 检查Jupyter Lab是否运行
ps aux | grep jupyter

# 重启Jupyter Lab
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
```

### MacBook相关

#### Q1: Homebrew安装失败

**问题**: 安装过程中报错

**解决方案**:
```bash
# 检查Xcode Command Line Tools
xcode-select --install

# 重试安装
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Q2: SSH密钥无法使用

**问题**: GitHub/GitLab提示密钥无效

**解决方案**:
```bash
# 检查ssh-agent是否运行
eval "$(ssh-agent -s)"

# 添加密钥
ssh-add ~/.ssh/id_ed25519

# 测试连接
ssh -T git@github.com
```

#### Q3: Python版本冲突

**问题**: 系统Python和pyenv版本冲突

**解决方案**:
```bash
# 检查当前Python
which python3
python3 --version

# 使用pyenv管理版本
pyenv versions
pyenv global 3.11.7

# 重新加载shell
exec "$SHELL"
```

#### Q4: VS Code无法连接远程服务器

**问题**: Remote-SSH连接失败

**解决方案**:
```bash
# 检查SSH配置
ssh -v gpu-server

# 在VS Code中查看输出
# View > Output > Remote-SSH

# 重新安装Remote-SSH扩展
code --install-extension ms-vscode-remote.remote-ssh --force
```

### 通用问题

#### Q1: 磁盘空间不足

```bash
# 检查磁盘使用
df -h

# 清理Docker
docker system prune -a

# 清理APT缓存
sudo apt clean
sudo apt autoremove
```

#### Q2: 网络连接问题

```bash
# 检查网络
ping 8.8.8.8

# 检查DNS
nslookup google.com

# 检查防火墙
sudo ufw status
```

#### Q3: 权限问题

```bash
# 检查文件权限
ls -la ~/.ssh/

# 修复权限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 600 ~/.ssh/config
```

---

## 维护和更新

### 定期更新

```bash
# 服务器
sudo apt update && sudo apt upgrade -y

# MacBook
brew update && brew upgrade
```

### 备份配置

```bash
# 备份Git配置
git config --list > ~/backups/git-config-backup.txt

# 备份SSH配置
cp -r ~/.ssh ~/backups/ssh-backup

# 备份VS Code设置
cp -r ~/Library/Application\ Support/Code/User ~/backups/vscode-settings
```

### 监控资源

```bash
# 服务器资源监控
htop                    # CPU和内存
nvidia-smi              # GPU使用情况
df -h                   # 磁盘使用情况

# MacBook资源监控
top                     # 系统监视器
activity_monitor        # 图形化监控
```

---

## 联系支持

如果遇到本文档未覆盖的问题，请联系：

- **系统管理员**: [联系方式]
- **IT支持**: [联系方式]
- **文档维护**: [联系方式]

---

*最后更新: 2024年*
