import streamlit as st
from openai import OpenAI
import os

# 页面设置，只能调用一次，并且必须是第一个Streamlit命令
st.set_page_config(
    page_title = "ai智能伴侣",
    page_icon="😺",
    # 布局
    layout="wide",
    # 侧边栏状态
    initial_sidebar_state="expanded",
    # 菜单项
    # menu_items={}
)

# 创建与AI模型对话的client
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

# 系统提示词
system_prompt = ""

# 大标题
st.title("AI智能伴侣")
# logo
st.logo("./resources/mhy.png",size = "large")

# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

# 展示聊天信息
for message in st.session_state.messages: # {"role": "user", "content": prompt}
    # if message["role"] == "user":
    #     st.chat_message("user").write(message["content"])
    # else:
    #     st.chat_message("assistant").write(message["content"])
    #简化
    st.chat_message(message["role"]).write(message["content"])

# 消息输入框
prompt = st.chat_input("请输入你的问题")


if prompt:
    st.chat_message("user").write(prompt)
    print("提示词：",prompt)
    # 保存用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用AI模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    # 打印大模型返回的结果
    print("大模型返回的结果：",response.choices[0].message.content)
    st.chat_message("assistant").write(response.choices[0].message.content)
    # 保存大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
