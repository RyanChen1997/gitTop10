import time
from datetime import datetime, timedelta
from git_trending.crawler import fetch_trending_page
from git_trending.parser import parse_trending_repositories
from git_trending.mailer import send_email
from git_trending.config import EMAIL_ADDRESS  # 可以从配置文件中加载默认收件人
from git_trending.ai_summary import AISummary

def fetch_and_send_trending_repositories(to_addresses=None):
    """
    获取GitHub趋势仓库并发送邮件
    
    Args:
        to_addresses (list): 收件人邮箱地址列表
    
    Returns:
        bool: 操作成功返回True，否则返回False
    """
    if to_addresses is None:
        to_addresses = [EMAIL_ADDRESS]  # 使用默认收件人

    # 获取趋势页面内容
    html_content = fetch_trending_page()
    
    # 解析前10个仓库
    repositories = parse_trending_repositories(html_content)
    
    # 发送邮件
    return send_email(to_addresses, repositories)

def schedule_daily_task(hour=8, minute=0):
    """
    每天定时执行任务
    
    Args:
        hour (int): 执行小时（24小时制）
        minute (int): 执行分钟
    """
    while True:
        now = datetime.now()
        # 如果当前时间超过了设定时间，则等待到明天同一时间
        next_run_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if now > next_run_time:
            next_run_time = next_run_time + timedelta(days=1)
        
        seconds_until_next_run = (next_run_time - now).total_seconds()
        print(f"下次执行时间: {next_run_time}")
        
        time.sleep(seconds_until_next_run)
        fetch_and_send_trending_repositories()

if __name__ == "__main__":
    # 直接运行时，发送到默认邮箱
    fetch_and_send_trending_repositories(["youremail@qq.com"])