# streamlit run ./streamlit/home_page.py
# 初始化
url = "http://127.0.0.1:5000/"

import streamlit as st
import requests
import json

# 初始化会话状态
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'waiting' not in st.session_state:
    st.session_state['waiting'] = False
if 'generating' not in st.session_state:
    st.session_state['generating'] = False


def login():
    """
    登录
    Returns:

    """
    _ = requests.get(url + 'register', json={
        'name': st.session_state['username'],
        'feature': ""
    })


def chat_with_dm(user_input):
    """
    与dm对话
    Args:
        user_input: 用户输入

    Returns:

    """
    # 发送请求到 Flask 路由
    response = requests.get(url + 'main', json={
        'text': user_input,
        'role': st.session_state['username']
    })

    if response.status_code == 200:
        data = response.json()
        st.write(f'You said: {user_input}')
        st.write(f'Response: {data["text"]}')
    else:
        st.write("Error: Unable to communicate with the server.")


# 渲染登录页面
def show_login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title('Login Page')
        username = st.text_input('Enter your username')
        login_button = st.button('Login')

        if login_button and username:
            st.session_state['waiting'] = True
            st.session_state['username'] = username
            st.rerun()  # 重新运行应用以更新页面内容


def show_waiting_page():
    st.write("欢迎来到【苍穹】大陆！")


# 渲染欢迎页面
def show_welcome_page():
    st.title('Welcome Page')
    st.write(f'Welcome, {st.session_state["username"]}!')
    st.write('This is the next page.')
    # 添加对话框
    st.write("Chat with us:")
    user_input = st.chat_input("Say something")
    if user_input:
        chat_with_dm(user_input)
    else:
        st.write("Please enter a message.")

    logout_button = st.button('Logout')
    if logout_button:
        st.session_state['logged_in'] = False
        if 'user_name' in st.session_state:
            st.session_state['username'] = None
        st.rerun()  # 重新运行应用以更新页面内容


# 根据登录状态显示不同的页面
if st.session_state['logged_in']:
    show_welcome_page()
else:
    if st.session_state['waiting']:
        show_waiting_page()
        login()
        st.session_state['waiting'] = False
        st.session_state['logged_in'] = True
        st.rerun()
    else:
        show_login_page()







