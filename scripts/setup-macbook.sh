#!/bin/bash
# ============================================================================
# MacBook环境配置脚本
# 用途：初始化MacBook开发环境
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

# 版本参数
NODE_VERSION="20"
PYTHON_VERSION="3.11"
PYENV_PYTHON_VERSIONS="3.10.13 3.11.7"

# 用户配置变量
GIT_USER_NAME="${GIT_USER_NAME:-Your Name}"
GIT_USER_EMAIL="${GIT_USER_EMAIL:-your_email@example.com}"
SERVER_HOSTNAME="${SERVER_HOSTNAME:-YOUR_SERVER_IP}"
SERVER_USERNAME="${SERVER_USERNAME:-your_username}"

# ============================================================================
# 辅助函数：幂等性追加配置到文件
# ============================================================================
append_if_missing() {
    local file="$1"
    local marker="$2"
    local content="$3"
    if ! grep -q "$marker" "$file" 2>/dev/null; then
        echo "$content" >> "$file"
    fi
}

# ============================================================================
# 1. 安装Homebrew
# ============================================================================
log_info "安装Homebrew..."

if ! command -v brew &> /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # 添加Homebrew到PATH（幂等性检查）
    if [[ $(uname -m) == "arm64" ]]; then
        BREW_SHELLENV='eval "$(/opt/homebrew/bin/brew shellenv)"'
        append_if_missing ~/.zprofile "brew shellenv" "$BREW_SHELLENV"
        eval "$(/opt/homebrew/bin/brew shellenv)"
    else
        BREW_SHELLENV='eval "$(/usr/local/bin/brew shellenv)"'
        append_if_missing ~/.zprofile "brew shellenv" "$BREW_SHELLENV"
        eval "$(/usr/local/bin/brew shellenv)"
    fi
else
    log_info "Homebrew已安装"
fi

# 更新Homebrew
brew update

# ============================================================================
# 2. 安装开发工具
# ============================================================================
log_info "安装开发工具..."

# 安装应用（幂等性：brew install --cask 会跳过已安装的）
brew install --cask visual-studio-code
brew install --cask obsidian
brew install --cask zotero
brew install --cask iterm2
brew install --cask rectangle

# ============================================================================
# 3. 安装SSH工具
# ============================================================================
log_info "安装SSH工具..."

# 安装openssh
brew install openssh

# 生成SSH密钥（如果不存在）
SSH_KEY="$HOME/.ssh/id_ed25519"
if [ ! -f "$SSH_KEY" ]; then
    log_info "生成SSH密钥..."

    # 提示用户输入密码短语
    read -r -p "是否为SSH密钥设置密码短语？(推荐: y) [y/N]: " use_passphrase
    if [[ "$use_passphrase" =~ ^[Yy]$ ]]; then
        log_info "请输入SSH密钥密码短语（输入时不会显示）:"
        ssh-keygen -t ed25519 -C "$GIT_USER_EMAIL" -f "$SSH_KEY"
    else
        log_warn "生成无密码短语的SSH密钥（不推荐用于生产环境）"
        ssh-keygen -t ed25519 -C "$GIT_USER_EMAIL" -f "$SSH_KEY" -N ""
    fi

    eval "$(ssh-agent -s)"
    ssh-add "$SSH_KEY"
    log_info "SSH密钥已生成，请将以下公钥添加到GitHub/GitLab:"
    cat "${SSH_KEY}.pub"
else
    log_info "SSH密钥已存在"
fi

# 配置SSH客户端（幂等性：如果已有配置则备份）
if [ -f ~/.ssh/config ]; then
    cp ~/.ssh/config ~/.ssh/config.backup.$(date +%Y%m%d%H%M%S)
fi

cat > ~/.ssh/config << EOF
Host *
    AddKeysToAgent yes
    UseKeychain yes
    IdentityFile ~/.ssh/id_ed25519

# GitHub
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

# GitLab
Host gitlab.com
    HostName gitlab.com
    User git
    IdentityFile ~/.ssh/id_ed25519

# 远程服务器
Host gpu-server
    HostName ${SERVER_HOSTNAME}
    User ${SERVER_USERNAME}
    IdentityFile ~/.ssh/id_ed25519
    Port 22
EOF

chmod 600 ~/.ssh/config

# ============================================================================
# 4. 安装VS Code插件
# ============================================================================
log_info "安装VS Code插件..."

# 基础插件
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-toolsai.jupyter
code --install-extension ms-vscode-remote.remote-ssh
code --install-extension ms-vscode.powershell

# 前端开发
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension bradlc.vscode-tailwindcss

# 工具插件
code --install-extension eamodio.gitlens
code --install-extension PKief.material-icon-theme
code --install-extension oderwat.indent-rainbow
code --install-extension usernamehw.errorlens

# AI助手
code --install-extension GitHub.copilot

# ============================================================================
# 5. 安装Node.js
# ============================================================================
log_info "安装Node.js..."

# 安装nvm（幂等性：nvm安装脚本会跳过已安装的情况）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# 加载nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# 安装Node.js
nvm install "$NODE_VERSION"
nvm use "$NODE_VERSION"
nvm alias default "$NODE_VERSION"

# 安装全局npm包
npm install -g \
    yarn \
    pnpm \
    nodemon \
    ts-node \
    typescript \
    @vue/cli \
    create-react-app \
    eslint \
    prettier

# ============================================================================
# 6. 安装Python
# ============================================================================
log_info "安装Python..."

# 安装Python
brew install "python@${PYTHON_VERSION}"

# 安装pyenv（幂等性）
if ! command -v pyenv &> /dev/null; then
    brew install pyenv
fi

# 幂等性追加pyenv配置到.zshrc
ZSHRC="$HOME/.zshrc"
append_if_missing "$ZSHRC" "# pyenv configuration" '
# pyenv configuration
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
'

# 安装Python版本（幂等性：pyenv install 会跳过已安装的）
for ver in $PYENV_PYTHON_VERSIONS; do
    pyenv install "$ver" || true
done
pyenv global "$PYTHON_VERSION"

# 创建Python虚拟环境进行pip安装（避免污染系统Python）
PYTHON_VENV_DIR="$HOME/venvs/tools"
mkdir -p "$HOME/venvs"
if [ ! -d "$PYTHON_VENV_DIR" ]; then
    python3 -m venv "$PYTHON_VENV_DIR"
fi
source "$PYTHON_VENV_DIR/bin/activate"

pip install --upgrade pip
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
    pydantic \
    black \
    flake8 \
    mypy

deactivate

# ============================================================================
# 7. 配置Git
# ============================================================================
log_info "配置Git..."

# Git全局配置
git config --global user.name "$GIT_USER_NAME"
git config --global user.email "$GIT_USER_EMAIL"

# Git默认分支名
git config --global init.defaultBranch main

# Git别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --oneline --graph --all"

# Git拉取策略
git config --global pull.rebase true

# Git推送策略
git config --global push.autoSetupRemote true

# Git合并工具 (macOS)
git config --global merge.tool opendiff

# Git差异工具
git config --global diff.tool opendiff

# Git凭据管理
git config --global credential.helper osxkeychain

# ============================================================================
# 8. 配置终端
# ============================================================================
log_info "配置终端..."

# 安装Oh My Zsh（幂等性：已安装则跳过）
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi

# 安装Zsh插件（幂等性：已存在则跳过）
ZSH_CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"
if [ ! -d "$ZSH_CUSTOM/plugins/zsh-autosuggestions" ]; then
    git clone https://github.com/zsh-users/zsh-autosuggestions "$ZSH_CUSTOM/plugins/zsh-autosuggestions"
fi
if [ ! -d "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting" ]; then
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting"
fi
if [ ! -d "$ZSH_CUSTOM/plugins/zsh-completions" ]; then
    git clone https://github.com/zsh-users/zsh-completions "$ZSH_CUSTOM/plugins/zsh-completions"
fi

# 配置Zsh（幂等性：备份现有配置）
if [ -f ~/.zshrc ]; then
    cp ~/.zshrc ~/.zshrc.backup.$(date +%Y%m%d%H%M%S)
fi

cat > ~/.zshrc << 'ZSHRC_EOF'
# Oh My Zsh配置
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="agnoster"

# 插件
plugins=(
    git
    zsh-autosuggestions
    zsh-syntax-highlighting
    zsh-completions
    docker
    docker-compose
    kubectl
    vscode
)

source $ZSH/oh-my-zsh.sh

# 用户配置
export LANG=en_US.UTF-8
export EDITOR='vim'

# 历史记录配置
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.zsh_history

# 别名
alias ll="ls -la"
alias la="ls -la"
alias l="ls -la"
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."

# Git别名
alias gs="git status"
alias ga="git add"
alias gc="git commit"
alias gp="git push"
alias gl="git log"
alias gd="git diff"

# Docker别名
alias dk="docker"
alias dkps="docker ps"
alias dki="docker images"
alias dkrm="docker rm"
alias dkrmi="docker rmi"

# 开发环境别名
alias py="python3"
alias pip="pip3"
alias jupyter="jupyter lab"

# 远程服务器连接
alias gpu-server="ssh gpu-server"

# pyenv配置
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# nvm配置
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
ZSHRC_EOF

# ============================================================================
# 9. 安装其他实用工具
# ============================================================================
log_info "安装其他实用工具..."

# 工具
brew install \
    tree \
    jq \
    yq \
    ripgrep \
    fd \
    bat \
    fzf \
    tldr

# 安装fzf键绑定（幂等性：已有则跳过）
if [ ! -f "$HOME/.fzf.zsh" ]; then
    "$(brew --prefix)"/opt/fzf/install
fi

# ============================================================================
# 10. 创建项目目录
# ============================================================================
log_info "创建项目目录结构..."

mkdir -p ~/projects/{ai,web,scripts,docs,data}
mkdir -p ~/data/{raw,processed,models,logs}
mkdir -p ~/backups

# ============================================================================
# 完成
# ============================================================================
log_info "=========================================="
log_info "MacBook环境配置完成!"
log_info "=========================================="
log_info ""
log_info "需要执行的操作:"
log_info "1. 将SSH公钥添加到GitHub/GitLab"
log_info "2. 登录VS Code"
log_info "3. 登录Obsidian"
log_info "4. 配置Zotero"
log_info ""
log_info "验证命令:"
log_info "  brew --version          # 检查Homebrew"
log_info "  code --version          # 检查VS Code"
log_info "  node --version          # 检查Node.js"
log_info "  python3 --version       # 检查Python"
log_info "  git --version           # 检查Git"
log_info "  ssh -T git@github.com   # 检查SSH连接"
