import time
import streamlit as st
import streamlit.components.v1 as components
import requests

from utils import *

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
# First we initalize some necessary global variables.



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

    user_input = st.chat_input("输入你的行动!")

    if user_input:
        battle_with_other(user_input)
