import requests
import base64
from git_trending.config import GITHUB_TRENDING_URL, DEFAULT_HEADERS

def fetch_trending_page():
    """
    从GitHub获取趋势页面内容
    
    Returns:
        str: 页面HTML内容，如果请求失败返回None
    """
    try:
        response = requests.get(GITHUB_TRENDING_URL, headers=DEFAULT_HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None

def fetch_github_readme(owner, repo):
    """
    获取指定 GitHub 仓库的 README 内容

    Args:
        owner (str): 仓库所有者的用户名
        repo (str): 仓库名称

    Returns:
        str: README 的内容，如果请求失败则返回 None
    """
    readme_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    
    try:
        response = requests.get(readme_url, headers=DEFAULT_HEADERS, timeout=10)
        response.raise_for_status()
        
        # 响应内容是 Base64 编码的 README 数据
        return base64.b64decode(response.json()['content']).decode('utf-8')
    except requests.RequestException as e:
        print(f"请求 README 失败: {e}")
        return None