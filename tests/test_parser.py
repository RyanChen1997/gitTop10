import pytest
import json
from git_trending.parser import parse_trending_repositories
from git_trending.crawler import fetch_trending_page
from bs4 import BeautifulSoup

def test_fetch_and_parse_trending_repositories():
    """
    真实调用fetch_trending_page方法并解析出仓库信息，断言返回的仓库列表非空
    """
    html_content = fetch_trending_page()
    repositories = parse_trending_repositories(html_content)
    print("解析出的仓库列表:")
    for repo in repositories:
        print(f"名称: {repo.name}, 排名: {repo.rank}, 地址: {repo.url}")
    assert len(repositories) > 0, "仓库列表不应为空"
    # 验证排名是否正确（在1到top之间）
    for i, repo in enumerate(repositories):
        assert repo.rank == i + 1
    
    # 测试不同top值
    for top in [5, 10, 15]:
        repositories = parse_trending_repositories(html_content, top=top)
        assert len(repositories) <= top
        # 验证排名是否正确（按今日星标数降序）
        for i in range(len(repositories)-1):
            if repositories[i].today_stars and repositories[i+1].today_stars:
                assert int(repositories[i].today_stars.replace(',', '')) >= int(repositories[i+1].today_stars.replace(',', ''))
    
    # 验证所有仓库都已解析
    all_repositories = parse_trending_repositories(html_content, top=100)
    assert len(all_repositories) <= 100

def test_parse_trending_repositories_with_valid_data():
    """
    测试解析包含有效数据的情况
    """
    # 创建模拟的HTML内容
    html_content = '''
    <article class="Box-row">
      <h2><a href="/user/repo1">user/repo1</a></h2>
      <p class="col-9">This is the description of repo1</p>
      <span itemprop="programmingLanguage">Python</span>
      <a class="Link--muted">100 stars</a>
      <span class="d-inline-block float-sm-right">10 today</span>
    </article>
    <article class="Box-row">
      <h2><a href="/user/repo2">user/repo2</a></h2>
      <p class="col-9">This is the description of repo2</p>
      <span itemprop="programmingLanguage">JavaScript</span>
      <a class="Link--muted">50 stars</a>
      <span class="d-inline-block float-sm-right">5 today</span>
    </article>
    <article class="Box-row">
      <h2><a href="/user/repo3">user/repo3</a></h2>
    </article>
    '''
    
    soup = BeautifulSoup(html_content, 'html.parser')
    repositories = parse_trending_repositories(str(soup))
    
    # 验证结果
    assert len(repositories) == 3
    
    # 验证第一个仓库
    assert repositories[0].name == "user/repo1"
    assert repositories[0].description == "This is the description of repo1"
    assert repositories[0].language == "Python"
    assert repositories[0].today_stars is not None
    assert int(repositories[0].today_stars) == 10
    assert repositories[0].rank == 1
    assert repositories[0].url == "https://github.com/user/repo1"
    
    # 验证第二个仓库
    assert repositories[1].name == "user/repo2"
    assert repositories[1].description == "This is the description of repo2"
    assert repositories[1].language == "JavaScript"
    assert repositories[1].today_stars is not None
    assert int(repositories[1].today_stars) == 5
    assert repositories[1].rank == 2
    assert repositories[1].url == "https://github.com/user/repo2"
    
    # 验证第三个仓库（没有语言和星标数信息）
    assert repositories[2].name == "user/repo3"
    assert repositories[2].description is None
    assert repositories[2].language is None
    assert repositories[2].stars is None
    assert repositories[2].today_stars is None
    assert repositories[2].rank == 3
    assert repositories[2].url == "https://github.com/user/repo3"

def test_parse_trending_repositories_with_empty_data():
    """
    测试解析空数据的情况
    """
    # 测试空HTML内容
    assert len(parse_trending_repositories("")) == 0

    # 测试None值
    assert len(parse_trending_repositories(None)) == 0