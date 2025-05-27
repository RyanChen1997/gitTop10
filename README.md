# 🚀 GitHub Top 10 - 每周热门项目自动抓取与总结

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/)
[![Project Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com/yourusername/github-top10)

自动获取每周 GitHub 上最热门的 10 个项目，生成的内容将以漂亮的 HTML 形式呈现。

![项目封面](https://github.com/RyanChen1997/gitTop10/blob/main/image/gittop10.jpg?raw=true)

## 特色功能：
1. 自动获取 GitHub 上最热门的 10 个项目。
2. 自动生成 HTML 文件，包含项目信息、描述、star 数、更新时间等信息。
3. 自动发送邮件。

## 使用方法：
### 1. 克隆仓库：
```bash
git clone https://github.com/yourusername/github-top10.git
```

### 2. 安装依赖：
使用uv安装依赖：
```bash
uv sync
```

### 3. 添加邮箱：
编辑`config.py`文件添加发送邮箱和密码
```py
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""
```
编辑`main.py`文件添加接受邮箱
```py
if __name__ == "__main__":
    # 直接运行时，发送到默认邮箱
    fetch_and_send_trending_repositories(["youremail@qq.com"])
```

### 4. 运行程序：
```bash
uv run main.py
```

## 未来计划
1. 添加AI总结的功能