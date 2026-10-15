#!/usr/bin/env bash
# vla-wam-scout 本地每日定时运行（配合 crontab 使用）
# 用法：crontab 加入  ->  0 4 * * * /workspace/vla-wam-scout/run_daily_local.sh
# 说明：
#   - 本地走 .env 配置的 LLM 端点（默认仍是灵枢，内网可达）
#   - 结果写入 reports/（daily-vla-wam-YYYY-MM-DD.md / latest.md / repos.md / state.json）
#   - 若存在 .push_enabled 文件且已配置 GitHub 凭据，则自动 commit + push 到仓库
# 日志：logs/daily.log
set -u
cd "$(dirname "$0")"
mkdir -p logs
LOG=logs/daily.log
LOCK=/tmp/vla_wam_scout.lock

echo "===== $(date -u '+%Y-%m-%d %H:%M:%S') UTC 开始 =====" >> "$LOG"

# 防止重叠运行：上次未结束则跳过本次
flock -n "$LOCK" python3 run_daily.py >> "$LOG" 2>&1 \
    || { echo "!! 上次运行未结束，本次跳过" >> "$LOG"; exit 0; }

# 可选推送：仓库根目录存在 .push_enabled 才执行（需已配置 git 凭据）
if [ -f .push_enabled ] && git status --porcelain | grep -q "^ M reports/\|^?? reports/"; then
    git add reports/ || true
    if git diff --cached --quiet; then
        echo "reports 无变化，无需提交" >> "$LOG"
    else
        git commit -m "每日VLA/WAM情报更新 - $(date -u '+%Y-%m-%d') [local cron]" >> "$LOG" 2>&1 \
            && git push origin main >> "$LOG" 2>&1 \
            && echo "已推送至 GitHub" >> "$LOG" \
            || echo "!! git push 失败（检查凭据）" >> "$LOG"
    fi
fi

echo "===== 完成 $(date -u '+%Y-%m-%d %H:%M:%S') UTC =====" >> "$LOG"
