import streamlit as st
import requests
import streamlit.components.v1 as components

from utils import *

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'condition_cha' not in st.session_state:
    st.session_state.condition_cha = 0
if 'task_cha' not in st.session_state:
    st.session_state.task_cha = ""
if 'user_input_cha' not in st.session_state:
    st.session_state.user_input_cha = ""
if 'task_list_cha' not in st.session_state:
    st.session_state.task_list = []
if 'focus_on_task_cha' not in st.session_state:
    st.session_state.focus_on_task_cha = False
if 'task_chat_history_cha' not in st.session_state:
    st.session_state['task_chat_history_cha'] = []
if 'selected_items_cha' not in st.session_state:
    st.session_state.selected_items_cha = []
if 'selected_items_tmp_cha' not in st.session_state:
    st.session_state.selected_items_tmp_cha = []
if 'selected_skills_cha' not in st.session_state:
    st.session_state.selected_skills_cha = []
if 'selected_skills_tmp_cha' not in st.session_state:
    st.session_state.selected_skills_tmp_cha = []

placeholder = play_music()

if "challenage_over" not in st.session_state:
    st.session_state["challenage_over"] = False

def battle_with_other(user_input):
    response = requests.get( url + 'battle', json = {
        'role': st.session_state["username"],
        'action': user_input,
        'id':st.session_state.battle_id,
        'items':st.session_state.selected_items_tmp_cha if "不使用装备" not in st.session_state.selected_items_tmp_cha else [],
        'skills':st.session_state.selected_skills_tmp_cha if "不使用技能" not in st.session_state.selected_skills_tmp_cha else [],
    })
    if response.status_code == 200:
        response = response.json()

        round = [
            {
                "role": st.session_state["username"],
                "text": user_input
            },
            {
                "role": response["role"],
                "text": response["action"]
            },
            {
                "role": "system",
                "text": response["result"]
            }
        ]
        if response["status"] == True:
            st.session_state.challenage_over = True
        try:
            assert response['status_code']==200
        except Exception as e:
            print(e)
        st.session_state["battle_history"] += round

def render_battle_history():
    st.title("正在掐架中...")

    # with open(ST_PATH+f"/image/me.png" , "rb") as avatar_file:
    #     me_avatar_base64 = base64.b64encode(avatar_file.read()).decode()
    # with open(ST_PATH+f"/image/me.png" , "rb") as avatar_file:
    #     other_avatar_base64 = base64.b64encode(avatar_file.read()).decode()

    # for message in st.session_state["battle_history"]:
    #     name, action = message["role"], message["text"]

    #     if name == st.session_state['username']:
    #         components.html(
    #             html_local_player.format(content = action, avatar_base64 = me_avatar_base64),
    #             height=50
    #         )
    #     elif name != "System":
    #         components.html(
    #             html_remote_player.format(content = action, avatar_base64 = other_avatar_base64),
    #             height=50
    #     )
    #     else:
    #         st.caption(action)
    for message in st.session_state['battle_history']:
        role, text = message['role'],message['text']
        if role is not None and role!="system":
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
            st.markdown(
                f'<div style="display: flex; align-items: center; margin-bottom: 10px;">'
                f'<img src="data:image/png;base64,{avatar_base64}" style="width: 60px; height: 60px; margin-right: 10px;">'
                f'<div><strong>{role}:</strong> {text}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(f'**{text}**')
    if st.session_state.challenage_over == True:
        if st.button("返回用户列表"):
            st.session_state.condition_cha = 0
            st.rerun()


    user_input = st.chat_input("输入你的行动!")

    if user_input:
        battle_with_other(user_input)

# 结束任务,目前需要正常结束才可清除历史角色
def end_task():
    st.session_state.condition_cha = 0
    # for role in st.session_state.roles_task_cha:
        # if role!="系统":
            # os.remove(ST_PATH + f"/image/{role}.png")
    # st.session_state.roles_task_cha = []

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
    # try:
    r = requests.get(url = url+"get_list", json={"role":st.session_state["username"]})
    r = r.json()
    st.session_state["online_roles"] = r["roles"]

    if st.session_state.condition_cha == 0:
        st.title('Tasks')
        st.write(f"{st.session_state['username']}, 当前其他在线用户,点击以发起挑战")
        # check_tasks()
        if st.button("查看挑战请求"):
            st.session_state.condition_cha = 1
            st.rerun()
        if len(st.session_state['online_roles']) == 0:
            st.write("暂无其他在线用户")
        else:
            for role in st.session_state['online_roles']:
                if role == st.session_state['username']:
                    continue
                if st.button(role):
                    #发起挑战
                    r = requests.get(url=url+"challenge",json = {'role1':st.session_state['username'],'role2':role,'image_data':None})
                    r = r.json()
                    if r["status_code"] == 200:
                        st.write("发起成功")
                    else:
                        st.write(f"错误码{r['status_code']}")

                    # st.rerun()
    elif st.session_state.condition_cha == 1:
        st.write("挑战请求")
        if st.button("返回在线列表"):
            st.session_state.condition_cha = 0
            st.rerun()
        col1, col2, col3 = st.columns([2, 1, 1])
        for idx,name in enumerate(st.session_state["role_list"]):
            with col1:
                st.write(name)
            with col2:
                if st.button(f"接受", key=f"accept_{name}"):
                    st.write(f"你接受了{name}")
                    try:
                        r = requests.get(url = url+"/accept_challenge",json={"role":st.session_state["username"],"id":st.session_state["id_list"][idx]})
                        r = r.json()
                        if r["status_code"]==200:
                            st.session_state["condition_cha"] = 3 #转入对话页面
                            st.session_state["battle_id"] = st.session_state["id_list"][idx]
                            st.session_state["battle_history"] = []
                            st.rerun()
                    except Exception as e:
                        print(e)

            with col3:
                if st.button(f"拒绝", key=f"reject_{name}"):
                    st.write(f"你拒绝了{name}")
                    try:
                        r = requests.get(url = url+"/reject_challenge",json={"role":st.session_state["username"],"id":st.session_state["id_list"][idx]})
                    except Exception as e:
                        print(e)
    # 玩家选择物品
    elif st.session_state.condition_cha == 3:
        st.title("选择你要带入任务的物品 (最多5件)")
        bag_items = get_bag_info()['equipments']
        selected_items = st.session_state.selected_items_cha

        # 显示背包物品并允许选择
        for item in bag_items:
            if st.checkbox(item, key=item):
                if item not in selected_items:
                    selected_items.append(item)
            else:
                if item in selected_items:
                    selected_items.remove(item)

        st.write(f"已选择的物品: {selected_items}")
        # selected_items.append("不使用装备") #NOTE
        # 限制选择的物品数量
        if len(selected_items) > 5:
            st.error("你最多只能选择5件物品！")
        else:
            if st.button("确认并选择技能"):
                selected_items.append("不使用装备") #NOTE
                st.session_state.condition_cha = 5
                st.rerun()

    # 玩家选择技能
    elif st.session_state.condition_cha == 5:
        st.title("选择你要带入任务的技能 (最多5个)")
        skill_items = get_skill_info()['skills']
        selected_skills = st.session_state.selected_skills_cha

        # 显示技能并允许选择
        for skill in skill_items:
            if st.checkbox(skill, key=skill):
                if skill not in selected_skills:
                    selected_skills.append(skill)
            else:
                if skill in selected_skills:
                    selected_skills.remove(skill)

        st.write(f"已选择的技能: {selected_skills}")
        # selected_skills.append("不使用技能")  #NOTE
        # 限制选择的技能数量
        if len(selected_skills) > 5:
            st.error("你最多只能选择5个技能！")
        else:
            if st.button("确认并进入对战"):
                selected_skills.append("不使用技能")
                st.session_state.condition_cha = 2
                st.rerun()
    elif st.session_state.condition_cha == 2:
        image_path = ST_PATH + f"/image/cover.png"
        opacity = 0.5  # 调节透明度，范围从 0 到 1
        try:
            set_background(image_path, opacity)
        except:
            image_path = ST_PATH + "/image/cover.png"
            set_background(image_path, opacity)

        render_battle_history()

        st.session_state.selected_skills_tmp_cha = []
        st.session_state.selected_items_tmp_cha = []
        st.sidebar.title("本轮使用")  # TODO
        st.sidebar.subheader("物品")
        selected_items = st.session_state.selected_items_cha

        selected_item = st.sidebar.radio("", selected_items, key="selected_item")

        # 更新临时选择的项目列表
        st.session_state.selected_items_tmp_cha = [selected_item] if selected_item else []

        st.sidebar.subheader("技能")
        selected_skills = st.session_state.selected_skills_cha
        selected_skill = st.sidebar.radio("", selected_skills, key="selected_skill")
        # 更新临时选择的项目列表
        st.session_state.selected_skills_tmp_cha = [selected_skill] if selected_skill else []
        if st.session_state.challenage_over == True:
            if st.button("结束战斗"):
                end_task()

while True:
    # if st.session_state.condition_cha == 2:
        # render_battle_history()
    if st.session_state["logged_in"]:
        refresh(st.session_state["username"],placeholder)
    time.sleep(5)
    st.rerun()


