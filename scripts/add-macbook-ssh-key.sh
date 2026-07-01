#!/bin/bash
# ============================================================================
# 服务器端脚本：添加MacBook SSH公钥
# 用途：将MacBook的公钥添加到服务器的authorized_keys
# ============================================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# 确保.ssh目录存在
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# 备份现有的authorized_keys
if [ -f ~/.ssh/authorized_keys ]; then
    cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.backup.$(date +%Y%m%d%H%M%S)
    log_info "已备份现有authorized_keys"
fi

# 提示用户输入公钥
log_info "请将MacBook的SSH公钥粘贴到下面（以ssh-ed25519或ssh-rsa开头）："
log_info "提示：在MacBook上运行 'cat ~/.ssh/id_ed25519.pub' 获取公钥"
echo ""
read -r -p "公钥内容: " SSH_PUBLIC_KEY

# 验证公钥格式
if [[ ! "$SSH_PUBLIC_KEY" =~ ^(ssh-ed25519|ssh-rsa|ecdsa-sha2-nistp256) ]]; then
    log_warn "公钥格式可能不正确，请确认后重试"
    exit 1
fi

# 检查是否已存在
if grep -q "$SSH_PUBLIC_KEY" ~/.ssh/authorized_keys 2>/dev/null; then
    log_warn "该公钥已存在于authorized_keys中"
    exit 0
fi

# 添加公钥
echo "$SSH_PUBLIC_KEY" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

log_info "SSH公钥添加成功！"
log_info ""
log_info "现在可以在MacBook上测试连接："
log_info "  ssh dell@$(hostname -I | awk '{print $1}')"
