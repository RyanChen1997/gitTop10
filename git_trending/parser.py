from bs4 import BeautifulSoup
from dataclasses import dataclass
from git_trending import Repository
from typing import List


def parse_trending_repositories(html_content, top=10) -> List[Repository]:
    """
    解析GitHub趋势页面内容，提取指定数量的仓库信息，并按今日星标数排序
    
    Args:
        html_content (str): GitHub趋势页面的HTML内容
        top (int): 返回前top个仓库，默认为10
    
    Returns:
        list: 包含指定数量仓库信息的列表，按今日星标数降序排列
    """
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    repositories = []
    
    # GitHub趋势页面上的仓库项
    repo_items = soup.select('article.Box-row')
    
    for index, item in enumerate(repo_items):  # 获取所有仓库
        # 提取仓库名称
        name_element = item.select_one('h2 a')
        name = ' '.join(name_element.get_text().strip().split()) if name_element else None
        
        # 提取仓库地址
        url = name_element['href'].strip() if name_element and 'href' in name_element.attrs else None
        if url:
            url = f"https://github.com{url}"
        
        # 提取描述
        description_element = item.select_one('p.col-9')
        description = description_element.get_text().strip() if description_element else None
        
        # 提取主要语言
        language_element = item.select_one('span[itemprop="programmingLanguage"]')
        language = language_element.get_text().strip() if language_element else None
        
        # 提取星标数
        stars_element = item.select_one('a.Link--muted')
        stars = stars_element.get_text().strip() if stars_element else None
        
        # 提取今日星标数
        today_stars_element = item.select_one('span.d-inline-block.float-sm-right')
        today_stars = today_stars_element.get_text().strip() if today_stars_element else None
        
        # 从today_stars中提取数字
        today_stars_number = None
        if today_stars:
            import re
            match = re.search(r'(\d+,?\d*)', today_stars)
            if match:
                today_stars_number = match.group(1).replace(',', '')
        
        if name:
            repositories.append(Repository(name=name, description=description, language=language, stars=stars, today_stars=today_stars_number, url=url))
    
    # 按今日星标数排序（假设today_stars是整数）
    repositories.sort(key=lambda x: int(x.today_stars) if x.today_stars else 0, reverse=True)

    for idx, repo in enumerate(repositories):
        repo.rank = idx + 1
    
    # 返回前top个仓库
    return repositories[:top]
