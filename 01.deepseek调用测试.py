# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI

# 创建与AI模型对话的client
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)
# 创建与AI模型对话
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是AI助理"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)
# 打印结果
print(response.choices[0].message.content)