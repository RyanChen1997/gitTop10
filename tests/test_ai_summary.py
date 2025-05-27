import pytest
from unittest.mock import patch, MagicMock

from git_trending.ai_summary import AISummary

@pytest.fixture
def mock_api_key():
    """为测试提供一个模拟的 API 密钥"""
    return "fake_openai_api_key"

def test_summarize_readme_success(mock_api_key):
    """测试 summarize_readme 成功返回摘要"""
    # 模拟 OpenAI 返回的响应数据
    mock_choice = MagicMock()
    mock_choice.message.content = "这是一个项目README的简明摘要。"

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with patch("git_trending.ai_summary.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        summarizer = AISummary(api_key=mock_api_key)
        result = summarizer.summarize_readme("原始 README 内容")

        assert result is not None
        assert "这是一个项目README的简明摘要" in result

def test_summarize_readme_with_empty_text(mock_api_key):
    """测试传入空文本时返回空字符串"""
    summarizer = AISummary(api_key=mock_api_key)
    result = summarizer.summarize_readme("")
    assert result == ""

def test_summarize_readme_failure(mock_api_key):
    """测试 OpenAI 接口异常时返回空字符串"""
    with patch("git_trending.ai_summary.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client

        summarizer = AISummary(api_key=mock_api_key)
        result = summarizer.summarize_readme("原始 README 内容")

        assert result == ""

def test_summarize_readme_from_file():
    with open("tests/mock_data/test_repo_readme.md", "r") as f:
        text = f.read()
    
    summarizer = AISummary()
    result = summarizer.summarize_readme(text)
    print(result)
    assert result is not None