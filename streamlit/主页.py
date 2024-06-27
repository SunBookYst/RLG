#streamlit run ./streamlit/主页.py --server.port 999 --server.enableXsrfProtection=false --server.maxUploadSize=1
# 初始化

import streamlit as st
import requests
import json
from utils import *

# # 初始化会话状态
# if 'logged_in' not in st.session_state:
#     st.session_state['logged_in'] = False
# if 'waiting' not in st.session_state:
#     st.session_state['waiting'] = False
# if 'generating' not in st.session_state:
#     st.session_state['generating'] = False
# if 'sign_up' not in st.session_state:
#     st.session_state['sign_up'] = False
# if 'chat_history' not in st.session_state:
#     st.session_state['chat_history'] = []
# if 'condition_cha' not in st.session_state:
#     st.session_state["condition_cha"] = 0

placeholder = play_music()

def login():
    """
    ? What is this about?
    """
    requests.get(url + 'register', 
                json={
        'name'   : st.session_state['username'],
        'feature': ""})


def chat_with_dm(user_input:str):
    """
    Talk with DM.
    Args:
        user_input: 用户输入
    """
    # 发送请求到 Flask 路由
    response = requests.get(url + 'main', json={
        'text': user_input,
        'role': st.session_state['username']
    })

    if response.status_code == 200:
        data = response.json()
        role = data['role']
        if role == None:
            role = "系统"
        user_message = f"{st.session_state['username']}: {user_input}"
        dm_message = f'{role}: {data["text"]}'
        st.session_state['chat_history'].append(user_message)
        st.session_state['chat_history'].append(dm_message)
    else:
        st.write("Error: Unable to communicate with the server.")


# 渲染登录页面
def show_login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title('RLG GAME')
        email = st.text_input('Email')
        password = st.text_input("Password", type="password")
        col2_1,col2_2 = st.columns([1, 1])
        with col2_1:
            login_button = st.button('Log in')
        with col2_2:
            signup_button = st.button('Sign up')

        if login_button and email and password :
            func = 'login'
            r = requests.get(url = url+func, json = {'email':email,'password':md5_encrypt(password),'ip':get_local_ip()+":"+get_local_port()})
            # r = json.loads(r.text)
            # try:
            r = json.loads(r.text)
            if r['status_code'] == 200:
                st.session_state['waiting'] = True
                st.session_state['username'] = r['username']
                save_base64_image_as_png(r["image_data"],ST_PATH+"/image/"+f"player_{st.session_state['username']}.png")
                st.rerun()
            else:
                st.write(f"登录出错，请检查，错误码是{r['status_code']}")
            # except:
                # st.write("与服务器的连接出错")
            # TODO 发送请求判断用户名与密码对应，待完善后台逻辑
            # st.session_state['waiting'] = True
            # st.session_state['username'] = username
            # st.rerun()  # 重新运行应用以更新页面内容
        if signup_button:
            st.session_state['sign_up'] = True
            st.rerun()

def show_signup_page():
    base64_image = None
    col1, col2, col3 = st.columns([1, 2, 1])
    uploaded_file = st.file_uploader("在此上传头像", type=["png", "jpg", "jpeg"])
    # if uploaded_file is not None:
        # image = Image.open(uploaded_file)
        # 压缩图片到100KB以内
        # compressed_image_data = compress_image(image, max_size_kb=200)
        # base64_image = image_to_base64(compressed_image_data)
    if uploaded_file is not None:
    # 将图片数据转换为 base64 格式
        base64_image = base64.b64encode(uploaded_file.read()).decode()
        # save_base64_image_as_png(base64_image,ST_PATH+"/image/"+f"player_{st.session_state['username']}.png")
    with col2:
        st.title('RLG GAME')
        email = st.text_input("Email")
        username = st.text_input('Username')
        password = st.text_input("Password", type="password")
        col_password, col_exclamation = st.columns([4, 1])
        with col_password:
            password2 = st.text_input("Confirm Password", type="password")
        with col_exclamation:
            if password != password2:
                st.write("Check!")
        col21, col22 = st.columns([1,1])
        with col21:
            signup_button = st.button('Sign up&Log in')
        with col22:
            login_button = st.button('Back')


        if signup_button and username and password and email and password==password2 and base64_image!=None:
            #TODO 发送请求判断判断是否可以注册，否则xxx，待完善后台逻辑
            # try:
            func = 'signup'
            r = requests.get(url = url+func, json = {'email':email,'username':username,'password':md5_encrypt(password),'ip':get_local_ip()+":"+get_local_port(),"image_data":base64_image})
            r = json.loads(r.text)
            if r['status_code']==200:
                st.session_state.username = username
                save_base64_image_as_png(base64_image,ST_PATH+"/image/"+f"player_{st.session_state['username']}.png")
                st.session_state['waiting'] = True
                st.session_state['username'] = username
                st.session_state['sign_up'] = False
                st.rerun()
            else:
                st.write(f"注册出错，请检查，错误码是{r['status_code']}")

        if login_button:
            st.session_state['sign_up'] = False
            st.rerun()

def show_waiting_page():
    st.title('欢迎来到苍穹大陆')


# 渲染欢迎页面
def show_welcome_page():
    # 设置背景图片和透明度
    image_path = ST_PATH + "/image/cover.png"
    opacity = 0.5  # 调节透明度，范围从 0 到 1
    set_background(image_path, opacity)
    st.title('欢迎来到苍穹大陆，')
    st.write(f'你好,{st.session_state["username"]}!')
    user_input = st.chat_input("说点什么")
    if user_input:
        disable_sidebar()
        chat_with_dm(user_input)
        enable_sidebar()
    for message in st.session_state['chat_history']:
        # st.write(message)
        role,text = parse_message(message)
        if role == st.session_state['username']:
            avatar_url = ST_PATH+f"/image/player_{st.session_state['username']}.png"  # 用户头像路径
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
    show_welcome_page()
elif st.session_state['waiting']:
    show_waiting_page()
    # login()
    st.session_state['waiting'] = False
    st.session_state['logged_in'] = True
    st.rerun()
elif st.session_state['sign_up']:
    show_signup_page()
else:
    show_login_page()



while True:
    if st.session_state["logged_in"]:
        refresh(st.session_state["username"],placeholder)
    time.sleep(5)







