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
import streamlit.components.v1 as components
import random
import base64
import io
from PIL import Image
from io import BytesIO

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from util.constant import FLASK_SERVER

def image_to_base64(image_bytes):
    """将图片字节数据转换为base64字符串"""
    return base64.b64encode(image_bytes).decode('utf-8')


def compress_image(image, max_size_kb):
    """压缩图片以确保其大小在指定的KB内"""
    quality = 95  # 初始压缩质量
    while True:
        with io.BytesIO() as output:
            # image.save(output, format='JPEG', quality=quality)
            size_kb = output.tell() / 1024
            if size_kb <= max_size_kb or quality <= 5:
                # 如果图片大小小于等于目标大小，或者质量已经非常低，则停止压缩
                return output.getvalue()
            quality -= 5  # 逐步降低质量


def save_base64_image_as_png(base64_string, save_path):
    """
    将 base64 格式的图片数据转换为 PNG 格式并保存到指定路径
    
    参数:
    base64_string (str): 待转换的 base64 格式图片数据
    save_path (str): 保存 PNG 图片的路径
    """
    # 解码 base64 字符串为二进制数据
    image_data = base64.b64decode(base64_string)
    
    # 使用 BytesIO 将二进制数据转换为 PIL Image 对象
    image = Image.open(BytesIO(image_data))
    
    # 保存图片为 PNG 格式
    image.save(save_path, "PNG")
    
    print(f"图片已成功保存至: {save_path}")

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
ip = "10.46.52.228"
port = "5000"

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
        <div><img src="data:image/png;base64,{avatar_base64}" style="width: 60px; height: 60px; margin-right: 10px;"></div>
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
        <div><img src="data:image/png;base64,{avatar_base64}" style="width: 60px; height: 60px; margin-right: 10px;"></div>
    </div>
    <div class="right">
        <div class="row-2">
            {content}
        </div>
    </div>
</div>
'''
