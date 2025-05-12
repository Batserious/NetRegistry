#!/bin/zsh
# 每隔5分钟执行auto.sh

# 检查是否已存在相同的crontab任务，避免重复添加
crontab -l 2>/dev/null | grep -q 'auto.sh' || (
  (crontab -l 2>/dev/null; echo "*/5 * * * * cd $(pwd) && ./auto.sh >> auto.log 2>&1") | crontab -
)

echo "已设置每5分钟自动执行auto.sh"