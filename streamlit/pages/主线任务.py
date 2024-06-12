import time

import streamlit as st
import requests

from utils import *


if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'condition' not in st.session_state:
    st.session_state.condition = 0
if 'task' not in st.session_state:
    st.session_state.task = ""
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'task_list' not in st.session_state:
    st.session_state.task_list = []
if 'focus_on_task' not in st.session_state:
    st.session_state.focus_on_task = False
if 'task_chat_history' not in st.session_state:
    st.session_state['task_chat_history'] = []


def check_tasks():
    response = requests.get(url + 'task_info', json={
        'role': st.session_state['username']
    })

    if response.status_code == 200:
        data = response.json()
        st.session_state['task_list'] = data["task_list"]
    else:
        st.write("Error: Unable to get task list.")


def select_task(task_name):
    response = requests.get(url + 'select', json={
        'role': st.session_state['username'],
        'task_name': task_name
    })

    if response.status_code == 200:
        data = response.json()
        return data['text']
    else:
        st.write("Error: Unable to select this task.")


def play_a_task(user_input):
    """
    与任务系统进行一轮对话
    Args:
        user_input:

    Returns:
    """
    response = requests.get(url + 'feedback', json={
        'role': st.session_state['username'],
        'text': user_input
    })

    if response.status_code == 200:
        data = response.json()
        role = data["role"]
        if role==None:
            role = "系统"
        user_message = f"{st.session_state['username']}: {user_input}"
        dm_message = f'{role}: {data["text"]}'
        if 'reward' not in data:
            st.session_state['task_chat_history'].append(user_message)
            st.session_state['task_chat_history'].append(dm_message)
            return data['text'], True
        else:
            st.session_state['task_chat_history'].append(user_message)
            st.session_state['task_chat_history'].append(dm_message)
            st.session_state['task_chat_history'].append("恭喜你获得了：")
            st.session_state['task_chat_history'].append(data['reward'])
            return data['text'], False
    else:
        st.write("Error: Unable to communicate with the server.")
        return None


def end_task():
    st.session_state.condition = 0


if not st.session_state['logged_in']:
    st.write("尊敬的勇士，请先表明身份！")
    st.page_link("主页.py", label="Go to login")
else:
    # 玩家此时并没有执行某个任务，进入任务选择界面
    if st.session_state.condition == 0:
        st.title('Tasks')
        st.write(f"{st.session_state['username']}, 请选择你的任务!")
        check_tasks()
        if len(st.session_state['task_list']) == 0:
            st.write("正在寻找任务...")
        else:
            for task in st.session_state['task_list']:
                if st.button(task):
                    st.session_state.condition = 2
                    st.session_state.task = task
                    st.rerun()

    # 玩家此时正在游玩某个任务，进入与任务系统的对话界面
    elif st.session_state.condition == 1:
        image_path = ST_PATH + "/image/task1.png"
        opacity = 0.5  # 调节透明度，范围从 0 到 1
        set_background(image_path, opacity)
        for message in st.session_state['task_chat_history']:
            # st.write(message)
            role,text = parse_message(message)
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
                    <img src="data:image/png;base64,{avatar_base64}"
                        style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;">
                    <div><strong>{role}:</strong> {text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        user_input = st.chat_input("说点什么")
        if user_input:
            # st.session_state.condition =
            st.session_state.user_input = user_input
            if st.session_state.focus_on_task:
                st.session_state.play, st.session_state.focus_on_task = play_a_task(st.session_state.user_input)
                # st.session_state['task_chat_history'].append(st.session_state.play)
                if st.session_state.focus_on_task:
                    st.session_state.condition = 1
                    st.rerun()
                else:
                    # st.write(st.session_state.play)
                    if st.button("exit", on_click=end_task):
                        st.session_state.condition = 0
                        st.write("感谢您的努力，下次再会！")
                        time.sleep(1.5)
                        st.rerun()

    # 玩家选择了某个任务，开始初始化
    elif st.session_state.condition == 2:
        st.write("任务初始化中...")
        time.sleep(0.5)
        st.session_state.condition = 3
        st.rerun()

    elif st.session_state.condition == 3:
        play = select_task(st.session_state.task)
        st.session_state.focus_on_task = True
        st.session_state.play = play
        st.session_state.condition = 1
        st.session_state['task_chat_history'].append(st.session_state['play'])
        st.rerun()



