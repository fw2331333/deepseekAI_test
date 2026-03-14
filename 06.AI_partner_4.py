import streamlit as st
from openai import OpenAI
import os
import datetime
import json
import re

# 页面设置，只能调用一次，并且必须是第一个Streamlit命令
st.set_page_config(
    page_title="ai智能伴侣",
    page_icon="😺",
    # 布局
    layout="wide",
    # 侧边栏状态
    initial_sidebar_state="expanded",
    # 菜单项
    # menu_items={}
)


def save_session():
    # 如果没有当前会话，则不保存
    if not st.session_state.current_session:
        return

    # 创建会话数据
    session_data = {
        "partner_name": st.session_state.partner_name,
        "nature": st.session_state.nature,
        "messages": st.session_state.messages,
        "current_session": st.session_state.current_session
    }

    # 如果不存在，则创建新的会话
    if not os.path.exists("sessions"):
        os.mkdir("sessions")

    with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=4)


# 加载所有会话
def load_sessions():
    session_list = []
    # 加载sessions目录下的所有会话
    if os.path.exists("sessions"):
        for filename in os.listdir("sessions"):
            if filename.endswith(".json"):
                # 正则匹配文件名，获取会话名称
                match = re.match(r'(.+?)\.json$', filename, re.IGNORECASE)
                if match:
                    session_list.append(match.group(1))
    return session_list

# 会话标识
def get_session_id():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# 加载会话信息
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            # 读取会话数据
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.partner_name = session_data["partner_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.messages = session_data["messages"]
                st.session_state.current_session = session_data["current_session"]
    except FileNotFoundError:
        st.error("会话不存在")

# 删除会话
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            # 删除当前会话，则更新消息列表
            if st.session_state.current_session == session_name:
                st.session_state.messages = []
                st.session_state.current_session = get_session_id()

    except Exception:
        st.error("会话不存在")


# 创建与AI模型对话的client
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

# 大标题
st.title("AI智能伴侣")
# logo
st.logo("./resources/mhy.png", size="large")

# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

# 昵称
if "partner_name" not in st.session_state:
    st.session_state.partner_name = "汤包"

# 性格
if "nature" not in st.session_state:
    st.session_state.nature = "温柔"

# 会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = get_session_id()

# # 当前会话标记
# if "current_session" not in st.session_state:
#     st.session_state.current_session = False

# 系统提示词
system_prompt = f"""
        你叫{st.session_state.partner_name},
        你是一个具有{st.session_state.nature}性格的AI智能伴侣，
        你的任务是帮助用户解决各种问题，
        请用中文回答问题
"""

# 展示聊天信息
st.text(f"会话名称: {st.session_state.current_session}")
for message in st.session_state.messages:  # {"role": "user", "content": prompt}
    # if message["role"] == "user":
    #     st.chat_message("user").write(message["content"])
    # else:
    #     st.chat_message("assistant").write(message["content"])
    # 简化
    st.chat_message(message["role"]).write(message["content"])

# 侧边栏 - with: streamlit中上下文管理器
with (st.sidebar):
    # 会话信息
    st.subheader("AI控制按钮")

    # 新建会话按钮
    if st.button("新建会话", use_container_width=True, icon="📝"):
        # 先保存当前会话（包含 messages）
        if st.session_state.current_session and st.session_state.messages:
            save_session()
        
        # 创建新的会话
        st.session_state.messages = []
        st.session_state.current_session = get_session_id()
        st.rerun()  # 重新运行当前页面

    # 会话历史
    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        # st.button("新建会话", use_container_width=True, icon="🕓")
        # st.button("新建会话", use_container_width=True, icon="❌")
        col1,col2 = st.columns([4, 1])
        with col1:
            # 加载会话
            if st.button(session,icon="🕓",key=f"load_{session}",type="primary" if st.session_state.get("current_session") == session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            # 删除会话
            if st.button("",icon="❌",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()
    # 伴侣信息
    st.subheader("伴侣信息")
    partner_name = st.text_input("昵称", placeholder="请输入昵称", value=st.session_state.partner_name)
    if partner_name:
        st.session_state.partner_name = partner_name
    nature = st.text_area("性格", placeholder="请输入性格", value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature

# 消息输入框
prompt = st.chat_input("请输入你的问题")

if prompt:
    st.chat_message("user").write(prompt)
    print("提示词：", prompt)
    # 保存用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用AI模型

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
        ],
        stream=True
    )
    # 打印大模型返回的结果(非流式输出）
    # print("大模型返回的结果：",response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)
    # 流式输出
    response.message = st.empty()  # 创建一个空的消息框
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response.message.chat_message("assistant").write(full_response)

    # 保存大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_session()