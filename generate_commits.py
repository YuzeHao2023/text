#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
750天真实贡献记录生成脚本
用于当前仓库中生成750天的commit记录
"""

import os
import sys
import random
from datetime import datetime, timedelta
from subprocess import Popen, CalledProcessError
import subprocess
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 提交消息模板
COMMIT_MESSAGES = [
    "更新文档: {date}",
    "修复小问题: {date}",
    "代码优化: {date}",
    "添加新功能: {date}",
    "重构代码: {date}",
    "更新配置: {date}",
    "修复bug: {date}",
    "改进性能: {date}",
    "添加测试: {date}",
    "更新依赖: {date}",
    "代码审查: {date}",
    "文档完善: {date}",
    "性能调优: {date}",
    "安全修复: {date}",
    "功能增强: {date}",
    "修复编译错误: {date}",
    "优化算法: {date}",
    "清理代码: {date}",
    "更新注释: {date}",
    "修复测试: {date}"
]


class RealisticCommitGenerator:
    """750天真实提交模式生成器"""
    
    def __init__(self):
        self.commit_count = 0
        
    def generate_750_days(self):
        """生成750天的真实贡献模式"""
        current_date = datetime.now()
        start_date = current_date - timedelta(days=750)
        
        logger.info(f"开始生成750天真实贡献模式")
        logger.info(f"时间范围: {start_date.date()} 到 {current_date.date()}")
        
        current_day = start_date
        consecutive_days = 0
        
        while current_day <= current_date:
            # 决定是否中断（每隔4-8天）
            if consecutive_days >= random.randint(4, 8):
                # 中断期：1-3天
                break_days = random.randint(1, 3)
                logger.info(f"中断期: {current_day.date()} (~{break_days}天)")
                current_day += timedelta(days=break_days)
                consecutive_days = 0
                continue
            
            # 生成当天的提交
            commits_today = random.randint(1, 5)
            self._generate_daily_commits(current_day, commits_today)
            
            consecutive_days += 1
            current_day += timedelta(days=1)
            
            # 每100次提交输出进度
            if self.commit_count % 100 == 0:
                logger.info(f"已生成 {self.commit_count} 次提交...")
        
        logger.info(f"750天真实贡献模式生成完成，总共 {self.commit_count} 次提交")
        return self.commit_count
    
    def _generate_daily_commits(self, date, commit_count):
        """生成一天的提交"""
        for i in range(commit_count):
            # 随机选择提交时间（9:00-23:00）
            hour = random.randint(9, 23)
            minute = random.randint(0, 59)
            commit_time = date.replace(hour=hour, minute=minute)
            
            self._make_commit(commit_time)
    
    def _make_commit(self, commit_time):
        """执行一次提交"""
        try:
            # 创建或更新文件
            self._update_file(commit_time)
            
            # 添加文件到暂存区
            self._run_command(['git', 'add', '.'])
            
            # 提交更改
            commit_message = self._generate_commit_message(commit_time)
            cmd = [
                'git', 'commit', '-m', commit_message,
                '--date', commit_time.strftime('%Y-%m-%d %H:%M:%S')
            ]
            self._run_command(cmd)
            
            self.commit_count += 1
            
        except Exception as e:
            logger.error(f"提交失败: {e}")
            raise
    
    def _update_file(self, date):
        """更新文件内容"""
        # 更新 CONTRIBUTIONS.md
        contrib_path = 'CONTRIBUTIONS.md'
        with open(contrib_path, 'a', encoding='utf-8') as file:
            file.write(f"贡献记录: {date.strftime('%Y-%m-%d %H:%M')}\n")
    
    def _generate_commit_message(self, date):
        """生成提交消息"""
        template = random.choice(COMMIT_MESSAGES)
        return template.format(date=date.strftime('%Y-%m-%d %H:%M'))
    
    def _run_command(self, commands):
        """执行 Git 命令"""
        try:
            process = Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                error_msg = stderr.decode('utf-8', errors='ignore')
                if 'nothing to commit' not in error_msg:
                    raise CalledProcessError(process.returncode, commands, stderr)
        except CalledProcessError as e:
            logger.error(f"命令执行失败: {' '.join(commands)}")
            raise


def main():
    """主函数"""
    print("=" * 60)
    print("🎯 750天真实贡献记录生成器")
    print("=" * 60)
    
    try:
        # 检查是否在git仓库中
        result = Popen(['git', 'rev-parse', '--git-dir'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
        stdout, stderr = result.communicate()
        
        if result.returncode != 0:
            print("❌ 当前目录不是一个git仓库")
            return 1
        
        print("✓ 检测到git仓库")
        
        # 创建生成器
        generator = RealisticCommitGenerator()
        
        # 生成贡献
        print("\n⏳ 正在生成750天的真实提交记录...")
        print("   模式: 每天 1-5 次提交，每隔 4-8 天中断一次\n")
        
        total_commits = generator.generate_750_days()
        
        print(f"\n{'=' * 60}")
        print(f"🎉 生成完成!")
        print(f"📊 总提交数: {total_commits}")
        print(f"📈 平均每天: {total_commits/750:.2f} 次提交")
        print(f"{'=' * 60}")
        
        # 推送到main分支
        print("\n⏳ 正在推送到main分支...")
        generator._run_command(['git', 'push', '-u', 'origin', 'main', '--force'])
        print("✓ 推送完成！")
        
        print("\n🎉 所有操作完成！您的GitHub绿墙已更新！")
        
        return 0
        
    except Exception as e:
        logger.error(f"程序执行失败: {e}")
        print(f"❌ 执行失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
