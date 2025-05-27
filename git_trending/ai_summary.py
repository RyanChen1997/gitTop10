import os
from openai import OpenAI

class AISummary:
    """AI摘要生成类，用于通过OpenAI API生成仓库说明文档的摘要"""
    
    def __init__(self, api_key=None):
        """初始化时加载OpenAI的API密钥"""
        if api_key is None:
            self.api_key = os.getenv('OPENAI_API_KEY')
        else:
            self.api_key = api_key
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables.")
        self.client = OpenAI(
            # 此为默认路径，您可根据业务所在地域进行配置
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            # 从环境变量中获取您的 API Key
            api_key=self.api_key,
        )
    
    def summarize_readme(self, text: str) -> str:
        """
        使用OpenAI Chat API对提供的文本生成摘要，专注于GitHub仓库描述和功能总结。
        
        参数:
            text (str): 需要总结的原始文本。
        
        返回:
            str: 由模型生成的摘要，控制在150字以内。
        """
        try:
            response = self.client.chat.completions.create(
                model="doubao-1-5-pro-32k-250115",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "你是一个专业的项目摘要生成器。你的任务是阅读项目的README内容，"
                            "并生成一个简洁明了的中文摘要，重点突出该项目的功能、用途和技术栈。"
                            "请将字数控制在150字以内，避免使用Markdown格式。"
                        ),
                    },
                    {
                        "role": "user",
                        "content": text,
                    },
                ],
                temperature=0.4,
                n=1,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error occurred while summarizing: {e}")
            return ""