import time
import streamlit as st
import requests
from utils import *

# 初始化 session_state 中的变量
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
if 'selected_items' not in st.session_state:
    st.session_state.selected_items = []
if 'roles_task' not in st.session_state:
    st.session_state.roles_task = ["系统"]

# 获取任务列表
def check_tasks():
    response = requests.get(url + 'task_info', json={
        'role': st.session_state['username']
    })

    if response.status_code == 200:
        data = response.json()
        st.session_state['task_list'] = data["task_list"]
    else:
        st.write("Error: Unable to get task list.")

# 选择任务
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

# 开始任务对话
def play_a_task(user_input, selected_items):
    response = requests.get(url + 'feedback', json={
        'role': st.session_state['username'],
        'text': user_input,
        'items': selected_items,
        'roles': st.session_state['roles_task']
    })

    if response.status_code == 200:
        data = response.json()
        role = data["role"]
        if role==None:
            role ="系统"
        if role not in st.session_state["roles_task"]:
            st.session_state["roles_task"].append(role)
            #TODO 接受图片并保存到相关路径下
            base64_image_data = data['image_data']
            if base64_image_data:
                # 解码 Base64 数据
                image_data = base64.b64decode(base64_image_data)
            output_path = ST_PATH+f"/image/{role}.png"  # 替换为实际的保存路径

            # 将解码后的数据保存为 PNG 格式的图片
            with open(output_path, "wb") as image_file:
                image_file.write(image_data)

        if 'reward' not in data:
            st.session_state['task_chat_history'].append((st.session_state['username'], user_input))
            st.session_state['task_chat_history'].append((role, data["text"]))
            return data['text'], True
        else:
            st.session_state['task_chat_history'].append((None, "恭喜你获得了："))
            st.session_state['task_chat_history'].append((None, str(data['reward'])))
            return data['text'], False
    else:
        st.write("Error: Unable to communicate with the server.")
        return None,False

# 结束任务,目前需要正常结束才可清除历史角色
def end_task():
    st.session_state.condition = 0
    for role in st.session_state.roles_task:
        os.remove(ST_PATH + f"/image/{role}.png")
    st.session_state.roles_task = []


# 获取背包信息
def get_bag_info():
    response = requests.get(url + 'bag', json={
        'role': st.session_state['username']
    })

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.write("Error: Unable to get bag info.")

# 获取技能信息
def get_skill_info():
    response = requests.get(url + 'skill', json={
        'role': st.session_state['username']
    })

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.write("Error: Unable to get skill info.")

# 主逻辑
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

    # 玩家选择了某个任务，开始初始化
    elif st.session_state.condition == 2:
        st.write("任务初始化中...")
        time.sleep(0.5)
        # st.session
        st.session_state.condition = 3
        st.rerun()
    # 玩家选择物品
    elif st.session_state.condition == 3:
        st.title("选择你要带入任务的物品 (最多10件)")
        bag_items = get_bag_info()['equipments']
        selected_items = st.session_state.selected_items

        # 显示背包物品并允许选择
        for item in bag_items:
            if st.checkbox(item, key=item):
                if item not in selected_items:
                    selected_items.append(item)
            else:
                if item in selected_items:
                    selected_items.remove(item)

        st.write(f"已选择的物品: {selected_items}")

        # 限制选择的物品数量
        if len(selected_items) > 10:
            st.error("你最多只能选择10件物品！")
        else:
            if st.button("确认并开始任务"):
                st.session_state.condition = 4
                st.rerun()

    # 任务初始化完成，进入任务对话界面
    elif st.session_state.condition == 4:
        play = select_task(st.session_state.task)
        st.session_state.focus_on_task = True
        st.session_state.play = play
        st.session_state.condition = 1
        st.session_state['task_chat_history'].append(("系统", st.session_state['play']))
        st.rerun()

    # 玩家此时正在游玩某个任务，进入与任务系统的对话界面
    elif st.session_state.condition == 1:
        image_path = ST_PATH + "/image/task1.png"
        opacity = 0.5  # 调节透明度，范围从 0 到 1
        set_background(image_path, opacity)

        # 显示对话历史
        for message in st.session_state['task_chat_history']:
            role, text = message
            if role is not None:
                if role == st.session_state['username']:
                    avatar_url = ST_PATH + "/image/me.png"  # 用户头像路径
                else:
                    avatar_url = ST_PATH + f"/image/{role}.png"  # DM头像路径
                try:
                    with open(avatar_url, "rb") as avatar_file:
                        avatar_base64 = base64.b64encode(avatar_file.read()).decode()
                except:
                    print(f"{avatar_url}不存在！切换为系统头像")
                    with open(ST_PATH + f"/image/系统.png", "rb") as avatar_file:
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
            else:
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <div>{text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # 在右侧栏显示带入任务的装备列表并允许选择
        with st.sidebar:
            st.title("任务装备")
            selected_items = st.session_state.selected_items
            for item in selected_items:
                st.checkbox(item, key=f"sidebar_{item}", value=True, disabled=True)

            # 允许在任务中选择装备
            st.write("在任务中选择的装备:")
            selected_task_items = []
            for item in selected_items:
                if st.checkbox(item, key=f"task_{item}"):
                    selected_task_items.append(item)
            st.session_state.selected_task_items = selected_task_items
            st.write(f"已选择的任务装备: {selected_task_items}")

        user_input = st.chat_input("说点什么")
        if user_input:
            st.session_state.user_input = user_input
            if st.session_state.focus_on_task:
                st.session_state.play, st.session_state.focus_on_task = play_a_task(
                    st.session_state.user_input,
                    st.session_state.selected_task_items
                                    )
                if st.session_state.focus_on_task:
                    st.session_state.condition = 1
                    st.rerun()
                else:
                    if st.button("exit", on_click=end_task):
                        st.session_state.condition = 0
                        st.write("感谢您的努力，下次再会！")
                        time.sleep(1.5)
                        st.rerun()