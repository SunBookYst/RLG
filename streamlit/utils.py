import os
import io
from io import BytesIO
import re
import sys
from PIL import Image
import socket
import hashlib
import random
import base64
import requests
import subprocess

from typing import Tuple

import streamlit as st

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from util.constant import SERVER

def image_to_base64(image_bytes:bytes) -> str:
    """
    Transform the image bytes to base64 string.

    Args:
        image_bytes (bytes): the image bytes.

    Returns:
        str: the base64 string.
    """
    return base64.b64encode(image_bytes).decode('utf-8')


def save_base64_image_as_png(base64_string:str, save_path:str):
    """
    Transform the base64 string to image bytes and save it as a PNG file.
    

    Args:
        base64_string (str): The base64 string of the image.
        save_path (str): The path to save the image.
    """

    # 解码 base64 字符串为二进制数据
    image_data = base64.b64decode(base64_string)
    
    # 使用 BytesIO 将二进制数据转换为 PIL Image 对象
    image = Image.open(BytesIO(image_data))
    
    # 保存图片为 PNG 格式
    image.save(save_path, "PNG")
    
    print(f"图片已成功保存至: {save_path}")

def md5_encrypt(password:str) -> str:
    """
    Encrypt the password using MD5 algorithm.

    Args:
        password (str): the password to encrypt.

    Returns:
        str: the enctypyed password.
    """

    md5_hash = hashlib.md5()
    md5_hash.update(password.encode('utf-8'))
    encrypted_password = md5_hash.hexdigest()
    
    return encrypted_password


def set_background(image_path:str, opacity:float):
    """

    Set the background image of the Streamlit app.

    Args:
        image_path (str): the path to the image file.
        opacity (float): the opacity of the background image.
    """
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


def parse_message(message:str) -> Tuple[str,str]:
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
    

def get_local_ip() -> str:
    if '_self_ip' not in st.session_state:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        st.session_state['_self_ip'] = str(local_ip)
    return st.session_state['_self_ip']

def get_local_port() -> str:
    if '_self_port' not in st.session_state:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 0))
        port = sock.getsockname()[1]
        sock.close()
        st.session_state['_self_port'] = str(port)
    return st.session_state['_self_port']

def start_flask_server():
    server_process = subprocess.Popen(["python", "flask_server.py", get_local_port()])
    return server_process

ip, port = SERVER

if ip == "0.0.0.0":
    ip = "127.0.0.1"

url = f"http://{ip}:{port}/"
ST_PATH = os.path.split(os.path.realpath(__file__))[0]

def refresh(role,placeholder):
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
        placeholder.markdown("### Challenge 🔴")
        st.session_state.condition_cha = 3
        st.session_state.battle_id = st.session_state.accept_id[0]
        st.session_state.battle_history = []
        st.rerun()
    if len(st.session_state.id_list)>0:
        placeholder.markdown("### Challenge 🔴")
    else:
        placeholder.markdown("")
    if r['role']!=None:
        st.session_state.battle_history.append({'role':r['role'],"text":r["role_text"]})
        st.session_state.battle_history.append({'role':"system","text":r["system_text"]})
    if r['status'] == True:
        st.session_state.challenage_over = True

def play_music():
#     # 定义本地音乐文件的目录
    music_dir = f'{ST_PATH}/music'
    # print(music_dir)
    # 获取目录中的所有音频文件
    audio_files = [os.path.join(music_dir, file) for file in os.listdir(music_dir) if file.endswith(('.mp3', '.wav'))]
    # 检查是否有音频文件
    if not audio_files:
        st.error("音乐目录中没有找到音频文件。请添加一些 .mp3 或 .wav 文件。")
    else:
        # 初始化 session state
        if 'playing' not in st.session_state:
            st.session_state.playing = True  # 默认播放状态
        if 'current_audio' not in st.session_state:
            st.session_state.current_audio = random.choice(audio_files)

        # 定义播放控制函数
        # def play_audio():
        st.session_state.playing = True

        # def stop_audio():
            # st.session_state.playing = False

        def next_audio():
            st.session_state.current_audio = random.choice(audio_files)
            st.session_state.playing = True

        # 将控制按钮和音频播放器放入侧边栏
        with st.sidebar:
            if st.session_state.playing:
                audio_placeholder = st.empty()
                audio_placeholder.audio(st.session_state.current_audio)
            if st.button("切换音乐"):
                next_audio()
        # 随机循环播放功能的 JavaScript 代码
        js_code = f"""
        <script>
        const audioElement = document.querySelector('audio');
        audioElement.addEventListener('ended', function() {{
            const nextAudio = '{random.choice(audio_files)}';
            const newAudioElement = new Audio(nextAudio);
            document.querySelector('audio').src = nextAudio;
            newAudioElement.play();
        }});
        </script>
        """
        st.components.v1.html(js_code, height=0)

    # 自定义 CSS 来隐藏 "Running" 标识
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    return st.sidebar.empty()


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

battle_attributes = {
    "waiting"       : False,
    "Generating"    : False,
    "battle_history": [],
    "username": ""
}

check_init_state(battle_attributes)