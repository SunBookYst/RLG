import streamlit as st
import requests
import time


url = "http://127.0.0.1:5000/"

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
        if 'reward' not in data:
            return data['text'], True
        else:
            st.write("恭喜你获得了：")
            st.write(data['reward'])
            return data['text'], False
    else:
        st.write("Error: Unable to communicate with the server.")
        return None


def end_task():
    st.session_state.condition = 0


if not st.session_state['logged_in']:
    st.write("尊敬的勇士，请先表明身份！")
    st.page_link("home_page.py", label="Go to login")
else:
    # 玩家此时并没有执行某个任务，进入任务选择界面
    if st.session_state.condition == 0:
        st.title('Tasks')
        st.write(f"{st.session_state['username']}, it's your turn!")
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
        st.write(st.session_state['play'])
        user_input = st.chat_input("Say something")
        if user_input:
            st.session_state.condition = 3
            st.session_state.user_input = user_input
            st.rerun()

    # 玩家选择了某个任务，开始初始化
    elif st.session_state.condition == 2:
        st.write("Initializing task...")
        time.sleep(0.5)
        st.session_state.condition = 4
        st.rerun()

    # 玩家提交了一段对话，等待系统回应
    elif st.session_state.condition == 3:
        st.write("Please wait")
        time.sleep(0.5)
        st.session_state.condition = 5
        st.rerun()

    elif st.session_state.condition == 4:
        play = select_task(st.session_state.task)
        st.session_state.focus_on_task = True
        st.session_state.play = play
        st.session_state.condition = 1
        st.rerun()

    elif st.session_state.condition == 5:
        if st.session_state.focus_on_task:
            st.session_state.play, st.session_state.focus_on_task = play_a_task(st.session_state.user_input)
            if st.session_state.focus_on_task:
                st.session_state.condition = 1
                st.rerun()
            else:
                st.write(st.session_state.play)
                if st.button("exit", on_click=end_task):
                    st.session_state.condition = 0
                    st.write("感谢您的努力，下次再会！")
                    time.sleep(1.5)
                    st.rerun()


