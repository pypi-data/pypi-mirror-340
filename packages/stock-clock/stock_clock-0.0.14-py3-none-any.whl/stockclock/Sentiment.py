#%%
# 情绪面分析工具类
# 导入库
import requests 
import json

#%%
# ==== 新闻获取与情绪 ====
class NewsUtils:
    def __init__(self):
        pass


    # 获取当下的财经新闻
    # 获取当下的财经新闻
    @classmethod
    def get_news(cls,
                 header:str,
                 max_token:int=20,
                 temperature:float=0.5,
                 content:str="请在此处输入你的问题!!!"):
        url = "https://spark-api-open.xf-yun.com/v1/chat/completions"

        data = {
                    "max_tokens": max_token,
                    "temperature": temperature,
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是一个专业的财经分析师，对于重要的财经新闻非常了解，并且能够结合国际局势，国内政策和行业情况给出自己的见解；此外，你也了解一下没有那么热门的“独家”新闻,获取最新的财经消息，模仿专业的财经分析师，以财经分析报告的口吻简述，并给出自己的见解；此外，还需要为当前股市和金融市场的情绪进行评分；还有其他相关工作。"
                        },
                        {
                            "role": "user",
                            "content": content
                        }
                    ],
                    "model": "4.0Ultra"
        }

        data["stream"] = False

        header = {
            "Authorization": header
        }

        response = requests.post(url, headers=header, json=data, stream=True)

        # 流式响应解析示例
        response.encoding = "utf-8"
        
        # 返回结果
        return response.json()



    

# %%
