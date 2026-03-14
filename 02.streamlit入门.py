import streamlit as st


# 页面设置
st.set_page_config(
    page_title = "streamlit入门",
    page_icon="🧊",
    # 布局
    layout="centered",
    # 侧边栏状态
    initial_sidebar_state="expanded",
    # 菜单项
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# 关注火花喵~"
    }
)

# 标题
st.title('Hello World')
st.header('Streamlit 一级标题')
st.subheader('Streamlit 二级标题')

# 段落文字
st.write("关注火花喵")
st.write("关注火花谢谢喵")
st.write("关注火花喵喵喵")

# logo
st.logo("./resources/mhy.png",size = "large")

# 图片
st.image("./resources/huohua.png")

# 音频
st.audio("./resources/还是会想你.mp3")

# 视频
st.video("./resources/小半.mp4")

# 表格
student_data = {
    "姓名": ["小王","小李","小张"],
    "学号": [1001,1002,1003],
    "性别": ["男","女","男"],
    "年龄": [18,19,20]
}
st.table(student_data)

# 输入框
name = st.text_input("请输入姓名")
st.write(f"您输入的姓名为：{name}")

password = st.text_input("请输入密码",type = "password")
st.write(f"您输入的密码为：{password}")

# 单选按钮
sex = st.radio("请选择性别",["男","女","未知"],index = 2)
st.write(f"您选择的性别为：{sex}")



