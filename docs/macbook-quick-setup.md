# MacBook 快速配置指南

## 服务器信息

| 项目 | 值 |
|------|-----|
| 服务器IP | 10.185.157.188 |
| 用户名 | dell |
| 主机名 | dell-Dell-Pro-Max-Tower-T2-FCT2250 |

## 步骤1: 传输配置脚本到MacBook

在MacBook上打开终端，执行以下命令从服务器下载脚本：

```bash
# 创建项目目录
mkdir -p ~/projects/robotics-learning-assistant
cd ~/projects/robotics-learning-assistant

# 从服务器下载脚本（需要输入服务器密码）
scp dell@10.185.157.188:/home/dell/文档/MimoCode/scripts/setup-macbook.sh .

# 下载完成后，设置环境变量并运行
export GIT_USER_NAME="你的姓名"
export GIT_USER_EMAIL="你的邮箱"
export SERVER_HOSTNAME="10.185.157.188"
export SERVER_USERNAME="dell"

chmod +x setup-macbook.sh
./setup-macbook.sh
```

## 步骤2: 配置SSH连接到服务器

脚本运行完成后，需要将MacBook的SSH公钥添加到服务器：

### 2.1 复制MacBook的SSH公钥

```bash
cat ~/.ssh/id_ed25519.pub
```

### 2.2 在服务器上添加公钥

在服务器上执行（或让我帮你添加）：

```bash
# 将上面复制的公钥内容粘贴到这里
echo "你的公钥内容" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 2.3 测试SSH连接

```bash
ssh dell@10.185.157.188
```

## 步骤3: 配置VS Code Remote-SSH

1. 打开VS Code
2. 按 `Cmd+Shift+P` 打开命令面板
3. 输入 `Remote-SSH: Connect to Host`
4. 选择 `dell@10.185.157.188`
5. 选择 Linux 作为平台

## 步骤4: 安装Obsidian和Zotero

1. 打开Obsidian，创建新的Vault：`~/Documents/Robotics-Learning`
2. 打开Zotero，配置同步账户

## 验证清单

- [ ] Homebrew安装成功：`brew --version`
- [ ] VS Code安装成功：`code --version`
- [ ] Node.js安装成功：`node --version`
- [ ] Python安装成功：`python3 --version`
- [ ] SSH连接成功：`ssh dell@10.185.157.188`
- [ ] VS Code Remote-SSH连接成功

## 常见问题

### Q: SSH连接被拒绝？
```bash
# 在服务器上检查SSH服务
sudo systemctl status ssh
sudo systemctl start ssh
```

### Q: 无法下载脚本？
```bash
# 确保服务器防火墙允许SSH
sudo ufw allow ssh
```

### Q: VS Code Remote-SSH连接失败？
1. 检查SSH配置：`cat ~/.ssh/config`
2. 手动测试连接：`ssh -v dell@10.185.157.188`
