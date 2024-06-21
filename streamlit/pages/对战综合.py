import streamlit as st
import requests
import streamlit.components.v1 as components

from utils import *

if "challenage_over" not in st.session_state:
    st.session_state["challenage_over"] = False

def battle_with_other(user_input):
    response = requests.get( url + 'battle', json = {
        'role': st.session_state["username"],
        'action': user_input
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
    st.title("战斗，爽!")

    with open(ST_PATH+f"/image/系统.png" , "rb") as avatar_file:
        avatar_base64 = base64.b64encode(avatar_file.read()).decode()

    for message in st.session_state["battle_history"]:
        name, action = message["role"], message["text"]

        if name == 'Player1':
            components.html(
                html_local_player.format(content = action, avatar_base64 = avatar_base64),
                height=50
            )
        elif name == 'Player2':
            components.html(
                html_remote_player.format(content = action, avatar_base64 = avatar_base64),
                height=50
        )
        else:
            st.caption(action)
    if st.session_state.challenage_over == True:
        if st.button("返回用户列表"):
            st.session_state.condition_cha = 0
            st.rerun()


    user_input = st.chat_input("输入你的行动!")

    if user_input:
        battle_with_other(user_input)

# 主逻辑
if not st.session_state['logged_in']:
    st.write("尊敬的勇士，请先表明身份！")
    st.page_link("主页.py", label="Go to login")
else:
    # try:
    r = requests.get(url = url+"get_list", json={"role":st.session_state["username"]})
    r = r.json()
    st.session_state["online_roles"] = r["roles"]
    # except:
        # st.session_state["online_roles"] = []

    if st.session_state.condition_cha == 0:
        st.title('Tasks')
        st.write(f"{st.session_state['username']}, 当前在线用户,点击以发起挑战")
        # check_tasks()
        if st.button("查看挑战请求"):
            st.session_state.condition_cha = 1
        if len(st.session_state['online_roles']) == 0:
            st.write("暂无其他在线用户")
        else:
            for role in st.session_state['online_roles']:
                if st.button(role):
                    #发起挑战
                    r = requests.get(url=url+"/challenge",json = {'role1':st.session_state['username'],'role2':role,'image_data':None})
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
                            st.session_state["condition_cha"] = 2 #转入对话页面
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

    # elif st.session_state.condition_cha == 2:
        # render_battle_history() #其余内容暂时放入utils内

while True:
    if st.session_state.condition_cha == 2:
        render_battle_history()
    if st.session_state["logged_in"]:
        refresh(st.session_state["username"])
    time.sleep(5)


