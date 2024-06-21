import os
import base64
import re
import time
import streamlit as st
import hashlib
import socket
import subprocess
import sys
import requests

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from util.constant import FLASK_SERVER

def md5_encrypt(password):
    # 创建一个 MD5 hash 对象
    md5_hash = hashlib.md5()
    
    # 更新 hash 对象，传入需要加密的密码（需要编码为字节）
    md5_hash.update(password.encode('utf-8'))
    
    # 获取加密后的十六进制字符串
    encrypted_password = md5_hash.hexdigest()
    
    return encrypted_password


def set_background(image_path, opacity):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, {opacity}), rgba(255, 255, 255, {opacity})),
                        url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def disable_sidebar():
    '''
    在等待系统交互的时候禁用侧边切换，以避免发生一些不可知的错误
    '''
    st.sidebar.markdown("<style>div[role='tablist'] {pointer-events: none;}</style>", unsafe_allow_html=True)


def enable_sidebar():
    '''
    系统交互结束后的时候重新启用侧边切换
    '''
    st.sidebar.markdown("<style>div[role='tablist'] {pointer-events: auto;}</style>", unsafe_allow_html=True)


def parse_message(message):
    """
    解析消息字符串，提取 role 和 text
    Args:
        message: 消息字符串，形如 "role: text"

    Returns:
        role: 角色
        text: 消息内容
    """
    match = re.match(r"([^:]+):\s*(.*)", message)
    if match:
        return match.group(1), match.group(2)
    else:
        return "系统", message
def get_local_ip():
    if '_self_ip' not in st.session_state:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        st.session_state['_self_ip'] = str(local_ip)
    return st.session_state['_self_ip']

def get_local_port():
    if '_self_port' not in st.session_state:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 0))
        port = sock.getsockname()[1]
        sock.close()
        st.session_state['_self_port'] = str(port)
    return st.session_state['_self_port']

def start_flask_server(port):
    server_process = subprocess.Popen(["python", "flask_server.py", get_local_port()])
    return server_process

# ip, port = FLASK_SERVER
ip = "10.43.104.129"
port = "5000"

if ip == "0.0.0.0":
    ip = "127.0.0.1"

url = f"http://{ip}:{port}/"
ST_PATH = os.path.split(os.path.realpath(__file__))[0]

def refresh(role):
    # pass
    if "battle_id" not in st.session_state:
        battle_id = None
    else:
        battle_id = st.session_state.battle_id 
    r = requests.get(url=url+"/refresh",json={'role':role,"battle_id":battle_id})
    r = r.json()
    st.session_state.id_list = r['id_list']
    st.session_state.role_list = r['role_list']
    st.session_state.accept_id = r['accept_id']
    if len(st.session_state.accept_id)>0:
        st.session_state.condition_cha = 2
        st.session_state.battle_id = st.session_state.accept_id[0]
        st.session_state.battle_history = []
    if len(st.session_state.id_list)>0:
        st.sidebar.markdown(f"### Challenge Info 🔴")
    if r['role']!=None:
        st.session_state.battle_history.append({'role':r['role'],"text":r["role_text"]})
        st.session_state.battle_history.append({'role':"System","text":r["system_text"]})



def check_init_state(attributes:dict):
    """
    
    For a more controllable, understandable way to make initialization.

    Args:
        attributes (dict{str:Any}): the attributes used in the st.

    Return:
        None.

    Raises:
        ValueError: If the key is not a string.
    """

    for key,value in attributes.items():
        if type(key) != str:
            raise KeyError("Invalid attribution settings.")
        if key not in st.session_state:
            st.session_state[key] = value

fake_dailoge = [
    {
        "role":"Player1",
        "text":"我决定让对手肚子痛！"
    },
    {
        "role":"Player2",
        "text":"我决定让对手手脚抽筋"
    },
    {
        "role":"System",
        "text":"Player1 和 Player2 分别使出了自己的独家绝学，尽管 Player2 感到腹中不适，他捂住肚子，开始想办法治疗自己，而 Player1 手脚突然抽痛，差点站不起来，Player1 难以维持一个适合战斗的状态！"
    },
    {
        "role":"Player1",
        "text":"我决定用大剑砍过去！"
    },
    {
        "role":"Player2",
        "text":"我决定射出知音箭！"
    },
    {
        "role":"System",
        "text":"Player2 射出了知音箭，知音箭箭如其名，带着音爆冲向 Player1, 但 Player1 用他的剑挡住了这一击！ Player1 将箭弹开后，一剑刺了过去！ Player2 堪堪躲开，然而手臂却不慎被割到，一两滴鲜血冒了出来。"
    },
]

battle_attributes = {
    "logged_in"     : False,
    "waiting"       : False,
    "Generating"    : False,
    "battle_history": fake_dailoge,
    "username": "ADMIN"
}



check_init_state(battle_attributes)

html_local_player = '''
<style>
.row-2{{
    position: relative;
    width: 95%;
    color: #fff;
    line-height: 1.4rem;
    font-size:large;
    word-wrap: break-word;
    border: 1px solid teal;
    border-radius: 10px;
    background: teal;
    padding: 0.5rem;
}}
.row-2::after{{
    content: '';
    position: absolute;
    width: 0;
    height: 0;
    top: 10px;
    right: -10px;
    border-top: 10px solid transparent;
    border-bottom: 10px solid transparent;
    border-left: 10px solid teal;
}}
.logline{{
    margin-top: 10px;
    margin-bottom: 10px;
    display: flex;
    width: 100%;
    align-items: flex-start;
}}
.left{{
    flex: 9;
    justify-content: center; 
    display: flex;
    align-items: center;
}}
.right{{
    flex:1;
    justify-content: center;
    display: flex;
    align-items: center;
}}
</style>

<div class="logline">
    <div class="left">
        <div class="row-2">
            {content}
        </div>
    </div>
    <div class="right">
        <div><img src="data:image/png;base64,{avatar_base64}" style="height: 60px;"></div>
    </div>
'''

html_remote_player = '''
<style>
.row-2{{
    position: relative;
    width: 95%;
    color: #fff;
    line-height: 1.4rem;
    font-size:large;
    word-wrap: break-word;
    border: 1px solid teal;
    border-radius: 10px;
    background: teal;
    padding: 0.5rem;
}}
.row-2::after{{
    content: '';
    position: absolute;
    width: 0;
    height: 0;
    top: 10px;
    left: -10px;
    border-top: 10px solid transparent;
    border-bottom: 10px solid transparent;
    border-right: 10px solid teal;
}}
.logline{{
    margin-top: 10px;
    margin-bottom: 10px;
    display: flex;
    width: 100%;
    align-items: flex-start;
}}
.left{{
    flex: 1;
    justify-content: center; 
    display: flex;
    align-items: center;
}}
.right{{
    flex:9;
    justify-content: center;
    display: flex;
    align-items: center;
}}
</style>
<div class="logline">
    <div class="left">
        <div><img src="data:image/png;base64,{avatar_base64}" style="height: 60px;"></div>
    </div>
    <div class="right">
        <div class="row-2">
            {content}
        </div>
    </div>
</div>
'''
