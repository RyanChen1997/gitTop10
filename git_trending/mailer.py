import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from git_trending.config import SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD
from git_trending import Repository
from typing import List

def send_email(to_addresses, repositories: List[Repository]):
    """
    发送包含趋势仓库信息的电子邮件
    
    Args:
        to_addresses (list): 收件人邮箱地址列表
        repositories (list): 仓库信息列表，每个元素是Repository对象
    
    Returns:
        bool: 邮件发送成功返回True，否则返回False
    """
    if not repositories:
        print("没有仓库信息可发送")
        return False

    # 创建邮件内容
    subject = "GitHub Trending Top 10 Repositories"
    body = generate_email_body(repositories)
    # print(body)
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'html', "utf-8"))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            
            msg['To'] = ", ".join(to_addresses)
            server.sendmail(EMAIL_ADDRESS, to_addresses, msg.as_string())
            print(f"邮件已发送至 {to_addresses}")
            server.quit()
            
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False

def generate_email_body(repositories: List[Repository]):
    """
    根据仓库信息生成美化后的邮件正文（HTML格式）

    Args:
        repositories (list): 仓库信息列表

    Returns:
        str: 美化后的HTML格式邮件正文
    """
    if repositories is None:
        repositories = []

    # 定义基础样式
    style = """
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f5f7fa;
                color: #333;
                padding: 20px;
                margin: 0;
            }
            .container {
                max-width: 800px;
                margin: auto;
                background: #ffffff;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                padding: 30px;
            }
            h2 {
                color: #2c3e50;
                border-bottom: 2px solid #e0e0e0;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }
            .repo-card {
                background-color: #f9f9f9;
                border-left: 5px solid #3498db;
                padding: 15px 20px;
                margin-bottom: 20px;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            }
            .repo-name {
                font-weight: bold;
                font-size: 1.1em;
                color: #2980b9;
            }
            .repo-name a {
                color: #2980b9;
                text-decoration: none;
            }
            .repo-name a:hover {
                text-decoration: underline;
            }
            .repo-info {
                margin-top: 10px;
                font-size: 0.95em;
                color: #555;
            }
            .repo-info span {
                display: block;
                margin-bottom: 5px;
            }
        </style>
    """

    # 构建邮件内容
    body = f"""
    <html>
    <head>
        {style}
    </head>
    <body>
        <div class="container">
            <h2>GitHub上今日最流行的10个仓库</h2>
            {''.join(generate_repo_card(repo) for repo in repositories)}
            <p style="text-align: center; color: #777; font-size: 0.9em;">感谢阅读！</p>
        </div>
    </body>
    </html>
    """
    return body

def generate_repo_card(repo):
    """生成单个仓库卡片的HTML结构"""
    info_items = []
    if repo.description:
        info_items.append(f"<span>{repo.description}</span>")
    if repo.language:
        info_items.append(f"<span><strong>语言:</strong> {repo.language}</span>")
    if repo.stars:
        info_items.append(f"<span><strong>星标总数:</strong> {repo.stars}</span>")
    if repo.today_stars:
        info_items.append(f"<span><strong>今日星标:</strong> {repo.today_stars}</span>")

    return f"""
    <div class="repo-card">
        <div class="repo-name"><a href="{repo.url}">{repo.name}</a></div>
        <div class="repo-info">
            {"".join(info_items)}
        </div>
    </div>
    """