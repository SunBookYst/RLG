# streamlit run ./streamlit/home_page.py
# 初始化

import streamlit as st
import requests
import json
import re

from utils import *

# 初始化会话状态
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'waiting' not in st.session_state:
    st.session_state['waiting'] = False
if 'generating' not in st.session_state:
    st.session_state['generating'] = False
if 'sign_up' not in st.session_state:
    st.session_state['sign_up'] = False
if 'chat_history_rq' not in st.session_state:
    st.session_state['chat_history_rq'] = []


def chat_with_dm(user_input):
    """
    与dm对话
    Args:
        user_input: 用户输入

    Returns:

    """
    # 发送请求到 Flask 路由
    response = requests.get(url + 'task_request', json={
        'text': user_input,
        'role': st.session_state['username']
    })

    if response.status_code == 200:
        data = response.json()
        role = data['role']
        if role == None:
            role = "系统"
        # user_message = f"{st.session_state['username']}: {user_input}"
        # dm_message = f'{role}: {data["text"]}'
        st.session_state['chat_history_rq'].append((st.session_state['username'],user_input))
        st.session_state['chat_history_rq'].append((role,data['text']))
    else:
        st.write("Error: Unable to communicate with the server.")


# 渲染对话页面
def show_main_page():
    # 设置背景图片和透明度
    image_path = ST_PATH + "/image/bg.png"
    opacity = 0.5  # 调节透明度，范围从 0 到 1
    set_background(image_path, opacity)
    st.title('欢迎来到苍穹大陆，')
    st.write(f'你好,{st.session_state["username"]}!')
    user_input = st.chat_input("说点什么")
    if user_input:
        chat_with_dm(user_input)
    for message in st.session_state['chat_history_rq']:
        # st.write(message)
        role,text = message
        if role == st.session_state['username']:
            avatar_url = ST_PATH+"/image/me.png"  # 用户头像路径
        else:
            avatar_url = ST_PATH+f"/image/{role}.png"  # DM头像路径
        try:
            with open(avatar_url, "rb") as avatar_file:
                avatar_base64 = base64.b64encode(avatar_file.read()).decode()
        except:
            print(f"{avatar_url}不存在！切换为系统头像")
            with open(ST_PATH+f"/image/系统.png" , "rb") as avatar_file:
                avatar_base64 = base64.b64encode(avatar_file.read()).decode()
        # 将头像和消息组合在一个 HTML 块中
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <img src="data:image/png;base64,{avatar_base64}" style="width: 60px; height: 60px; margin-right: 10px;">
                <div><strong>{role}:</strong> {text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    logout_button = st.button('退出登录')
    if logout_button:
        st.session_state['logged_in'] = False
        if 'user_name' in st.session_state:
            st.session_state['username'] = None
        st.rerun()  # 重新运行应用以更新页面内容


# 根据登录状态显示不同的页面
if st.session_state['logged_in']:
    show_main_page()
else:
    st.write("尊敬的勇士，请先表明身份！")
    st.page_link("主页.py", label="Go to login")






