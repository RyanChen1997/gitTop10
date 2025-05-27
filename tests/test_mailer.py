import pytest
from git_trending.mailer import send_email, generate_email_body
from unittest.mock import patch, MagicMock
from git_trending.parser import Repository
from git_trending.config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

def test_generate_email_body_with_repositories():
    """
    测试生成包含仓库信息的邮件正文
    """
    repositories = [
        Repository(name="user/repo1", description="This is the description of repo1", language="Python", stars=None, today_stars=None, rank=1),
        Repository(name="user/repo2", description="This is the description of repo2", language=None, stars=None, today_stars=None, rank=2),
        Repository(name="user/repo3", description=None, language="JavaScript", stars=None, today_stars=None, rank=3)
    ]
    
    email_body = generate_email_body(repositories)
    # print(email_body)
    
    # 验证邮件正文是否包含所有仓库信息
    assert "GitHub上今日最流行的10个仓库" in email_body
    assert "user/repo1" in email_body
    assert "This is the description of repo1" in email_body
    assert "Python" in email_body
    assert "user/repo2" in email_body
    assert "This is the description of repo2" in email_body
    assert "user/repo3" in email_body
    assert "JavaScript" in email_body
    assert "感谢阅读！" in email_body

def test_generate_email_body_with_empty_repositories():
    """
    测试生成空仓库列表的邮件正文
    """
    # 验证空仓库列表
    email_body = generate_email_body([])
    assert "GitHub上今日最流行的10个仓库" in email_body
    assert "感谢阅读！" in email_body

    # None值
    email_body = generate_email_body(None)
    assert "GitHub上今日最流行的10个仓库" in email_body
    assert "感谢阅读！" in email_body
    
    # 仓库列表为None
    email_body = generate_email_body(None)
    assert "GitHub上今日最流行的10个仓库" in email_body
    assert "感谢阅读！" in email_body

# 测试send_email函数 - 使用mock模拟smtplib.SMTP
def test_send_email_success():
    """
    测试邮件发送成功的情况
    """
    # 创建一个模拟的 server 实例
    mock_server = MagicMock()

    # 模拟smtplib.SMTP
    with patch("smtplib.SMTP") as mock_smtp:
        mock_smtp.return_value.__enter__.return_value = mock_server
        # 准备测试数据
        to_addresses = ["test1@example.com", "test2@example.com"]
        repositories = [
            Repository(name="user/repo1", description="This is the description of repo1", language="Python", stars=None, today_stars=None, rank=1)
        ]
        
        # 调用函数
        result = send_email(to_addresses, repositories)
        
        # 验证结果
        assert result is True
        # 验证连接是否被正确调用
        mock_smtp.assert_called_once_with(SMTP_SERVER, SMTP_PORT)
        # 验证 login 是否被正确调用
        mock_server.login.assert_called_once_with(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # 验证 sendmail 是否被每个收件人调用
        assert mock_server.sendmail.call_count == len(to_addresses)
        
def test_send_email_failure():
    """
    测试邮件发送失败的情况
    """
    # 模拟smtplib.SMTP并抛出异常
    with patch("smtplib.SMTP") as mock_smtp:
        # 设置异常
        mock_smtp.side_effect = Exception("Mock SMTP error")
        
        # 准备测试数据
        to_addresses = ["test1@example.com"]
        repositories = [
            Repository(name="user/repo1", description="This is the description of repo1", language="Python", stars=None, today_stars=None, rank=1)
        ]
        
        # 调用函数
        result = send_email(to_addresses, repositories)
        
        # 验证结果
        assert result is False

def test_send_email_real():
    """
    测试真实发送邮件到指定邮箱
    """
    # 准备测试数据
    to_addresses = ["youremail@outlook.com"]
    repositories = [
        Repository(name="user/repo1", description="This is the description of repo1", language="Python", stars=None, today_stars=None, rank=1)
    ]
    
    # 调用函数
    result = send_email(to_addresses, repositories)
    
    # 验证结果
    assert result is True
