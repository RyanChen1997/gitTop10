import pytest
import base64
import requests
from git_trending.crawler import fetch_trending_page, fetch_github_readme

def test_fetch_trending_page_no_mock():
    """
    不使用mock调用fetch_trending_page方法，并打印输出
    """
    result = fetch_trending_page()
    # print("fetch_trending_page返回内容:", result)
    assert result is not None  # 确保返回内容不为空

# 测试fetch_trending_page函数
def test_fetch_trending_page_success(monkeypatch):
    """
    测试成功获取页面内容的情况
    """
    # 模拟requests.get方法
    class MockResponse:
        def __init__(self):
            self.status_code = 200
            
        def raise_for_status(self):
            return None
            
        @property
        def text(self):
            return "<html>Mock HTML Content</html>"

    def mock_get(*args, **kwargs):
        return MockResponse()

    # 替换掉requests.get
    monkeypatch.setattr(requests, 'get', mock_get)
    
    result = fetch_trending_page()
    assert result == "<html>Mock HTML Content</html>"

def test_fetch_trending_page_failure(monkeypatch):
    """
    测试页面请求失败的情况
    """
    # 模拟requests.get方法抛出异常
    def mock_get(*args, **kwargs):
        raise requests.RequestException("Mock 请求失败")

    # 替换掉requests.get
    monkeypatch.setattr(requests, 'get', mock_get)
    
    result = fetch_trending_page()
    assert result is None

def test_fetch_github_readme_success(monkeypatch):
    """
    测试成功获取 GitHub 仓库 README 的情况
    """
    # 读取本地 README 文件内容（假设你有一个测试用的 README 文件）
    with open("tests/mock_data/test_repo_readme.md", "r", encoding="utf-8") as f:
        mock_readme_content = f.read()

    # 构造模拟响应对象
    class MockResponse:
        def __init__(self):
            self.status_code = 200

        def raise_for_status(self):
            return None

        def json(self):
            return {
                "content": base64.b64encode(mock_readme_content.encode("utf-8")).decode("utf-8")
            }

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    result = fetch_github_readme("biliup", "biliup-rs")
    assert result is not None
    assert "B 站命令行投稿工具" in result

def test_fetch_github_readme_failure(monkeypatch):
    """
    测试获取 GitHub 仓库 README 失败的情况
    """
    # 模拟requests.get方法抛出异常
    def mock_get(*args, **kwargs):
        raise requests.RequestException("Mock 请求失败")

    # 替换掉requests.get
    monkeypatch.setattr(requests, 'get', mock_get)

    # 调用测试函数
    result = fetch_github_readme("mockuser", "mockrepo")

    # 验证返回结果是否为None
    assert result is None