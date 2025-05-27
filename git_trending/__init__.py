from dataclasses import dataclass


@dataclass
class Repository:
    """
    用于存储仓库信息的类
    """

    name: str  # 仓库名称
    description: str  # 仓库描述
    language: str  # 主要编程语言
    stars: str  # 星标数
    today_stars: str  # 今日星标数
    rank: int = 0  # 排名（在列表中的位置）
    url: str = ""  # 仓库地址
    summary: str = ""  # 仓库摘要
