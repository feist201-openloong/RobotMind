#!/bin/bash
# ============================================================================
# 今晚自动化安装主控脚本
# 功能：在后台依次执行所有安装阶段
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$HOME/install-logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/install_${TIMESTAMP}.log"

echo "============================================"
echo "  RobotMind 自动化安装启动"
echo "  日志文件: $LOG_FILE"
echo "============================================"

# 执行第一阶段
echo "[$(date)] 开始第一阶段安装..." | tee -a "$LOG_FILE"
bash "$SCRIPT_DIR/setup-phase1.sh" 2>&1 | tee -a "$LOG_FILE"

echo ""
echo "[$(date)] 第一阶段完成！" | tee -a "$LOG_FILE"
echo ""
echo "请执行以下命令重启系统："
echo "  sudo reboot"
echo ""
echo "重启后运行："
echo "  cd $SCRIPT_DIR"
echo "  chmod +x setup-phase2.sh setup-isaac-unitree.sh"
echo "  ./setup-phase2.sh && ./setup-isaac-unitree.sh"
echo ""
echo "或者使用自动重启："
echo "  sudo reboot"
echo "  # 重启后登录并运行上述命令"
